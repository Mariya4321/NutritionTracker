import requests
from requests.auth import HTTPBasicAuth
import datetime as dt
import os

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["sheet_endpoint"]

app_id = os.environ["api_id"]
app_key = os.environ["api_key"]

basic = HTTPBasicAuth(os.environ["basic_un"], os.environ["basic_pss"])

weight = os.environ["weight"]
height = os.environ["height"]
age = os.environ["age"]

parameter = {
    "query": input("Tell me which exercise you did today: "),
    "weight_kg": weight,
    "height_cm": height,
    "age": age,
}

header = {
    "x-app-id": app_id,
    "x-app-key": app_key,
}

response = requests.post(url=exercise_endpoint, json=parameter, headers=header)
result = response.json()

date = dt.datetime.now().strftime("%d/%m/%Y")
time = dt.datetime.now().strftime("%X")

for exercise in result["exercises"]:
    row_parameter = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]}
    }
    get_response = requests.post(url=sheet_endpoint, json=row_parameter, auth=basic)
    print(get_response.text)
