from django.contrib import admin
from django.db import router
from .views import LoginAPIView,RegisterView,userpost,postList,userCommentLike,PostDetailAPIView,HelloView
from django.urls import path,include
from rest_framework.routers import SimpleRouter




# router=SimpleRouter()
# router.register('CustomerViewSet',CustomerViewSet)

# # urlpatterns=router.urls

# urlpatterns = [
#     path('', include(router.urls)),
# ]



# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    # path('', include(router.urls)),
    
    path('user-login/', LoginAPIView.as_view(), name="user-login"),
    path('user-register/', RegisterView.as_view(), name="user-register"),
    path('userpost/', userpost.as_view(), name="userpost"),
    path('postList/', postList.as_view(), name="postList"),
    path('userCommentLike/', userCommentLike.as_view(), name="userCommentLike"),
    path('postDetail/<PostId>', PostDetailAPIView.as_view(), name="PostDetail"),
    path('HelloView', HelloView.as_view(), name="HelloView"),
    
]
