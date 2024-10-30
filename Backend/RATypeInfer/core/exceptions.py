from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "error": response.data.get("detail", "An error occurred"),
            "status_code": response.status_code
        }
        response.data = custom_data
    else:
        # Fallback for unexpected errors
        response = Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
