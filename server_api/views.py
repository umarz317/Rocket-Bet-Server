from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework.decorators import api_view

from server_api import bet_processor


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


@api_view(['POST'])
def processBet(request):
    receiver = request.POST['receiver']
    amount = (request.POST['amount'])
    tx_hash = request.POST['tx_hash']
    return JsonResponse(bet_processor.processBet(receiver, amount, tx_hash))
