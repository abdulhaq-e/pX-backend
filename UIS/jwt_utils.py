from datetime import datetime
from rest_framework_jwt.settings import api_settings

# from UIS.api.serialisers import UserSerialiser


def jwt_payload_handler(user):
    try:
        username = user.get_username()
    except AttributeError:
        username = user.username

    return {
        'user_id': str(user.pk),
        'email': user.email,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }


def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        # 'userID': UserSerialiser(user.userprofile).data
    }
