import openpyxl
import win32print
import win32con

# Open the Excel file and select the sheet
workbook = openpyxl.load_workbook('printers.xlsx')
sheet = workbook.active

printer_list = win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS | win32print.PRINTER_ENUM_LOCAL)
printer_ip = input("Enter the IP address of the network printer: ")

for printer in printer_list:
    if printer[1][1] == f"IP_{printer_ip}":
        print(f"Printer Name: {printer[2]}")
        print(f"IP Address: {printer_ip}")
        print(f"Port Name: {printer[1]['pPortName']}")
        break
else:
    print(f"Could not find a printer with the IP address {printer_ip}")

# Get a list of all printers installed on the computer
all_printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS + win32print.PRINTER_ENUM_LOCAL)

# Find the printer name based on the IP address
printer_name = ''
for printer in all_printers:
    if printer[1][1] == f"IP_{printer_ip}":
        printer_name = printer[1]['pPrinterName']
        break

# If the printer name was not found, display an error message and exit the script
if printer_name == '':
    print('Could not find a printer with the specified IP address.')
    exit()

# Get the printer handle using the printer name
printer_handle = win32print.OpenPrinter(printer_name)

# Get the printer information
printer_info = win32print.GetPrinter(printer_handle, 2)

# Get the printer status
status = win32print.GetPrinter(printer_handle, 9)

# Get the printer properties
properties = win32print.GetPrinter(printer_handle, 8)

# Write the information to the Excel sheet
sheet['A1'] = 'Printer Name'
sheet['B1'] = 'Printer Driver Name'
sheet['C1'] = 'Port Name'
sheet['D1'] = 'Printer Comment'
sheet['E1'] = 'Jobs Count'
sheet['F1'] = 'Total Pages Printed'

sheet['A2'] = printer_info['pPrinterName']
sheet['B2'] = properties['DriverName']
sheet['C2'] = printer_info['pPortName']
sheet['D2'] = printer_info['pComment']
sheet['E2'] = status['Jobs']
sheet['F2'] = win32print.DeviceCapabilities(printer_handle, printer_info['pPrinterName'], win32con.DC_PAGES, None, None)

# Close the printer handle
win32print.ClosePrinter(printer_handle)

# Save the Excel file
workbook.save('printers.xlsx')