import http.client
import json
import os
import google.auth.transport.requests

from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

conn = http.client.HTTPSConnection("fcm.googleapis.com")


def _get_access_token():
  
  service_account_info = {
  "type": "service_account",
  "project_id": os.environ.get('PROJECT_ID'),
  "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
  "private_key": os.environ.get('PRIVATE_KEY'),
  "client_email": os.environ.get('CLIENT_EMAIL'),
  "client_id": os.environ.get('CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ypjlm%40ecommerce-31838.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
} 
  


  print('1')
  try :
      credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
  except Exception as error:
    print("An error occurred:", error)
  print('2')
  request = google.auth.transport.requests.Request()
  print('3')
  credentials.refresh(request)
  print('4')
  return credentials.token



def send_notification(title, message, topic, pageid, pagename):

 
  headersList = {
  "Content-Type": "application/json; UTF-8",
  "Authorization": f"Bearer {_get_access_token()}" 
  }
  print('5')


  payload = json.dumps({
  "message": {
    "topic": topic,
    "notification": {
      "title": title,
      "body": message,
    },
    "data": {
      "pageid": pageid,
      'pagename':pagename
    }}})

  print('6')

  conn.request("POST", f"/v1/projects/{os.environ.get('PROJECT_ID')}/messages:send", payload, headersList)
  print('7')
  response = conn.getresponse()
  print('8')
  result = response.read()
  print('9')
  print(result.decode("utf-8"))

