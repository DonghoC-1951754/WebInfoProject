import os

from ariadne import gql, load_schema_from_path, QueryType, graphql_sync, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    gql_schema = load_schema_from_path('./GraphQL/schema.graphql')
    query = QueryType()

    schema = make_executable_schema(gql_schema, query)

    profiles_test_data = [
        {"id": "1", "firstName": "John", "name": "Doe", "email": "john.doe@example.com", "location": "Belgium"},
        {"id": "2", "firstName": "Mary", "name": "Jane", "email": "mary.jane@example.com", "location": "USA"},
        {"id": "3", "firstName": "Peter", "name": "Pan", "email": "peter.pan@example.com", "location": "Neverland"},
        {"id": "4", "firstName": "Danny", "name": "Dirk", "email": "danny.dirk@example.com", "location": "Netherlands"},
        {"id": "5", "firstName": "Tom", "name": "Jerry", "email": "tom.jerry@example.com", "location": "USA"},
        {"id": "6", "firstName": "Jos", "name": "Brinkie", "email": "jos.brinkie@example.com", "location": "USA"},
    ]

    # Resolver for `profiles` query
    @query.field("profiles")
    def resolve_profiles(_, info):
        return profiles_test_data


    # Resolver for `profile` query
    @query.field("profile")
    def resolve_profile(_, info, id):
        # Find profile by ID
        return next((profile for profile in profiles_test_data if profile["id"] == id), None)


    @query.field("hello")
    def resolve_hello(_, info):
        request = info.context
        user_agent = request.headers.get("User-Agent", "Guest")
        return "Hello, %s!" % user_agent


    @app.route("/graphql", methods=["GET"])
    def graphql_explorer():
        # On GET request serve the GraphQL explorer.
        # You don't have to provide the explorer if you don't want to
        # but keep on mind this will not prohibit clients from
        # exploring your API using desktop GraphQL explorer app.
        return explorer_html, 200


    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        # GraphQL queries are always sent as POST
        data = request.get_json()

        # Note: Passing the request to the context is optional.
        # In Flask, the current request is always accessible as flask.request
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request},
            debug=app.debug
        )

        status_code = 200 if success else 400
        return jsonify(result), status_code

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app