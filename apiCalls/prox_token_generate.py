import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def generateToken():
  url = "https://192.168.4.82:8006/api2/json/access/ticket?username=root@pam&password=!@%23Supp0rt1"
  payload = {}
  response = requests.request("POST", url, data = payload, verify=False)
  result = response.json()
  if result['data'] == None:
    raise Exception("Yeah Something went wrong somewhere")
  else:
    return result