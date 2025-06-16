from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class SomethingWentWrongException(BaseHTTPException):
    detail = "Something went wrong..."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class AnalyseIsNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Analyse is not found."
