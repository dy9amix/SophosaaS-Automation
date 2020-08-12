import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def startVM(vmId,csrfToken,authCookie):
    url = f"https://192.168.4.82:8006/api2/json/nodes/saas/qemu/{vmId}/status/start"

    payload = {}
    headers = {
    'CSRFPreventionToken': f'{csrfToken}',
        'Cookie': f'PVEAuthCookie={authCookie}'
    }

    response = requests.request("POST", url, headers=headers, data = payload, verify=False)

    return response.text.encode('utf8')