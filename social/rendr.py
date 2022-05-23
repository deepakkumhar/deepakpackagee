from django.http import JsonResponse
from rest_framework import renderers
import json
from rest_framework import status

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({
                    'ResponseCode': status.HTTP_404_NOT_FOUND,
                    'ResponseMessage': 'Sorry',
                    'ResponseData': data
                })
        else:
            response = json.dumps({
                    'ResponseCode': status.HTTP_200_OK,
                    'ResponseMessage': 'Success',
                    'ResponseData': data
                })
        return response

def error_404(request, code, message):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 404
    return response

def error_400(request, code, message):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 400
    return response


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        # 'token': token,
        # 'username': user.username,
        'user_id' : user.id,
        # 'email' : user.email
    }



