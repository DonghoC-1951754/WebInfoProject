import os
import bcrypt
import datetime
from ariadne import gql, load_schema_from_path, QueryType, MutationType, graphql_sync, make_executable_schema, ScalarType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify
from flask_cors import CORS


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
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
    @app.route("/graphql", methods=["GET"])
    def graphql_explorer():
        for user in users_test_data:
            print(user)
            print("\n")
        return ExplorerGraphiQL().render()

    # GraphQL server route
    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()

        # Handle the request
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request},
            debug=app.debug
        )
        status_code = 200 if success else 400
        for user in users_test_data:
            print(user)
            print("\n")
        return jsonify(result), status_code

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
