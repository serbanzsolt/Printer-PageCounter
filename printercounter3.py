from pysnmp.hlapi import *

# Function to get the page count of a printer
def get_page_count(printer_ip, community_string):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community_string),
               UdpTransportTarget((printer_ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-SMI', 'mib-2', 1, 3, 6))
        )
    )
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

# Example usage
get_page_count("10.160.167.209", "public")