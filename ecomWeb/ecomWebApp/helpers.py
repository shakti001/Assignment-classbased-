from django.core.mail import send_mail
# import requests
import datetime
from .models import *
import math
import random
# from twilio.rest import Client

# def sendMail(subject, message, recipient):
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email="carenet761@gmail.com",
#         recipient_list=recipient,
#     )
#     return None


# def sendsms(to, text):
#     url = "http://api.messaging-service.com/sms/1/text/single"
#     # send_sms(to, text)
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": "Basic Y2FyZW5ldC50ZXh0Z2xvYmFsOjVoeTRtRDBuMyE=",
#     }

#     payload = {"from": "carenet", "to": to, "text": text}

#     # response = requests.post(url, data=payload, headers=headers)
#     response = requests.post(url=url, json=payload, headers=headers)
#     print(response.text, "=======")
#     # {"from": "447912123799", "to": to, "text": text}
#     # Username = "carenet.textglobal"
#     # Password = "5hy4mD0n3!"
#     # userpass = Username + ":" + Password
#     # encoded_u = base64.b64encode(userpass.encode()).decode()
#     # # headers = {"Authorization" : "Basic %s" % encoded_u}
#     # print(encoded_u, "ffffffffffffffffffffffffffffffffffffffff")
#     # headers = {
#     #     "Accept": "application/json",
#     #     "Content-Type": "application/json",
#     #     "Authorization": "Basic %s" % encoded_u,
#     # }
#     # response = requests.post(url, headers=headers)

#     # print(response.text, "ggggggggggggggggggggggggggggggggggg")


# # def set_pending():
# #     now = datetime.today()
# #     obj = (
# #         Shift_Post.objects.exclude(accepted=True)
# #         .exclude(pending=True)
# #         .exclude(completed=True)
# #         .exclude(status=False)
# #     )
# #     obj1 = obj.filter(in_time__lte=now)
# #     for i in obj1:
# #         i.pending = True
# #         i.save()
# # def test(request):
# SMS_BACKEND = "sms.backends.twilio.SmsBackend"
# TWILIO_ACCOUNT_SID = "AC409eaecfc3666c04e7ed4d31c9e477e0"
# TWILIO_AUTH_TOKEN = "b4a73ede09e853ca80b8eb9482e35e6c"
# TWILIO_NUMBER = "+12766249807"

# # from_no = settings.TWILIO_NUMBER
# # sms_sid = settings.TWILIO_ACCOUNT_SID
# # sms_token = settings.TWILIO_AUTH_TOKEN



# # def sendSMS(user, contact):
# #     to_contact = contact
# #     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
# #     otp = random.randint(1000, 9999)
# #     user.OTP = otp
# #     user.save()
# #     message = client.messages.create(
# #         body=f"Hi, your test result is {otp} Great job",
# #         from_=TWILIO_NUMBER,
# #         to="+918305697945",
# #     )
# #     if message:
# #         print("yesss doneee")
# #     else:
# #         print("bghhh bsdddkkkk")
        




def generatePassword():
    # Declare a digits variable
    # which stored all digits
    digits = "Abcdefgh@#()1234567890"
    Password = ""
    # length of password can be changed
    # by changing value in range
    for i in range(8):
        Password += digits[math.floor(random.random() * 10)]
    return Password

def generateOTP():
    # Declare a digits variable
    # which stored all digits
    digits = "1234567890"
    Otp = ""
    # length of password can be changed
    # by changing value in range
    for i in range(4):
        Otp += digits[math.floor(random.random() * 10)]
    return Otp