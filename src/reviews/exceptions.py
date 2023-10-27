from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status, Response
import logging


def exception_handler(error):
    logging.warning(error)
    print(error)
    error_message = "Unknown error has occurred"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    if isinstance(error, SQLAlchemyError):
        error_message = "Failed to save review"
    elif isinstance(error, IntegrityError):
        if "UNIQUE constraint failed: users.id" in str(error):
            error_message = "Failed to save user: Duplicate ID detected"
        else:
            error_message = "Failed to save user"

    return Response(
        content=error_message,
        media_type="application/json",
        status_code=status_code,
    )
