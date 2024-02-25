# rain-forecast-api
Python / Flask API

- Using connexion framework (to build the Flask API)
- API key authentication
- SQLAchemy + PostgreSQL database


Running:

`$ python app.py`

Now open your browser and go to http://localhost:8080/openapi/ui/ or 
http://localhost:8080/swagger/ui/ to see the Swagger UI.

The hardcoded apikey is asdf1234567890.

Test it out (in another terminal):

`$ curl -H 'X-Auth: asdf1234567890' http://localhost:8080/openapi/openapi/resources`