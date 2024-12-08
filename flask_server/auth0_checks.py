import jwt
from graphql import GraphQLError
from jwt import PyJWKClient

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
    
def get_userId_by_request(current_request):
    auth_header = current_request.headers.get("Authorization")
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