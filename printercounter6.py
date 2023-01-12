from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import subprocess

class PrinterPageCounter(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Printer Page Counter")

        # Create a button to select the input Excel file
        self.select_file_button = QtWidgets.QPushButton("Select Input File", self)
        self.select_file_button.clicked.connect(self.selectInputFile)

        # Create a button to run the script
        self.run_button = QtWidgets.QPushButton("Run", self)
        self.run_button.clicked.connect(self.runScript)

        # Create a text box to display the results
        self.results_text_box = QtWidgets.QTextEdit(self)
        self.results_text_box.setReadOnly(True)

        # Create a layout to hold the widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.results_text_box)

    def selectInputFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        self.input_file, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select input file", "","Excel Files (*.xlsx)", options=options)

    def get_page_count(self,ip_address, community):
        oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'
        try:
            result = subprocess.run(['snmpget', '-v', '1', '-c', community, ip_address, oid], stdout=subprocess.PIPE, check=True, timeout=5)
            # Extract page count from the output
            page_count = result.stdout.decode().split()[-1]
            return int(page_count)
        except subprocess.CalledProcessError:
            return 'Offline'
        except subprocess.TimeoutExpired:
            return 'Offline'
    def runScript(self):
        ip_addresses_df = pd.read_excel(self.input_file)
        results = []
        for index, row in ip_addresses_df.iterrows():
            ip_address = row['IP Address']
            community = row['Community']
            page_count = self.get_page_count(ip_address, community)
            results.append({'IP Address': ip_address, 'Page Count': page_count})
        results_df = pd.DataFrame(results)
        self.results_text_box.setText(results_df.to_string())

        # Writing the results to Excel
        results_df.to_excel('results.xlsx', index=False)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = PrinterPageCounter()
    window.show()
    app.exec_()
