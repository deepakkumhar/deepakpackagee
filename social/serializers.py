from dataclasses import fields
from email.mime import image
from importlib.resources import path
from lib2to3.pgen2 import token
from pyexpat import model
from tokenize import Token
from pkg_resources import require
from rest_framework import serializers
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from .models import *
from rest_framework.validators import UniqueValidator
from rest_framework_recursive.fields import RecursiveField
# from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed



class userPostserializer(serializers.ModelSerializer):
    # User = serializers.CharField()
    caption = serializers.CharField()

    class Meta:
        model = userPost
        fields = ['caption']


class LoginSerializer(serializers.ModelSerializer):
    # userPost =  userPostserializer(read_only=True)
    # hi =  serializers.CharField(read_only=True)


    email = serializers.EmailField(max_length=255, min_length=7)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    first_name = serializers.CharField(max_length=255, min_length=3, read_only=True)
    last_name = serializers.CharField(max_length=255, min_length=3, read_only=True)
    id = serializers.CharField(read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username','email', 'password', 'id','tokens']


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        email=User.objects.filter(email=email)
        
        if not email:
            raise AuthenticationFailed('given email id not exist')

        if not user:
            raise AuthenticationFailed('incorrect password')

        if not user.is_verified:
            raise AuthenticationFailed('Account email has not yet been verified.')
        if not user.is_actives:
            raise AuthenticationFailed('Account disabled, please contact an administrator.')

        return {
            'email': user.email,
            'username': user.username,
            'id': user.id,
            'first_name' : user.first_name, 
            'last_name' : user.last_name, 
            'tokens': user.tokens

    
        }

        # return super().validate(attrs)

##################################################################################################################################################for comment all data
##################################################################################################################################################

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user


#for response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class UserDetailSerializer(serializers.Serializer):
    ResponseCode = serializers.IntegerField()
    ResponseMessage = serializers.CharField(max_length=255)
    ResponseData = UserSerializer()


##################################################################################################################################################
class userPostSerializers(serializers.Serializer): 
    # commentlike=userCommunicationSerializers(many=True,read_only=True)
    userImage=serializers.ImageField()
    caption=serializers.CharField(required=False)   
    user=serializers.CharField(required=False)
    PostId=serializers.CharField(required=False)
    likes=serializers.CharField(required=False)
    views=serializers.CharField(required=False)
    comment=serializers.CharField(required=False)
    # userImage=serializers.SerializerMethodField()
    # class Meta:
    #     fields=( 'userImage','caption', 'user','PostId','likes','views','comment','userImage_urls')
    # userImage_urls=serializers.SerializerMethodField('userImage_urls')
 
    # def get_userImage(self,image):
    #     request = self.context.get('request')
    #     print(self.image)
    #     photo_url = image.userImage.url
    #     print(photo_url)
    #     return request.build_absolute_uri(photo_url)
    # class Meta(serializers.Serializer):
    #     fields=( 'userImage','caption', 'user','PostId','likes','views','comment','userImage_urls')


##################################################################################################################################################
class userPostSerializerss(serializers.Serializer): 
    # user=serializers.IntegerField(required=False)
    Token=serializers.CharField(required=True)
    userImage=serializers.ImageField(required=False)
    caption=serializers.CharField(required=False)
    # class Meta:
    #     model = userPost
    #     fields = ('userImage','caption')
    # user=serializers.IntegerField(required=False)
    # userImage=serializers.ImageField(required=False)
    # caption=serializers.CharField(required=False)

    # def create(self, validated_data):
    #     image=validated_data["userImage"]
    #     caption=validated_data["caption"]
    #     user = User.objects.get(1)
    #     post = userPost.objects.create(
    #         user=user,
    #         userImage=image,
    #         caption=caption
    #     )
    #     post.save()

    #     return post




##################################################################################################################################################

class userCommunicationSerializer(serializers.Serializer):
    Token=serializers.CharField(required=True)
    # user=serializers.CharField(required=True)
    PostId=serializers.CharField(required=True)
    likes=serializers.BooleanField(required=False)
    comments=serializers.CharField(required=False)
    parents=serializers.CharField(required=False)
    # class Meta:
    #     model=postDetails
    #     fields=('user','PostId','likes','comments','parents')

##################################################################################################################################################



# class postDetailsSerializer(serializers.ModelSerializer):
#     email=getusernameserializer(read_only=True)
#     sub_comment=RecursiveField(many=True)
#     class Meta:
#         model=postDetails
#         fields=('id','user','PostId','comments','sub_comment','email')



class postDetailsSerializer(serializers.ModelSerializer):
    post= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=postDetails
        fields=('id','PostId','post','comments','sub_comment')
    def get_post(self, obj):
        data=[]
        data.append({
            "user":obj.PostId.id,
            "caption":str(obj.PostId.caption),
            "userImage":(obj.PostId.userImage.path)
        })
        return data
    def get_fields(self):
        fields = super(postDetailsSerializer, self).get_fields()
        fields['sub_comment'] = postDetailsSerializer(many=True, required=False)
        return fields

#token



