import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def createVM(vmId, client_name, csrfToken, authCookie):
  url = f"https://192.168.4.82:8006/api2/json/nodes/saas/qemu/103/clone?newid={vmId}&name={client_name}&storage=local-zfs&full=1"

  payload  = {}
  headers = {
    'CSRFPreventionToken': f'{csrfToken}',
    'Cookie': f'PVEAuthCookie={authCookie}'
  }
  response = requests.request("POST", url,
                               headers=headers, data = payload,
                                verify=False)
  return response.text.encode('utf8')
