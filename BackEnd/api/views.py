import os
import datetime
import bcrypt
import jwt
import base64

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db.models import Avg
from BackEnd.settings import SECRET_KEY
from api.models import User, Request, Ride
from api.serializers import UserSerializer, RequestSerializer, RideSerializer
from rest_framework.decorators import api_view


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        element = JSONParser().parse(request)
        element_serializer = UserSerializer(data=element)
        password = element_serializer.initial_data['password']
        encrypted = bcrypt.hashpw(bytes(str(password), 'utf-8'), bcrypt.gensalt())
        print(str(encrypted).split("\'")[1])
        element_serializer.initial_data['password'] = str(encrypted).split("\'")[1]
        element_serializer.initial_data['photo'] = 'user.png'
        element_serializer.initial_data['rating'] = 1
        if element_serializer.is_valid():
            element_serializer.save()
            data = {
                'code': 1,
                'message': 'success'
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            data = {
                'code': 2,
                'message': 'error'
            }
        return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    try:
        if request.method == 'POST':
            element = JSONParser().parse(request)
            element_serializer = UserSerializer(data=element)
            if True:
                elements = User.objects.all()
                elements = elements.filter(email__icontains=element_serializer.initial_data['email'])
                if len(elements) > 0:
                    given_password = element_serializer.initial_data['password']
                    password = elements[0].password
                    if bcrypt.checkpw(str(given_password).encode('utf-8'), str(password).encode('utf-8')):
                        token = jwt.encode({"email": element_serializer.initial_data['email']}, SECRET_KEY,
                                           algorithm="HS256")
                        data = {
                            'code': 1,
                            'role': elements[0].role,
                            'id': elements[0].id,
                            'token': token,
                            'message': 'success'
                        }
                        return JsonResponse(data, status=status.HTTP_200_OK)
                    else:
                        data = {
                            'code': 2,
                            'message': 'error'
                        }
                        return JsonResponse(data, status=status.HTTP_200_OK)
                else:
                    data = {
                        'code': 3,
                        'message': 'error'
                    }
                    return JsonResponse(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'code': 4,
                    'message': element_serializer.error_messages
                }
                return JsonResponse(data, status=status.HTTP_200_OK)
    except Exception as e:
        data = {
            'code': 4,
            'message': str(e)
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def handle_users(request):
    token = request.headers['Authorization']
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if decoded["email"] is None:
        data = {
            'code': 5,
            'message': 'unauthorized access'
        }
        return JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        elements = User.objects.all()
        email = request.GET.get('email', None)
        id = request.GET.get('id', None)
        role = request.GET.get('role', None)
        if email is not None:
            elements = elements.filter(email__icontains=email)
            elements_serializer = UserSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
        elif role is not None:
            elements = elements.filter(role__icontains=role)
            elements_serializer = UserSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
        elif id is not None:
            element = User.objects.get(id=id)
            element_serializer = UserSerializer(element)
            return JsonResponse(element_serializer.data, safe=False)
        else:
            elements_serializer = UserSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
    elif request.method == 'PUT':
        id = request.GET.get('id', None)
        if id is not None:
            model = User.objects.get(id=id)
            element_serializer = UserSerializer(model, request.data)
            photo = element_serializer.initial_data['photo']
            if photo != '':
                path = os.path.dirname(os.path.realpath(__file__)) + "/static/photos/"
                name = "photo" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
                with open(path + name, "wb") as fh:
                    fh.write(base64.decodebytes(str(photo).encode('utf-8')))
                element_serializer.initial_data['photo'] = name
            else:
                element_serializer.initial_data['photo'] = model.photo
            if element_serializer.is_valid():
                element_serializer.save()
                data = {
                    'code': 1,
                    'message': 'success'
                }
                return JsonResponse(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'code': 2,
                    'message': 'error'
                }
            return JsonResponse(data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user_id = request.GET.get('id', None)
        if user_id is not None:
            User.objects.filter(pk=user_id).delete()
            data = {
                'code': 1,
                'message': 'success'
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            data = {
                'code': 2,
                'message': 'error'
            }
            return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
def handle_requests(request):
    token = request.headers['Authorization']
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if decoded["email"] is None:
        data = {
            'code': 5,
            'message': 'unauthorized access'
        }
        return JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        elements = Request.objects.all()
        driver = request.GET.get('driver', None)
        if driver is not None:
            elements = elements.filter(driver__exact=driver)
            elements_serializer = RequestSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
        else:
            elements = elements.filter(status__exact='PENDING')
            elements_serializer = RequestSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
    elif request.method == 'POST':
        element = JSONParser().parse(request)
        element_serializer = RequestSerializer(data=element)
        identity = element_serializer.initial_data['identity']
        licence = element_serializer.initial_data['licence']
        path = os.path.dirname(os.path.realpath(__file__)) + "/static/identity/"
        name = "identity" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        element_serializer.initial_data['identity'] = name
        with open(path + name, "wb") as fh:
            fh.write(base64.decodebytes(str(identity).encode('utf-8')))
        path = os.path.dirname(os.path.realpath(__file__)) + "/static/licence/"
        name = "licence" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        with open(path + name, "wb") as fh:
            fh.write(base64.decodebytes(str(licence).encode('utf-8')))
        element_serializer.initial_data['licence'] = name
        element_serializer.initial_data['status'] = 'PENDING'
        if element_serializer.is_valid():
            element_serializer.save()
            data = {
                'code': 1,
                'message': 'success'
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            data = {
                'code': 2,
                'message': 'error'
            }
        return JsonResponse(data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        driver = request.GET.get('driver', None)
        if driver is not None:
            Request.objects.filter(driver__exact=driver).update(status='ACCEPTED')
            if True:
                data = {
                    'code': 1,
                    'message': 'success'
                }
                return JsonResponse(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'code': 2,
                    'message': 'error'
                }
            return JsonResponse(data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        driver_id = request.GET.get('driver', None)
        if driver_id is not None:
            Request.objects.filter(driver__exact=driver_id).delete()
            data = {
                'code': 1,
                'message': 'success'
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            data = {
                'code': 2,
                'message': 'error'
            }
            return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
def handle_rides(request):
    token = request.headers['Authorization']
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if decoded["email"] is None:
        data = {
            'code': 5,
            'message': 'unauthorized access'
        }
        return JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        elements = Ride.objects.all()
        client = request.GET.get('client', None)
        driver = request.GET.get('driver', None)
        if client is not None:
            elements = elements.filter(client__exact=client)
            elements_serializer = RideSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
        elif driver is not None:
            elements = elements.filter(driver__exact=driver, status__exact='PENDING')
            elements_serializer = RideSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
        else:
            elements_serializer = RideSerializer(elements, many=True)
            return JsonResponse(elements_serializer.data, safe=False)
    elif request.method == 'POST':
        element = JSONParser().parse(request)
        element_serializer = RideSerializer(data=element)
        element_serializer.initial_data['day'] = datetime.datetime.now().strftime("%d-%m-%Y")
        element_serializer.initial_data['time'] = datetime.datetime.now().strftime("%H:%M:%S")
        element_serializer.initial_data['status'] = 'PENDING'
        if element_serializer.is_valid():
            element_serializer.save()
            data = {
                'code': 1,
                'message': 'success'
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            data = {
                'code': 2,
                'message': 'error'
            }
        return JsonResponse(data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        id = request.GET.get('id', None)
        idd = request.GET.get('idd', None)
        if id is not None:
            element = JSONParser().parse(request)
            element_serializer = RideSerializer(data=element)
            rating = element_serializer.initial_data['rating']
            if rating is not None:
                Ride.objects.filter(id=id).update(rating=rating)
                driver_id = Ride.objects.filter(id=id).values('driver')[0].get('driver')
                average = Ride.objects.all().filter(driver__exact=driver_id).aggregate(Avg('rating')).get('rating__avg')
                average = float("{:.2f}".format(average))
                User.objects.filter(id=driver_id).update(rating=average)
            if True:
                data = {
                    'code': 1,
                    'message': 'success'
                }
                return JsonResponse(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'code': 2,
                    'message': 'error'
                }
                return JsonResponse(data, status=status.HTTP_200_OK)
        elif idd is not None:
            element = JSONParser().parse(request)
            element_serializer = RideSerializer(data=element)
            the_status = element_serializer.initial_data['status']
            if the_status is not None:
                Ride.objects.filter(id=idd).update(status=the_status)
            if True:
                data = {
                    'code': 1,
                    'message': 'success'
                }
                return JsonResponse(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'code': 2,
                    'message': 'error'
                }
                return JsonResponse(data, status=status.HTTP_200_OK)
