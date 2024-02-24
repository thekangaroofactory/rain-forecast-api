from pathlib import Path

import connexion
from connexion.exceptions import OAuthProblem

# -- Replace this by an env variable
TOKEN_DB = {"asdf1234567890": {"uid": 100}}


def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem("Invalid token")

    return info


# referenced in the spec file (openapi): operationId: app.get_secret
def get_secret(user) -> str:
    return f"You are {user} and the secret is 'wbevuec'"


# referenced in the spec file (swagger): operationId: app.post_greeting
def post_greeting(name: str) -> str:
    return f"Hello {name}"


# define the api(s)
app = connexion.FlaskApp(__name__, specification_dir="spec/")
app.add_api("openapi.yaml", arguments={"title": "openapi spec Example"})
app.add_api("swagger.yaml", arguments={"title": "swagger spec Example"})


if __name__ == "__main__":
    app.run(f"{Path(__file__).stem}:app", port=8080)
