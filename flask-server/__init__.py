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

    profiles_test_data = [
        {"id": "1", "firstName": "John", "name": "Doe", "email": "john.doe@example.com", "location": {"country": "Belgium", "city": "Brussels", "cityCode": 1000}, "gender": "Male", "dateOfBirth": "1985-02-12", "password": "hashedPassword1"},
        {"id": "2", "firstName": "Mary", "name": "Jane", "email": "mary.jane@example.com", "location": {"country": "USA", "city": "New York", "cityCode": 10001}, "gender": "Female", "dateOfBirth": "1990-03-15", "password": "hashedPassword2"},
        {"id": "3", "firstName": "Peter", "name": "Pan", "email": "peter.pan@example.com", "location": {"country": "Neverland", "city": "Neverland", "cityCode": 12345}, "gender": "Male", "dateOfBirth": "1995-07-23", "password": "hashedPassword3"},
        {"id": "4", "firstName": "Danny", "name": "Dirk", "email": "danny.dirk@example.com", "location": {"country": "Netherlands", "city": "Amsterdam", "cityCode": 2000}, "gender": "Male", "dateOfBirth": "1982-09-01", "password": "hashedPassword4"},
        {"id": "5", "firstName": "Tom", "name": "Jerry", "email": "tom.jerry@example.com", "location": {"country": "USA", "city": "Los Angeles", "cityCode": 90001}, "gender": "Male", "dateOfBirth": "1992-05-14", "password": "hashedPassword5"},
        {"id": "6", "firstName": "Jos", "name": "Brinkie", "email": "jos.brinkie@example.com", "location": {"country": "USA", "city": "Chicago", "cityCode": 60601}, "gender": "Male", "dateOfBirth": "1988-11-28", "password": "hashedPassword6"},
    ]

    # Resolver for `profiles` query
    @query.field("profiles")
    def resolve_profiles(_, info):
        return profiles_test_data

    # Resolver for `profile` query
    @query.field("profile")
    def resolve_profile(_, info, id):
        return next((profile for profile in profiles_test_data if profile["id"] == id), None)
    
    # Resolver for `profileByEmail` query
    @query.field("profileByEmail")
    def resolve_profile_by_email(_, info, email):
        return next((profile for profile in profiles_test_data if profile["email"] == email), None)

    # Helper function to hash passwords
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # Resolver for `createProfile` mutation
    @mutation.field("createProfile")
    def resolve_create_profile(_, info, firstName, name, email, password, dateOfBirth, location, gender):
        # Check if the email already exists
        if any(profile["email"] == email for profile in profiles_test_data):
            raise Exception(f"Profile with email '{email}' already exists.")
        
        # Hash the password before saving it
        hashed_password = hash_password(password)
        
        # Create the new profile
        new_id = str(len(profiles_test_data) + 1)
        new_profile = {
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
        profiles_test_data.append(new_profile)
        return new_profile

    # Resolver for `updateProfile` mutation
    @mutation.field("updateProfile")
    def resolve_update_profile(_, info, id, firstName=None, name=None, email=None, location=None, gender=None, dateOfBirth=None, password=None, educations=None, experiences=None):
        profile = next((p for p in profiles_test_data if p["id"] == id), None)
        if not profile:
            return None  # Return None if no profile matches the ID

        # Update fields if provided
        if firstName:
            profile["firstName"] = firstName
        if name:
            profile["name"] = name
        if email:
            profile["email"] = email
        if location:
            profile["location"] = location
        if gender:
            profile["gender"] = gender
        if dateOfBirth:
            profile["dateOfBirth"] = dateOfBirth
        if password:
            # Hash the password before updating it
            profile["password"] = hash_password(password)
        if educations is not None:
            profile["educations"] = educations
        if experiences is not None:
            profile["experiences"] = experiences
        return profile

    # Create executable schema including the Date scalar
    schema = make_executable_schema(gql_schema, query, mutation, date_scalar)

    # GraphQL explorer route
    @app.route("/graphql", methods=["GET"])
    def graphql_explorer():
        for profile in profiles_test_data:
            print(profile)
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
        for profile in profiles_test_data:
            print(profile)
            print("\n")
        return jsonify(result), status_code

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
