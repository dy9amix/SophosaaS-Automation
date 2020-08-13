import requests

url = """https://172.16.16.16:4444/webconsole/APIController?reqxml=
<Request>
    <Login>
        <Username>coollink</Username>
        <Password passwordform = \"encrypt\">C7465CDBF6A489824DB58E0FC7567B3D</Password>
    </Login>
    <Set operation = \"update\">
    <Interface>	
        <Name>Port3</Name>
        <Hardware>Port3</Hardware>
        <NetworkZone>None</NetworkZone>
        <MTU>1500</MTU>
        <MSS>
            <OverrideMSS>Disable</OverrideMSS>
            <MSSValue>1455</MSSValue>
        </MSS>  
    </Interface>
    </Set>
</Request>"""

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
