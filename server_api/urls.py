from django.urls import path
from .views import home, claimReward

urlpatterns = [
    # path('api/activate', views.activate),
    path('', home),
    # path('api/signup', SignUp.as_view()),
    # path('api/login', Login),
    # path('api/refreshtoken', refreshSession),
    # path('api/claimreward', claimReward),
    # path('api/updateavatar', updateAvatar),
    # path('api/updatechips',updateChips),
    # path('api/getchips', getChips),
    # path('api/getavatar', getAvatar),
    # path('api/getprice/<int:amount>', getPrice),
    # path('api/requestreset',request_reset),
    # path('api/initiatereset', reset_login),
    # path('api/resetpassword', reset_password),
    # path('api/test', test),
    path('api/signaturetest',claimReward)

]
