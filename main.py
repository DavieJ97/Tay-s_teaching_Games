from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout, QScrollArea, QDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from add_words import SubPage
from show_dialoge import GameStartDialog
from Pirates_of_the_classroom.game import play_game

class TeachingGamesApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tay's Teaching Games")
        self.setFixedSize(1375, 700)  # Set initial window size
        # Set background color
        self.setStyleSheet("background-color: #9ccdc2;")

         # Main layout (Inside Scroll Area)
        main_widget = QWidget()
        main_layout = QVBoxLayout()  # Holds everything

        # Load and Set Fixed Image
        self.image_label = QLabel(self)
        self.pixmap = QPixmap("images\Intro_page_imgs\Tays_Teaching_Games_Intro.png")

        if not self.pixmap.isNull():
            self.pixmap = self.pixmap.scaled(800, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Fixed size
            self.image_label.setPixmap(self.pixmap)

        self.image_label.setFixedSize(800, 300)
        main_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Grid Layout for Buttons
        button_grid = QGridLayout()

        buttons = []
        function_list = [
            self.game,  # Function reference
            lambda: print("Review Game"),  # Wrap `print()` in a lambda to delay execution
            lambda: print("Speaking Game"),
            lambda: print("Writing Game"),
            self.open_subpage,
            lambda: print("About Page")
            ]
        image_paths = [
            "images\Intro_page_imgs\TTG_reading_button_img.png",
            "images\Intro_page_imgs\TTG_review_button_img.png",
            "images\Intro_page_imgs\TTG_speaking_button_img.png",
            "images\Intro_page_imgs\TTG_writing_button_img.png",
            "images\Intro_page_imgs\TTG_Teachers_Page.png",
            "images\Intro_page_imgs\TTG_About.png",
        ]

        for i, img_path in enumerate(image_paths):
            btn = QPushButton()
            btn.setFixedSize(200, 200)  # Set button size
            btn.setIcon(QIcon(img_path))  # Set icon
            btn.setIconSize(QSize(170, 170))  # Adjust icon size
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 25px;  /* Round edges */
                    border: 2px solid #b3ebde; /* Blue border */
                    background-color: #b3ebde; /* Light blue background */
                    color: white; /* White text */
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #3399FF; /* Darker blue on hover */
                }
                QPushButton:pressed {
                    background-color: #0056b3; /* Even darker on click */
                }
            """)
            btn.clicked.connect(lambda checked, num = i: function_list[num]())
            buttons.append(btn)


        for i, btn in enumerate(buttons):
            button_grid.addWidget(btn, i // 3, i % 3)  # 3 buttons per row
           


        main_layout.addLayout(button_grid)

        # Set layout for the main widget
        main_widget.setLayout(main_layout)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidget(main_widget)
        scroll_area.setWidgetResizable(True)  # Allows scrolling when needed

        # Final Layout
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def game(self):
        dialog = GameStartDialog()
        result = dialog.exec()  # Shows the dialog and waits for user response

        if result == QDialog.DialogCode.Accepted:
            selected_grade, selected_lesson = dialog.get_selection()
            print(f"Starting game with: Grade {selected_grade}, Lesson {selected_lesson}")
            play_game(selected_grade, selected_lesson)
    
    def open_subpage(self):
        self.sub_page = SubPage()
        self.sub_page.showMaximized()
        self.sub_page.show()

# Run App
app = QApplication([])
window = TeachingGamesApp()
window.showMaximized()
app.exec()