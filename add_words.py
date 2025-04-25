from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout, QScrollArea, QComboBox, QListWidget, QLineEdit, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import json

class SubPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Subpage - Add Words")
        self.setFixedSize(1375, 700)

        self.get_json()

        layout = QVBoxLayout()
        self.grade_label = QLabel("Select Grade:")
        self.lesson_label = QLabel("Select Lesson:")
        self.words_label = QLabel("Words:")

        # Dropdowns
        self.grade_dropdown = QComboBox()
        self.grade_dropdown.setEditable(True)  # Allow typing new grades
        self.lesson_dropdown = QComboBox()
        self.lesson_dropdown.setEditable(True)  # Allow typing new lessons

         # Delete Buttons
        self.delete_grade_button = QPushButton("Delete Grade")
        self.delete_lesson_button = QPushButton("Delete Lesson")

        # Word List
        self.word_list_widget = QListWidget()

        # Input for adding words
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Enter a new word")

        # Add Word Button
        self.add_word_button = QPushButton("Add Word")
        self.add_word_button.clicked.connect(self.add_new_word)

        # Populate grade dropdown
        self.grade_dropdown.addItems(self.data.keys())  # Add grades

        # Connect dropdown changes
        self.grade_dropdown.currentTextChanged.connect(self.update_lessons)
        self.lesson_dropdown.currentTextChanged.connect(self.display_words)

        # Detect new grade/lesson entries
        self.grade_dropdown.editTextChanged.connect(self.add_new_grade)
        self.lesson_dropdown.editTextChanged.connect(self.add_new_lesson)

        # Delete button actions
        self.delete_grade_button.clicked.connect(self.delete_grade)
        self.delete_lesson_button.clicked.connect(self.delete_lesson)
       

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Layouts for dropdowns + delete buttons
        grade_layout = QHBoxLayout()
        grade_layout.addWidget(self.grade_dropdown)
        grade_layout.addWidget(self.delete_grade_button)

        lesson_layout = QHBoxLayout()
        lesson_layout.addWidget(self.lesson_dropdown)
        lesson_layout.addWidget(self.delete_lesson_button)

        # Add word input and button
        word_layout = QHBoxLayout()
        word_layout.addWidget(self.word_input)
        word_layout.addWidget(self.add_word_button)

        # Add widgets to layout
        layout.addWidget(self.grade_label)
        layout.addLayout(grade_layout)
        layout.addWidget(self.lesson_label)
        layout.addLayout(lesson_layout)
        layout.addWidget(self.words_label)
        layout.addLayout(word_layout)
        layout.addWidget(self.word_list_widget)


        layout.addWidget(close_button)
        self.setLayout(layout)
        self.update_lessons()
    
    def get_json(self):
        json_file = "Pirates_of_the_classroom/assets/json/words.json"
        with open(json_file, "r", encoding="utf-8") as file:
            self.data = json.load(file)
    
    def save_json(self):
        """ Saves the current data dictionary back to JSON file """
        json_file = "Pirates_of_the_classroom/assets/json/words.json"
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def update_lessons(self):
        """ Updates the lessons dropdown based on selected grade """
        selected_grade = self.grade_dropdown.currentText()
        self.lesson_dropdown.clear()
        print("running")
        if selected_grade in self.data:
            self.lesson_dropdown.addItems(self.data[selected_grade].keys())

    def display_words(self):
        """ Displays words from the selected grade and lesson """
        self.word_list_widget.clear()
        selected_grade = self.grade_dropdown.currentText()
        selected_lesson = self.lesson_dropdown.currentText()

        if selected_grade in self.data and selected_lesson in self.data[selected_grade]:
            words = self.data[selected_grade][selected_lesson]
            self.word_list_widget.addItems(words)

    def add_new_grade(self):
        """ Adds a new grade if it does not exist """
        new_grade = self.grade_dropdown.currentText().strip()
        if new_grade and new_grade not in self.data:
            self.data[new_grade] = {}  # Create an empty lessons dictionary
            self.save_json()

    def add_new_lesson(self):
        """ Adds a new lesson if it does not exist in the selected grade """
        selected_grade = self.grade_dropdown.currentText().strip()
        new_lesson = self.lesson_dropdown.currentText().strip()

        if selected_grade in self.data and new_lesson and new_lesson not in self.data[selected_grade]:
            self.data[selected_grade][new_lesson] = []  # Create an empty word list
            self.save_json()

    def add_new_word(self):
        """ Adds a new word to the selected grade and lesson """
        selected_grade = self.grade_dropdown.currentText().strip()
        selected_lesson = self.lesson_dropdown.currentText().strip()
        new_word = self.word_input.text().strip()

        if selected_grade and selected_lesson and new_word:
            if selected_grade in self.data and selected_lesson in self.data[selected_grade]:
                if new_word not in self.data[selected_grade][selected_lesson]:  # Prevent duplicates
                    self.data[selected_grade][selected_lesson].append(new_word)
                    self.save_json()
                    self.display_words()  # Refresh word list
                    self.word_input.clear()  # Clear input field

    def delete_grade(self):
        """ Deletes the selected grade and its lessons """
        selected_grade = self.grade_dropdown.currentText().strip()
        if selected_grade in self.data:
            confirmation = QMessageBox.question(
                self, "Delete Grade", f"Are you sure you want to delete grade '{selected_grade}' and all its lessons?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                del self.data[selected_grade]
                self.save_json()
                self.grade_dropdown.clear()
                self.grade_dropdown.addItems(self.data.keys())  # Refresh dropdown
                self.lesson_dropdown.clear()
                self.word_list_widget.clear()

    def delete_lesson(self):
        """ Deletes the selected lesson from the selected grade """
        selected_grade = self.grade_dropdown.currentText().strip()
        selected_lesson = self.lesson_dropdown.currentText().strip()

        if selected_grade in self.data and selected_lesson in self.data[selected_grade]:
            confirmation = QMessageBox.question(
                self, "Delete Lesson", f"Are you sure you want to delete lesson '{selected_lesson}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                del self.data[selected_grade][selected_lesson]
                self.save_json()
                self.update_lessons()
                self.word_list_widget.clear()
