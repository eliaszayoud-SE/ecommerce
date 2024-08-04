import http.client
import json

import google.auth.transport.requests

from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  credentials = service_account.Credentials.from_service_account_file(
    'E:\service-account.json', scopes=SCOPES)
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

  conn.request("POST", "/v1/projects/flutter-course-4a0be/messages:send", payload, headersList)
  response = conn.getresponse()
  result = response.read()
  print(result.decode("utf-8"))

send_notification()