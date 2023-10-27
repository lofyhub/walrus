from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status, Response
import logging


# TODO: a beter way to log this errors i.e push them to discord for notification
def exception_handler(error):
    logging.warning(error)
    print(error)
    if isinstance(error, SQLAlchemyError):
        error_message = "Failed to save user:"
        return Response(
            content=error_message,
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    elif isinstance(error, IntegrityError):
        if "UNIQUE constraint failed: users.id" in str(error):
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save user: Duplicate ID detected",
            )
        else:
            raise Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save user",
            )
    else:
        error_message = "Unkown error has occured"
        return Response(
            content=error_message,
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
