from PyQt6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QComboBox, QDialog, QMessageBox, QWidget
)
import json


class GameStartDialog(QDialog):
    """ Pop-up that asks the user to select a grade and lesson before starting the game. """
    def __init__(self):
        super().__init__()
        print("Showing_dialog")
        self.setWindowTitle("Select Grade & Lesson")
        self.setFixedSize(400, 200)

        self.get_json()  # Load words data

        layout = QVBoxLayout()

        # Labels
        grade_label = QLabel("Select Grade:")
        lesson_label = QLabel("Select Lesson:")

        # Dropdowns
        self.grade_dropdown = QComboBox()
        self.lesson_dropdown = QComboBox()

        # Populate grades dropdown
        self.grade_dropdown.addItems(self.data.keys())
        self.grade_dropdown.currentTextChanged.connect(self.update_lessons)

        # Default lessons update
        self.update_lessons()

        # Buttons
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start Game")
        cancel_button = QPushButton("Cancel")

        start_button.clicked.connect(self.accept_selection)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(start_button)
        button_layout.addWidget(cancel_button)

        # Add widgets to layout
        layout.addWidget(grade_label)
        layout.addWidget(self.grade_dropdown)
        layout.addWidget(lesson_label)
        layout.addWidget(self.lesson_dropdown)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_json(self):
        """ Loads JSON data containing grades, lessons, and words """
        json_file = "Pirates_of_the_classroom/assets/json/words.json"
        with open(json_file, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def update_lessons(self):
        """ Updates lesson dropdown based on selected grade """
        selected_grade = self.grade_dropdown.currentText()
        self.lesson_dropdown.clear()
        if selected_grade in self.data:
            self.lesson_dropdown.addItems(self.data[selected_grade].keys())

    def accept_selection(self):
        """ Returns selected grade & lesson if valid, otherwise shows error """
        selected_grade = self.grade_dropdown.currentText()
        selected_lesson = self.lesson_dropdown.currentText()
        print("checking")
        if not selected_grade or not selected_lesson:
            QMessageBox.warning(self, "Selection Error", "Please select both a grade and a lesson.")
        else:
            self.accept()  # Closes dialog with a success status

    def get_selection(self):
        """ Returns selected grade & lesson as a tuple """
        return self.grade_dropdown.currentText(), self.lesson_dropdown.currentText()