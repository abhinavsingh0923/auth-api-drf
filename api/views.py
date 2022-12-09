from rest_framework.decorators import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import jwt ,datetime

# Create your views here.


class RegisterUser(APIView):
    def post(self,request):
        serializer=Userserializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status':403,'error':serializer.errors,'message':'some thing wents wrong'})

        serializer.save()
        user =User.objects.get(username=serializer.data['username'])
        token_obj = Token.objects.get_or_create(user=user)

        return Response({'status':200, 'playload':serializer.data, 'token':str(token_obj),'message':'your data is save'})

class LoginUser(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']

        user=User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('no user found')
        if user.check_password(password):
            raise AuthenticationFailed('incorrect password')


        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,"secret",algorithm='HS256')#.decode('utf-8')
        response= Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={'jwt':token}

        return response      


class Userview(APIView):
    def get (self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('no token found')
        try:
            payload=jwt.decode(token,"secret",algorithms=['HS256'])    
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token expired')

        user=User.objects.filter(id=payload['id']).first()
        serializer=Userserializer(user)    
        return Response(serializer.data)        



class LogoutUser(APIView):
    def post(self , request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':"successfully logout"
        }        
        return response