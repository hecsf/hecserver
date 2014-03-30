# Download the Python helper library from twilio.com/docs/python/install
from surveygizmo import SurveyGizmo
import json

# authentication
sg = SurveyGizmo(api_version='v3', response_type='json')
sg.config.auth_method = "user:pass"
sg.config.username = "kgruneisen@ecs-sf.org"
sg.config.password = "HEC123"

# generate a URL with a unique sguid tied to the user


# get response for a dict
survey_id = "1599451"
response_json = sg.api.surveyresponse.list(survey_id)
response_dict = json.loads(response_json)
for user_response in response_dict["data"]:
    if "[url(\"sguid\")]" in user_response.keys():
        print user_response["[url(\"sguid\")]"]