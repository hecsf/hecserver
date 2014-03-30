# Download the Python helper library from twilio.com/docs/python/install
from surveygizmo import SurveyGizmo
import json

sg = SurveyGizmo(api_version='v3', response_type='json')
sg.config.auth_method = "user:pass"
sg.config.username = "kgruneisen@ecs-sf.org"
sg.config.password = "HEC123"

response_json = sg.api.surveyresponse.list('1599451')
response_dict = json.loads(response_json)
for user_response in response_dict["data"]:
    print user_response