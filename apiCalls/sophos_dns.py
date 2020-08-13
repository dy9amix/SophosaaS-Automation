import requests

url = """https://172.16.16.16:4444/webconsole/APIController?reqxml=
<Request>
<Login><Username>coollink</Username>
<Password passwordform = \"encrypt\">C7465CDBF6A489824DB58E0FC7567B3D</Password>
</Login>
<Set operation = \"update\">
    <DNS>
		<IPv4Settings>
			<ObtainDNSFrom>Static</ObtainDNSFrom>
			<DNSIPList><!--This tag should be used only when <ObtainDNSFrom>has value \"Static\"	-->
				<DNS1>41.78.211.30</DNS1>
				<DNS2>8.8.8.8</DNS2>
			</DNSIPList>
		</IPv4Settings>
        <DNSQueryConfiguration>ChooseServerBasedOnIncomingRequestsRecordType</DNSQueryConfiguration>
	</DNS>
</Set></Request>"""

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
