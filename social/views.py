from email.mime import image
from multiprocessing.sharedctypes import Value
from urllib import response
from webbrowser import get
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from .serializers import *
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from .models import *
from .rendr import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import generics, status,mixins,authentication
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from backend.utils import jwt_response_payload_handler
from rest_framework_simplejwt.tokens import AccessToken


# Create your views here.


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = [UserRenderer]
    # parser_classes = (MultiPartParser,)
    # authentication_classes = (authentication.TokenAuthentication,)

    @extend_schema(
        responses={201: UserDetailSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

##################################################################################################################################################






class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer]
    parser_classes = (MultiPartParser,)

    @extend_schema(
        responses={201: UserDetailSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


##################################################################################################################################################




class userpost(generics.CreateAPIView):
    queryset = userPost.objects.all()
    serializer_class = userPostSerializerss
    parser_classes = (MultiPartParser,)
    # renderer_classes = [UserRenderer]

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    def post(self, request):
        #from me
        # tokens=self.kwargs['token']
        tokens=request.data['Token']
        try:
            access_token_obj = AccessToken(tokens)
        except:
            return error_404(request,status.HTTP_404_NOT_FOUND,"Token unvalid")
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        image=request.data["userImage"]
        caption=request.data["caption"]
        if caption!="" or image!="":
            userPost.objects.create(
                user=User.objects.get(id=user_id),
                userImage=image,
                caption=caption,

            )
            model={
                "user":user_id,
                "userImage":str(image),
                "caption":caption
            }
            # serializer = self.serializer_class(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            return Response({"responseCode":200,"responseMessage":"post created successfull","responseData":model})
        else:
            return error_400(request,status.HTTP_400_BAD_REQUEST,"you can only post both or any one")


##################################################################################################################################################      
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class postList(generics.GenericAPIView):
    serializer_class = userPostSerializers
    queryset = userPost.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]
    # permission_classes = (IsAuthenticated,)
    # pagination_class = StandardResultsSetPagination
    def get(self, request):
        queryset = userPost.objects.all()

        userPost_data=[]
        userPost_data_all = []
        for post in queryset:
            # print(post.user)
            # comments=postDetails.objects.filter(user=post.user.id,parents=None).all()
            comments=postDetails.objects.filter(PostId=post.id,parents=None)[0:2]
            like=postDetails.objects.filter(PostId=post.id,likes=1).count()
            # YourModel.objects.all().order_by(-id).first().id
            # m=postDetails.objects.all().order_by(-id).first().id
            views=postDetails.objects.filter(PostId=post.id).filter(id=post.id).all()
            for vi in views:
                view=vi.views
            # print(m)
            comment_data=[]
            for comment_value in comments:
                comment_data.append({
                    "comment":comment_value.comments,
                    # "userPost":comment_value.PostId.id
                })
            # image_post=("http://"+(request.get_host())+"/media/"+str(post.userImage))
            if post.userImage!="":
                image_post=("http://"+(request.get_host())+"/media/"+str(post.userImage))
            else:
                image_post=None
            # print(image_post)
            # value="http://localhost:8000/media/"+str(post.userImage)
            # print( post.userImage.url)
            # print(value)
            # print(post.userImage.path)s
            userPost_data.append({
                "user":(post.user.id),
                "PostId":post.id,
                "userImage":(image_post),
                "caption":post.caption,
                "likes":like,
                "views":view,   
                "comment":(comment_data)
            })
        return Response(userPost_data)


##################################################################################################################################################

class userCommentLike(generics.CreateAPIView):
    queryset = postDetails.objects.all()
    serializer_class = userCommunicationSerializer
    permission_classes = [AllowAny] 
    parser_classes = (MultiPartParser,)
    renderer_classes = [UserRenderer]
    # pagination_class = StandardResultsSetPagination

    def post(self, request):
        tokens=request.data['Token']
        try:
            access_token_obj = AccessToken(tokens)
        except:
            return error_404(request,status.HTTP_404_NOT_FOUND,"Token unvalid")
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        PostId=request.data['PostId']
        likes=request.data['likes']
        comments=request.data['comments']
        # if userPost.objects.filter(id=request.data['user']).exists()==False:
        #     return error_404(request,status.HTTP_404_NOT_FOUND,"sorry user not having any post")
        if userPost.objects.filter(id=request.data['PostId']).exists()==False:
            return error_404(request,status.HTTP_404_NOT_FOUND,"sorry post id not matching")
        if request.data['parents']!="":
            if userPost.objects.filter(id=request.data['parents']).exists()==False:
                return error_404(request,status.HTTP_404_NOT_FOUND,"sorry comment not exist")
        if request.data['likes'] ==True:
            like=1
        else:
            like=0
        if request.data['parents']=="":
            parents_value=None
        else:
            parents_value=postDetails.objects.get(id=request.data['parents'])
        if likes!="" or comments!="":
            postDetails.objects.create(
                user=User.objects.get(id=user_id),
                PostId=userPost.objects.get(id=request.data['PostId']),
                likes=like,
                parents=parents_value,
                comments=request.data['comments'],
            )
            model={
                "user":user_id,
                "PostId":request.data['PostId'],
                "likes":like,
                "parents":request.data['parents'],
                "comments":request.data['comments'],

            }
            # serializer = self.serializer_class(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            return Response(model)
        else:
            return error_400(request,status.HTTP_400_BAD_REQUEST,"comment and like both can not be null")

##################################################################################################################################################

#for recursion

class PostDetailAPIView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = postDetailsSerializer
    model = serializer_class.Meta.model
    def get(self, request, *args, **kwargs):
        PostId = self.kwargs['PostId']
        query_check = postDetails.objects.filter(PostId=self.kwargs['PostId']).exists()
        if query_check==False:
            return error_404(request,status.HTTP_404_NOT_FOUND,"sorry PostId not found")
        #     print(queryset)
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        PostId = self.kwargs['PostId']
        view=postDetails.objects.filter(PostId=PostId).values('views')[0].get('views')
        querysett = self.model.objects.filter(parents__isnull=True,PostId=PostId).all()
        # view=querysett.views
        postDetails.objects.filter(PostId=PostId).update(
                views=view+1
            )
        return querysett



class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)






#token




