import secrets
from fastapi import Request
import logging
from datetime import datetime


def create_random_session_string() -> str:
    return secrets.token_urlsafe(32)


def validate_session(request: Request) -> bool:
    session_authorization = request.cookies.get("Authorization")
    session_id = request.session.get("session_id")
    session_access_token = request.session.get("access_token")
    token_exp = request.session.get("token_exp")

    if not session_authorization and not session_access_token:
        logging.info(
            "No Authorization and access_token in session, redirecting to login"
        )
        return False

    if session_authorization != session_id:
        logging.info("Authorization does not match Session Id, redirecting to login")
        return False

    if is_token_exp(token_exp):
        logging.info("Access token is expired, redirecting to login")

    return True


def is_token_exp(timestamp: int) -> bool:
    if timestamp:
        formatted_timestamp = datetime.fromtimestamp(timestamp)
        current_date = datetime.now()
        difference_in_minutes = (
            formatted_timestamp - current_date
        ).total_seconds() / 60
        return difference_in_minutes <= 0

    return True
