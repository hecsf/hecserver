from django.shortcuts import render
from django.http import HttpResponse
from twilio.rest import TwilioRestClient

from server.models import User

# Create your views here.
def index(request):
    return render(request, 'server/index.html', {})

def send_sms(request):
    account_sid = "AC82d60753961205b203960366b473fdab"
    auth_token  = "c9936326a39d39213509a0b54efcdaca"
    client = TwilioRestClient(account_sid, auth_token)

    result = []
    users = User.objects.all()
    for user in users:
        message = client.messages.create(body="www.google.com/",
                                         to="+1%s" % user.phone_number,
                                         from_="14157809109")
        result.append({
            'user' : user,
            'external_id' : message,
    })
    return render(request, 'server/send_sms.html', {'surveys': result})
