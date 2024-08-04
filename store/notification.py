import http.client
import json
import os
import google.auth.transport.requests

from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


def _get_access_token():
  
  service_account_info = {
    'type': 'service_account', 
    'project_id': os.environ.get('PROJECT_ID'), 
    'private_key_id': os.environ.get('PRIVATE_KEY_ID'), 
    'private_key':os.environ.get('PRIVATE_KEY'),
    'client_email':os.environ.get('CLIENT_EMAIL'),
    'client_id':os.environ.get('CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ypjlm%40ecommerce-31838.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"

  }
  credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  return credentials.token


conn = http.client.HTTPSConnection("fcm.googleapis.com")

def send_notification():

  headersList = {
  "Content-Type": "application/json; UTF-8",
  "Authorization": f"Bearer {_get_access_token()}" 
  }

  payload = json.dumps({
      "message": {
          "token": "eG2BbJX9RpqYOKCHZFLRvp:APA91bEhYwMWQKXzsOzDYGnBpCJhAxQxQPIRsRQtHNwJfVQRsv-uZQuz7SYudRnBVey4L_QLE-zPj9Sh33ajJkzOBHWFGaeVcyRBM3KlYlSmgz-vvrQU4ipCuXdA1ptCSos1sDho6v1Q",
          "notification": {
              "title": "Hello from FCM",
              "body": "This is a test message"
          },
          
          "data":{
            "id":"12",
            "name":"elias",
            "age":"23",
            "type":"chat"
          }
          
      }
  })

  conn.request("POST", F"/v1/projects/{os.environ.get('PROJECT_ID')}/messages:send", payload, headersList)
  response = conn.getresponse()
  result = response.read()
  print(result.decode("utf-8"))

