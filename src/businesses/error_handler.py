from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, Response
import logging


# TODO: a beter way to log this errors i.e push them to discord for notification
def exception_handler(error):
    logging.warning(error)
    print(error)
    if isinstance(error, SQLAlchemyError):
        error_message = "An error occured while saving the Business"
        return Response(
            content=error_message,
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    else:
        error_message = "Unkown error has occured"
        return Response(
            content=error_message,
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
