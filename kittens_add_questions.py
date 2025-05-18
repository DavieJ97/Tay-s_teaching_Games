from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import json
from objects import Button, ComboBox, Label, LineEdit, ToggleSwitch
import os
import shutil

BASEFOLDER = "images/uploaded_image/Kittens"

class SubPageKittens(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = "teacher"
        self.com_checked = False
        self.question_index = 0
        self.setWindowTitle("Subpage - Add questions")
        self.setFixedSize(1375, 700)

        self.get_json()

        # labels
        grade_label = Label("Select the Grade: ", 14)
        lesson_label = Label("Select the Lesson: ", 14)
        self.page_label = Label("_/_", 14)
        question_label = Label("Add an Question or Instructions", 14)
        text_or_img_label = Label("Add Text or an Image", 14)
        answer_label = Label("Add the answer", 14)
        print("made Labels")

        # buttons
        self.add_grade_button = Button(100, 50, text="Add")
        self.add_grade_button.toggle_styleSheet(self.mode)
        self.add_lesson_button = Button(100, 50, text="Add")
        self.add_lesson_button.toggle_styleSheet(self.mode)
        self.del_grade_button = Button(100, 50, text="Delete")
        self.del_grade_button.toggle_styleSheet(self.mode)
        self.del_lesson_button = Button(100, 50, text="Delete")
        self.del_lesson_button.toggle_styleSheet(self.mode)
        self.next_page_button = Button(50, 50, img_path="images/Intro_page_imgs/next.png")
        self.next_page_button.toggle_styleSheet(self.mode)
        self.previous_page_button = Button(50, 50, img_path="images/Intro_page_imgs/left.png")
        self.previous_page_button.toggle_styleSheet(self.mode)
        self.save_button = Button(300, 80, text="Save")
        self.save_button.toggle_styleSheet(self.mode)
        self.close_button = Button(300, 80, text="Close")
        self.close_button.toggle_styleSheet(self.mode)
        print("made Buttons")

        # Comboboxes
        self.grade_box = ComboBox(self.mode)
        self.grade_box.setEditable(True)
        self.lesson_box = ComboBox(self.mode)
        self.lesson_box.setEditable(True)
        print("made Comboboxes")

        # lineedits
        self.question_input = LineEdit()
        self.question_input.setPlaceholderText("Add a question or Instruction here.")
        self.text_or_img_input = LineEdit()
        self.text_or_img_input.setPlaceholderText("Add an additional image or text here.")
        self.answer_input = LineEdit()
        self.answer_input.setPlaceholderText("Add the answer to the question here.")
        print("made Lineedits")

        # switches
        self.image_switch = ToggleSwitch("Choose to select an Image")
        print("made Switch")

        # layouts
        main_layout = QVBoxLayout()
        self.grade_layout = QHBoxLayout()
        self.page_dirc_layout = QHBoxLayout()
        self.text_or_image_layout = QHBoxLayout()
        self.save_layout = QHBoxLayout()
        print("made Layouts")

        # adding widgets to Hlayouts
        self.grade_layout.addWidget(grade_label)
        self.grade_layout.addWidget(self.grade_box)
        self.grade_layout.addWidget(self.add_grade_button)
        self.grade_layout.addWidget(self.del_grade_button)
        self.grade_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.grade_layout.addWidget(lesson_label)
        self.grade_layout.addWidget(self.lesson_box)
        self.grade_layout.addWidget(self.add_lesson_button)
        self.grade_layout.addWidget(self.del_lesson_button)
        

        self.page_dirc_layout.addWidget(self.previous_page_button)
        self.page_dirc_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.page_dirc_layout.addWidget(self.page_label)
        self.page_dirc_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.page_dirc_layout.addWidget(self.next_page_button)

        self.text_or_image_layout.addWidget(self.text_or_img_input)
        self.text_or_image_layout.addWidget(self.image_switch)

        self.save_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.save_layout.addWidget(self.save_button)
        self.save_layout.addWidget(self.close_button)
        self.save_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        print("made mini_layouts")

        # add widgets and layouts to main_layout
        main_layout.addLayout(self.grade_layout)
        main_layout.addLayout(self.page_dirc_layout)
        main_layout.addWidget(question_label)
        main_layout.addWidget(self.question_input)
        main_layout.addWidget(text_or_img_label)
        main_layout.addLayout(self.text_or_image_layout)
        main_layout.addWidget(answer_label)
        main_layout.addWidget(self.answer_input)
        main_layout.addLayout(self.save_layout)

        self.grade_box.addItems(self.data.keys())
        # connect widgets
        self.add_grade_button.clicked.connect(self.add_new_grade)
        self.del_grade_button.clicked.connect(self.delete_grade)
        self.add_lesson_button.clicked.connect(self.add_new_lesson)
        self.del_lesson_button.clicked.connect(self.delete_lesson)
        self.save_button.clicked.connect(self.add_new_word)
        self.close_button.clicked.connect(self.close)
        self.grade_box.currentTextChanged.connect(self.update_lessons)
        self.lesson_box.currentTextChanged.connect(self.display_words)
        self.next_page_button.clicked.connect(self.next_page)
        self.previous_page_button.clicked.connect(self.pervious_page)
        self.image_switch.stateChanged.connect(self.toggle_input)
        self.setLayout(main_layout)
        self.update_lessons()

    def get_json(self):
        json_file = "Exploding_kittens/assets/json/questions.json"
        with open(json_file, "r", encoding="utf-8") as file:
            self.data = json.load(file)
    
    def save_json(self):
        """ Saves the current data dictionary back to JSON file """
        json_file = "Exploding_kittens/assets/json/questions.json"
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def update_lessons(self):
        """ Updates the lessons dropdown based on selected grade """
        selected_grade = self.grade_box.currentText()
        self.lesson_box.clear()
        print("running")
        if selected_grade in self.data:
            self.lesson_box.addItems(self.data[selected_grade].keys())

    def display_words(self):
        """Displays words from the selected grade and lesson"""
        selected_grade = self.grade_box.currentText()
        selected_lesson = self.lesson_box.currentText()
        if not selected_grade or not selected_lesson:
            return

        print("Counting questions...")
        questions = self.data.get(selected_grade, {}).get(selected_lesson, [])
        if not questions:
            self.page_label.setText("0/0")
            self.question_input.clear()
            self.text_or_img_input.clear()
            self.answer_input.clear()
            self.image_switch.setChecked(False)
            return

        numberofquestions = len(questions)
        self.page_label.setText(f"{(self.question_index)+1}/{numberofquestions}")
        if self.question_index >= numberofquestions:
            self.question_index = 0

        mini_dict = questions[self.question_index]

        self.question_input.setText(mini_dict.get("Instructions", ""))
        self.text_or_img_input.setText(mini_dict.get("Question", ""))
        self.answer_input.setText(mini_dict.get("Answer", ""))
        word = mini_dict.get("Question", "")
        if word.endswith(".png") or word.endswith(".jpg") or word.endswith(".jpeg"):
            self.com_checked = True
            self.image_switch.setChecked(True)
            self.com_checked = False
        else:
            self.com_checked = True
            self.image_switch.setChecked(False)
            self.com_checked = False
        

    def add_new_grade(self):
        """ Adds a new grade if it does not exist """
        new_grade = self.grade_box.currentText().strip()
        if new_grade and new_grade not in self.data:
            confirmation = QMessageBox.question(
                self, "Add New Grade", f"Are you sure you want to add a new grade '{new_grade}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.data[new_grade] = {}  # Create an empty lessons dictionary
                self.update_lessons()
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
        selected_grade = self.grade_box.currentText().strip()
        new_lesson = self.lesson_box.currentText().strip()
        if selected_grade in self.data and new_lesson and new_lesson not in self.data[selected_grade]:
            confirmation = QMessageBox.question(
                self, "Add New Lesson", f"Are you sure you want to add a new lesson '{new_lesson}' to Grade '{selected_grade}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.data[selected_grade][new_lesson] = []  # Create an empty word list
                for _ in range(27):
                    mini_dict ={}
                    mini_dict["Instructions"] = ""
                    mini_dict["Question"] = ""
                    mini_dict["Answer"] = ""
                    self.data[selected_grade][new_lesson].append(mini_dict)
                self.save_json()
                self.display_words()
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
        """Adds or updates a question for the selected grade and lesson"""
        selected_grade = self.grade_box.currentText().strip()
        selected_lesson = self.lesson_box.currentText().strip()
        
        if not selected_grade or not selected_lesson:
            QMessageBox.warning(self, "Missing Selection", "Please select both a grade and a lesson.")
            return

        instructions = self.question_input.text().strip()
        question = self.text_or_img_input.text().strip()
        answer = self.answer_input.text().strip()

        # 🛠 Ensure the grade and lesson exist
        if selected_grade not in self.data:
            self.data[selected_grade] = {}
        if selected_lesson not in self.data[selected_grade]:
            self.data[selected_grade][selected_lesson] = []

        # 🧠 Either update existing question or append a new one
        if self.question_index < len(self.data[selected_grade][selected_lesson]):
            # Update existing
            # mini_dict = self.data[selected_grade][selected_lesson][self.question_index]
            self.data[selected_grade][selected_lesson][self.question_index]["Instructions"] = instructions
            self.data[selected_grade][selected_lesson][self.question_index]["Question"] = question
            self.data[selected_grade][selected_lesson][self.question_index]["Answer"] = answer

        self.save_json()
        print(self.data[selected_grade][selected_lesson][self.question_index]["Question"])
        self.display_words()

    def delete_grade(self):
        """ Deletes the selected grade and its lessons """
        selected_grade = self.grade_box.currentText().strip()
        if selected_grade in self.data:
            confirmation = QMessageBox.question(
                self, "Delete Grade", f"Are you sure you want to delete grade '{selected_grade}' and all its lessons?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                del self.data[selected_grade]
                self.save_json()
                self.grade_box.clear()
                self.grade_box.addItems(self.data.keys())  # Refresh dropdown
                self.lesson_box.clear()
                self.display_words()

    def delete_lesson(self):
        """ Deletes the selected lesson from the selected grade """
        selected_grade = self.grade_box.currentText().strip()
        selected_lesson = self.lesson_box.currentText().strip()

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

    def next_page(self):
        selected_grade = self.grade_box.currentText().strip()
        selected_lesson = self.lesson_box.currentText().strip()

        if (self.question_index)+1 == len(self.data[selected_grade][selected_lesson]):
            self.question_index = 0
        else:
            self.question_index += 1
        self.display_words()
    
    def pervious_page(self):
        selected_grade = self.grade_box.currentText().strip()
        selected_lesson = self.lesson_box.currentText().strip()

        if (self.question_index)+1 == 1:
            self.question_index = len(self.data[selected_grade][selected_lesson])-1
        else:
            self.question_index -= 1
        self.display_words()

    def toggle_input(self):
        if not self.com_checked:
            grade = self.grade_box.currentText().strip()
            lesson = self.lesson_box.currentText().strip()
            image_folder = os.path.join(os.path.dirname(__file__), BASEFOLDER, f"Grade {grade} Lesson {lesson}")
            os.makedirs(image_folder, exist_ok=True)
            if self.image_switch.isChecked():
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
                    self.text_or_img_input.setText(self.image_path)
                    
            else:
                self.text_or_img_input.clear()

