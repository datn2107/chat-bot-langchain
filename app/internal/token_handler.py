import os
import jwt
import logging
import requests
import datetime
from urllib.parse import quote_plus
from typing import Union

EMAIL_KEY = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
NAME_KEY = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"
ROLE_KEY = "http://schemas.microsoft.com/ws/2008/06/identity/claims/role"
USER_TYPE_KEY = "AccountType"

EMAIL_VERIFY_LOGGING = "Email Verification [{email}]: {message}"
TOKEN_VERIFY_LOGGING = "Token Verification [{token}]: {message}"


def generate_external_server_token() -> str:
    token = jwt.encode(
        {
            NAME_KEY: os.getenv("EXTERNAL_SERVER_NAME"),
            EMAIL_KEY: os.getenv("EXTERNAL_SERVER_EMAIL"),
            ROLE_KEY: "Admin",
            USER_TYPE_KEY: "Free",
            "StartDate": "1/1/0001 12:00:00 AM",
            "EndDate": "1/1/0001 12:00:00 AM",
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=int(os.getenv("JWT_EXPIRE_TIME"))),
            "iss": os.getenv("EXTERNAL_SERVER_ISS"),
            "aud": os.getenv("EXTERNAL_SERVER_AUD"),
        },
        os.environ.get("JWT_SECRET"),
        algorithm=os.environ.get("JWT_ALGORITHM"),
    )
    return token


def get_user_by_email(email: str) -> Union[dict, Exception]:
    url = os.getenv(
        "EXTERNAL_SERVER_URL"
    ) + "/api/Customer/GetByEmail?email={email}".format(email=quote_plus(email))
    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + generate_external_server_token()},
    )

    if response.status_code != 200:
        logging.debug(
            EMAIL_VERIFY_LOGGING.format(
                email=email,
                message="Response status {status} and message {message}".format(
                    status=response.status_code, message=response
                ),
            )
        )
        return None

    return response.json()


def is_valid_email(email: str) -> Union[bool, Exception]:
    response = get_user_by_email(email)

    try:
        response_email = response["accountTypeById"]["result"]["email"]
    except Exception as e:
        logging.debug(
            EMAIL_VERIFY_LOGGING.format(
                email=email, message="Response JSON wrong format"
            )
        )
        return False

    if response_email != email:
        logging.debug(
            EMAIL_VERIFY_LOGGING.format(
                email=email, message="Email not match with response"
            )
        )
        return False

    return True


def is_valid_token(token: str) -> Union[bool, Exception]:
    try:
        payload = jwt.decode(
            token,
            os.environ.get("JWT_SECRET"),
            algorithms=os.environ.get("JWT_ALGORITHM"),
            audience=os.environ.get("EXTERNAL_SERVER_AUD"),
        )

        if EMAIL_KEY not in payload:
            logging.debug(
                TOKEN_VERIFY_LOGGING.format(token=token, message="No email in token")
            )
            return False

        return True
    except Exception as e:
        logging.debug(TOKEN_VERIFY_LOGGING.format(token=token, message=str(e)))
        return False


def get_account_type(token: str) -> str:
    if not is_valid_token(token):
        logging.debug(
            TOKEN_VERIFY_LOGGING.format(
                token=token, message="Invalid Token ['function: get_account_type']"
            )
        )
        return None

    payload = jwt.decode(
        token,
        options={"verify_signature": False},
        algorithms=os.environ.get("JWT_ALGORITHM"),
    )
    return payload[USER_TYPE_KEY]


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    token = generate_external_server_token()
    print(token)
    print(is_valid_token(token))
    print(is_valid_email("khoa@gmail.com"))
    print(get_account_type(token))
