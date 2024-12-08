from rdflib import Graph, Literal, Namespace, URIRef
import datetime


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

    SELECT ?firstName ?name ?email ?dateOfBirth ?country ?city ?cityCode ?street ?houseNumber ?gender
    WHERE {{
      ?user a ex:User ;
            ex:id "{id}" ;
            ex:firstName ?firstName ;
            ex:name ?name ;
            ex:email ?email ;
            ex:dateOfBirth ?dateOfBirth ;
            ex:gender ?gender ;
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

    SELECT ?companyName ?jobTitle ?startDate ?endDate ?description
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
    }}
    """

    query_results = graph.query(query)
    query_results_education = graph.query(queryEducation)
    query_results_experience = graph.query(queryExperience)
    
    user = {}

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
            "educations": [],
            "experiences": []
        }

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
                "name": str(row["companyName"])
            },
            "jobTitle": str(row["jobTitle"]),
            "startDate": row["startDate"].toPython(),
            "endDate": endDate,
            "description": str(row["description"])
        }
        user["experiences"].append(experience)

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

def update_user(id, firstName, name, location, gender, educations, experiences, graph):
    query = f"""
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    """
    delete = "DELETE {"

    if firstName:
        delete += "?user ex:firstName ?firstname ."
    if name:
        delete += "?user ex:name ?name ."
    if gender:
        delete += "?user ex:gender ?gender ."

    delete += "}"
    
    insert = """
    INSERT {"""

    if firstName:
        insert += f"?user ex:firstName \"{firstName}\" ."
    if name:
        insert += f"?user ex:name \"{name}\" ."
    if gender:
        insert += f"?user ex:gender \"{gender}\" ."

    insert += "}"
    where = f"""
    WHERE {{
        ?user a ex:User ;
              ex:id "{id}" .
    }}
    """

    delete = query + delete + where

    print(delete)   

    graph.update(delete)

    insert = query + insert + where

    print(insert)

    graph.update(insert)

    user = {}

    user["id"] = id

    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?firstName ?name ?email ?dateOfBirth ?country ?city ?cityCode ?street ?gender ?houseNumber
    WHERE {{
      ?user a ex:User ;
            ex:id "{id}" ;
            ex:firstName ?firstName ;
            ex:name ?name ;
            ex:email ?email ;
            ex:dateOfBirth ?dateOfBirth ;
            ex:gender ?gender ;
            ex:location ?location .

      ?location ex:country ?country ;
                ex:city ?city ;
                ex:cityCode ?cityCode ;
                ex:street ?street;
                ex:houseNumber ?houseNumber .
    }}
    """

    query_results = graph.query(query)

    for row in query_results:
        user = {
            "id": id,
            "firstName": str(row["firstName"]),
            "name": str(row["name"]),
            "email": str(row["email"]),
            "dateOfBirth": row["dateOfBirth"].toPython(),
            "gender" : str(row["gender"]),
            "location": {
                "country": str(row["country"]),
                "city": str(row["city"]),
                "cityCode": str(row["cityCode"]),
                "street": str(row["street"]),
                "houseNumber": str(row["houseNumber"])
            }
        }

    print(user)
    
    return user, graph


