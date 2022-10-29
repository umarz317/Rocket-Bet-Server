from django.urls import path
from .views import SignUp, Login, refreshSession, updateAvatar,updateChips,getChips,getAvatar,getPrice,claimReward
from .views import home
from . import views

urlpatterns = [
    path('api/activate', views.activate),
    path('', home),
    path('api/signup', SignUp.as_view()),
    path('api/login', Login),
    path('api/refreshtoken', refreshSession),
    path('api/claimreward', claimReward),
    path('api/updateavatar', updateAvatar),
    path('api/updatechips',updateChips),
    path('api/getchips', getChips),
    path('api/getavatar', getAvatar),
    path('api/getprice/<int:amount>', getPrice),
]
