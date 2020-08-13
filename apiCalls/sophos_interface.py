import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def configureInterface(lanIP, lanSubnet, wanIP, wanSubnet, wanGateway):
    url = f"""https://172.16.16.16:4444/webconsole/APIController?reqxml=
    <Request>
        <Login>
            <Username>coollink</Username>
            <Password passwordform = \"encrypt\">C7465CDBF6A489824DB58E0FC7567B3D</Password>
        </Login>
        <Set operation = \"update\">
            <Interface>
                <Name>Port2</Name>
                <Hardware>Port2</Hardware>
                <NetworkZone>LAN</NetworkZone>
                <!-- IPv4Configuration -->
                <IPv4Configuration>Enable</IPv4Configuration>
                <IPv4Assignment>Static</IPv4Assignment>
                <!--  For Static -->
                <IPAddress>{lanIP}</IPAddress>
                <Netmask>{lanSubnet}</Netmask>
                <MTU>1500</MTU>
                <MSS>
                    <OverrideMSS>Disable</OverrideMSS>
                    <MSSValue>1455</MSSValue>
                </MSS>
            </Interface>
            <Interface>	
                <Name>Port3</Name>
                <Hardware>Port3</Hardware>
                <NetworkZone>WAN</NetworkZone>
                <!-- IPv4Configuration -->
                <IPv4Configuration>Enable</IPv4Configuration>
                <IPv4Assignment>Static</IPv4Assignment>
                <!--  For Static -->
                <IPAddress>{wanIP}</IPAddress>
                <Netmask>{wanSubnet}</Netmask>
                <GatewayName>SaaSGW</GatewayName>
                <GatewayIP>{wanGateway}</GatewayIP>
                <MTU>1500</MTU>
                <MSS>
                    <OverrideMSS>Disable</OverrideMSS>
                    <MSSValue>1455</MSSValue>
                </MSS>  
            </Interface>
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

    response = requests.request("GET", url, headers=headers, data = payload, verify=False)

    return response.text.encode('utf8')

def configureInterfacempls(lanIP, lanSubnet, wanIP, wanSubnet, wanGateway,vlanID):
    url = f"""https://172.16.16.16:4444/webconsole/APIController?reqxml=
    <Request>
        <Login>
            <Username>coollink</Username>
            <Password passwordform = \"encrypt\">C7465CDBF6A489824DB58E0FC7567B3D</Password>
        </Login>
        <Set operation = \"update\">
            <VLAN>
                <Name>MPLS</Name>
                <Hardware>Port2.{vlanID}</Hardware>
                <Interface>Port2</Interface>
                <Zone>LAN</Zone>
                <VLANID>{vlanID}</VLANID>
                <IPv4Configuration>Enable</IPv4Configuration><!-- default on -->
                <IPv4Assignment>Static</IPv4Assignment>
                <IPAddress>{lanIP}</IPAddress>
                <Netmask>{lanSubnet}</Netmask>
            </VLAN>
            <Interface>	
                <Name>Port3</Name>
                <Hardware>Port3</Hardware>
                <NetworkZone>WAN</NetworkZone>
                <!-- IPv4Configuration -->
                <IPv4Configuration>Enable</IPv4Configuration>
                <IPv4Assignment>Static</IPv4Assignment>
                <!--  For Static -->
                <IPAddress>{wanIP}</IPAddress>
                <Netmask>{wanSubnet}</Netmask>
                <GatewayName>SaaSGW</GatewayName>
                <GatewayIP>{wanGateway}</GatewayIP>
                <MTU>1500</MTU>
                <MSS>
                    <OverrideMSS>Disable</OverrideMSS>
                    <MSSValue>1455</MSSValue>
                </MSS>  
            </Interface>
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

    response = requests.request("GET", url, headers=headers, data = payload, verify=False)

    return response.text.encode('utf8')
