import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def listSubscribers(csrf_token, auth_ticket):
    url = "https://192.168.4.82:8006/api2/json/nodes/saas/qemu"

    payload = {}
    headers = {
    'CSRFPreventionToken': f'{csrf_token}',
    'Cookie': f'PVEAuthCookie={auth_ticket}'
    }

    response = requests.request("GET", url, headers=headers, data = payload, verify=False)
    result = response.json()
    return result

