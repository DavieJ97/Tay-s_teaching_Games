from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy, QGridLayout, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import json
from objects import Button, ComboBox, Label, LineEdit, ToggleSwitch
import os
import shutil

BASEFOLDER = "images/uploaded_image/Pirates"

class SubPagePirate(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = "teacher"
        self.com_checked = False
        self.setWindowTitle("Subpage - Add Words")
        self.setFixedSize(1375, 700)

        self.get_json()

        layout = QVBoxLayout()
        self.grade_label = Label("Select Grade:", 15)
        self.lesson_label = Label("Select Lesson:", 15)
        self.words_label = Label("Words:", 15)

        # Dropdowns
        self.grade_dropdown = ComboBox(self.mode)
        self.grade_dropdown.setEditable(True)  # Allow typing new grades
        self.lesson_dropdown = ComboBox(self.mode)
        self.lesson_dropdown.setEditable(True)  # Allow typing new lessons

         # Delete Buttons
        self.delete_grade_button = Button(150, 50, text="Delete Grade")
        self.delete_grade_button.toggle_styleSheet(self.mode)
        self.delete_lesson_button = Button(150, 50, text="Delete Lesson")
        self.delete_lesson_button.toggle_styleSheet(self.mode)

        # add Buttons
        self.add_grade_button = Button(150, 50, text="Save Grade")
        self.add_grade_button.toggle_styleSheet(self.mode)
        self.add_lesson_button = Button(150, 50, text="Save Lesson")
        self.add_lesson_button.toggle_styleSheet(self.mode)

        # Horizontal Inputs
        self.mini_layouts = []
        for _ in range(11):
            mini_layout = QHBoxLayout()
            word_input = LineEdit(200)
            word_input.setPlaceholderText("Enter a new word")
            switch = ToggleSwitch("Change text to image")
            label = Label()
            mini_layout.addWidget(word_input)
            mini_layout.addWidget(switch)
            mini_layout.addWidget(label)
            mini_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
            mini_layout_dic = {}
            mini_layout_dic["layout"] = mini_layout
            mini_layout_dic["input"] = word_input
            mini_layout_dic["switch"] = switch
            mini_layout_dic["label"] = label
            self.mini_layouts.append(mini_layout_dic)
            
        # Populate grade dropdown
        self.grade_dropdown.addItems(self.data.keys())  # Add grades

        # Connect dropdown changes
        self.grade_dropdown.currentTextChanged.connect(self.update_lessons)
        self.lesson_dropdown.currentTextChanged.connect(self.display_words)

        # Detect new grade/lesson entries
        self.add_grade_button.clicked.connect(self.add_new_grade)
        self.add_lesson_button.clicked.connect(self.add_new_lesson)

        # Delete button actions
        self.delete_grade_button.clicked.connect(self.delete_grade)
        self.delete_lesson_button.clicked.connect(self.delete_lesson)
       
        close_button = Button(300, 80, text="Close")
        close_button.toggle_styleSheet(self.mode)
        close_button.clicked.connect(self.close)

        save_words_button = Button(300, 80, text="Save")
        save_words_button.toggle_styleSheet(self.mode)
        save_words_button.clicked.connect(self.add_new_word)

        close_layout = QHBoxLayout()
        close_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        close_layout.addWidget(save_words_button)
        close_layout.addWidget(close_button)
        close_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Layouts for dropdowns + delete buttons
        grade_layout = QHBoxLayout()
        grade_layout.addWidget(self.grade_dropdown)
        grade_layout.addWidget(self.add_grade_button)
        grade_layout.addWidget(self.delete_grade_button)

        lesson_layout = QHBoxLayout()
        lesson_layout.addWidget(self.lesson_dropdown)
        lesson_layout.addWidget(self.add_lesson_button)
        lesson_layout.addWidget(self.delete_lesson_button)

        # Add word input and button
        word_layout = QGridLayout()
        column_label = Label("Column words", 14)
        row_label = Label("Rows words", 14)
        word_layout.addWidget(column_label, 0, 0)
        word_layout.addWidget(row_label, 0, 1)
        row = 1
        column = 0
        for lay in self.mini_layouts:
            word_layout.addLayout(lay["layout"], row, column)
            if row <= 5:
                row += 1
            else:
                row = 1
                column += 1

        # Add widgets to layout
        print("starting to layout")
        try:
            layout.addWidget(self.grade_label)
            print("laid grade label")
        except Exception as e:
            print("Error adding grade label:", e)
        layout.addLayout(grade_layout)
        layout.addWidget(self.lesson_label)
        layout.addLayout(lesson_layout)
        layout.addWidget(self.words_label)
        layout.addLayout(word_layout)
        layout.addLayout(close_layout)
        self.setLayout(layout)
        self.update_lessons()
        print("connecting switches")
        for i, lay in enumerate(self.mini_layouts):
            swtch = lay["switch"]
            swtch.stateChanged.connect(lambda checked, num = i: self.toggle_input(num))

    
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
        selected_grade = self.grade_dropdown.currentText()
        selected_lesson = self.lesson_dropdown.currentText()
        words = self.data.get(selected_grade, {}).get(selected_lesson, [])
        print("looping through layouts")
        for i, lay in enumerate(self.mini_layouts):
            lineedit = lay["input"]
            switch = lay["switch"]
            label = lay["label"]
            if i < len(words):
                lineedit.setText(words[i])
                word = words[i]
                print("Checking if image")
                if word.endswith(".png") or word.endswith(".jpg") or word.endswith(".jpeg"):
                    self.com_checked = True
                    switch.setChecked(True)
                    self.com_checked = False
                    pixmap = QPixmap(word)
                    pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    label.setPixmap(pixmap)
            else:
                lineedit.clear()

    def add_new_grade(self):
        """ Adds a new grade if it does not exist """
        new_grade = self.grade_dropdown.currentText().strip()
        if new_grade and new_grade not in self.data:
            confirmation = QMessageBox.question(
                self, "Add New Grade", f"Are you sure you want to add a new grade '{new_grade}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.data[new_grade] = {}  # Create an empty lessons dictionary
                self.save_json()
        elif new_grade and new_grade in self.data:
            QMessageBox.warning(
                self, "Already exists!!", f"The Grade you are trying to add already exists.", QMessageBox.StandardButton.Ok
            )
        elif not new_grade:
           QMessageBox.warning(
                self, "Cannot add an empty Grade!!", f"You cannot add an empty grade.", QMessageBox.StandardButton.Ok
            ) 

    def add_new_lesson(self):
        """ Adds a new lesson if it does not exist in the selected grade """
        selected_grade = self.grade_dropdown.currentText().strip()
        new_lesson = self.lesson_dropdown.currentText().strip()
        if selected_grade in self.data and new_lesson and new_lesson not in self.data[selected_grade]:
            confirmation = QMessageBox.question(
                self, "Add New Lesson", f"Are you sure you want to add a new lesson '{new_lesson}' to Grade '{selected_grade}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.data[selected_grade][new_lesson] = []  # Create an empty word list
                self.save_json()
        elif selected_grade not in self.data:
            QMessageBox.warning(
                self, "Grade does not exists!!", f"The Grade does not yet exist, Please first add the Grade.", QMessageBox.StandardButton.Ok
            )
        elif selected_grade in self.data and new_lesson in self.data[selected_grade]:
            QMessageBox.warning(
                self, "Already exists!!", f"The Lesson you are trying to add already exists.", QMessageBox.StandardButton.Ok
            )
        elif not new_lesson:
           QMessageBox.warning(
                self, "Cannot add an empty Lesson!!", f"You cannot add an empty lesson.", QMessageBox.StandardButton.Ok
            ) 

    def add_new_word(self):
        """ Adds a new word to the selected grade and lesson """
        selected_grade = self.grade_dropdown.currentText().strip()
        selected_lesson = self.lesson_dropdown.currentText().strip()
        self.data[selected_grade][selected_lesson] = []
        for layout in self.mini_layouts:
            lineedit = layout["input"]
            new_word = lineedit.text().strip()
            if selected_grade and selected_lesson and new_word:
                if selected_grade in self.data and selected_lesson in self.data[selected_grade]:
                    if new_word not in self.data[selected_grade][selected_lesson]:  # Prevent duplicates
                        self.data[selected_grade][selected_lesson].append(new_word)
                        lineedit.clear()  # Clear input field
        self.save_json()
        self.display_words()

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
                self.display_words()

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
                self.display_words()
    
    def toggle_input(self, index):
        if not self.com_checked:
            grade = self.grade_dropdown.currentText().strip()
            lesson = self.lesson_dropdown.currentText().strip()
            image_folder = os.path.join(os.path.dirname(__file__), BASEFOLDER, f"Grade{grade} Lesson{lesson}")
            os.makedirs(image_folder, exist_ok=True)
            input = self.mini_layouts[index]["input"]
            switch = self.mini_layouts[index]["switch"]
            label = self.mini_layouts[index]["label"]
            if switch.isChecked():
                file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
                if file_path:
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(image_folder, file_name)
                    base, ext = os.path.splitext(file_name)
                    count = 1
                    while os.path.exists(destination_path):
                        file_name = f"{base}_{count}{ext}"
                        destination_path = os.path.join(image_folder, file_name)
                        count += 1
                    shutil.copy(file_path, destination_path)
                    self.image_path = os.path.relpath(destination_path)
                    QMessageBox.information(self, "Image Added", f"Image saved as: {self.image_path}")
                    input.setText(self.image_path)
                    pixmap = QPixmap(self.image_path)
                    if not pixmap.isNull():
                        pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        label.setPixmap(pixmap)
            else:
                input.clear()
                label.clear()



