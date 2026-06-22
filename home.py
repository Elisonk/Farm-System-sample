import sys
import csv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox
)

FILE_NAME = "crops.csv"


class FarmApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Farm Management")
        self.resize(700,400)

        self.selected_row = None

        layout = QVBoxLayout()

        self.crop_input = QLineEdit()
        self.crop_input.setPlaceholderText("Crop name")
        
        self.planting_cost_input = QLineEdit()
        self.planting_cost_input.setPlaceholderText("Planting Cost")

        self.seed_buying_cost_input = QLineEdit()
        self.seed_buying_cost_input.setPlaceholderText("Seed Buying Cost")
        
        self.labour_cost_input = QLineEdit()
        self.labour_cost_input.setPlaceholderText("labour Costs")
        
        self.fertilizer_cost_input = QLineEdit()
        self.fertilizer_cost_input.setPlaceholderText("Fertilizer Cost")

        self.sell_input = QLineEdit()
        self.sell_input.setPlaceholderText("Selling price")

        add_button = QPushButton("Add Crop")
        add_button.clicked.connect(self.add_crop)
        
        edit_button = QPushButton("Edit Crop")
        edit_button.clicked.connect(self.edit_crop)
        
        update_button = QPushButton("Update Crop")
        update_button.clicked.connect(self.update_crop)
        
        delete_button = QPushButton("Delete Crop")
        delete_button.clicked.connect(self.delete_crop)
        
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.confirm_exiting)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Crop","Planting cost", "Seeds buying cost", "Labour cost","Fertilizer cost", "Selling","Profit"]
        )
       

        layout.addWidget(self.crop_input)
        layout.addWidget(self.planting_cost_input)
        layout.addWidget(self.seed_buying_cost_input)
        layout.addWidget(self.labour_cost_input)
        layout.addWidget(self.fertilizer_cost_input)
        layout.addWidget(self.sell_input)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(update_button)
        layout.addWidget(delete_button)
        layout.addWidget(self.table)
        layout.addWidget(exit_button)

        self.setLayout(layout)

        self.load_data()
        self.clear_up()

    def add_crop(self):

        crop = self.crop_input.text().strip()
        
        if not crop:
            QMessageBox.critical(self, "Error", "Please Enter Crop name")
            return
        try:
            planting_cost = int(self.planting_cost_input.text())
            seed_buying_cost = int(self.seed_buying_cost_input.text())
            labour_cost = int(self.labour_cost_input.text())
            fertilizer_cost = int(self.fertilizer_cost_input.text())
            sell = int(self.sell_input.text())
            
            if planting_cost <= 0 or labour_cost <= 0 or fertilizer_cost <= 0 or sell <= 0 :
                QMessageBox.critical(self, "Error", "input the values in these fields")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "Please fill in the fields")
            return
        

        profit = sell - planting_cost - seed_buying_cost - labour_cost - fertilizer_cost

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([crop,planting_cost, seed_buying_cost , labour_cost, fertilizer_cost,sell,profit])
            QMessageBox.information(self, "Success", "Crop added Successifully")

        self.load_data()
        self.clear_up() 
        
    def delete_crop(self):

        selected = self.table.currentRow()

        # 1️⃣ Check selection
        if selected < 0:
            QMessageBox.warning(self, "Warning", "No crop selected")
            return

        # 2️⃣ Confirm delete
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this crop?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            # 3️⃣ Read CSV
            with open(FILE_NAME, "r", newline="") as file:
                rows = list(csv.reader(file))

            # 4️⃣ Adjust index (skip header)
            csv_index = selected + 1

            # 5️⃣ Remove row from data
            if csv_index < len(rows):
                del rows[csv_index]

            # 6️⃣ Update table
            self.table.removeRow(selected)

            # 7️⃣ Write updated data back
            with open(FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            QMessageBox.information(self, "Success", "Crop deleted successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
            
    def confirm_exiting(self):
        reply = QMessageBox.question(
            self,
            "Cofrim Exit",
            "Are you want to exit? ",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton. Yes:
            self.close()
        
        
        self.load_data()
        self.clear_up()
     
            
    def edit_crop(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a row to edit.")
            return

        self.selected_row = row

    # Collect items safely
        items = [self.table.item(row, col) for col in range(6)]

        if any(item is None for item in items):
            QMessageBox.critical(self, "Error", "Selected row contains empty data.")
            return

    # Fill inputs
        inputs = [
            self.crop_input,
            self.planting_cost_input,
            self.seed_buying_cost_input,
            self.labour_cost_input,
            self.fertilizer_cost_input,
            self.sell_input
    ]

        for input_field, item in zip(inputs, items):
            if item is not None:
                input_field.setText(item.text())
                
        self.load_data()
        self.clear_up()

    def update_crop(self):

        if self.selected_row is None:
            QMessageBox.warning(self, "Update Error", "No crop selected for update.")
            return

    # Get input values
        inputs = [
            self.crop_input.text().strip(),
            self.planting_cost_input.text().strip(),
            self.seed_buying_cost_input.text().strip(),
            self.labour_cost_input.text().strip(),
            self.fertilizer_cost_input.text().strip(),
            self.sell_input.text().strip()
    ]

    # Validate inputs
        if not inputs[0]:
            QMessageBox.warning(self, "Input Error", "Crop name cannot be empty.")
            return

    # Validate numeric fields
        try:
            numeric_values = [int(value) for value in inputs[1:]]
        except ValueError:
            QMessageBox.critical(self, "Input Error", "All costs must be valid numbers.")
            return

    # Update table
        for col, value in enumerate(inputs):
            self.table.setItem(self.selected_row, col, QTableWidgetItem(value))

        QMessageBox.information(self, "Success", "Crop updated successfully.")

    # Reset selection
        self.selected_row = None
        
        self.load_data()
        self.clear_up()  
        
    def clear_up(self):
        self.crop_input.clear()
        self.planting_cost_input.clear()
        self.seed_buying_cost_input.clear()
        self.labour_cost_input.clear()
        self.fertilizer_cost_input.clear()
        self.sell_input.clear()
          
    

    def load_data(self):
        # Clear table
        self.table.setRowCount(0)

        # Initialize totals using list (cleaner)
        totals = [0, 0, 0, 0, 0, 0]  # planting, seed, labour, fertilizer, sell, profit

        try:
            with open(FILE_NAME, "r", newline="") as file:
                reader = csv.reader(file)

                # Skip header safely
                header = next(reader, None)

                for row_data in reader:

                    # Skip empty or incomplete rows
                    if len(row_data) < 7:
                        continue

                    # Insert row into table
                    row = self.table.rowCount()
                    self.table.insertRow(row)

                    # Fill table cells
                    for column, data in enumerate(row_data):
                        self.table.setItem(row, column, QTableWidgetItem(data))

                    # Safely accumulate totals
                    for i in range(6):  # columns 1–6
                        try:
                            totals[i] += int(row_data[i + 1])
                        except ValueError:
                            continue

        except FileNotFoundError:
            QMessageBox.warning(self, "File Error", "No records found.")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error:\n{str(e)}")
            return

        # ➤ Add TOTAL row
        total_row = self.table.rowCount()
        self.table.insertRow(total_row)

        self.table.setRowHeight(total_row, 30)
        self.table.resizeColumnsToContents()

        # Label
        self.table.setItem(total_row, 0, QTableWidgetItem("TOTAL (KSH)"))

        # Insert totals
        for i, value in enumerate(totals):
            self.table.setItem(total_row, i + 1, QTableWidgetItem(str(value)))

   
app = QApplication(sys.argv)

window = FarmApp()
window.show()

app.exec()