# utils.py
import jwt
from datetime import datetime, timedelta,timezone
from django.conf import settings  # Use Django's SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Tenant, Landlord, Employee, Agent


def generate_token(user, model_name):
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user.id,
        'model': model_name,
        'exp': now + timedelta(days=1),  # Token valid for 1 day
        'iat': now
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

# authentication.py

MODEL_MAP = {
    'Tenant': Tenant,
    'Landlord': Landlord,
    'Employee': Employee,
    'Agent': Agent
}

class MultiModelTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No token provided

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        model_name = payload.get('model')
        user_id = payload.get('user_id')
        model = MODEL_MAP.get(model_name)
        if not model:
            raise AuthenticationFailed('Invalid model in token')
        try:
            user = model.objects.get(pk=user_id)
        except model.DoesNotExist:
            # raise AuthenticationFailed('User not found')
            raise AuthenticationFailed(f'{model_name} user with ID {user_id} does not exist.')

        return (user, token)
