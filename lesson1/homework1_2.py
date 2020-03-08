import requests
import json
from pprint import pprint

# client_id = '...'
# client_secret = '...'
#
# r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
#                   data={
#                       "client_id": client_id,
#                       "client_secret": client_secret
#                   })
#
# j = json.loads(r.text)
#
# token = j["token"]

token= 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6IiIsInN1YmplY3RfYXBwbGljYXRpb24iOiI1ZGY5MWYwZTAxMDU5MDAwMTIxMThiNzYiLCJleHAiOjE1ODQyODk4OTMsImlhdCI6MTU4MzY4NTA5MywiYXVkIjoiNWRmOTFmMGUwMTA1OTAwMDEyMTE4Yjc2IiwiaXNzIjoiR3Jhdml0eSIsImp0aSI6IjVlNjUxZGU1MGU2YjNhMDAwZDQ0MWZhYiJ9.5Y_U-JMUIxYShYHMKaxPCeau63aruL71uCdtE3TzDeE'

headers = {"X-Xapp-Token" : token}
artist_name = "banksy"
r = requests.get(f"https://api.artsy.net/api/artists/{artist_name}", headers=headers)

j = json.loads(r.text)

pprint(j)

with open(f'{artist_name}.json', 'w') as f:
    json.dump(j, f)