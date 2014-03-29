from django.shortcuts import render
from django.http import HttpResponse
from twilio.rest import TwilioRestClient

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def send_sms(request):
    account_sid = "AC82d60753961205b203960366b473fdab"
    auth_token  = "c9936326a39d39213509a0b54efcdaca"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="www.google.com/",
                                 to="+16263536082",
                                 from_="+14157809109")
    return HttpResponse(""+message.sid)
