from psycopg2 import Error
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if isinstance(exc, Error):
        return Response(
            {"error_message": "Something wrong with database"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
