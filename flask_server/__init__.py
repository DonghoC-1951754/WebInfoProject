import os
import bcrypt
import datetime
from ariadne import gql, load_schema_from_path, QueryType, MutationType, graphql_sync, make_executable_schema, ScalarType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify, url_for, redirect, session
from flask_cors import CORS
from rdflib import Graph, Namespace, RDF, Literal
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from os import environ as env
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask_server.convert_graphql import graphql_to_sparql, convert_response


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
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
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
        print("hier")
        return users_test_data

    # Resolver for `user` query
    @query.field("user")
    def resolve_user(_, info, id):
        return next((user for user in users_test_data if user["id"] == id), None)
    
    # Resolver for `userByEmail` query
    @query.field("userByEmail")
    def resolve_user_by_email(_, info, email):
        return next((user for user in users_test_data if user["email"] == email), None)

    @query.field("activeVacancies")
    def resolve_active_vacancies(_, info, currentDate):
        return [vacancy for vacancy in vacancies_test_data if vacancy["startDate"] <= currentDate <= vacancy["endDate"]]

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

    # GraphQL explorer route
    # @app.route("/graphql", methods=["GET"])
    # def graphql_explorer():
    #     for user in users_test_data:
    #         print(user)
    #         print("\n")
    #     return ExplorerGraphiQL().render()

    # GraphQL server route
    @app.route("/getusers", methods=["POST"])
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

        rows = convert_response(rows)

        # Return the results as JSON
        json = jsonify(rows)
        return json, 200

        # Handle the request
        # success, result = graphql_sync(
        #     schema,
        #     data,
        #     context_value={"request": request},
        #     debug=app.debug
        # )
        # print("result2: ", result)
        # status_code = 200 if success else 400
        # # for user in users_test_data:
        # #     print(user)
        # #     print("\n")
        # return jsonify(result), status_code

    @app.route("/getvacancies", methods=["POST"])
    def getvacancies():
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

        rows = convert_response(rows)

        # Return the results as JSON
        json = jsonify(rows)
        return json, 200

    # OAuth login
    @app.route("/login")
    def login():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )

    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect("hello")

    # @app.route("/homepage")
    # def home():
    #     return render_template("http://localhost:3000/", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    
    @app.route('/logout')
    def logout():
        session.clear()  # Clears the session
        return redirect('/')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/sparql')
    def sparql_query():
        query = """
        SELECT ?subject ?predicate ?object
        WHERE {
            ?subject ?predicate ?object .
        }
        """
        query = """
        PREFIX ex: <http://example.com/schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?user ?firstName ?name ?email ?country ?city ?institution ?degree
        WHERE {
        ?user a ex:User ;
                ex:firstName ?firstName ;
                ex:name ?name ;
                ex:email ?email ;
                ex:location ?location ;
                ex:educations ?education .

        ?location ex:country ?country ;
                    ex:city ?city .

        ?education ex:institution ?institution ;
                    ex:degree ?degree .
        }
        """
        headers = []  # Column headers for the table
        rows = []  # Data rows for the table

        try:
            # Execute the SPARQL query
            query_results = rdf_graph.query(query)

            # Extract variable names for headers
            headers = [str(var) for var in query_results.vars]

            # Iterate over the query results and store them
            rows = [
                {headers[i]: str(row[i]) for i in range(len(headers))}
                for row in query_results
            ]

        except Exception as e:
            return jsonify({"error": str(e)})

        # Return the results as JSON
        json = jsonify({"headers": headers, "rows": rows})
        #print(json)
        return json

    @app.route('/converttosparql')
    def convert_to_sparql():
        query = """
        query {
          users {
            id
            firstName
            name
            location {
              country
              city
            }
          }
        }
        """
        sparql_query = graphql_to_sparql(query)
        return jsonify({"sparql_query": sparql_query})
    return app
