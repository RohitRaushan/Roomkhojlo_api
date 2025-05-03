from rest_framework import serializers
from .models import enquiry
from rest_framework import serializers
from .models import Tenant, Building, Booking, Payment, Review

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'email','password', 'contact', 'gender', 'address', 'photo', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            password = validated_data.pop('password')
            tenant = Tenant(**validated_data)
            tenant.set_password(password)
            tenant.save()
            return tenant

from .models import Landlord
class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields = ['id', 'name', 'email','password', 'contact', 'alternate_contact', 'address', 'photo', 'id_proof_type', 'id_proof_number', 'is_active', 'is_staff', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            password = validated_data.pop('password')
            landlord = Landlord(**validated_data)
            landlord.set_password(password)
            landlord.save()
            return landlord

from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email','password', 'contact', 'gender', 'date_of_birth', 'date_of_joining', 'salary', 'address', 'photo', 'role', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            password = validated_data.pop('password')
            employee = Employee(**validated_data)
            employee.set_password(password)
            employee.save()
            return employee
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

from .models import Agent

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'email','password', 'agency_name', 'contact', 'alternate_contact', 'address', 'photo', 'id_proof_type', 'id_proof_number', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            password = validated_data.pop('password')
            agent = Agent(**validated_data)
            agent.set_password(password)
            agent.save()
            return agent

class enquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = enquiry
        fields = ['id','name', 'contact', 'email','room_type','location','gender','assigned_to','status','created_at','updated_at']

class buildingSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Building
        fields = ['id','landlord_id','building_name','building_type','room_type','gender','amenities','furnishing_status','photo','total_floors','total_rooms','min_rent','max_rent','state','district','city','street_address','pincode','locality','lattitude','longitude','availability_status','emp_id','created_at','updated_at']

        read_only_fields = ['created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'building_id', 'agent_id', 'emp_id', 'tenant_id', 'landlord_id', 'name', 'contact', 'booking_date', 'check_in_date', 'duration_of_stay', 'rent_amt', 'deposit_amt', 'room_type', 'booking_status', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking_id', 'payment_id', 'payment_mdoe', 'payment_statue', 'payment_date', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'building_id', 'tenant_id','emp_id', 'rating','comment', 'created_at', 'updated_at']

