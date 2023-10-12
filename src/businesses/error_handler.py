from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, HTTPException
from .schemas import SQLAlchemyErrorMessage
import logging



def exception_handler(error):
    logging.warning(error)
    if isinstance(error, SQLAlchemyError):
        print("SQLAlchemy error: %s", str(error))
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)
    else:
        print("Unexpected error:", str(error))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(error)}")
