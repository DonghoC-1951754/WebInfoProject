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
import random
import string
from flask_server.sparql_utils import get_companiy_by_id, get_user_by_id, check_email, check_id, add_new_user, add_new_company, get_all_vacancies
from functools import wraps
from urllib.parse import urlencode
from graphql import GraphQLError

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

def check_jwt(request):
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise GraphQLError("Authorization header is missing")
    try:
        token = auth_header.split(" ")[1]
        jwks_client = PyJWKClient("https://webinfoproject.eu.auth0.com/.well-known/jwks.json")
        signing_key = jwks_client.get_signing_key_from_jwt(token).key
        decoded_id_token = jwt.decode(token, signing_key, algorithms=["RS256"], audience="p44ZPot04hccnnkPGtx7ELWEZvym0yDi", issuer="https://webinfoproject.eu.auth0.com/")
        # print("Decoded token: ", decoded_id_token)

    except jwt.ExpiredSignatureError:
        raise GraphQLError("The token has expired.")
    except jwt.InvalidAudienceError:
        raise GraphQLError("Invalid audience claim.")
    except jwt.InvalidIssuerError:
        raise GraphQLError("Invalid issuer claim.")
    except jwt.DecodeError:
        raise GraphQLError("Error decoding the JWT.")
    except jwt.PyJWTError as e:
        raise GraphQLError(f"JWT Error: {e}")
    except Exception as e:
        raise GraphQLError(f"Authentication failed!")


def create_app(test_config=None):
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)
        print ("Loaded .env file")
    else:
        print ("No .env file found")


    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = env.get("APP_SECRET_KEY")
    oauth = OAuth(app)
    oauth.register(
        "auth_client",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
            "audience": "https://auth0-graphql-api"
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )
    
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
        return companies_test_data

    @query.field("company")
    def resolve_companies(_, info, id):
        return get_companiy_by_id(id, rdf_graph)

    # Resolver for `user` query
    @query.field("user")
    def resolve_user(_, info, id):
        return get_user_by_id(id, rdf_graph)

    # @query.field("userByEmail")
    # def resolve_user_by_email(_, info, email):
    #     if check_email(email, rdf_graph):
    #         return None
    
    
    # Resolver for `userByEmail` query
    # @query.field("userByEmail")
    # def resolve_user_by_email(_, info, email):
    #     return next((user for user in users_test_data if user["email"] == email), None)

    @query.field("activeVacancies")
    def resolve_active_vacancies(_, info, currentDate):
        return get_all_vacancies(rdf_graph)


    # Resolver for `createuser` mutation
    @mutation.field("createUser")
    # @jwt_required
    def resolve_create_user(_, info, firstName, name, email, dateOfBirth, location, gender):
        current_request = info.context.get('request')
        check_jwt(current_request)
            
        userID = info.context.get('user_id')
        if (userID is None):
            userID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))

        if not check_email(email, rdf_graph):
            raise GraphQLError(str(f"user with email '{email}' already exists."))
        
        if not check_id(userID, rdf_graph):
            raise GraphQLError(str(f"user with id '{userID}' already exists."))
        
        new_user = {
            "id": userID,
            "firstName": firstName,
            "name": name,
            "email": email,
            "dateOfBirth": dateOfBirth,  # This will be handled by the Date scalar
            "location": location,
            "gender": gender,
            "educations": [],
            "experiences": []
        }
        print("New user")
        print(f"State of rdf_graph before adding new user: {rdf_graph}")
        new_user = add_new_user(new_user, rdf_graph)
        print(f"State of rdf_graph after adding new user: {rdf_graph}")
        return new_user
    
    @mutation.field("createCompany")
    def resolve_create_company(_, info,name, email, location):
        current_request = info.context.get('request')
        check_jwt(current_request)

        compID = info.context.get('user_id')
        if not check_email(email, rdf_graph):
            raise GraphQLError(str(f"user with email '{email}' already exists."))
        
        if not check_id(compID, rdf_graph):
            raise GraphQLError(str(f"user with id '{compID}' already exists."))
        
        if (compID is None):
            compID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
        print("CompId: ", compID)
        new_company = {
            "id": compID,
            "name": name,
            "email": email,
            "location": location,
            "vacancies": []
        }
        new_company = add_new_company(new_company, rdf_graph)
        return new_company
    
    # Resolver for `updateUser` mutation
    @mutation.field("updateUser")
    def resolve_update_user(_, info, id, firstName=None, name=None, email=None, location=None, gender=None, dateOfBirth=None, educations=None, experiences=None):
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
        if educations is not None:
            user["educations"] = educations
        if experiences is not None:
            user["experiences"] = experiences
        return user

    # Create executable schema including the Date scalar
    schema = make_executable_schema(gql_schema, query, mutation, date_scalar)

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

    @app.route("/graphql", methods=["POST"])
    def graphqlhandle():
        data = request.get_json()
        user_ID = get_userId_by_request(request)

        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request, "user_id": user_ID},
            debug=app.debug
        )
        
        status_code = 200 if success else 400
        return jsonify(result), status_code

    @app.route('/login')
    def login():
        # Redirect to Auth0's login page
        redirect_uri = url_for('callback', _external=True)
        return oauth.auth_client.authorize_redirect(redirect_uri)
    
    @app.route('/logout')
    def logout():
        session.clear()

        logout_url = f'https://{env.get("AUTH0_DOMAIN")}/v2/logout'

        params = {
            'client_id': env.get("AUTH0_CLIENT_ID"),
            'returnTo': "http://localhost:3000"  # URL to redirect to after logout
        }

        # Redirect to Auth0's logout URL
        return redirect(f"{logout_url}?{urlencode(params)}")

    @app.route('/callback')
    def callback():
        token = oauth.auth_client.authorize_access_token(audience="https://auth0-graphql-api")
        id_token = token['id_token']
        user_id = token['userinfo']['sub']
        if user_id and user_id.startswith("auth0|"):
            user_id = user_id.split("|")[1]

        print("User ID: ", user_id)
        user_by_id = get_user_by_id(user_id, rdf_graph)
        if user_by_id:
            return redirect(f'http://localhost:3000/?token={id_token}&userID={user_id}')
        return redirect(f'http://localhost:3000/registration?token={id_token}&userID={user_id}')
  

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    return app

def get_userId_by_request(current_request):
    auth_header = current_request.headers.get("Authorization")
    print(f"Authorization header: {auth_header}")
    # print(data)
    user_id = None

    if auth_header:
        token = auth_header.split("Bearer ")[-1]  # Extract the JWT token from Bearer token
        try:
            jwks_client = PyJWKClient("https://webinfoproject.eu.auth0.com/.well-known/jwks.json")
            signing_key = jwks_client.get_signing_key_from_jwt(token).key
            decoded_id_token = jwt.decode(token, signing_key, algorithms=["RS256"], audience="p44ZPot04hccnnkPGtx7ELWEZvym0yDi", issuer="https://webinfoproject.eu.auth0.com/")
            user_id = decoded_id_token.get("sub")
            if user_id and user_id.startswith("auth0|"):
                user_id = user_id.split("|")[1]

        except Exception as e:
            print("Invalid token:", e)
            user_id = None  # If token is invalid, leave user_id as None
    
    return user_id