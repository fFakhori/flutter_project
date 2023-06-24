from rest_framework import serializers
from api.models import User, Request, Ride


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'address',
                  'photo',
                  'password',
                  'role',
                  'identity_code',
                  'rating')
        extra_kwargs = {
            'email': {'required': False},
            'password': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False},
            'photo': {'required': False},
            'role': {'required': False},
            'identity_code': {'required': False},
            'rating': {'required': False}
        }


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id',
                  'driver',
                  'type',
                  'identity',
                  'licence',
                  'matriculation',
                  'status')
        extra_kwargs = {
            'status': {'required': False}
        }


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('id',
                  'client',
                  'driver',
                  'source',
                  'day',
                  'time',
                  'destination',
                  'destination_name',
                  'price',
                  'status',
                  'distance',
                  'rating')
        extra_kwargs = {
            'rating': {'required': False}
        }
