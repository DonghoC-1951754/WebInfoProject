import os
import bcrypt
import datetime
from ariadne import gql, load_schema_from_path, QueryType, MutationType, graphql_sync, make_executable_schema, ScalarType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify, url_for, redirect, session
from flask_cors import CORS
from rdflib import Graph, Namespace, RDF, Literal
from flask_server.convert_graphql import graphql_to_sparql, convert_response_users, convert_response_companies
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from os import environ as env
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
from jwt import PyJWKClient

oauth = OAuth()
# load in the RDF graph
rdf_graph = Graph()
rdf_graph.parse("./flask_server/linkrec.ttl", format="turtle")

# load in instances of the classes
instances_graph = Graph()
instances_graph.parse("./flask_server/instances.ttl", format="turtle")

# combine graphs
rdf_graph = rdf_graph + instances_graph

# Define namespaces
EX = Namespace("http://example.org/")

# Define a custom Date scalar
date_scalar = ScalarType("Date")

def get_user_by_id(id):
    query = f"""
    PREFIX ex: <http://example.com/schema#>

    SELECT ?id ?firstName ?name ?email ?dateOfBirth ?country ?city ?cityCode ?street ?houseNumber ?gender
    WHERE {{
      ?user a ex:User ;
            ex:id ?id ;
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

      FILTER (?id = "{id}")
    }}
    GROUP BY ?id ?firstName ?name ?email ?dateOfBirth ?country ?city ?cityCode ?street ?houseNumber ?gender
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

    query_results = rdf_graph.query(query)
    query_results_education = rdf_graph.query(queryEducation)
    query_results_experience = rdf_graph.query(queryExperience)
    
    user = {}

    for row in query_results:
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

    print(user)

    return user



def get_all_vacancies():
    query = """
    PREFIX ex: <http://example.com/schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?vacancy ?jobTitle ?companyName ?country ?city ?cityCode ?requiredskills ?startDate ?endDate
    WHERE {
        ?vacancy a ex:Vacancy ;
                 ex:jobTitle ?jobTitle ;
                 ex:company ?company ;
                 ex:requiredSkills ?requiredskills ;
                 ex:startDate ?startDate ;
                 ex:endDate ?endDate .

        ?company ex:name ?companyName ;
                 ex:location ?location .

        ?location ex:country ?country ;
                  ex:city ?city ;
                  ex:cityCode ?cityCode .
    }
    """
    query_results = rdf_graph.query(query)


    vacancies = []
    for row in query_results:
        vacancy = {
            "id": str(row["vacancy"]),
            "jobTitle": str(row["jobTitle"]),
            "company": {
                "name": str(row["companyName"]),
                "location": {
                    "country": str(row["country"]),
                    "city": str(row["city"]),
                    "cityCode": int(row["cityCode"])
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


# Serialize the Date to a string (ISO format)
@date_scalar.serializer
def serialize_date(value):
    if isinstance(value, datetime.date):
        return value.isoformat()  # Return date in 'YYYY-MM-DD' format
    raise ValueError("Expected a datetime.date object, got {0}".format(type(value)))

# Parse the Date from a string (ISO format)
@date_scalar.value_parser
def parse_date(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()  # Parse string to date
    except ValueError:
        raise ValueError(f"Invalid date format: {value}, expected 'YYYY-MM-DD'")



def create_app(test_config=None):
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)
        print ("Loaded .env file")
    else:
        print ("No .env file found")


    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    app.secret_key = env.get("APP_SECRET_KEY")
    oauth = OAuth(app)
    oauth.register(
        "auth_client",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )

    
    def jwt_required(func):
        def wrapper(*args, **kwargs):
            # Get token from Authorization header
            auth_header = request.headers.get("Authorization", None)
            if not auth_header:
                return jsonify({"message": "Authorization header is missing"}), 401
            try:
                token = auth_header.split(" ")[1]
                # Public Key: https://webinfoproject.eu.auth0.com/.well-known/jwks.json
                jwks_client = PyJWKClient("https://webinfoproject.eu.auth0.com/.well-known/jwks.json")
                signing_key = jwks_client.get_signing_key_from_jwt(token)
                claims = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=["RS256"],
                    issuer="https://webinfoproject.eu.auth0.com/",
                    audience="https://auth0-graphql-api"
                )
                # Store the decoded token's data in the request context
                request.user = claims
            except Exception as e:
                return jsonify({"message": f"Authentication failed!"}), 401

        # If token is valid, continue to the actual endpoint
            return func(*args, **kwargs)
        return wrapper
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    

    CORS(app)

    # Load the schema and include the Date scalar
    gql_schema = load_schema_from_path('./GraphQL/schema.graphql')
    query = QueryType()
    mutation = MutationType()

    users_test_data = [
        {"id": "1", "firstName": "John", "name": "Doe", "email": "john.doe@example.com", "location": {"country": "Belgium", "city": "Brussels", "cityCode": 1000}, "gender": "Male", "dateOfBirth": "1985-02-12", "password": "hashedPassword1"},
        {"id": "2", "firstName": "Mary", "name": "Jane", "email": "mary.jane@example.com", "location": {"country": "USA", "city": "New York", "cityCode": 10001}, "gender": "Female", "dateOfBirth": "1990-03-15", "password": "hashedPassword2"},
        {"id": "3", "firstName": "Peter", "name": "Pan", "email": "peter.pan@example.com", "location": {"country": "Neverland", "city": "Neverland", "cityCode": 12345}, "gender": "Male", "dateOfBirth": "1995-07-23", "password": "hashedPassword3"},
        {"id": "4", "firstName": "Danny", "name": "Dirk", "email": "danny.dirk@example.com", "location": {"country": "Netherlands", "city": "Amsterdam", "cityCode": 2000}, "gender": "Male", "dateOfBirth": "1982-09-01", "password": "hashedPassword4"},
        {"id": "5", "firstName": "Tom", "name": "Jerry", "email": "tom.jerry@example.com", "location": {"country": "USA", "city": "Los Angeles", "cityCode": 90001}, "gender": "Male", "dateOfBirth": "1992-05-14", "password": "hashedPassword5"},
        {"id": "6", "firstName": "Jos", "name": "Brinkie", "email": "jos.brinkie@example.com", "location": {"country": "USA", "city": "Chicago", "cityCode": 60601}, "gender": "Male", "dateOfBirth": "1988-11-28", "password": "hashedPassword6"},
    ]

    companies_test_data = [
        {"id":"1","name":"TechCorp","email":"info@techcorp.com","password":"hashedPassword1","location":{"country":"USA","city":"San Francisco","cityCode":"94107","street":"Market Street","houseNumber":"123"}},
        {"id":"2","name":"GreenLife","email":"contact@greenlife.org","password":"hashedPassword2","location":{"country":"Canada","city":"Toronto","cityCode":"M5G 1P5","street":"Queen Street","houseNumber":"456"}},
        {"id":"3","name":"Innovatech","email":"support@innovatech.io","password":"hashedPassword3","location":{"country":"Germany","city":"Berlin","cityCode":"10117","street":"Unter den Linden","houseNumber":"789"}},
        {"id":"4","name":"EduLearn","email":"hello@edulearn.edu","password":"hashedPassword4","location":{"country":"Netherlands","city":"Amsterdam","cityCode":"1011","street":"Damrak","houseNumber":"12A"}},
        {"id":"5","name":"HealthPlus","email":"care@healthplus.com","password":"hashedPassword5","location":{"country":"UK","city":"London","cityCode":"EC1A 1BB","street":"Bishopsgate","houseNumber":"202"}},
        {"id":"6","name":"AgriWorld","email":"info@agriworld.net","password":"hashedPassword6","location":{"country":"Australia","city":"Sydney","cityCode":"2000","street":"George Street","houseNumber":"88"}}
    ]

    vacancies_test_data = [
        # id = 1, 4 and 6 are active vacancies
        {"id": "1", "jobTitle": "Software Engineer", "company": {"name": "Google", "location": {"country": "USA", "city": "New York", "cityCode": 10001}}, "requiredSkills": ["Python", "JavaScript", "React"], "startDate": datetime.date(2024, 3, 1), "endDate": datetime.date(2024, 12, 31)},
        {"id": "2", "jobTitle": "Data Scientist", "company": {"name": "Facebook", "location": {"country": "USA", "city": "Los Angeles", "cityCode": 90001}}, "requiredSkills": ["Python", "R", "SQL"], "startDate": datetime.date(2024, 12, 1), "endDate": datetime.date(2024, 12, 31)},
        {"id": "3", "jobTitle": "DevOps Engineer", "company": {"name": "Amazon", "location": {"country": "USA", "city": "Chicago", "cityCode": 60601}}, "requiredSkills": ["Docker", "Kubernetes", "Jenkins"], "startDate": datetime.date(2023, 1, 1), "endDate": datetime.date(2023, 12, 31)},
        {"id": "4", "jobTitle": "Product Manager", "company": {"name": "Microsoft", "location": {"country": "USA", "city": "Seattle", "cityCode": 98101}}, "requiredSkills": ["Agile", "Scrum", "Product Management"], "startDate": datetime.date(2024, 1, 1), "endDate": datetime.date(2024, 12, 31)},
        {"id": "5", "jobTitle": "UX Designer", "company": {"name": "Apple", "location": {"country": "USA", "city": "San Francisco", "cityCode": 94101}}, "requiredSkills": ["UI/UX", "Wireframing", "Prototyping"], "startDate": datetime.date(2022, 1, 1), "endDate": datetime.date(2024, 11, 29)},
        {"id": "6", "jobTitle": "Sales Manager", "company": {"name": "Tesla", "location": {"country": "USA", "city": "Palo Alto", "cityCode": 94301}}, "requiredSkills": ["Sales", "Negotiation", "CRM"], "startDate": datetime.date(2022, 2, 1), "endDate": datetime.date(2024, 12, 1)},
    ]

    # Resolver for `users` query
    @query.field("users")
    def resolve_users(_, info):
        return users_test_data
    
    # Resolver for `companies` query
    @query.field("companies")
    def resolve_companies(_, info):
        print("hier")
        return companies_test_data

    # Resolver for `user` query
    @query.field("user")
    def resolve_user(_, info, id):
        return get_user_by_id(id)
        return next((user for user in users_test_data if user["id"] == id), None)
    
    
    # Resolver for `userByEmail` query
    @query.field("userByEmail")
    def resolve_user_by_email(_, info, email):
        return next((user for user in users_test_data if user["email"] == email), None)

    @query.field("activeVacancies")
    def resolve_active_vacancies(_, info, currentDate):
        return get_all_vacancies()
        #return [vacancy for vacancy in vacancies_test_data if vacancy["startDate"] <= currentDate <= vacancy["endDate"]]

    # Helper function to hash passwords
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # Resolver for `createuser` mutation
    @mutation.field("createUser")
    def resolve_create_user(_, info, firstName, name, email, password, dateOfBirth, location, gender):
        # Check if the email already exists
        if any(user["email"] == email for user in users_test_data):
            raise Exception(f"user with email '{email}' already exists.")
        
        # Hash the password before saving it
        hashed_password = hash_password(password)
        
        # Create the new user
        new_id = str(len(users_test_data) + 1)
        new_user = {
            "id": new_id,
            "firstName": firstName,
            "name": name,
            "email": email,
            "password": hashed_password,  # Save the hashed password
            "dateOfBirth": dateOfBirth,  # This will be handled by the Date scalar
            "location": location,
            "gender": gender,
            "educations": [],
            "experiences": []
        }
        users_test_data.append(new_user)
        return new_user
    
    @mutation.field("createCompany")
    def resolve_create_company(_, info,name, email, password, location):
        # Check if the email already exists
        if any(user["email"] == email for user in companies_test_data):
            raise Exception(f"user with email '{email}' already exists.")
        
        # Hash the password before saving it
        hashed_password = hash_password(password)
        
        # Create the new user
        new_id = str(len(users_test_data) + 1)
        new_company = {
            "id": new_id,
            "name": name,
            "email": email,
            "password": hashed_password,  # Save the hashed password
            "location": location,
            "vacancies": []
        }
        companies_test_data.append(new_company)
        return new_company
    
    # Resolver for `updateUser` mutation
    @mutation.field("updateUser")
    def resolve_update_user(_, info, id, firstName=None, name=None, email=None, location=None, gender=None, dateOfBirth=None, password=None, educations=None, experiences=None):
        user = next((p for p in users_test_data if p["id"] == id), None)
        if not user:
            return None  # Return None if no user matches the ID

        # Update fields if provided
        if firstName:
            user["firstName"] = firstName
        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if location:
            user["location"] = location
        if gender:
            user["gender"] = gender
        if dateOfBirth:
            user["dateOfBirth"] = dateOfBirth
        if password:
            # Hash the password before updating it
            user["password"] = hash_password(password)
        if educations is not None:
            user["educations"] = educations
        if experiences is not None:
            user["experiences"] = experiences
        return user

    # Create executable schema including the Date scalar
    schema = make_executable_schema(gql_schema, query, mutation, date_scalar)

    # GraphQL server route
    @app.route("/getusers", methods=["POST"])
    # @jwt_required
    def graphql_server():
        data = request.get_json()

        query = data['query']
        sparqlquery = graphql_to_sparql(query)

        headers = []  # Column headers for the table
        rows = []  # Data rows for the table

        try:
            # Execute the SPARQL query
            query_results = rdf_graph.query(sparqlquery)

            # Extract variable names for headers
            headers = [str(var) for var in query_results.vars]

            # Iterate over the query results and store them
            rows = [
                {headers[i]: str(row[i]) for i in range(len(headers))}
                for row in query_results
            ]

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 400


        # check if the query is for users or companies and convert the response accordingly
        if "users" in query:
            rows = convert_response_users(rows)
        elif "companies" in query:
            rows = convert_response_companies(rows)
        else:
            # throw an error if the query is not for users or companies
            return jsonify({"error": "Invalid query"}), 400

        # Return the results as JSON
        json = jsonify(rows)
        return json, 200

    @app.route("/getuserbyid", methods=["POST"])
    def getuserbyid():
        data = request.get_json()

        #Handle the request
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request},
            debug=app.debug
        )
        status_code = 200 if success else 400
        # for user in users_test_data:
        #     print(user)
        #     print("\n")
        return jsonify(result), status_code


    @app.route('/login')
    def login():
        # Redirect to Auth0's login page
        redirect_uri = url_for('callback', _external=True)
        return oauth.auth_client.authorize_redirect(redirect_uri)
    
    @app.route('/callback')
    def callback():
        token = oauth.auth_client.authorize_access_token()
        userinfo = token['userinfo']
        sub = userinfo['sub']
        access_token = token['access_token']
        # user = oauth.auth_client.parse_id_token(token)
        return jsonify(access_token)

    @app.route("/getvacancies", methods=["POST"])
    def getvacancies():
        data = request.get_json()

        #Handle the request
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request},
            debug=app.debug
        )
        status_code = 200 if success else 400
        # for user in users_test_data:
        #     print(user)
        #     print("\n")
        return jsonify(result), status_code

    # a simple page that says hello
    @app.route('/hello')
    @jwt_required
    def hello():
        return 'Hello, World!'



    return app
