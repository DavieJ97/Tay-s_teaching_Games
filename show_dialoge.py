from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QMessageBox
import json
from objects import Button, Label, ComboBox


class GameStartDialog(QDialog):
    """ Pop-up that asks the user to select a grade and lesson before starting the game. """
    def __init__(self, game):
        super().__init__()
        print("Showing_dialog")
        if game == "pirate":
            self.json_path = "Pirates_of_the_classroom/assets/json/words.json"
        elif game == "kittens":
            self.json_path = "Exploding_kittens/assets/json/questions.json"
        self.setWindowTitle("Select Grade & Lesson")
        self.setFixedSize(400, 300)
        # Set background color
        self.setStyleSheet("background-color: #9ccdc2;")

        self.get_json()  # Load words data

        layout = QVBoxLayout()

        # Labels
        grade_label = Label("Select Grade:", 16)
        lesson_label = Label("Select Lesson:", 16)

        # Dropdowns
        self.grade_dropdown = ComboBox()
        self.lesson_dropdown = ComboBox()

        # Populate grades dropdown
        self.grade_dropdown.addItems(self.data.keys())
        self.grade_dropdown.currentTextChanged.connect(self.update_lessons)

        # Default lessons update
        self.update_lessons()

        # Buttons
        button_layout = QHBoxLayout()
        start_button = Button(150, 50, text ="Start Game")
        start_button.toggle_styleSheet("normal")
        cancel_button = Button(150, 50, text ="Cancel")
        cancel_button.toggle_styleSheet("normal")

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
        json_file = self.json_path
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