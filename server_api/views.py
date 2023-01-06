import json
import random
import requests
import secrets
import time

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from .validators import PasswordValidator,LengthValidator

from . import claimprocessor
from .models import User, Auth, Session, Chips, Reset
from .serializers import UserSerializer


class SignUp(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        token = generate_token()
        user = serializer.save()
        # 6 hours
        timeout = time.time() + (60 * 60 * 6)
        auth = Auth(user=user, token=token, expiry=timeout)
        chips = Chips(user=user)
        if send(user.user_email, token) == 1:
            auth.save()
            chips.save()
        else:
            user.delete()
            raise ValidationError("Email not sent")

    def create(self, request, *args, **kwargs):
        json = {'status': 1, 'message': "Account Created, Please check your email for authorization code to activate "
                                        "your account!"}
        try:
            super().create(request, *args, **kwargs)
        except Exception as e:
            json['status'] = 0
            json['message'] = (e.__dict__['detail'][list(dict(e.__dict__['detail']).keys())[0]])[0].title()
        return JsonResponse(json)


@api_view(['POST'])
def Login(request):
    user_email = request.POST['user_email']
    password = request.POST['password']
    try:
        user = User.objects.get(user_email=user_email, password=password)
        if not user.is_active:
            try:
                auth = Auth.objects.get(user=user)
                if auth.expiry > time.time():
                    return JsonResponse(
                        {'status': -1, 'message': 'User not activated! Check email for existing Authorization '
                                                  'code.'})
                else:
                    token = generate_token()
                    send(user_email, token)
                    auth.token = token
                    # 6 hours
                    auth.expiry = time.time() + (60 * 60 * 6)
                    auth.save()
                    return JsonResponse(
                        {'status': -1, 'message': 'User not activated! Check email for Authorization code.'})
            except Exception as e:
                print(e)
        else:
            chips = Chips.objects.get(user=user)
            try:
                session = Session.objects.get(user=user)
                session.token = secrets.token_hex(16)
                session.expiry = time.time() + (60 * 10)
                session.save()
                return JsonResponse(
                    {'status': 1, 'message': 'Success', 'user_name': user.user_name, 'token': session.token,
                     "avatar": user.avatar,
                     'chips': chips.chips_count})
            except:
                session = Session(user=user, token=secrets.token_hex(16))
                session.save()
                return JsonResponse(
                    {'status': 1, 'message': 'Success', 'user_name': user.user_name, 'token': session.token,
                     "avatar": user.avatar,
                     'chips': chips.chips_count}
                )
    except Exception as e:
        return JsonResponse({'status': 0, 'message': 'Invalid Credentials!'})


@api_view(['POST'])
def activate(request):
    token = request.POST['token']
    try:
        auth = Auth.objects.get(token=token)
        expiry = auth.expiry
        if expiry < time.time():
            token = generate_token()
            send(auth.user.user_email, token)
            auth.token = token
            auth.expiry = time.time() + (3 * 60)
            auth.save()
            return JsonResponse({'status': -1, 'message': 'Token Timed out! Check email for new Authorization token!'})
    except:
        return JsonResponse({'status': 0, 'message': 'Invalid Token!'})
    user = auth.user
    user.is_active = True
    user.save()
    auth.delete()
    return JsonResponse({'status': 1, 'message': 'Account Activated!'})


# @api_view(["POST"])
# def resend(request):
#     email = request.POST['user_email']
#     try:
#         user = User.objects.get(user_email=email)
#         is_active = user.is_active
#         if is_active:
#             return JsonResponse({'status': 0, 'message': 'Account already Activated!'})
#         token = generate_token()
#         try:
#             auth = Auth.objects.get(user=user)
#             if auth.expiry < time.time():
#                 auth.delete()
#             else:
#                 return JsonResponse({'status': 0, 'message': "Authorization token is active!"})
#         except Exception as e:
#             print(e)
#         if send(email, token) == 1:
#             auth = Auth(user=user, token=token, expiry=time.time() + (60 * 3))
#             auth.save()
#             return JsonResponse({'status': 1, 'message': "Email sent, Verify your account!"})
#     except Exception as e:
#         print(e)
#         return JsonResponse({'status': 0, 'message': "User not found!"})


@api_view(['POST'])
def refreshSession(request):
    try:
        session = Session.objects.get(token=request.POST['token'])
        if session.expiry > time.time():
            return JsonResponse({'status': 0, 'message': "Token still active"})
        else:
            session.token = secrets.token_hex(16)
            session.expiry = time.time() + (10 * 60)
            session.save()
            return JsonResponse(
                {'status': 1, 'message': "Session Refreshed!", 'token': session.token, 'expiry': session.expiry})
    except Exception as e:
        return JsonResponse({'status': -1, 'message': "Invalid Session!"})


@api_view(['POST'])
def claimReward(request):
    token = request.POST['token']
    amount = request.POST['amount']
    try:
        session = Session.objects.get(token=token)
        if session.expiry <= time.time():
            return JsonResponse({'status': 0, 'message': "Token Expired!"})
        user = session.user
        try:
            result = claimprocessor.transferReward(user.wallet_address, amount)
        except Exception as e:
            print(e,'wow')
            if '(' in str(e):
                return JsonResponse({"status": 0, "message": str(e).split(',')[1].split(':')[1].split('\'')[1].split('(')[0]})
            else:
                return JsonResponse(
                    {"status": 0, "message": str(e)})
        if result == 1:
            return JsonResponse({"status": 1, "message": "Claim Rewarded!"})
        else:
            return JsonResponse({"status": 0, "message": "Could not process reward!"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": 0, "message": "Invalid Session Token!"})


@api_view(['POST'])
def updateAvatar(request):
    token = request.POST['token']
    avatar = request.POST['avatar_id']
    try:
        session = Session.objects.get(token=token)
        if session.expiry >= time.time():
            user = session.user
            user.avatar = avatar
            user.save()
            return JsonResponse({"status": 1, "message": 'Avatar Updated'})
        else:
            return JsonResponse({"status": 0, "message": 'Session Token Expired'})
    except:
        return JsonResponse({"status": 0, "message": 'Invalid Session'})


@api_view(['POST'])
def updateChips(request):
    token = request.POST['token']
    chips = request.POST['chips']
    try:
        session = Session.objects.get(token=token)
        if session.expiry >= time.time():
            user = session.user
            chipsObj = Chips.objects.get(user=user)
            chipsObj.chips_count = chips
            chipsObj.save()
            return JsonResponse({"status": 1, "message": 'Chips Updated'})
        else:
            return JsonResponse({"status": 0, "message": 'Session Token Expired'})
    except:
        return JsonResponse({"status": 0, "message": 'Invalid Session'})


@api_view(['POST'])
def getChips(request):
    token = request.POST['token']
    try:
        session = Session.objects.get(token=token)
        if session.expiry >= time.time():
            user = session.user
            chips = Chips.objects.get(user=user)
            return JsonResponse({"status": 1, "chips": chips.chips_count})
        else:
            return JsonResponse({"status": 0, "message": 'Session Token Expired'})
    except:
        return JsonResponse({"status": 0, "message": 'Invalid Session'})


@api_view(['POST'])
def getAvatar(request):
    token = request.POST['token']
    try:
        session = Session.objects.get(token=token)
        if session.expiry >= time.time():
            user = session.user
            return JsonResponse({"status": 1, "Avatar": user.avatar})
        else:
            return JsonResponse({"status": 0, "message": 'Session Token Expired'})
    except:
        return JsonResponse({"status": 0, "message": 'Invalid Session'})


@api_view(['GET'])
def getPrice(request, amount):
    if amount == 0:
        return JsonResponse({"status": 0, "message": 'Invalid Amount!'})
    else:
        req = requests.get('https://api.coingecko.com/api/v3/coins/minebase')
        amount = int(amount) * float(req.json()['tickers'][0]['last'])
    return JsonResponse({'status': 1, 'value': amount})


@api_view(["POST"])
def request_reset(request):
    email = request.POST['user_email']
    try:
        user = User.objects.get(user_email=email)
        token = generate_token()
        try:
            resetToken = Reset(user=user, token=token)
            resetToken.save()
        except Exception as e:
            return JsonResponse({'status': -1, 'message': "Reset token already sent!"})
        send(email, token, True)
        return JsonResponse({'status': 1, 'message': "Reset token sent on the email."})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 0, 'message': "Invalid Email!"})


@api_view(["POST"])
def reset_login(request):
    token = request.POST['token']
    try:
        reset_obj = Reset.objects.get(token=token)
        user = reset_obj.user
        # set reset
        user.reset_requested = True
        user.save()
        reset_obj.delete()
        chips = Chips.objects.get(user=user)
        # login
        try:
            session = Session(user=user, token=secrets.token_hex(16))
            session.expiry = time.time() + (60 * 10)
            session.save()
        except Exception as e:
            session = Session.objects.get(user=user)
        return JsonResponse(
            {'status': 1, 'message': 'Reset Login!', 'user_name': user.user_name, 'token': session.token,
             "avatar": user.avatar,
             'chips': chips.chips_count})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 0, 'message': "Invalid Reset Token!"})


@api_view(["POST"])
def reset_password(request):
    token = request.POST['token']
    password = request.POST['new_password']
    try:
        session = Session.objects.get(token=token)
        user = session.user
        if not user.reset_requested:
            return JsonResponse({'status': 0, 'message': "User did not request password reset!"})
        try:
            PasswordValidator(password)
            LengthValidator(password)
        except ValidationError as e:
            # print(e)
            return JsonResponse({'status': 0, 'message': e.message})
        user.reset_requested = False
        user.password = password
        user.save()
        return JsonResponse({'status': 1, 'message': "Password reset!"})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 0, 'message': "Invalid Session Token!"})

# @api_view(["POST"])
# def test(request):
#     passw = request.POST['password']
#     try:
#         LengthValidator(passw)
#
#     except Exception as e:
#         print(e)
#         return HttpResponse('Wow')
#     return HttpResponse('Not wow')

def send(email, token, reset=False):
    if reset:
        return send_mail("Minebase-Game Password Reset", str(token), "reset@minebase.com", recipient_list=[email])

    else:
        return send_mail("Minebase-Game Auth Token", str(token), "auth@minebase.com", recipient_list=[email])


def generate_token():
    return random.randint(pow(10, 5), pow(10, 6) - 1)


def home(request):
    return HttpResponse("Server!")
