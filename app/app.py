from pathlib import Path

import connexion


# referenced in the spec file(s): operationId: app.post_greeting
def post_greeting(name: str) -> str:
    return f"Hello {name}"


# define the api(s)
app = connexion.FlaskApp(__name__, specification_dir="spec/")
app.add_api("openapi.yaml", arguments={"title": "openapi spec Example"})
app.add_api("swagger.yaml", arguments={"title": "swagger spec Example"})


if __name__ == "__main__":
    app.run(f"{Path(__file__).stem}:app", port=8080)
