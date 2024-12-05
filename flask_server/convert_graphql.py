from graphql.language.parser import parse

# Mapping GraphQL fields to RDF properties
FIELD_MAPPING = {
    "users": {"class": "ex:User", "id": "?user"},
    "id": "ex:id",
    "email": "ex:email",
    "firstName": "ex:firstName",
    "name": "ex:name",
    "location": {"property": "ex:location", "class": "ex:Location"},
    "country": "ex:country",
    "city": "ex:city",
    "cityCode": "ex:cityCode",
    "street": "ex:street", 
    "houseNumber": "ex:houseNumber",
    "vacancies": {"class": "ex:Vacancy", "id": "?vacancy"},

}

def graphql_to_sparql(graphql_query):
    # Parse the GraphQL query into an AST
    query_ast = parse(graphql_query)
    
    # Initialize SPARQL components
    prefixes = "PREFIX ex: <http://example.com/schema#>\n\n"
    select_clauses = []
    where_clauses = []
    
    def process_selection_set(selection_set, parent_var):
        """Recursively process GraphQL selection sets."""
        for field in selection_set.selections:
            field_name = field.name.value
            if field_name not in FIELD_MAPPING:
                continue
            
            field_mapping = FIELD_MAPPING[field_name]
            
            if isinstance(field_mapping, dict) and "class" in field_mapping:
                # Handle nested object relationships
                nested_var = f"?{field_name}"
                where_clauses.append(f"{parent_var} {field_mapping['property']} {nested_var} .")
                process_selection_set(field.selection_set, nested_var)
            else:
                # Handle simple fields
                sparql_var = f"?{field_name}"
                select_clauses.append(sparql_var)
                where_clauses.append(f"{parent_var} {field_mapping} {sparql_var} .")
    
    # Start processing the root query
    root_field = query_ast.definitions[0].selection_set.selections[0]
    root_var = FIELD_MAPPING[root_field.name.value]["id"]
    select_clauses.append(root_var)
    process_selection_set(root_field.selection_set, root_var)
    
    # Combine SPARQL components
    sparql_query = (
        prefixes +
        "SELECT " + " ".join(select_clauses) + "\n" +
        "WHERE {\n" +
        "  " + "\n  ".join(where_clauses) + "\n" +
        "}"
    )
    return sparql_query

def filter_query_vacancies_current_date(sparql_query):
    # cut off function names from graphql query (query GetActiveVacancies($currentDate: Date!) {vactiveVacancies(currentDate: $currentDate) { --> query {)
    sparql_query = sparql_query.replace("GetActiveVacancies($currentDate: Date!) {", "")
    sparql_query = sparql_query.replace("activeVacancies(currentDate: $currentDate)", "vacancies")

    # delete last } from query
    sparql_query = sparql_query[:-1]

    print("converted query", sparql_query)


    sparql_query = graphql_to_sparql(sparql_query)

    
    print("sparql_query", sparql_query)
     

    # sparql_query = sparql_query.replace(
    #     "WHERE {",
    #     "WHERE {\n  FILTER (xsd:dateTime(?startDate) < xsd:dateTime(NOW()))"
    # )
    # return sparql_query



def convert_response(sparqlrows):

    outer = { 'data': { 'users': [] } }

    for user in sparqlrows:
        inner = { 'id': user['id'], 'firstName': user['firstName'], 'name': user['name'], 'email': user['email'], 'location': { 'country': user['country'], 'city': user['city'], 'cityCode':user['cityCode'], 'street':user['street'], 'houseNumber':user['houseNumber']} }
        outer['data']['users'].append(inner)

    return outer


# Example GraphQL query
graphql_query = """
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

# Convert and print SPARQL query
sparql_query = graphql_to_sparql(graphql_query)
#print(sparql_query)
