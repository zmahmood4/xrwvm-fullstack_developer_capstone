# Uncomment the imports below before you add the function code
import os

import requests
from requests.exceptions import RequestException
from dotenv import (
    load_dotenv,
)

load_dotenv()

backend_url = os.getenv(
    "backend_url",
    default="http://localhost:3030",
)
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    default="http://localhost:5050/",
)


# def get_request(endpoint, **kwargs):
# Add code for get requests to back end
def get_request(
    endpoint,
    **kwargs,
):
    params = ""
    if kwargs:
        for (
            key,
            value,
        ) in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except RequestException as e:
        # If any network-related error occurs
        print(f"Network exception occurred: {e}")


# def analyze_review_sentiments(text):
def analyze_review_sentiments(
    text,
):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(
    data_dict,
):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(
            request_url,
            json=data_dict,
        )
        print(response.json())
        return response.json()
    except RequestException as e:
        print(f"Network exception occurred: {e}")
