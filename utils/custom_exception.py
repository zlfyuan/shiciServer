from rest_framework.views import exception_handler

from utils.custom_json_response import JsonResponse


def custom_exception_handler(exc, context):

    # Call REST framework's default exception handler
    response = exception_handler(exc, context)
    request = context['request']

    # print exception to console
    print(response)

    # Now add the HTTP status code to the response.
    if response is not None:
        code = 1
        if isinstance(response.data, list):
            msg = '; '.join(response.data)
        elif isinstance(response.data, str):
            msg = response.data
        elif isinstance(response.data, dict):
            msg = response.data['detail']
            code = response.status_code
        else:
            msg = 'Sorry, we make a mistake (*￣︶￣)!'
        return JsonResponse(data=None, code=code, msg=msg)

    # 如果 response 为 None 则直接触发上面的 ExceptionGlobeMiddleware
    return response
