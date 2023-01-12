import subprocess

def get_page_count(ip_address, community):
    # SNMP OID for page count
    oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'

    result = subprocess.run(['snmpget', '-v', '1', '-c', community, ip_address, oid], stdout=subprocess.PIPE)
    print (result)
    
    # Extract page count from the output
    page_count = result.stdout.decode().split()[-1]

    return int(page_count)

# Example usage
ip_address = '10.160.167.207'
community = 'public'
print(get_page_count(ip_address, community))