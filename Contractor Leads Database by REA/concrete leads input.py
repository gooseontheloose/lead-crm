import sys
import json
import os
import csv
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QTabWidget, QFileDialog, QAbstractItemView
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PyQt5.QtWidgets import QStyledItemDelegate, QMessageBox

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Failed to install required dependencies.")
        sys.exit(1)

def check_dependencies():
    try:
        import PyQt5
        import reportlab
    except ImportError:
        return False
    return True

class ContractorLeadsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contractor Leads Database by REA")
        self.setGeometry(100, 100, 1600, 800)

        if not check_dependencies():
            install_dependencies()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.leads = []
        self.load_leads_data()

        self.setup_ui()

    def setup_ui(self):
        self.tabs = TabWidget(self, self.leads)
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("logo.png")
        self.logo_pixmap = self.logo_pixmap.scaledToWidth(150, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.tabs)
        self.central_widget.setLayout(layout)

        self.set_dark_theme()

    def set_dark_theme(self):
        app = QApplication.instance()
        app.setStyle("Fusion")

        # Dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, Qt.black)
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        app.setPalette(dark_palette)

        # Set the font for all widgets to improve readability
        app_font = QFont("Arial", 10)
        app.setFont(app_font)

    def closeEvent(self, event):
        self.save_leads_data()
        event.accept()

    def save_leads_data(self):
        with open("leads_data.json", "w") as file:
            json.dump(self.leads, file)

    def load_leads_data(self):
        if os.path.exists("leads_data.json"):
            try:
                with open("leads_data.json", "r") as file:
                    self.leads = json.load(file)
            except json.JSONDecodeError:
                self.leads = []
        else:
            folder_path = os.path.dirname(os.path.abspath(__file__))
            os.makedirs(folder_path, exist_ok=True)
            self.leads = []

class TabWidget(QWidget):
    def __init__(self, parent, leads_list):
        super().__init__()

        self.leads_list = leads_list

        self.tabs = QTabWidget(self)

        self.contractor_input_tab = ContractorInputTab(self.leads_list, self)
        self.leads_table_tab = LeadsTableTab(self.leads_list)  # Remove the second argument

        self.tabs.addTab(self.contractor_input_tab, "Contractor Leads Input")
        self.tabs.addTab(self.leads_table_tab, "Leads Table View")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

class ContractorInputTab(QWidget):
    def __init__(self, leads_list, parent):
        super().__init__()

        self.leads_list = leads_list
        self.parent = parent

        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()

        self.last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()

        # Address Fields
        self.address1_label = QLabel("Address Line 1:")
        self.address1_input = QLineEdit()

        self.address2_label = QLabel("Address Line 2:")
        self.address2_input = QLineEdit()

        self.city_label = QLabel("City:")
        self.city_input = QLineEdit()

        self.state_label = QLabel("State:")
        self.state_input = QLineEdit()

        self.zip_label = QLabel("Zip:")
        self.zip_input = QLineEdit()

        self.phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        self.notes_label = QLabel("Notes:")
        self.notes_input = QTextEdit()

        self.referred_by_label = QLabel("Referred By:")
        self.referred_by_input = QLineEdit()
        
        self.job_type_label = QLabel("Job Type:")
        self.job_type_dropdown = QComboBox()
        self.job_type_dropdown.addItems(["Residential", "Commercial", "Unknown"])
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.add_lead)

        layout = QVBoxLayout()
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.address1_label)
        layout.addWidget(self.address1_input)
        layout.addWidget(self.address2_label)
        layout.addWidget(self.address2_input)
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.state_label)
        layout.addWidget(self.state_input)
        layout.addWidget(self.zip_label)
        layout.addWidget(self.zip_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.notes_label)
        layout.addWidget(self.notes_input)
        layout.addWidget(self.referred_by_label)
        layout.addWidget(self.referred_by_input)
        layout.addWidget(self.job_type_label)
        layout.addWidget(self.job_type_dropdown)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_lead(self):
        # Get the values from input fields
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        address1 = self.address1_input.text()
        address2 = self.address2_input.text()
        city = self.city_input.text()
        state = self.state_input.text()
        zip_code = self.zip_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        notes = self.notes_input.toPlainText()
        referred_by = self.referred_by_input.text()
        job_type = self.job_type_dropdown.currentText()

        # Create the widgets here
        status_combo = QComboBox()
        status_combo.addItems(["In System", "Good Lead", "Contact Later", "Bad Lead", "Passed Along", "Closed"])
        status_combo.setCurrentText("In System")
        status_combo.currentTextChanged.connect(self.status_changed)

        first_name_item = QLineEdit(first_name)
        first_name_item.editingFinished.connect(lambda: self.name_changed(first_name_item.text()))

        last_name_item = QLineEdit(last_name)
        last_name_item.editingFinished.connect(lambda: self.name_changed(last_name_item.text()))

        address1_item = QLineEdit(address1)
        address1_item.editingFinished.connect(lambda: self.address_changed(address1_item.text()))

        address2_item = QLineEdit(address2)
        address2_item.editingFinished.connect(lambda: self.address_changed(address2_item.text()))

        city_state_zip_item = QLineEdit(f"{city}, {state}, {zip_code}")
        city_state_zip_item.editingFinished.connect(lambda: self.address_changed(city_state_zip_item.text()))

        phone_input = QLineEdit(phone)
        phone_input.editingFinished.connect(lambda: self.phone_changed(phone_input.text()))

        email_input = QLineEdit(email)
        email_input.editingFinished.connect(lambda: self.email_changed(email_input.text()))

        notes_input = QLineEdit(notes)
        notes_input.editingFinished.connect(lambda: self.notes_changed(notes_input.text()))

        job_type_combo = QComboBox()
        job_type_combo.addItems(["Residential", "Commercial", "Unknown"])
        job_type_combo.setCurrentText(job_type)
        job_type_combo.currentTextChanged.connect(self.job_type_changed)

        referred_by_input = QLineEdit(referred_by)
        referred_by_input.editingFinished.connect(lambda: self.referred_by_changed(referred_by_input.text()))

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_lead)

        # Now add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.address1_label)
        layout.addWidget(self.address1_input)
        layout.addWidget(self.address2_label)
        layout.addWidget(self.address2_input)
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.state_label)
        layout.addWidget(self.state_input)
        layout.addWidget(self.zip_label)
        layout.addWidget(self.zip_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.notes_label)
        layout.addWidget(self.notes_input)
        layout.addWidget(self.referred_by_label)
        layout.addWidget(self.referred_by_input)
        layout.addWidget(self.job_type_label)
        layout.addWidget(self.job_type_dropdown)
        layout.addWidget(self.submit_button)  # Move this line to the correct position

        self.setLayout(layout)

        # Append the lead data to the list
        self.leads_list.append({
            "First Name": first_name,
            "Last Name": last_name,
            "Address Line 1": address1,
            "Address Line 2": address2,
            "City": city,
            "State": state,
            "Zip": zip_code,
            "Phone": phone,
            "Email": email,
            "Notes": notes,
            "Referred By": referred_by,
            "Job Type": job_type,
            "Lead Status": "In System"
        })

        # Clear input fields after adding the lead
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.address1_input.clear()
        self.address2_input.clear()
        self.city_input.clear()
        self.state_input.clear()
        self.zip_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.notes_input.clear()
        self.referred_by_input.clear()
        self.job_type_dropdown.setCurrentIndex(0)

        # Update the table view in the other tab
        self.parent.leads_table_tab.populate_table()


class CustomDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.editingFinished.connect(lambda: self.commitData.emit(editor))
        elif isinstance(editor, QComboBox):
            editor.currentIndexChanged.connect(lambda: self.commitData.emit(editor))
        return editor
        
class LeadsTableTab(QWidget):
    def __init__(self, leads_list):
        super().__init__()
        self.edit_mode = False

        self.leads_list = leads_list

        # Create the table with additional columns
        self.table = QTableWidget(self)
        self.table.setColumnCount(15)  # Adjusted column count
        self.table.setHorizontalHeaderLabels(
            ["Lead Status", "First Name", "Last Name", "Address Line 1", "Address Line 2", "City", "State", "Zip", "Phone", "Email", "Notes", "Job Type", "Referred By", "Referred To", "Actions"])  # Adjusted header labels
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Apply custom delegate to handle editing of cell widgets
        delegate = CustomDelegate()
        self.table.setItemDelegate(delegate)

        # Create the refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.populate_table)

        # Create the export buttons
        self.export_csv_button = QPushButton("Export to CSV")
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.export_pdf_button = QPushButton("Export to PDF")
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        self.export_txt_button = QPushButton("Export to TXT")
        self.export_txt_button.clicked.connect(self.export_to_txt)

        # Create the toggle edit mode button
        self.toggle_edit_button = QPushButton("Toggle Edit Mode")
        self.toggle_edit_button.clicked.connect(self.toggle_edit_mode)

        # Modify the button sizes here
        button_width = 120
        button_height = 30

        # Set fixed sizes for the buttons
        self.refresh_button.setFixedSize(button_width, button_height)
        self.export_csv_button.setFixedSize(button_width, button_height)
        self.export_pdf_button.setFixedSize(button_width, button_height)
        self.export_txt_button.setFixedSize(button_width, button_height)
        self.toggle_edit_button.setFixedSize(button_width, button_height)

        # Create a layout for the export buttons
        export_button_layout = QVBoxLayout()
        export_button_layout.addWidget(self.export_csv_button)
        export_button_layout.addWidget(self.export_pdf_button)
        export_button_layout.addWidget(self.export_txt_button)

        # Create a layout for the buttons and set alignment
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addLayout(export_button_layout)
        button_layout.addWidget(self.toggle_edit_button)
        button_layout.setAlignment(Qt.AlignCenter)

        # Create the main layout for the tab
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.populate_table()

    def toggle_edit_mode(self):
        self.edit_mode = not getattr(self, "edit_mode", False)
        
        for row in range(self.table.rowCount()):
            for col in range(1, self.table.columnCount() - 1):
                item = self.table.cellWidget(row, col)
                if isinstance(item, QLineEdit):
                    item.setReadOnly(not self.edit_mode)
        
        self.toggle_edit_button.setText("Editing Enabled" if self.edit_mode else "Editing Disabled")

    def createEditor(self, parent, option, index):
        if not self.edit_mode:
            QMessageBox.warning(self, "Editing Mode Off", "Editing must be enabled to edit cell data.")
            return None

        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.editingFinished.connect(lambda: self.commitData.emit(editor))
        elif isinstance(editor, QComboBox):
            editor.currentIndexChanged.connect(lambda: self.commitData.emit(editor))
        return editor

    def populate_table(self):
        self.table.setRowCount(len(self.leads_list))  # Clear existing rows
        for row, lead in enumerate(self.leads_list):

            
            # Add all the widgets to a layout to create a single line in each cell
            layout = QHBoxLayout()
            layout.addWidget(status_combo)
            layout.addWidget(first_name_item)
            layout.addWidget(last_name_item)
            layout.addWidget(address1_item)
            layout.addWidget(address2_item)
            layout.addWidget(city_state_zip_item)
            layout.addWidget(phone_input)
            layout.addWidget(email_input)
            layout.addWidget(notes_input)
            layout.addWidget(job_type_combo)
            layout.addWidget(referred_by_input)
            layout.addWidget(referred_to_input)
            layout.addWidget(delete_button)

            # Create a container widget and set the layout
            container = QWidget()
            container.setLayout(layout)

            # Set the container widget as the cell widget
            self.table.setCellWidget(row, 0, container)

            # Status Combo Box
            status_combo = QComboBox()
            status_combo.addItems(["In System", "Good Lead", "Contact Later", "Bad Lead", "Passed Along", "Closed"])
            current_status = lead.get("Lead Status", "In System")
            status_combo.setCurrentText(current_status)
            status_combo.currentTextChanged.connect(lambda text, r=row: self.status_changed(r, text))
            self.table.setCellWidget(row, 0, status_combo)

            # Split First Name and Last Name
            name_parts = lead["First Name"].split()
            first_name = name_parts[0] if name_parts else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            first_name_item = QLineEdit(first_name)
            last_name_item = QLineEdit(last_name)
            first_name_item.editingFinished.connect(lambda r=row, input_field=first_name_item: self.input_field_changed(r, "First Name", input_field.text()))
            last_name_item.editingFinished.connect(lambda r=row, input_field=last_name_item: self.input_field_changed(r, "Last Name", input_field.text()))
            self.table.setCellWidget(row, 1, first_name_item)
            self.table.setCellWidget(row, 2, last_name_item)

            # Split Address
            address_parts = [lead["Address Line 1"], lead["Address Line 2"], lead["City"], lead["State"], lead["Zip"]]
            address1 = address_parts[0] if address_parts else ""
            address2 = address_parts[1] if len(address_parts) > 1 else ""
            city_state_zip = ", ".join(address_parts[2:]) if len(address_parts) > 2 else ""
            address1_item = QLineEdit(address1)
            address2_item = QLineEdit(address2)
            city_state_zip_item = QLineEdit(city_state_zip)
            address1_item.editingFinished.connect(lambda r=row, input_field=address1_item: self.input_field_changed(r, "Address Line 1", input_field.text()))
            address2_item.editingFinished.connect(lambda r=row, input_field=address2_item: self.input_field_changed(r, "Address Line 2", input_field.text()))
            city_state_zip_item.editingFinished.connect(lambda r=row, input_field=city_state_zip_item: self.input_field_changed(r, "City, State, Zip", input_field.text()))
            self.table.setCellWidget(row, 3, address1_item)
            self.table.setCellWidget(row, 4, address2_item)
            self.table.setCellWidget(row, 5, city_state_zip_item)
        
            phone_input = QLineEdit(lead["Phone"])
            phone_input.editingFinished.connect(lambda r=row, input_field=phone_input: self.input_field_changed(r, "Phone", input_field.text()))
            self.table.setCellWidget(row, 6, phone_input)

            email_input = QLineEdit(lead["Email"])
            email_input.editingFinished.connect(lambda r=row, input_field=email_input: self.input_field_changed(r, "Email", input_field.text()))
            self.table.setCellWidget(row, 7, email_input)
            
            # Notes
            notes_input = QLineEdit(lead["Notes"])
            self.table.setCellWidget(row, 8, notes_input)

            #Type, Referred to/by
            self.table.setItem(row, 9, QTableWidgetItem(lead["Job Type"]))
            self.table.setItem(row, 10, QTableWidgetItem(lead["Referred By"]))
            self.table.setItem(row, 11, QTableWidgetItem(lead.get("Referred To", "")))

            # Job Type Combo Box
            job_type_combo = QComboBox()
            job_type_combo.addItems(["Residential", "Commercial", "Other"])
            current_job_type = lead.get("Job Type", "Unknown")
            job_type_combo.setCurrentText(current_job_type)
            job_type_combo.currentTextChanged.connect(lambda text, r=row: self.job_type_changed(r, text))
            self.table.setCellWidget(row, 12, job_type_combo)

            # Referred By, Referred To
            referred_by_input = QLineEdit(lead.get("Referred By", ""))
            referred_by_input.textChanged.connect(lambda text, r=row: self.referred_by_changed(r, text))
            self.table.setCellWidget(row, 13, referred_by_input)
            referred_to_input = QLineEdit(lead.get("Referred To", ""))
            referred_to_input.textChanged.connect(lambda text, r=row: self.referred_to_changed(r, text))
            self.table.setCellWidget(row, 14, referred_to_input)

            # Delete Button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=row: self.delete_lead(r))
            self.table.setCellWidget(row, 15, delete_button)

            # Connect input field changes to corresponding functions
            referred_by_input.textChanged.connect(lambda text, r=row: self.input_field_changed(r, "Referred By", text))
            referred_to_input.textChanged.connect(lambda text, r=row: self.input_field_changed(r, "Referred To", text))
            
    def input_field_changed(self, row, field_name, new_value):
        self.leads_list[row][field_name] = new_value

    def status_changed(self, row, text):
        self.leads_list[row]["Lead Status"] = text

    def name_changed(self, row, text):
        self.leads_list[row]["Name"] = text
        
    def address_changed(self, row, text):
        self.leads_list[row]["Address"] = text
        
    def phone_changed(self, row, text):
        self.leads_list[row]["Phone"] = text
        
    def email_changed(self, row, text):
        self.leads_list[row]["Email"] = text
        
    def notes_changed(self, row, text):
        self.leads_list[row]["Notes"] = text
        
    def referred_by_changed(self, row, text):
        self.leads_list[row]["Referred By"] = text

    def referred_to_changed(self, row, text):
        self.leads_list[row]["Referred To"] = text
        
    def export_to_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # Write the header
                writer.writerow(["Name", "Address", "Phone", "Email", "Notes", "Job Type"])
                # Write the data
                for lead in self.leads_list:
                    writer.writerow([lead["Name"], lead["Address"], lead["Phone"], lead["Email"], lead["Notes"], lead["Job Type"]])

    def export_to_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            doc = SimpleDocTemplate(file_name, pagesize=letter)
            elements = []
            data = [["Name", "Address", "Phone", "Email", "Notes", "Job Type"]]
            for lead in self.leads_list:
                data.append([lead["Name"], lead["Address"], lead["Phone"], lead["Email"], lead["Notes"], lead["Job Type"]])
            t = Table(data)
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            elements.append(t)
            doc.build(elements)

    def export_to_txt(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to TXT", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "w") as file:
                for lead in self.leads_list:
                    file.write(f"Name: {lead['Name']}\n")
                    file.write(f"Address: {lead['Address']}\n")
                    file.write(f"Phone: {lead['Phone']}\n")
                    file.write(f"Email: {lead['Email']}\n")
                    file.write(f"Notes: {lead['Notes']}\n")
                    file.write(f"Job Type: {lead['Job Type']}\n")
                    file.write("\n")

    def delete_lead(self, row):
        confirmation = QMessageBox.question(
            self, "Confirm Deletion",
            "Are you sure you want to delete this lead?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirmation == QMessageBox.Yes:
            del self.leads_list[row]
            self.populate_table()  # Refresh the table

    def job_type_changed(self, row, text):
        self.leads_list[row]["Job Type"] = text
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContractorLeadsApp()
    window.show()
    sys.exit(app.exec_())
