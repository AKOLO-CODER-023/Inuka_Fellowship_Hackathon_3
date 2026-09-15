import requests


BASE_URL = "http://127.0.0.1:8000"


def get_health():
    response = requests.get(
        f"{BASE_URL}/health"
    )
    response.raise_for_status()
    return response.json()


def get_inventory():

    response = requests.get(
        f"{BASE_URL}/inventory"
    )

    response.raise_for_status()

    return response.json()


def get_alerts():

    response = requests.get(
        f"{BASE_URL}/alerts"
    )

    response.raise_for_status()

    return response.json()


def get_batches():

    response = requests.get(
        f"{BASE_URL}/batches"
    )

    response.raise_for_status()

    return response.json()


def get_roi():

    response = requests.get(
        f"{BASE_URL}/roi"
    )

    response.raise_for_status()

    return response.json()