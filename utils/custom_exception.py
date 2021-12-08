from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        print(response.data)
        # print(response)
        def get_detail_error(ser):
            try:
                keys = list(ser.keys())
                values = list(ser.values())
                if keys[0] == "non_field_errors":
                    return values[0][0]
                errors_message = keys[0] + values[0][0]
                errors_message = errors_message.replace("null。", "空")
                return errors_message
            except Exception as e:
                print("错误信息 : ", e)
            return "error message"

        message = get_detail_error(response.data)

        response.data.clear()
        response.data['code'] = response.status_code
        response.data['data'] = None

        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "Not found"
                print(response)
            except KeyError:
                response.data['message'] = "Not found"
                print(response)

        if response.status_code == 400:
            response.data['code'] = 233
            response.data['message'] = message

        elif response.status_code == 401:
            response.data['message'] = "未登录，请先登录"

        elif response.status_code >= 500:
            response.data['message'] = "Internal service errors"

        elif response.status_code == 403:
            response.data['message'] = "Access denied"

        elif response.status_code == 405:
            response.data['message'] = 'Request method error'
        response.code = response.status_code
        response.status_code = 200
    return response
