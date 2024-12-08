from rdflib import Graph, Literal, Namespace, URIRef
import datetime
import random
import string


def check_email(email, graph):
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?email
    WHERE {{

      ?user a ex:User ;
            ex:email ?email .

      FILTER (?email = "{email}")
    }}
    """

    query_results = graph.query(query)

    if len(query_results) > 0:
        return False
    
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?email
    WHERE {{

      ?company a ex:Company ;
            ex:email ?email .

      FILTER (?email = "{email}")
    }}
    """

    query_results = graph.query(query)

    return len(query_results) == 0


def check_id(id, graph):
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?id
    WHERE {{

      ?user a ex:User ;
            ex:id ?id .

      FILTER (?id = "{id}")
    }}
    """

    query_results = graph.query(query)

    if len(query_results) > 0:
        return False
    
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?id
    WHERE {{

      ?company a ex:Company ;
            ex:id ?id .

      FILTER (?id = "{id}")
    }}
    """

    query_results = graph.query(query)

    return len(query_results) == 0

def add_new_user(user, graph):
    # Create a new user node
    query = f"""
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {{
        ex:{user["id"]} a ex:User ;
            ex:id "{user["id"]}" ;
            ex:firstName "{user["firstName"]}" ;
            ex:name "{user["name"]}" ;
            ex:email "{user["email"]}" ;
            ex:dateOfBirth "{user["dateOfBirth"]}"^^xsd:date ;
            ex:gender "{user["gender"]}" ;
            ex:lookingForWork "true"^^xsd:boolean ;
            ex:location [ a ex:Location ;
                            ex:country "{user["location"]["country"]}" ;
                            ex:city "{user["location"]["city"]}" ;
                            ex:cityCode "{user["location"]["cityCode"]}" ;
                            ex:street "{user["location"]["street"]}" ;
                            ex:houseNumber "{user["location"]["houseNumber"]}" ] ;
        }}"""

    graph.update(query)

    return user

def add_new_company(company, graph):
    # Create a new company node
    query = f"""
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {{
        ex:{company["id"]} a ex:Company ;
            ex:id "{company["id"]}" ;
            ex:name "{company["name"]}" ;
            ex:email "{company["email"]}" ;
            ex:location [ a ex:Location ;
                            ex:country "{company["location"]["country"]}" ;
                            ex:city "{company["location"]["city"]}" ;
                            ex:cityCode "{company["location"]["cityCode"]}" ;
                            ex:street "{company["location"]["street"]}" ;
                            ex:houseNumber "{company["location"]["houseNumber"]}" ] ;
        }}"""

    graph.update(query)

    return company


def get_user_by_id(id, graph):
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?firstName ?name ?email ?dateOfBirth ?country ?city ?cityCode ?street ?houseNumber ?gender ?lookingForWork
    WHERE {{
      ?user a ex:User ;
            ex:id "{id}" ;
            ex:firstName ?firstName ;
            ex:name ?name ;
            ex:email ?email ;
            ex:dateOfBirth ?dateOfBirth ;
            ex:gender ?gender ;
            ex:lookingForWork ?lookingForWork ;
            ex:location ?location .

      ?location ex:country ?country ;
                ex:city ?city ;
                ex:cityCode ?cityCode ;
                ex:street ?street ;
                ex:houseNumber ?houseNumber .
    }}
    """

    # get the education of the user
    queryEducation = f"""
    PREFIX ex: <http://example.com/schema#>
    
    SELECT ?institution ?degree ?fieldOfStudy ?yearGraduated
    WHERE {{
        ?user a ex:User ;
                ex:id "{id}" ;
                ex:educations ?education .
        ?education ex:institution ?institution ;
                     ex:degree ?degree ;
                     ex:fieldOfStudy ?fieldOfStudy ;
                     ex:yearGraduated ?yearGraduated .  
    }}
    """

    queryExperience = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?companyId ?companyName ?jobTitle ?startDate ?endDate ?description
    WHERE {{
        ?user a ex:User ;
                ex:id "{id}" ;
                ex:experiences ?experience .
        ?experience ex:Company ?company ;
                    ex:jobTitle ?jobTitle ;
                    ex:startDate ?startDate ;
                    ex:description ?description .
        OPTIONAL {{ ?experience ex:endDate ?endDate . }}
        ?company ex:name ?companyName .
        ?company ex:id ?companyId .
    }}
    """

    query_skills = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?skills
    WHERE {{
        ?user a ex:User ;
                ex:id "{id}" ;
                ex:skills ?skills .
    }}
    """

    query_results = graph.query(query)
    query_results_education = graph.query(queryEducation)
    query_results_experience = graph.query(queryExperience)
    query_results_skills = graph.query(query_skills)
    
    user = {}
    qskills = []

    for row in query_results_skills:
        qskills.append(str(row["skills"]))

    for row in query_results:
        user = {
            "id": id,
            "firstName": str(row["firstName"]),
            "name": str(row["name"]),
            "email": str(row["email"]),
            "dateOfBirth": row["dateOfBirth"].toPython(),
            "location": {
                "country": str(row["country"]),
                "city": str(row["city"]),
                "cityCode": str(row["cityCode"]),
                "street": str(row["street"]),
                "houseNumber": str(row["houseNumber"])
            },
            "gender": str(row["gender"]),
            "lookingForWork": bool(row["lookingForWork"]),
            "skills": [],
            "connections": [],   
            "educations": [],
            "experiences": []
        }

    user["skills"] = qskills

    for row in query_results_education:
        education = {
            "institution": str(row["institution"]),
            "degree": str(row["degree"]),
            "fieldOfStudy": str(row["fieldOfStudy"]),
            "yearGraduated": str(row["yearGraduated"])
        }
        user["educations"].append(education)

    for row in query_results_experience:
        endDate = row["endDate"].toPython() if row["endDate"] != None else None
        experience = {
            "company" : {
                "id" : str(row["companyId"]),
                "name": str(row["companyName"])
            },
            "jobTitle": str(row["jobTitle"]),
            "startDate": row["startDate"].toPython(),
            "endDate": endDate,
            "description": str(row["description"])
        }
        user["experiences"].append(experience)

    # get the connections of the user
    queryConnections = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?connectionId ?userFromId ?userFromName ?userToId ?userToName ?status
    WHERE {{
        {{?connectionfrom a ex:UserConnection ;
                    ex:id ?connectionId ;
                    ex:fromUser ?userfrom ;
                    ex:toUser ?userto ;
                    ex:status ?status .
        ?userfrom a ex:User ;
                ex:id ?userFromId ;
                ex:firstName ?userFromName .
        ?userto a ex:User ;
                ex:id ?userToId ;
                ex:firstName ?userToName .
        FILTER (?userFromId = "{id}")
        }}
        UNION
        {{?connectionto a ex:UserConnection ;
                    ex:id ?connectionId ;
                    ex:fromUser ?userfrom ;
                    ex:toUser ?userto ;
                    ex:status ?status .
        ?userfrom a ex:User ;
                ex:id ?userFromId ;
                ex:firstName ?userFromName .
        ?userto a ex:User ;
                ex:id ?userToId ;
                ex:firstName ?userToName .
        FILTER (?userToId = "{id}")
        }}

    }}
    """

    query_results_connections = graph.query(queryConnections)

    for row in query_results_connections:
        connection = {
            "id": str(row["connectionId"]),
            "fromUser": {
                "id": str(row["userFromId"]),
                "name": str(row["userFromName"])
            },
            "toUser": {
                "id": str(row["userToId"]),
                "name": str(row["userToName"])
            },
            "status": str(row["status"])
        }
        user["connections"].append(connection)

    return user


def get_companiy_by_id(id, graph):
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?name ?email ?country ?city ?cityCode ?street ?houseNumber
    WHERE {{
      ?company a ex:Company ;
            ex:id "{id}" ;
            ex:name ?name ;
            ex:email ?email ;
            ex:location ?location .

      ?location ex:country ?country ;
                ex:city ?city ;
                ex:cityCode ?cityCode ;
                ex:street ?street ;
                ex:houseNumber ?houseNumber .
    }}
    """

    query_results = graph.query(query)
    
    company = {}

    for row in query_results:
        company = {
            "id": id,
            "name": str(row["name"]),
            "email": str(row["email"]),
            "location": {
                "country": str(row["country"]),
                "city": str(row["city"]),
                "cityCode": str(row["cityCode"]),
                "street": str(row["street"]),
                "houseNumber": str(row["houseNumber"])
            },
            "vacancies": []
        }

    vacancies_query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?id ?vacancy ?jobTitle ?requiredSkills ?startDate ?endDate
    WHERE {{
        ?company a ex:Company ;
                ex:id "{id}" ;
                ex:vacancies ?vacancy .
        ?vacancy ex:id ?id ;
                 ex:jobTitle ?jobTitle ;
                 ex:requiredSkills ?requiredSkills ;
                 ex:startDate ?startDate ;
                 ex:endDate ?endDate .
    }}
    """

    vacancies_query_results = graph.query(vacancies_query)

    vacancies = []

    for row in vacancies_query_results:
        vacancy = {
            "id": str(row["id"]),
            "jobTitle": str(row["jobTitle"]),
            "startDate": row["startDate"].toPython(),
            "requiredSkills": str(row["requiredSkills"]),
            "endDate": row["endDate"].toPython()
        }
        vacancies.append(vacancy)

    vacancy_skills = {}
    current_id = None
    for vacancy in vacancies:
        if current_id == vacancy['id']:
            vacancy_skills[current_id].append(vacancy['requiredSkills'])
        else:
            current_id = vacancy['id']
            vacancy_skills[current_id] = [vacancy['requiredSkills']]

    # remove duplicates
    current_id = None
    i = 0
    while i < len(vacancies):
        if current_id == vacancies[i]['id']:
            vacancies.pop(i)
        else:
            current_id = vacancies[i]['id']
            i += 1

    for vacancy in vacancies:
        vacancy['requiredSkills'] = vacancy_skills[vacancy['id']]

    company["vacancies"] = vacancies

    return company


def get_all_vacancies(graph):
    query = """
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?vacancy ?jobTitle ?companyId ?companyName ?country ?city ?cityCode ?street ?houseNumber ?requiredskills ?startDate ?endDate
    WHERE {
        ?vacancy a ex:Vacancy ;
                 ex:jobTitle ?jobTitle ;
                 ex:company ?company ;
                 ex:requiredSkills ?requiredskills ;
                 ex:startDate ?startDate ;
                 ex:endDate ?endDate .

        ?company ex:name ?companyName ;
                 ex:id ?companyId ;
                 ex:location ?location .

        ?location ex:country ?country ;
                  ex:city ?city ;
                  ex:cityCode ?cityCode ;
                  ex:street ?street ;
                  ex:houseNumber ?houseNumber .
    }
    """
    query_results = graph.query(query)


    vacancies = []
    for row in query_results:
        vacancy = {
            "id": str(row["vacancy"]),
            "jobTitle": str(row["jobTitle"]),
            "company": {
                "id": str(row["companyId"]),
                "name": str(row["companyName"]),
                "location": {
                    "country": str(row["country"]),
                    "city": str(row["city"]),
                    "cityCode": int(row["cityCode"]),
                    "street": str(row["street"]),
                    "houseNumber": str(row["houseNumber"])
                }
            },
            "requiredSkills": row['requiredskills'],
            "startDate": row["startDate"].toPython(),
            "endDate": row["endDate"].toPython()
        }
        vacancies.append(vacancy)

    # group skills by vacancy
    current_id = None
    skills = {}
    for vacancy in vacancies:
        if current_id == vacancy['id']:
            skills[current_id].append(vacancy['requiredSkills'])
        else:
            current_id = vacancy['id']
            skills[current_id] = [vacancy['requiredSkills']]

    # remove duplicates
    current_id = None
    i = 0
    while i < len(vacancies):
        if current_id == vacancies[i]['id']:
            vacancies.pop(i)
        else:
            current_id = vacancies[i]['id']
            i += 1

    # add skills to vacancies
    for vacancy in vacancies:
        vacancy['requiredSkills'] = skills[vacancy['id']]

    return vacancies

def get_active_vacancies(graph):
    vacancies = get_all_vacancies(graph)

    active_vacancies = []

    for vacancy in vacancies:
        if vacancy['endDate'] == None or vacancy['endDate'] > datetime.datetime.now().date():
            active_vacancies.append(vacancy)

    return active_vacancies

def update_user(id, firstName, name, location, gender, lookingForWork, skills, educations, experiences, graph):

    query = f"""
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    """
    delete = "DELETE {"

    if firstName:
        delete += "?user ex:firstName ?firstName ."
    if name:
        delete += "?user ex:name ?name ."
    if gender:
        delete += "?user ex:gender ?gender ."
    if lookingForWork is not None:
        delete += "?user ex:lookingForWork ?lookingForWork ."

    delete += f"""}}
    WHERE {{
        ?user a ex:User ;"""
    if firstName:
        delete += f"""
              ex:firstName ?firstName ;"""
    if name:
        delete += f"""
              ex:name ?name ;"""
    if gender:
        delete += f"""
              ex:gender ?gender ;"""
    if lookingForWork is not None:
        delete += f"""
              ex:lookingForWork ?lookingForWork ;"""
    delete += f"""
              ex:id "{id}" .
    }}
    """

    insert = """
    INSERT {"""

    if firstName:
        insert += f"?user ex:firstName \"{firstName}\" ."
    if name:
        insert += f"?user ex:name \"{name}\" ."
    if gender:
        insert += f"?user ex:gender \"{gender}\" ."
    if lookingForWork is not None:
        insert += f"?user ex:lookingForWork \"{lookingForWork}\"^^xsd:boolean ."

    insert += "}"
    where = f"""
    WHERE {{
        ?user a ex:User ;
                ex:id "{id}" . 
    }}
    """

    delete = query + delete

    graph.update(delete)

    insert = query + insert + where

    graph.update(insert)

    if location:
        query = f"""
        PREFIX ex: <http://example.com/schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        DELETE {{"""
        if location["country"]:
            query += "?location ex:country ?country ."
        if location["city"]:
            query += "?location ex:city ?city ."
        if location["cityCode"]:
            query += "?location ex:cityCode ?cityCode ."
        if location["street"]:
            query += "?location ex:street ?street ."
        if location["houseNumber"]:
            query += "?location ex:houseNumber ?houseNumber ."
        
        query += f"""}}WHERE {{
            ?user a ex:User ;
                    ex:id "{id}" ;
                    ex:location ?location ."""
        if location["country"]:
            query += "?location ex:country ?country ."
        if location["city"]:
            query += "?location ex:city ?city ."
        if location["cityCode"]:
            query += "?location ex:cityCode ?cityCode ."
        if location["street"]:
            query += "?location ex:street ?street ."
        if location["houseNumber"]:
            query += "?location ex:houseNumber ?houseNumber ."

        query += f"""
        }}
        """
        graph.update(query)

        query = f"""
        PREFIX ex: <http://example.com/schema#>

        INSERT {{"""
        if location["country"]:
            query += "?location ex:country \"" + location["country"] + "\" ."
        if location["city"]:
            query += "?location ex:city \"" + location["city"] + "\" ."
        if location["cityCode"]:
            query += "?location ex:cityCode \"" + location["cityCode"] + "\" ."
        if location["street"]:
            query += "?location ex:street \"" + location["street"] + "\" ."
        if location["houseNumber"]:
            query += "?location ex:houseNumber \"" + location["houseNumber"] + "\" ."
        query += f"""}}
        WHERE {{
            ?user a ex:User ;
                    ex:id "{id}" .
            OPTIONAL {{
                ?user ex:location ?location .
            }}
        }}

        """
        graph.update(query)


    user = {}

    user["id"] = id

    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?firstName ?name ?email ?dateOfBirth ?country ?city ?cityCode ?street ?gender ?houseNumber ?lookingForWork
    WHERE {{
      ?user a ex:User ;
            ex:id "{id}" ;
            ex:firstName ?firstName ;
            ex:name ?name ;
            ex:email ?email ;
            ex:dateOfBirth ?dateOfBirth ;
            ex:gender ?gender ;
            ex:lookingForWork ?lookingForWork ;
            ex:location ?location .

      ?location ex:country ?country ;
                ex:city ?city ;
                ex:cityCode ?cityCode ;
                ex:street ?street;
                ex:houseNumber ?houseNumber .
    }}
    """

    query_results = graph.query(query)

    skills_query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?skills
    WHERE {{
        ?user a ex:User ;
                ex:id "{id}" ;
                ex:skills ?skills .
    }}
    """

    qskills = []

    skills = graph.query(skills_query)

    for row in skills:
        qskills.append(str(row["skills"]))

    for row in query_results:
        user = {
            "id": id,
            "firstName": str(row["firstName"]),
            "name": str(row["name"]),
            "email": str(row["email"]),
            "dateOfBirth": row["dateOfBirth"].toPython(),
            "gender" : str(row["gender"]),
            "lookingForWork": bool(row["lookingForWork"]),
            "skills": [],
            "location": {
                "country": str(row["country"]),
                "city": str(row["city"]),
                "cityCode": str(row["cityCode"]),
                "street": str(row["street"]),
                "houseNumber": str(row["houseNumber"])
            }
        }

    user["skills"] = qskills
    
    return user

def make_connection_request(fromUserId, toUserId, graph):

    connectionid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))

    query = f"""
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT {{
        ex:{connectionid} a ex:UserConnection ;
            ex:id "{connectionid}" ;
            ex:fromUser ?fromUser ;
            ex:toUser ?toUser ;
            ex:status "pending" .
    }}
    WHERE {{
        ?fromUser a ex:User ;
                ex:id "{fromUserId}" .
        ?toUser a ex:User ;
                ex:id "{toUserId}" .
    }}
    """

    connection = {
        "id": connectionid,
        "fromUser": {
            "id": fromUserId
        },
        "toUser": {
            "id": toUserId
        },
        "status": "pending"
    }   

    graph.update(query)

    return connection


def update_connection_request(connectionId, status, rdf_graph):
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    DELETE {{
        ?connection ex:status ?status .
    }} 
    WHERE {{
        ?connection a ex:UserConnection ;
                    ex:id "{connectionId}" ;
                    ex:status ?status .
    }}
    """

    rdf_graph.update(query)

    query = f"""
    INSERT {{
        ?connection ex:status "{status}" .
    }}
    WHERE {{
        ?connection a ex:UserConnection ;
                    ex:id "{connectionId}".
    }}
    """

    rdf_graph.update(query)

    get_connection_query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?fromId ?toId ?status
    WHERE {{
        ?connection a ex:UserConnection ;
            ex:id "{connectionId}" ;
            ex:fromUser ?from ;
            ex:toUser ?to ;
            ex:status ?status .

        ?from ex:id ?fromId .
        ?to ex:id ?toId .
    }}
    """

    query_results = rdf_graph.query(get_connection_query)

    connection = {}

    for row in query_results:
        connection = {
            "id": connectionId,
            "fromUser": {
                "id": str(row["fromId"])
            },
            "toUser": {
                "id": str(row["toId"])
            },
            "status": str(row["status"])
        }

    return connection

def delete_connection(connectionId, graph):
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    DELETE {{
        ?connection ?p ?o .
    }}
    WHERE {{
        ?connection a ex:UserConnection ;
                    ex:id "{connectionId}" .
        ?connection ?p ?o .
    }}
    """

    graph.update(query)

    return connectionId

def make_user_experience(userId, companyId, jobTitle, startDate, endDate, description, graph):
    experienceId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))

    query = f"""
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT {{
        ex:{experienceId} a ex:Experience ;
            ex:id "{experienceId}" ;
            ex:Company ?company ;
            ex:jobTitle "{jobTitle}" ;
            ex:startDate "{startDate}"^^xsd:date ;"""
    if endDate:
        query += f"""
            ex:endDate "{endDate}"^^xsd:date ;"""

    query += f"""
            ex:description "{description}" .
        ?user ex:experiences ex:{experienceId} .
    }} WHERE {{
        ?company a ex:Company ;
                ex:id "{companyId}" .
        ?user a ex:User ;
                ex:id "{userId}" .
    }}
    """
    graph.update(query)

    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?companyName ?jobTitle ?startDate ?endDate ?description
    WHERE {{
        ?company a ex:Company ;
                ex:id "{companyId}" ;
                ex:name ?companyName .
        ?experience a ex:Experience ;
                    ex:id "{experienceId}" ;
                    ex:Company ?company ;
                    ex:jobTitle ?jobTitle ;
                    ex:startDate ?startDate ;
                    ex:description ?description .
    }}
    """

    query_results = graph.query(query)
    userexp = {}

    for row in query_results:
        userexp = {
            "id": experienceId,
            "company": {
                "id": companyId,
                "name": str(row["companyName"])
            },
            "jobTitle": str(row["jobTitle"]),
            "startDate": row["startDate"].toPython(),
            "endDate": None,
            "description": str(row["description"])
        }

    if endDate:
        userexp["endDate"] = endDate

    return userexp

def get_all_users(graph):
    query = """
    PREFIX ex: <http://example.com/schema#>

    SELECT ?id ?firstName ?name ?email ?dateOfBirth ?country ?city ?cityCode ?street ?houseNumber ?lookingForWork
    WHERE {
        ?user a ex:User ;
                ex:id ?id ;
                ex:firstName ?firstName ;
                ex:name ?name ;
                ex:email ?email ;
                ex:dateOfBirth ?dateOfBirth ;
                ex:lookingForWork ?lookingForWork ;
                ex:location ?location .

        ?location ex:country ?country ;
                  ex:city ?city ;
                  ex:cityCode ?cityCode ;
                  ex:street ?street ;
                  ex:houseNumber ?houseNumber .
    }
    """

    query_results = graph.query(query)

    users = []

    for row in query_results:
        skills_query = f"""
        PREFIX ex: <http://example.com/schema>
        SELECT ?skills
        WHERE {{
            ?user a ex:User ;
                    ex:id "{row["id"]}" ;
                    ex:skills ?skills .
        }}
        """

        skills = graph.query(skills_query)

        qskills = []

        for skill in skills:
            qskills.append(str(skill["skills"]))

        user = {
            "id": str(row["id"]),
            "firstName": str(row["firstName"]),
            "name": str(row["name"]),
            "email": str(row["email"]),
            "dateOfBirth": row["dateOfBirth"].toPython(),
            "location": {
                "country": str(row["country"]),
                "city": str(row["city"]),
                "cityCode": str(row["cityCode"]),
                "street": str(row["street"]),
                "houseNumber": str(row["houseNumber"])
            },
            "lookingForWork": bool(row["lookingForWork"]),
            "skills": qskills
        }
        users.append(user)

    return users