# capstone_api


### To run the fastapi api:
* uvicorn api.main:app


### Curl testing commands
* http://127.0.0.1:8000/


## Sample API calls

#### Test working correctly end to end with small sample
curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":10}"

#### Get best 15 movies (using full list)
curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":0}"

#### Get best 15 movies (running on Heroku)
curl -X POST "https://fifth-fastapi2.herokuapp.com/predict" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":0}"