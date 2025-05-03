from django.contrib.auth.backends import BaseBackend
from .models import Employee, Tenant, Landlord, Agent
class MultiModelAuthBackend(BaseBackend):
    def authenticate(self, request, contact=None, password=None):
        for model in [Employee, Tenant, Landlord, Agent]:
            try:
                user = model.objects.get(contact=contact)
                if user.check_password(password):
                    return user
            except model.DoesNotExist:
                continue
        return None

    def get_user(self, user_id):
        for model in [Employee, Tenant, Landlord, Agent]:
            try:
                return model.objects.get(pk=user_id)
            except model.DoesNotExist:
                continue
        return None
