from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, QWidget, QVBoxLayout, QDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from pirate_add_words import SubPagePirate
from kittens_add_questions import SubPageKittens
from show_dialoge import GameStartDialog
from Pirates_of_the_classroom.game import play_pirate_game
from Exploding_kittens.game import play_kitten_game
from objects import Button, ToggleSwitch, ScrollArea, Label

class TeachingGamesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = "normal"
        self.function_list = [
                self.pirate_button_clicked,  # Function reference
                self.kitten_button_clicked,
                lambda: print("Speaking Game"),
                lambda: print("Writing Game"),
                lambda: print("Teacher's Page"),
                lambda: print("About Page")
                ]
        self.setWindowTitle("Tay's Teaching Games")
        self.setFixedSize(1375, 700)  # Set initial window size
        self.setWindowIcon(QIcon("images\Intro_page_imgs\TTG _icon2.png"))


         # Main layout (Inside Scroll Area)
        main_widget = QWidget()
        main_layout = QVBoxLayout()  # Holds everything

        # Load and Set Fixed Image
        self.image_label = QLabel(self)
        self.pixmap = QPixmap("images\Intro_page_imgs\Tays_Teaching_Games_Intro2.png")

        if not self.pixmap.isNull():
            self.pixmap = self.pixmap.scaled(1200, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Fixed size
            self.image_label.setPixmap(self.pixmap)

        self.image_label.setFixedSize(1200, 300)
        main_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Grid Layout for Buttons
        button_grid = QGridLayout()

        self.buttons = []
        
        image_paths = [
            "images\Intro_page_imgs\TTG_Pirates_of_the_classroom.png",
            "images\Intro_page_imgs\TTG_Exploding_kittens.png",
            "images\Intro_page_imgs\TTG_Pokemon_shuffle.png",
            "images\Intro_page_imgs\TTG_spots_and_spiderwebs.png",
            "images\Intro_page_imgs\TTG_Teachers_Page.png",
            "images\Intro_page_imgs\TTG_About.png",
        ]

        for i, img_path in enumerate(image_paths):
            btn = Button(400, 200, img_path)
            self.buttons.append(btn)

        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda checked, num = i: self.function_list[num]())
            btn.toggle_styleSheet(self.mode)

        for i, btn in enumerate(self.buttons):
            button_grid.addWidget(btn, i // 3, i % 3)  # 3 buttons per row
           
        # Toggle switch (styled checkbox)
        self.toggle_switch = ToggleSwitch("Change to Teacher Mode")
        dedication_label = Label("Made by Dawid De Lange", 11)
        
        self.toggle_switch.stateChanged.connect(self.toggle_mode)
        main_layout.addLayout(button_grid)

        main_layout.addWidget(self.toggle_switch, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(dedication_label, alignment=Qt.AlignmentFlag.AlignRight)

        # Set layout for the main widget
        main_widget.setLayout(main_layout)

        # Scroll Area
        scroll_area = ScrollArea()
        scroll_area.setWidget(main_widget)
        scroll_area.setWidgetResizable(True)  # Allows scrolling when needed

        # Final Layout
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.update_ui()
        self.setLayout(layout)

    def update_ui(self):
        if self.mode == "normal":
            # Set background color
            self.setStyleSheet("background-color: #9ccdc2;")
            
        elif self.mode == "teacher":
            self.setStyleSheet("background-color: grey;")

        for btn in self.buttons:
            btn.toggle_styleSheet(self.mode)

    def toggle_mode(self):
        if self.toggle_switch.isChecked():
            self.mode = 'teacher'
        else:
            self.mode = 'normal'
        self.update_ui()

    def pirate_button_clicked(self):
        if self.mode == "normal":
            self.game("pirate")
        elif self.mode == "teacher":
            self.open_subpage("pirate")

    def kitten_button_clicked(self):
        if self.mode == "normal":
            self.game("kittens")
        elif self.mode == "teacher":
            self.open_subpage("kittens")

    def game(self, game):
        dialog = GameStartDialog(game)
        result = dialog.exec()  # Shows the dialog and waits for user response

        if result == QDialog.DialogCode.Accepted:
            selected_grade, selected_lesson = dialog.get_selection()
            if game == "pirate":
                print(f"Starting game with: Grade {selected_grade}, Lesson {selected_lesson}")
                play_pirate_game(selected_grade, selected_lesson)
            else:
                print(f"Starting game with: Grade {selected_grade}, Lesson {selected_lesson}")
                play_kitten_game(selected_grade, selected_lesson)
    
    def open_subpage(self, game):
        if game == "pirate":
            self.sub_page = SubPagePirate()
            self.sub_page.showMaximized()
            self.sub_page.show()
        elif game == "kittens":
            self.sub_page = SubPageKittens()
            self.sub_page.showMaximized()
            self.sub_page.show()

# Run App
app = QApplication([])
window = TeachingGamesApp()
window.showMaximized()
app.exec()
# This app I want to dedicate to God Who made it possible. Without His help I would not have gotten so far.