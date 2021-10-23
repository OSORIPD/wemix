import simplejson as json
import time
import requests
import base64
import hashlib
import hmac



ACCESS_TOKEN = "4b72dfc3-11ec-4855-92d0-b870caeb74d7"
SECRET_KEY = "17ecd160-738a-4495-abc3-7b35420bc846"
API_NAME = "trader_v1"




def post_param(url, param):
  '''signature를 반환함'''

  # to json
  json_param = json.dumps(param)
  print(json_param)

  # X-COINONE-PAYLOAD
  payload = base64.b64encode(json_param.encode())

  # X-COINONE-SIGNATURE
  signature = hmac.new(str(SECRET_KEY).upper().encode(), str(payload).encode(), hashlib.sha512).hexdigest()

  headers = {
    'Content-type': 'application/json',
    'X-COINONE-PAYLOAD': payload,
    'X-COINONE-SIGNATURE': signature
  }

  res = requests.post(url=url, data=payload, headers=headers)
  print(res.status_code)

  return res



# def get_access_token():

#   url = "https://api.coinone.co.kr/oauth/access_token/"

#   param = {
#     'request_token': ACCESS_TOKEN,
#     'app_id': API_NAME,
#     'app_secret': SECRET_KEY,
#     'nonce' :  int(time.time()*1000)
#   }

#   response = post_param(url, param)
#   print(response.json())



def get_balance():

  url = "https://api.coinone.co.kr/v2/account/balance/"

  param = {
    'access_token':ACCESS_TOKEN,
    'nonce' :  int(time.time()*1000)
    }


  response = post_param(url, param)
  print(response.json())



if __name__ == '__main__':
  get_balance()
  




    