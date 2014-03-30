# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC82d60753961205b203960366b473fdab"
auth_token  = "c9936326a39d39213509a0b54efcdaca"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body="www.google.com/",
                                 to="+16263536082",
                                 from_="+14157809109")
print message.sid
