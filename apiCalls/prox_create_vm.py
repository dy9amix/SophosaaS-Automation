import requests

def createVM(vmId, client_name, csrfToken, authCookie):
  url = f"https://192.168.4.82:8006/api2/json/nodes/saas/qemu/103/clone?newid={vmId}&name={client_name}&storage=local-lvm&full=1"

  payload  = {}
  headers = {
    'CSRFPreventionToken': f'{csrfToken}',
    'Cookie': f'{authCookie}'
  }
  response = requests.request("POST", url,
                               headers=headers, data = payload,
                                verify=False)
  print(response.text.encode('utf8'))
