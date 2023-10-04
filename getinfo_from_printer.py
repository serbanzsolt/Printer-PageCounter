from pysnmp.hlapi import *

def get_print_jobs(printer_ip, community):
    print_jobs = []

    # Define the SNMP OID for print job information
    oid = ObjectIdentity('SNMPv2-MIB', 'sysOREntry')

    # Create an SNMP GET request
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((printer_ip, 161)),
        ContextData(),
        ObjectType(oid)
    )

    # Retrieve and process the SNMP response
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print("Error:", errorIndication)
        else:
            for varBind in varBinds:
                print_jobs.append(varBind)

    return print_jobs

printer_ip = "10.160.71.217"
community = "public"

print_jobs = get_print_jobs(printer_ip, community)
for job in print_jobs:
    print(job)