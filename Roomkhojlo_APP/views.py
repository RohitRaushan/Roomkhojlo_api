# garmentsApp/views.py
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Tenant, Landlord, Employee, Agent, Building, Booking, Payment, Review,enquiry
from .serializers import TenantSerializer, LandlordSerializer, EmployeeSerializer, AgentSerializer, BookingSerializer, PaymentSerializer, ReviewSerializer, enquirySerializer
from rest_framework.permissions import BasePermission
from .custom_permissions import IsAuthenticatedEmployee
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework import status
from .serializers import buildingSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Tenant, Landlord, Employee, Agent
from django.contrib.auth.hashers import check_password
from .custom_token import generate_token, MultiModelTokenAuthentication
from rest_framework.exceptions import PermissionDenied
# Create view for Tenant
class TenantCreateView(generics.CreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [AllowAny]

class TenantDetailView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            user = request.user
            if hasattr(user, 'role') and user.role == 'tenant':
                tenant = Tenant.objects.get(pk=id)
                serializer = TenantSerializer(tenant)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data,
                }, status=status.HTTP_200_OK)
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Tenant.DoesNotExist:
            return Response({
                'isSuccess': False,
                "error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

class TenantUpdateView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            tenant = Tenant.objects.get(id=id)
        except Tenant.DoesNotExist:
            return Response({
                'isSuccess' : True,
                "error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TenantSerializer(tenant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'isSuccess' : True,
                'message' : "Tenant updated successfully",
                'data' : serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TenantDeleteView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            tenant = Tenant.objects.get(id=id)
        except Tenant.DoesNotExist:
            return Response({
                'isSuccess' : False,
                "error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        tenant.delete()
        return Response({"isSuccess": True,
                         'message' : 'Tenant deleted Successfully'
                         },status=status.HTTP_204_NO_CONTENT)


# Create view for Landlord
class LandlordCreateView(generics.CreateAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    permission_classes = [AllowAny]

class LandlordListView(APIView):
    def get(self, request):
        landlords = Landlord.objects.all()
        serializer = LandlordSerializer(landlords, many=True)
        return Response({
            'isSuccess': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class LandlordListAuthView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        landlords = Landlord.objects.all()
        serializer = LandlordSerializer(landlords, many=True)
        return Response({
            'isSuccess': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class LandlordDetailView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            user = request.user
            if hasattr(user, 'role') and user.role == 'landlord':
                landlord = Landlord.objects.get(pk=id)
                serializer = LandlordSerializer(landlord)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Landlord.DoesNotExist:
            return Response({'isSuccess': False,"error": "Landlord not found"}, status=status.HTTP_404_NOT_FOUND)

class LandlordUpdateView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            landlord = Landlord.objects.get(id=id)
        except Landlord.DoesNotExist:
            return Response({'isSuccess': False,"error": "Landlord not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LandlordSerializer(landlord, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'isSuccess': True,
                             'data': serializer.data
                             }, status=status.HTTP_200_OK)
        return Response({"isSuccess":True,
                         "message":serializer.errors
                         }, status=status.HTTP_400_BAD_REQUEST)

class LandlordDeleteView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            landlord = Landlord.objects.get(id=id)
        except Landlord.DoesNotExist:
            return Response({"isSuccess":True,"error": "Landlord not found"}, status=status.HTTP_404_NOT_FOUND)
        
        landlord.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create view for Employee
class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()

        return Response({
            'isSuccess': True,
            'message': employee.name+'Employee created successfully',
            
        }, status=status.HTTP_201_CREATED)
# create view for employee with token
class EmployeeCreateTokenView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class EmployeeListView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if hasattr(user, 'role') and user.role in ['employee', 'Admin', 'SuperAdmin']:
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response({
                "isSuccess": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "isSuccess": False,
            "error": "Unauthorized"
        }, status=status.HTTP_403_FORBIDDEN)

class EmployeeDetailView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        print('employee detail')
        try:
            user = request.user
            if hasattr(user, 'role') and user.role in ['employee', 'Admin', 'SuperAdmin']:
                employee = Employee.objects.get(pk=id)
                serializer = EmployeeSerializer(employee)
                return Response({"isSuccess":True,
                                 "data":serializer.data
                                 }, status=status.HTTP_200_OK)
            return Response({"isSuccess":False,"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Employee.DoesNotExist:
            return Response({"isSuccess":False,"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

class EmployeeUpdateView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):  # Optional: change to `patch()` for REST compliance
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response({
                "isSuccess": False,
                "error": "Employee not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "isSuccess": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "isSuccess": False,
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDeleteView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response({"isSuccess":False,"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create view for Agent
class AgentCreateView(generics.CreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [AllowAny]

class AgentDetailView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            user = request.user
            if hasattr(user, 'role') and user.role == 'agent':
                agent = Agent.objects.get(pk=id)
                serializer = AgentSerializer(agent)
                return Response({"isSuccess":True,
                                 "data":serializer.data
                                 }, status=status.HTTP_200_OK)
            return Response({"isSuccess":False,"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Agent.DoesNotExist:
            return Response({"isSuccess":False,"error": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)

class AgentUpdateView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            agent = Agent.objects.get(id=id)
        except Agent.DoesNotExist:
            return Response({"isSuccess":False,"error": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AgentSerializer(agent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"isSuccess":True,
                             "data": serializer.data
                             }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgentDeleteView(APIView):
    authentication_classes = [MultiModelTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            agent = Agent.objects.get(id=id)
        except Agent.DoesNotExist:
            return Response({"isSuccess":False,"error": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
        
        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# garmentsApp/views.py


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        contact = request.data.get('contact')
        password = request.data.get('password')

        if not contact or not password:
            return Response({"isSuccess":False,'message': 'Contact and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        user_model=None
        for model in [Tenant, Landlord, Employee, Agent]:
            potential_user = model.objects.filter(contact=contact).first()
            if potential_user and check_password(password, potential_user.password):
                user_model=model
                if not potential_user.is_active:
                    return Response({"isSuccess":False,'message': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)
                user = potential_user
                break

        if not user:
            return Response({"isSuccess":True,'message': 'Invalid contact or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT token
        model_name = user_model.__name__
        if not model_name:
            return Response({
                'isSuccess': False,
                'messages':"Model name is required!"
            })
        token = generate_token(user, model_name)
        user.token=token
        user.save()
        return Response({
            'isSuccess': True,
            'id' : user.id,
            'name': user.name,
            'role': user.role,
            'token': token,
        })
    
class LandlordCreateByEmployeeView(generics.CreateAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to create landlords.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save landlord with emp_id automatically filled
        landlord = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Landlord created successfully.",
            "landlord": {
                "id": landlord.id,
                "name": landlord.name,
                "contact": landlord.contact,
                "email": landlord.email,
                "emp_id": landlord.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class LandlordDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LandlordSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() in ['employee', 'admin', 'superadmin']:                
                landlord = Landlord.objects.get(pk=id)
                serializer = LandlordSerializer(landlord)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Landlord.DoesNotExist:
            return Response({'isSuccess': False,"error": "Landlord not found"}, status=status.HTTP_404_NOT_FOUND)

class LandlordListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        landlords = Landlord.objects.filter(emp_id=user.id)

        serializer = LandlordSerializer(landlords, many=True)

        return Response({
            'isSuccess': True,
            'count': landlords.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK) 

class LandlordUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LandlordSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to update landlords.")

        try:
            landlord = Landlord.objects.get(pk=id)

            # Ensure that the landlord was created by the current employee
            if str(landlord.emp_id) != str(user.id):
                raise PermissionDenied("You can only update landlords you created.")

            serializer = LandlordSerializer(landlord, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Landlord updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Landlord.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Landlord not found."
            }, status=status.HTTP_404_NOT_FOUND)

class LandlordDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to delete landlords.")

        try:
            landlord = Landlord.objects.get(pk=id)

            # Ensure that the landlord was created by the current employee
            if str(landlord.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete landlords you created.")

            landlord.delete()

            return Response({
                'isSuccess': True,
                'message': "Landlord deleted successfully."
            }, status=status.HTTP_200_OK)

        except Landlord.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Landlord not found."
            }, status=status.HTTP_404_NOT_FOUND)  

class TenantCreateByEmployeeView(generics.CreateAPIView):
    queryset = Landlord.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to create tenants.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save tenant with emp_id automatically filled
        tenant = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Tenant created successfully.",
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "contact": tenant.contact,
                "email": tenant.email,
                "emp_id": tenant.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class TenantDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TenantSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() in ['employee', 'admin', 'superadmin']:                
                tenant = Tenant.objects.get(pk=id)
                serializer = Tenant(tenant)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Tenant.DoesNotExist:
            return Response({'isSuccess': False,"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

class TenantListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        tenant = Tenant.objects.filter(emp_id=user.id)

        serializer = TenantSerializer(tenant, many=True)

        return Response({
            'isSuccess': True,
            'count': tenant.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class TenantUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TenantSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees are allowed to update tenants.")

        try:
            tenant = Tenant.objects.get(pk=id)

            # Ensure that the tenant was created by the current employee
            if str(tenant.emp_id) != str(user.id):
                raise PermissionDenied("You can only update tenants you created.")

            serializer = TenantSerializer(tenant, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Tenant updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Tenant.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Tenant not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class TenantDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to delete tenants.")

        try:
            tenant = Tenant.objects.get(pk=id)

            # Ensure that the tenant was created by the current employee
            if str(tenant.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete tenants you created.")

            tenant.delete()

            return Response({
                'isSuccess': True,
                'message': "Tenant deleted successfully."
            }, status=status.HTTP_200_OK)

        except Tenant.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Tenant not found."
            }, status=status.HTTP_404_NOT_FOUND)

class AgentCreateByEmployeeView(generics.CreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees are allowed to create agents.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save agent with emp_id automatically filled
        agent = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Agent created successfully.",
            "agent": {
                "id": agent.id,
                "name": agent.name,
                "contact": agent.contact,
                "email": agent.email,
                "emp_id": agent.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class AgentDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:                
                agent = Agent.objects.get(pk=id)
                serializer = AgentSerializer(agent)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Agent.DoesNotExist:
            return Response({'isSuccess': False,"error": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)

class AgentListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        agent = Agent.objects.filter(emp_id=user.id)

        serializer = AgentSerializer(agent, many=True)

        return Response({
            'isSuccess': True,
            'count': agent.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class AgentUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to update agents.")

        try:
            agent = Agent.objects.get(pk=id)

            # Ensure that the agent was created by the current employee
            if str(agent.emp_id) != str(user.id):
                raise PermissionDenied("You can only update agents you created.")

            serializer = AgentSerializer(agent, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Agent updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Agent.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Agent not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class AgentDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to delete agents.")

        try:
            agent = Agent.objects.get(pk=id)

            # Ensure that the agent was created by the current employee
            if str(agent.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete agents you created.")

            agent.delete()

            return Response({
                'isSuccess': True,
                'message': "Agent deleted successfully."
            }, status=status.HTTP_200_OK)

        except Agent.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Agent not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BuildingCreateByEmployeeView(generics.CreateAPIView):
    queryset = Building.objects.all()
    serializer_class = buildingSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to create buildings.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save building with emp_id automatically filled
        building = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Building created successfully.",
            "building": {
                "id": building.id,
                "name": building.building_name,
                "emp_id": building.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class BuildingDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = buildingSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() in ['employee', 'admin', 'superadmin']:                
                building = Building.objects.get(pk=id)
                serializer = buildingSerializer(building)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Building.DoesNotExist:
            return Response({'isSuccess': False,"error": "Building not found"}, status=status.HTTP_404_NOT_FOUND)

class BuildingListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        building = Building.objects.filter(emp_id=user.id)

        serializer = buildingSerializer(building, many=True)

        return Response({
            'isSuccess': True,
            'count': building.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class BuildingUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = buildingSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to update buildings.")

        try:
            building = Building.objects.get(pk=id)

            # Ensure that the building was created by the current employee
            if str(building.emp_id) != str(user.id):
                raise PermissionDenied("You can only update buildings you created.")

            serializer = buildingSerializer(building, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Building updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Building.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Building not found."
            }, status=status.HTTP_404_NOT_FOUND)

class BuildingDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() not in ['employee', 'admin', 'superadmin']:
            raise PermissionDenied("Only employees, admins, or superadmins are allowed to delete buildings.")

        try:
            building = Building.objects.get(pk=id)

            # Ensure that the building was created by the current employee
            if str(building.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete buildings you created.")

            building.delete()

            return Response({
                'isSuccess': True,
                'message': "Building deleted successfully."
            }, status=status.HTTP_200_OK)

        except Building.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Building not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
#building by landlord
class BuildingCreateByLandlordView(generics.CreateAPIView):
    queryset = Building.objects.all()
    serializer_class = buildingSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            raise PermissionDenied("Only landlords are allowed to create buildings.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save building with landlord_id automatically filled
        building = serializer.save(landlord_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Building created successfully.",
            "building": {
                "id": building.id,
                "name": building.building_name,
                "landlord_id": building.landlord_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class BuildingDetailByLandlordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = buildingSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() == 'landlord':                
                building = Building.objects.get(pk=id)
                serializer = buildingSerializer(building)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Building.DoesNotExist:
            return Response({'isSuccess': False,"error": "Building not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BuildingListByLandlordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        building = Building.objects.filter(landlord_id=user.id)

        serializer = buildingSerializer(building, many=True)

        return Response({
            'isSuccess': True,
            'count': building.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class BuildingUpdateByLandlordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = buildingSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            raise PermissionDenied("Only landlords are allowed to update buildings.")

        try:
            building = Building.objects.get(pk=id)

            # Ensure that the building was created by the current landlord
            if str(building.landlord_id) != str(user.id):
                raise PermissionDenied("You can only update buildings you created.")

            serializer = buildingSerializer(building, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Building updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Building.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Building not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BuildingDeleteByLandlordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            raise PermissionDenied("Only landlords are allowed to delete buildings.")

        try:
            building = Building.objects.get(pk=id)

            # Ensure that the building was created by the current landlord
            if str(building.landlord_id) != str(user.id):
                raise PermissionDenied("You can only delete buildings you created.")

            building.delete()

            return Response({
                'isSuccess': True,
                'message': "Building deleted successfully."
            }, status=status.HTTP_200_OK)

        except Building.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Building not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
#booking by employee
class BookingCreateByEmployeeView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to create bookings.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save booking with emp_id automatically filled
        booking = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Booking created successfully.",
            "booking": {
                "id": booking.id,
                "name": booking.name,
                "emp_id": booking.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class BookingDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() == 'employee':                
                booking = Booking.objects.get(pk=id)
                serializer = BookingSerializer(booking)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Booking.DoesNotExist:
            return Response({'isSuccess': False,"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BookingListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        booking = Booking.objects.filter(emp_id=user.id)

        serializer = BookingSerializer(booking, many=True)

        return Response({
            'isSuccess': True,
            'count': booking.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class BookingUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to update bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current employee
            if str(booking.emp_id) != str(user.id):
                raise PermissionDenied("You can only update bookings you created.")

            serializer = BookingSerializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Booking updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BookingDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to delete bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current employee
            if str(booking.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete bookings you created.")

            booking.delete()

            return Response({
                'isSuccess': True,
                'message': "Booking deleted successfully."
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BookingCreateByLandlordView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            raise PermissionDenied("Only landlords are allowed to create bookings.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save booking with landlord_id automatically filled
        booking = serializer.save(landlord_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Booking created successfully.",
            "booking": {
                "id": booking.id,
                "name": booking.name,
                "landlord_id": booking.landlord_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class BookingDetailByLandlordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() != 'landlord':                
                booking = Booking.objects.get(pk=id)
                serializer = BookingSerializer(booking)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Booking.DoesNotExist:
            return Response({'isSuccess': False,"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BookingListByLandlordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        booking = Booking.objects.filter(landlord_id=user.id)

        serializer = BookingSerializer(booking, many=True)

        return Response({
            'isSuccess': True,
            'count': booking.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class BookingUpdateByLandlordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            raise PermissionDenied("Only landlords are allowed to update bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current landlord
            if str(booking.landlord_id) != str(user.id):
                raise PermissionDenied("You can only update bookings you created.")

            serializer = BookingSerializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Booking updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BookingDeleteByLandlordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'landlord':
            raise PermissionDenied("Only landlords are allowed to delete bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current landlord
            if str(booking.landlord_id) != str(user.id):
                raise PermissionDenied("You can only delete bookings you created.")

            booking.delete()

            return Response({
                'isSuccess': True,
                'message': "Booking deleted successfully."
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BookingCreateByAgentView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'agent':
            raise PermissionDenied("Only agents are allowed to create bookings.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save booking with agent_id automatically filled
        booking = serializer.save(agent_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Booking created successfully.",
            "booking": {
                "id": booking.id,
                "name": booking.name,
                "agent_id": booking.agent_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class BookingDetailByAgentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() != 'agent':                
                booking = Booking.objects.get(pk=id)
                serializer = BookingSerializer(booking)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Booking.DoesNotExist:
            return Response({'isSuccess': False,"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

class BookingListByAgentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'agent':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        booking = Booking.objects.filter(agent_id=user.id)

        serializer = BookingSerializer(booking, many=True)

        return Response({
            'isSuccess': True,
            'count': booking.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class BookingUpdateByAgentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'agent':
            raise PermissionDenied("Only agents are allowed to update bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current agent
            if str(booking.agent_id) != str(user.id):
                raise PermissionDenied("You can only update bookings you created.")

            serializer = BookingSerializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Booking updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)

class BookingDeleteByAgentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'agent':
            raise PermissionDenied("Only agents are allowed to delete bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current agent
            if str(booking.agent_id) != str(user.id):
                raise PermissionDenied("You can only delete bookings you created.")

            booking.delete()

            return Response({
                'isSuccess': True,
                'message': "Booking deleted successfully."
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BookingCreateByTenantView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'tenant':
            raise PermissionDenied("Only tenants are allowed to create bookings.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save booking with tenant_id automatically filled
        booking = serializer.save(tenant_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Booking created successfully.",
            "booking": {
                "id": booking.id,
                "name": booking.name,
                "tenant_id": booking.tenant_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class BookingDetailByTenantView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() != 'tenant':                
                booking = Booking.objects.get(pk=id)
                serializer = BookingSerializer(booking)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Booking.DoesNotExist:
            return Response({'isSuccess': False,"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BookingListByTenantView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'tenant':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        booking = Booking.objects.filter(tenant_id=user.id)

        serializer = BookingSerializer(booking, many=True)

        return Response({
            'isSuccess': True,
            'count': booking.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class BookingUpdateByTenantView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'tenant':
            raise PermissionDenied("Only tenants are allowed to update bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current tenant
            if str(booking.tenant_id) != str(user.id):
                raise PermissionDenied("You can only update bookings you created.")

            serializer = BookingSerializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Booking updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class BookingDeleteByTenantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'tenant':
            raise PermissionDenied("Only tenants are allowed to delete bookings.")

        try:
            booking = Booking.objects.get(pk=id)

            # Ensure that the booking was created by the current tenant
            if str(booking.tenant_id) != str(user.id):
                raise PermissionDenied("You can only delete bookings you created.")

            booking.delete()

            return Response({
                'isSuccess': True,
                'message': "Booking deleted successfully."
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Booking not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
#Payment by employee
class PaymentCreateByEmployeeView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to create payments.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save payment with emp_id automatically filled
        payment = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Payment created successfully.",
            "payment": {
                "id": payment.id,
                "emp_id": payment.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class PaymentDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() == 'employee':                
                payment = Payment.objects.get(pk=id)
                serializer = PaymentSerializer(payment)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Payment.DoesNotExist:
            return Response({'isSuccess': False,"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
class PaymentListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        payment = Payment.objects.filter(emp_id=user.id)

        serializer = PaymentSerializer(payment, many=True)

        return Response({
            'isSuccess': True,
            'count': payment.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class PaymentUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to update payments.")

        try:
            payment = Payment.objects.get(pk=id)

            # Ensure that the payment was created by the current employee
            if str(payment.emp_id) != str(user.id):
                raise PermissionDenied("You can only update payments you created.")

            serializer = PaymentSerializer(payment, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Payment updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Payment.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Payment not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class PaymentDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to delete payments.")

        try:
            payment = Payment.objects.get(pk=id)

            # Ensure that the payment was created by the current employee
            if str(payment.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete payments you created.")

            payment.delete()

            return Response({
                'isSuccess': True,
                'message': "Payment deleted successfully."
            }, status=status.HTTP_200_OK)

        except Payment.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Payment not found."
            }, status=status.HTTP_404_NOT_FOUND)

#review without authenticaion
class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # No permission_classes, open access

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Simply save the review (no auto emp_id handling now)
        review = serializer.save()

        response_data = {
            "isSuccess": True,
            "message": "Review created successfully.",
            "review": {
                "id": review.id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
#Review by employee       
class ReviewCreateByEmployeeView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to create reviews.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save review with emp_id automatically filled
        review = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Review created successfully.",
            "review": {
                "id": review.id,
                "emp_id": review.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class ReviewDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() == 'employee':                
                review = Review.objects.get(pk=id)
                serializer = ReviewSerializer(review)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except Review.DoesNotExist:
            return Response({'isSuccess': False,"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
#review list without authentication
class ReviewListPublicView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)

        return Response({
            'isSuccess': True,
            'count': reviews.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK) 
     
class ReviewListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        review = Review.objects.filter(emp_id=user.id)

        serializer = ReviewSerializer(review, many=True)

        return Response({
            'isSuccess': True,
            'count': review.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class ReviewUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to update reviews.")

        try:
            review = Review.objects.get(pk=id)

            # Ensure that the review was created by the current employee
            if str(review.emp_id) != str(user.id):
                raise PermissionDenied("You can only update reviews you created.")

            serializer = ReviewSerializer(review, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Review updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Review not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class ReviewDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to delete reviews.")

        try:
            review = Review.objects.get(pk=id)

            # Ensure that the review was created by the current employee
            if str(review.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete reviews you created.")

            review.delete()

            return Response({
                'isSuccess': True,
                'message': "Review deleted successfully."
            }, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Review not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
#get all building without authentication
class BuildingListView(APIView):
    # No permission_classes → public access

    def get(self, request):
        buildings = Building.objects.all()  # Fetch all buildings

        serializer = buildingSerializer(buildings, many=True)

        return Response({
            'isSuccess': True,
            'count': buildings.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
#building filter 
class BuildingFilteredListView(APIView):
    def get(self, request):
        queryset = Building.objects.all()

        filter_fields = {
            'state__iexact': 'state',
            'building_name__iexact': 'building_name',
            'city__iexact': 'city',
            'district__iexact': 'district',
            'room_type__iexact': 'room_type',
            'gender__iexact': 'gender',
            'amenities__iexact': 'amenities',
            'locality__iexact': 'locality',
            'pincode__iexact': 'pincode',
            'furnishing_status__iexact': 'furnishing_status',
        }

        # Build filters from standard params
        filters = {
            model_field: request.query_params.get(param_name)
            for model_field, param_name in filter_fields.items()
            if request.query_params.get(param_name) is not None
        }

        # Special logic: match 'occupancy' and 'tenants_type' to room_type
        for param in ['occupancy', 'tenants_type']:
            value = request.query_params.get(param)
            if value:
                filters['room_type__iexact'] = value

        # Apply filters
        if filters:
            queryset = queryset.filter(**filters)

        serializer = buildingSerializer(queryset, many=True)

        return Response({
            'isSuccess': True,
            'count': queryset.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)

#enquiry without authentication
class EnquiryCreateView(generics.CreateAPIView):
    queryset = enquiry.objects.all()
    serializer_class = enquirySerializer
    permission_classes = [AllowAny]  # No authentication required

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save enquiry without setting emp_id
        enquiry_instance = serializer.save()

        response_data = {
            "isSuccess": True,
            "message": "Enquiry created successfully.",
            "enquiry": {
                "id": enquiry_instance.id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class EnquiryCreateByEmployeeView(generics.CreateAPIView):
    queryset = enquiry.objects.all()
    serializer_class = enquirySerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to create enquiries.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save enquiry with emp_id automatically filled
        enquiry = serializer.save(emp_id=user.id)

        response_data = {
            "isSuccess": True,
            "message": "Enquiry created successfully.",
            "enquiry": {
                "id": enquiry.id,
                "emp_id": enquiry.emp_id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class EnquiryDetailByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = enquirySerializer
    def get(self, request, id=None):
        try:
            user = request.user
            if not hasattr(user, 'role') or user.role.lower() != 'employee':                
                enquiry = enquiry.objects.get(pk=id)
                serializer = enquirySerializer(enquiry)
                return Response({
                    'isSuccess' : True,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        except enquiry.DoesNotExist:
            return Response({'isSuccess': False,"error": "Enquiry not found"}, status=status.HTTP_404_NOT_FOUND)
        
class EnquiryListByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            return Response({
                'isSuccess': False,
                "error": "Unauthorized"
            }, status=status.HTTP_403_FORBIDDEN)

        enquiry = enquiry.objects.filter(emp_id=user.id)

        serializer = enquirySerializer(enquiry, many=True)

        return Response({
            'isSuccess': True,
            'count': enquiry.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class EnquiryUpdateByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = enquirySerializer

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to update enquiries.")

        try:
            enquiry = enquiry.objects.get(pk=id)

            # Ensure that the enquiry was created by the current employee
            if str(enquiry.emp_id) != str(user.id):
                raise PermissionDenied("You can only update enquiries you created.")

            serializer = enquirySerializer(enquiry, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'isSuccess': True,
                'message': "Enquiry updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except enquiry.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Enquiry not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class EnquiryDeleteByEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user

        if not hasattr(user, 'role') or user.role.lower() != 'employee':
            raise PermissionDenied("Only employees are allowed to delete enquiries.")

        try:
            enquiry = enquiry.objects.get(pk=id)

            # Ensure that the enquiry was created by the current employee
            if str(enquiry.emp_id) != str(user.id):
                raise PermissionDenied("You can only delete enquiries you created.")

            enquiry.delete()

            return Response({
                'isSuccess': True,
                'message': "Enquiry deleted successfully."
            }, status=status.HTTP_200_OK)

        except enquiry.DoesNotExist:
            return Response({
                'isSuccess': False,
                'error': "Enquiry not found."
            }, status=status.HTTP_404_NOT_FOUND)
        

#booking create without authentication
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = serializer.save()

        response_data = {
            "isSuccess": True,
            "message": "Booking created successfully.",
            "booking": {
                "id": booking.id,
                "name": booking.name,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class BookingListView(APIView):

    def get(self, request):
        bookings = Booking.objects.all()  

        serializer = BookingSerializer(bookings, many=True)

        return Response({
            'isSuccess': True,
            'count': bookings.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
