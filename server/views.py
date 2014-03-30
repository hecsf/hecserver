from datetime import datetime
from urllib import quote
import json
import uuid

from django.conf import settings

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from surveygizmo import SurveyGizmo
from twilio.rest import TwilioRestClient
import tinyurl

from server.models import User
from server.models import Survey
from server.models import Employer

def sms_send(body, to):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(body=body, to=to,
                                     from_=settings.TWILIO_PHONE_NUMBER)
    return message
    

def build_body_for(user):
    unique_id = str(uuid.uuid4())
    now = timezone.now()
    
    survey = Survey(user=user, date_sent=now, external_id=unique_id)
    survey.save()
    
    url = tinyurl.create_one("http://www.surveygizmo.com/s3/%s/HEC-Alumni-Form?sguid=%s&employer=%s&role=%s&program=%s" % (
        settings.SURVEY_GIZMO_SURVEY_ID, unique_id,
        quote(user.last_employer.name if user.last_employer is not None else ""),
        quote(user.last_role),
        quote(user.last_program.name),
        ))
    return "Please complete this survey: %s" % url


def index(request):
    return render(request, 'server/index.html', {})


def send_sms(request):
    result = []
    users = User.objects.all()
    for user in users:
        message = sms_send(build_body_for(user), "+1%s" % user.phone_number)
        result.append({
            'user' : user,
            'external_id' : message,
        })
    return render(request, 'server/send_sms.html', {'surveys': result})


def periodic_check(request):
    now = timezone.now()
    result = []
    users = User.objects.all()
    for user in users:
        if (user.last_contact is None or 
            (user.last_reply is None and (now - user.last_contact).days > 7) or
            (user.last_reply is not None and (now - user.last_reply).days > 30)
        ):
            body = build_body_for(user)
            message = sms_send(body, "+1%s" % user.phone_number)
            user.last_contact = now
            user.save()
            result.append({
                'user' : user,
                'external_id' : message,
            })
    return render(request, 'server/send_sms.html', {'surveys': result})


def periodic_get_surveys(request):
    sg = SurveyGizmo(api_version='v3')
    sg.config.auth_method = "user:pass"
    sg.config.username = settings.SURVEY_GIZMO_USERNAME
    sg.config.password = settings.SURVEY_GIZMO_PASSWORD
    
    result = ""
    page = 1
    pages = 1
    while page <= pages:
        result += "getting page %d\n" % page
        response_dict = sg.api.surveyresponse.list(settings.SURVEY_GIZMO_SURVEY_ID, page=page)
        try:
            pages = int(response_dict['total_pages'])
        except:
            result += json.dumps(response_dict)
        page += 1
        for user_response in response_dict["data"]:
            if "[url(\"sguid\")]" in user_response.keys():
                unique_id = user_response["[url(\"sguid\")]"]
                result += "Found id %s\n" % unique_id
                try:
                    survey = Survey.objects.get(external_id = unique_id)
                    if survey.date_replied is None:
                        survey.date_replied = timezone.now()
                        survey.reply = json.dumps(user_response)
                        survey.user.last_reply = timezone.now()
                        try:
                            role = user_response['[question(36)]']
                            company = user_response['[question(35)]']
                            same_company = user_response['[question(12)]'] == "Yes"
                            same_title = user_response['[question(13)]'] == "Yes"
                            employed_somewhere_else = user_response['[question(37)]'] == "Yes"

                            if role:
                                survey.user.last_role = role
                            if not same_company:
                                if employed_somewhere_else:
                                    try:
                                        employer = Employer.objects.get(name=company)
                                    except ObjectDoesNotExist:
                                        employer = Employer(name=company)
                                        employer.save()
                                    survey.user.last_employer = employer
                                else:
                                    survey.user.last_employer = None
                                    survey.user.last_role = None
                            survey.save()
                            survey.user.save()
                        except Exception as e:
                            result += "Exception: %s %s\n" % (e, user_response)
                            pass

                        result += "Found survey and saved\n"
                    else:
                        result += "Already had survey\n"
                    
                except ObjectDoesNotExist:
                    result += "Could not find survey\n"

    return render(request, 'server/simple.html', {'result': result})
