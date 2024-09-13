from django.shortcuts import render
from rest_framework import serializers
from users.models import User
from rest_framework.generics import CreateAPIView,ListAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import FriendRequests
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

# Create your views here.


class BaseUserSerializer(serializers.ModelSerializer):
    """
        Serializer to show user details
    """
    class Meta:
        model = User
        fields = ("id","username",)

   

class ListUserAPI(ListAPIView):
    """
        API to list users based on search keyword
    """
    class ListUserQueryParamSerializer(serializers.Serializer):
        """
            Input serializer to list the users based on search
        """
        search = serializers.CharField(required=True,max_length=100)
        


    
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        serializer = self.ListUserQueryParamSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        query_params = dict(serializer.validated_data)
        qs = self.queryset.filter(email=query_params["search"])
        if not qs:
            qs = self.queryset.filter(username__contains=query_params["search"])

        return qs



class SendFriendRequestSerializer(serializers.ModelSerializer):
    """
        Serializer to send friend requests to users
    """
    class Meta:
        model = FriendRequests
        fields = ("request_sent_to",)







class SendFriendRequestAPI(CreateAPIView):
    """
        API to send friend requests to users(only 3 request/minute)
    """
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated,]




   
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User,id=request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        friend_request = FriendRequests.objects.get_or_create(
            request_sent_to= data["request_sent_to"],request_sent_by=user
            
        )
        return Response(data={"detail":"Request sent successfully!"},status=status.HTTP_200_OK)
    

  
      
        


class UpdateFriendRequestSerializer(serializers.ModelSerializer):
    """
        Serializer to update friend request status(accepted/rejected)
    """
    class Meta:
        model = FriendRequests
        fields = ("status",)

    



class UpdateFriendRequestAPI(CreateAPIView):
    """
        API to update friend request status(accepted/rejected)
    """

    serializer_class = UpdateFriendRequestSerializer
    permission_classes = [IsAuthenticated,]

    lookup_url_kwarg = "friend_request_id"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        f_request = get_object_or_404(FriendRequests,id=self.kwargs["friend_request_id"])
        f_request.status = data["status"]
        f_request.save()
        return Response(data={"detail":"Request updated successfully"},status=status.HTTP_200_OK)


class FriendRequestStatusSerializer(serializers.ModelSerializer):
    """
        Serializer to get pending and recieved friend requests
    """
    request_sent_to = BaseUserSerializer()
    class Meta:
        model = FriendRequests
        fields = ("request_sent_to",)





class AcceptedFriendRequestAPI(GenericAPIView):
    """
        API to get user accepted friend requests
    """
    serializer_class = FriendRequestStatusSerializer
    permission_classes = [IsAuthenticated,]


    def get(self,request,*args,**kwargs):
        user = get_object_or_404(User,id=request.user.id)
        f_requests = FriendRequests.objects.filter(request_sent_by=user,status="accepted")
        serializer = FriendRequestStatusSerializer(f_requests,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    



class PendingFriendRequestAPI(GenericAPIView):
    """
        API to get user recieved friend requests which are pending
    """
    serializer_class = FriendRequestStatusSerializer
    permission_classes = [IsAuthenticated,] 

    def get(self,request,*args,**kwargs):
        user = get_object_or_404(User,id=request.user.id)
        f_requests = FriendRequests.objects.filter(request_sent_to=user,status="pending")
        serializer = FriendRequestStatusSerializer(f_requests,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)