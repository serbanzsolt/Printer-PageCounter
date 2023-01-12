import requests
from bs4 import BeautifulSoup

# Function to get the page count of a printer
def get_page_count(printer_ip):
    # Send a GET request to the printer's web interface
    r = requests.get("http://" + printer_ip)
    soup = BeautifulSoup(r.content, "html.parser")
    # Find the page count element on the web page
    page_count_element = soup.find("div", {"id": "Összes"})
    # Extract the page count value
    page_count = page_count_element.text
    return page_count

# Example usage
print(get_page_count("10.160.167.206"))