import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def deleteVM(token, ticket, vmID):
  url = f"https://192.168.4.82:8006/api2/json/nodes/saas/qemu/{vmID}"

  payload = {}
  headers = {
    'CSRFPreventionToken': f'{token}',
    'Cookie': f'{ticket}'
  }

  response = requests.request("DELETE", url, headers=headers, data = payload, verify=False)

  print(response.text.encode('utf8'))
