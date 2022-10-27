from django.urls import path
from .views import SignUp, Login, refreshSession, levelCleared, getLevelsCleared
from .claimprocessor import mintReward
from .views import home
from . import views

urlpatterns = [
    path('api/activate', views.activate),
    path('', home),
    path('api/signup', SignUp.as_view()),
    path('api/login', Login),
    path('api/refreshtoken', refreshSession),
    path('api/levelcleared', levelCleared),
    path('api/getlevelscleared', getLevelsCleared)
]
