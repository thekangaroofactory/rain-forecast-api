from pathlib import Path
import datetime

import connexion
from connexion.exceptions import OAuthProblem
import orm
from connexion import NoContent


# -- Replace this by an env variable
TOKEN_DB = {"asdf1234567890": {"uid": 100}}

db_session = None


def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem("Invalid token")

    return info


# get object from database

def get_resources(limit):
    q = db_session.query(orm.Resource)
    return [p.dump() for p in q][:limit]


def get_resource(resource_id):
    resource = db_session.query(orm.Resource).filter(orm.Resource.id == resource_id).one_or_none()
    return resource.dump() if resource is not None else ("Not found", 404)


def put_resource(resource_id, resource):
    p = db_session.query(orm.Resource).filter(orm.Resource.id == resource_id).one_or_none()
    resource["id"] = resource_id
    if p is not None:
        # logging.info("Updating resource %s..", resource_id)
        p.update(**resource)
    else:
        # logging.info("Creating resource %s..", resource_id)
        resource["created"] = datetime.datetime.utcnow()
        db_session.add(orm.Resource(**resource))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_resource(resource_id):
    resource = db_session.query(orm.Resource).filter(orm.Resource.id == resource_id).one_or_none()
    if resource is not None:
        # logging.info("Deleting resource %s..", resource_id)
        db_session.query(orm.Resource).filter(orm.Resource.id == resource_id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404


# referenced in the spec file (swagger): operationId: app.post_greeting
def post_greeting(name: str) -> str:
    return f"Hello {name}"


# os.environ['USER']


dialect = "postgresql"
db_user = "tilxuclh"
db_pwd = "hK3oZSbfZC9FlNzC5nUvGp05_SbUc9yt"
db_url = "abul.db.elephantsql.com"
db_name = "tilxuclh"
db_uri = dialect + "://" + db_user + ":" + db_pwd + "@" + db_url + "/" +db_name
# "postgresql://tilxuclh:hK3oZSbfZC9FlNzC5nUvGp05_SbUc9yt@abul.db.elephantsql.com/tilxuclh"


# logging.basicConfig(level=logging.INFO)
db_session = orm.init_db(db_uri)


# define the api(s)
app = connexion.FlaskApp(__name__, specification_dir="spec/")
app.add_api("openapi.yaml", arguments={"title": "openapi spec Example"})
app.add_api("swagger.yaml", arguments={"title": "swagger spec Example"})

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(f"{Path(__file__).stem}:app", port=8080)
