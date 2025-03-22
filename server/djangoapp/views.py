# Uncomment the required imports before adding the code

import json
import logging


from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.models import (
    User,
)
from django.http import (
    JsonResponse,
)

from django.views.decorators.csrf import (
    csrf_exempt,
)

from .models import (
    CarMake,
    CarModel,
)
from .populate import (
    initiate,
)
from .restapis import (
    analyze_review_sentiments,
    get_request,
    post_review,
)

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(
    request,
):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    # Try to check if provide credential can be authenticated
    user = authenticate(
        username=username,
        password=password,
    )
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(
            request,
            user,
        )
        data = {
            "userName": username,
            "status": "Authenticated",
        }
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(
    request,
):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        data = {
            "userName": username,
            "status": "Logged out",
        }
    else:
        data = {"status": "No active session"}

    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(
    request,
):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    username_exist = False
    email_exist = False

    # Check if user already exists
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        # If not, simply log this is a new user
        pass

    # Check if email already exists
    try:
        User.objects.get(email=email)
        email_exist = True
    except User.DoesNotExist:
        pass

    if username_exist:
        data = {
            "userName": username,
            "error": "Username already exists",
        }
        return JsonResponse(data)

    if email_exist:
        data = {
            "email": email,
            "error": "Email already exists",
        }
        return JsonResponse(data)

    # Create user in the auth_user table
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )

    # Login the user automatically
    login(
        request,
        user,
    )

    # Respond with username and status
    data = {
        "userName": username,
        "status": "Authenticated",
    }
    return JsonResponse(data)


# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(
    request,
    state="All",
):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse(
        {
            "status": 200,
            "dealers": dealerships,
        }
    )


def get_dealer_details(
    request,
    dealer_id,
):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse(
            {
                "status": 200,
                "dealer": dealership,
            }
        )
    else:
        return JsonResponse(
            {
                "status": 400,
                "message": "Bad Request",
            }
        )


def get_dealer_reviews(
    request,
    dealer_id,
):
    # if dealer id has been provided
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            print(response)
            review_detail["sentiment"] = response["sentiment"]
        return JsonResponse(
            {
                "status": 200,
                "reviews": reviews,
            }
        )
    else:
        return JsonResponse(
            {
                "status": 400,
                "message": "Bad Request",
            }
        )


def add_review(
    request,
):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse(
                {
                    "status": 401,
                    "message": "Error in posting review",
                }
            )
    else:
        return JsonResponse(
            {
                "status": 403,
                "message": "Unauthorized",
            }
        )


def get_cars(
    request,
):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append(
            {
                "CarModel": car_model.name,
                "CarMake": car_model.car_make.name,
            }
        )
    return JsonResponse({"CarModels": cars})
