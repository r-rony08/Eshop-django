
from http import HTTPStatus
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    print('response', response)

    if response is not None:
        http_code_to_message = {v.value: v. description for v in HTTPStatus}

        error_payload = {
            "error":{
                "Status_code": 0,
                "message": "",
                "details": []
            }
        }

        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data

        response.data = error_payload
        return response
    
    # else:
    #     error = {
    #         "error":"somthing Went Wrong"
    #     }

        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
