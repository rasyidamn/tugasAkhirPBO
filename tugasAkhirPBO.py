from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QCalendarWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import QTimer, QDateTime, Qt, QDate, QLocale

class TodoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Todo List App')
        self.setGeometry(500, 100, 1000, 750)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_layout = QHBoxLayout()
        self.input_label = QLabel("Todo:")
        self.input_text = QLineEdit()
        self.input_button = QPushButton("Tambah")
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_text)
        self.input_layout.addWidget(self.input_button)

        self.date_layout = QGridLayout()
        self.date_clock_label = QLabel()
        self.date_calender = QCalendarWidget()
        self.date_day_label = QLabel()
        self.date_day_label.setAlignment(Qt.AlignCenter)
        self.date_clock_label.setAlignment(Qt.AlignCenter)
        self.date_clock_label.setStyleSheet('font-size:50px;')
        self.date_day_label.setStyleSheet('font-size:24px;')

        self.date_clock = QTimer()
        self.date_clock.timeout.connect(self.update_time)
        self.date_clock.start(1000)
        self.update_day()

        self.date_layout.addWidget(self.date_clock_label, 0, 0)
        self.date_layout.addWidget(self.date_calender, 0, 1, 0, 2)
        self.date_layout.addWidget(self.date_day_label, 1, 0)

        self.todo_layout = QVBoxLayout()

        self.todo_list = QListWidget()
        self.simpan_button = QPushButton("Simpan Gak sih")
        self.hapus_button = QPushButton("Hapus Gak Sih")
        self.hapus_button.clicked.connect(self.delete_item)
        self.simpan_button.clicked.connect(self.save_data)
        self.todo_data = {}
        self.load_data()

        self.todo_layout.addWidget(self.todo_list)
        self.todo_layout.addWidget(self.simpan_button)
        self.todo_layout.addWidget(self.hapus_button)

        self.layout.addLayout(self.date_layout)
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.todo_layout)

        self.input_button.clicked.connect(self.tambah_todo)
        self.date_calender.clicked.connect(self.update_selected_date)

    def update_day(self):
        current_day = QDate.currentDate()
        locale = QLocale()
        formatted_date = locale.toString(current_day, "dddd, dd MMMM yyyy")
        self.date_day_label.setText(formatted_date)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString('hh:mm:ss')
        self.date_clock_label.setText(current_time)

    def tambah_todo(self):
        todo = self.input_text.text()
        selected_date = self.date_calender.selectedDate()
        if todo and selected_date.isValid():
            date_str = selected_date.toString(Qt.ISODate)
            if date_str not in self.todo_data:
                self.todo_data[date_str] = []
            self.todo_data[date_str].append(todo)
            self.todo_list.addItem(todo)
            self.input_text.clear()
            self.show_message("Todo Ditambahkan", "Todo berhasil ditambahkan.")

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                data = file.readlines()
                for item in data:
                    date_str, todo = item.strip().split(";")
                    if date_str not in self.todo_data:
                        self.todo_data[date_str] = []
                    self.todo_data[date_str].append(todo)
                    self.todo_list.addItem(todo)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("data.txt", "w") as file:
            for date_str, todos in self.todo_data.items():
                for todo in todos:
                    file.write(f"{date_str};{todo}\n")
        self.show_message("Data Disimpan", "Data todo berhasil disimpan.")

    def delete_item(self):
        selected_indexes = self.todo_list.selectedIndexes()
        if len(selected_indexes) > 0:
            result = QMessageBox.question(self, "Konfirmasi", "Apakah Anda yakin ingin menghapus item ini?",
                                        QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                for index in selected_indexes:
                    item = self.todo_list.takeItem(index.row())
                    selected_date = self.date_calender.selectedDate()
                    if selected_date.isValid():
                        date_str = selected_date.toString(Qt.ISODate)
                        if date_str in self.todo_data:
                            self.todo_data[date_str].remove(item.text())
                self.save_data()
                self.show_message("Todo Dihapus", "Todo berhasil dihapus.")
        else:
            self.show_message("Pilih Item", "Silakan pilih item yang ingin dihapus.")

    def update_selected_date(self):
        selected_date = self.date_calender.selectedDate()
        if selected_date.isValid():
            date_str = selected_date.toString(Qt.ISODate)
            self.todo_list.clear()
            if date_str in self.todo_data:
                self.todo_list.addItems(self.todo_data[date_str])

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

app = QApplication([])
todo_app = TodoListApp()
todo_app.show()
app.exec_()
