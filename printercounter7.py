import subprocess
import pandas as pd

def get_page_count(ip_address, community):
    # SNMP OID for page count
    oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'

    result = subprocess.run(['snmpget', '-v', '1', '-c', community, ip_address, oid], stdout=subprocess.PIPE)

    # Extract page count from the output
    page_count = result.stdout.decode().split()[-1]

    return int(page_count)

# Reading IP addresses from Excel file
ip_addresses_df = pd.read_excel('ip_addresses.xlsx')

# Create a list to store the results
results = []

# Loop through the IP addresses
for index, row in ip_addresses_df.iterrows():
    ip_address = row['IP Address']
    community = row['Community']
    page_count = get_page_count(ip_address, community)

    # Append the results to the list
    results.append({'IP Address': ip_address, 'Page Count': page_count})

# Create a DataFrame from the results list
results_df = pd.DataFrame(results)

# Writing the results to Excel
results_df.to_excel('results.xlsx', index=False)
