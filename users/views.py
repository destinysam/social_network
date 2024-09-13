from django.shortcuts import render
from rest_framework import serializers
from .models import User
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .exceptions import InvalidCredentials
from django.utils.translation import gettext_lazy as _
from .service import get_login_token,get_token_from_refresh_token
# Create your views here.


class SignUpSerializer(serializers.ModelSerializer):
    """
        Serializer to onboard/signup a user
    """
    
    class Meta:
        model = User
        fields = ("username","email","password",)


  
    

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        user = User.objects.create_user(**validated_data)
        return user
    








class SignUpAPI(CreateAPIView):
    """
        API to onboard/signup a user
    """
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


    def post(self,request):
        serializer = self.get_serializer(data=request.data)   
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message":"Signup completed!"},status=status.HTTP_201_CREATED)
    



class SignInSerializer(serializers.Serializer):
    """
        Serializer to signin a user using email and password
    """
    email = serializers.EmailField(required=True,max_length=100)
    password = serializers.CharField(required=True,max_length=100)


    def validate_email(self,value):
        return value.lower()




class SignInAPI(GenericAPIView):
    """
        API to to signin a user using email and password
    """
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]


    def post(self,request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        user = authenticate(**{"username":data["email"],"password":data["password"]})
        
        if not user:
            raise InvalidCredentials(_("Invalid email or password"))
        
        data = get_login_token(request,user)
        return Response(data=data,status=status.HTTP_200_OK)
        



class RefreshTokenSerializer(serializers.Serializer):
    """
        Serializer to refresh token from refresh token
    """
    refresh_token = serializers.CharField()     




class RefreshTokenAPI(GenericAPIView):
    """
        API to refresh token from refresh token
    """
    serializer_class = RefreshTokenSerializer
    

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        token_data = get_token_from_refresh_token(data["refresh_token"])
        return Response(data=token_data,status=status.HTTP_200_OK)