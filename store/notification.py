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
  "private_key": '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzLHHeieunb0qB\nyvlepBUj+L++bo9r4UgGjdgKsjWhEEgEWMmKKVX007sNb9tOIo2eYwv608N/yapC\n/OrjskEtvF23CtnH+3TZetPWieeTDC2ooIKmegxwRg/qkcXuJol+xt3E4BGlQQA0\n8e2XZTil8FyTkNvA1gQEl1L42IdVPyLUQxOcx1iHOQS3TSdGfadkR1nkg5D8GudA\nm22jQPfpQMETKz5+mXArUcuJWRaxf7rqD+CXh4e+WujtEPoafeg+6+9yimGaIKqA\nF072ckS0EweSipV6iLt76imR4OCdFmb0XtHwVo6zVT82Jics0PNaQbyEr4Y4ulkS\nUMjNAA8LAgMBAAECggEAVsHXE0gaNNVVMPrM+9AcsnHQuo+DX9vSSeYl7avz/tzI\n2l35nK4+QlHBmZSHjtJ5W2+fTeF7IOXPzSb1P7LBD7nNcQPOhyCRqHrql0/oM1Iq\ny6OJD746RqUOMOlL+3BqlFoL6TgMI0YRqRFaF7w6DVORKBz0429du7FgSkFialpa\nP9HB3lllPvssitXpRGtzeyoIumEMcu+BOtCsfhVSsCaVMjWYFtw7N6fdNMAiUc48\n35uvNR2yZVfgRqqVGWRLQSsZA9yLLVeKV0KQY90QxmC5zz+/eZxx5PZ0/H+3nmRn\nMwRmXGjtIlHbrM7vxDcsty9648s7J5VcaiGCs+L/TQKBgQD0CyNiZcJdGtIRLkuW\nPNBOzvxg0Bm3VxV+zXPmz5NPy+Z4rIMm+9e8hP+k520IiEvGJMDBhm1anB1XjemV\ngl2rSWc/gXNjOS+6fEk1Lfi12CNmzsLJS0u0gicF5jF65Xm2lU4aG3S95hRQ8xp3\nsWtgwLKEte+2dT6U89oQfah+FwKBgQC787Cz0NOGhdrR8X8n2Nxf3e3+2TXQbpij\nBvAcVoR4tkvV8goBP+7+jOWB2OSnMig1eIZvfHP66DoolCDQ6JOofrO0k6GKB9dl\nN26KJ9E09oFcM7RAxtJJR9NYwto6plHjp7OROkOdHxRDQ7TNIbjwgtUl1Otwd6r9\nzKewabljLQKBgE3g6A/UjWwMzRCyh2iQS6F6qEt03WAGqFNo2R3FDCug1BGaa9ga\n8kO05agIOmFIrXWz8NdRQMBzpWF1Zh9SFPY+XHaFpv75FuQaGXqhCwdszA9Y2AxI\nvQYDqtRVG2EureK4Ts5CCMU5ES6sBbxAoBWmKNH1BWRikfASyXoNv6FNAoGBAJei\n0eshDac4kwRSfC4fzhwiJwM3Jy2ULN1KmamjO5lQKfrgHaZIeH8yGXAbFs61rq8F\nICEOHVxOw609ZQRmv8pu/nkvqmJ8VRE6GZqo6SZ7wn4q0MB6J+orYp34BqzOxr6O\n7Fa81RQMoQJru5DMJjMUuvacw56nTXMaDChOA925AoGAYCKA0cgxPNAojxYIW9sk\nxU4rHawVp1sOSvWlnN3OwI/GvuGqHzii0YCNtVWZybaYY89al3T0pkTYbXOKDy2d\necTFhdj1K3bHxQ5z+x60VBytZ27M1KJlmUNKC64dtdKu1YR7eLp8xZYyhGe7JWRD\nqL0M9CCYKW4CEx9B+EEuz9Y=\n-----END PRIVATE KEY-----\n',
  "client_email": os.environ.get('CLIENT_EMAIL'),
  "client_id": os.environ.get('CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ypjlm%40ecommerce-31838.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


  credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
  
  
  request = google.auth.transport.requests.Request()
  
  credentials.refresh(request)
  
 

  return credentials.token



def send_notification(title, message, topic, pageid, pagename):


  headersList = {
  "Content-Type": "application/json; UTF-8",
  "Authorization": f"Bearer {_get_access_token()}" 
  }


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

  conn.request("POST", f"/v1/projects/{os.environ.get('PROJECT_ID')}/messages:send", payload, headersList)
  response = conn.getresponse()
  result = response.read()
  print(result.decode("utf-8"))

