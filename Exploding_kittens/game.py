import pygame
import random
import json
from Exploding_kittens.objectKittens import Image, Box, Text, Sound
import traceback
import sys
import os

class Game:
    def __init__(self, grade, lesson):
        info = pygame.display.Info()
        self.isRunning = True
        self.active = True
        self.moving = False
        self.change_size = False
        self.shaking = False
        self.demo = False
        self.grade = f"{grade}"
        self.lesson = f"{lesson}"
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.grey = (211, 211, 211)
        self.page = "intro"
        self.font_url = "Exploding_kittens/assets/font/Boldonse-Regular.ttf"
        self.abc_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X"]
        self.numOfTeams = 1
        self.turn = 0
        self.max_size = 0
        self.shake_dif = 0
        self.width, self.height = info.current_w, info.current_h  # Get screen resolution
        print(f"{self.width}, {self.height}")
        self.font_size = self.width//20
        self.game_window = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        pygame.mixer.music.load("Exploding_kittens/assets/audio/Battle Theme - Kitty Letter Music EXTENDED (Exploding Kittens Inc & The Oatmeal).mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        with open("Exploding_kittens/assets/json/questions.json", "r") as file:
            data = json.load(file)
        self.data = data[self.grade][self.lesson]
        self.json_i = 0
        self.create_intro_objects()
        self.make_random_lists()

    def make_random_lists(self, card_list:bool = False):
        if not card_list:
            self.random_chance_list = []
            self.random_chance_list = [random.randint(1, 5) for _ in range(25)]
        elif card_list:
            self.random_card_list = []
            i = 1
            make_num = True
            while make_num: 
                random_num = random.randint(0, 6)
                if i < 3:
                    if random_num != 0 and random_num != 6:
                        self.random_card_list.append(random_num)
                        i +=1 
                else:
                    self.random_card_list.append(random_num) 
                    if random_num in (0, 6):
                        make_num = False 
                    i+=1       
    # Demo run
    def demo_run(self):
        self.demo = True
        self.demo_teams = 2
        self.demo_page = "demo_main"
        self.demo_letter_list = ["A","B","C","D"]
        self.demo_instruction = "Unscramble the word"
        self.demo_question = "llohe"
        self.demo_answer = "Hello"
        self.demo_random_card_list1 = [1,2,3,4,5,0]
        self.demo_random_card_list2 = [1,2,3,4,5,6]
        self.demo_random_card_list = self.demo_random_card_list1
        self.demo_random_chance_list = [1, 1, 2, 5, 5]
        self.demo_random_num1 = 1
        self.demo_random_num2 = 2
        self.demo_random_num = self.demo_random_num1

    # Intro Functions
    def create_intro_objects(self):
        self.intro_background = Image(self.game_window, 0, 0, "Exploding_kittens/assets/images/Intro_image.png", self.width, self.height)
        self.exit_button = Image(self.game_window, self.width*0.007, self.height-(self.height*.104), "Exploding_kittens/assets/images/incorrect_button.png", self.width*.06, self.height*.09)
        self.choose_teams_box = Image(self.game_window, self.width*0.073, self.height - (self.height*.13), "Exploding_kittens/assets/images/answer_bar.png", self.width - (self.width*.13),self.height*.13, text= f"How many teams will play?: {self.numOfTeams}", fontUrl=self.font_url, text_size= int(self.width*.029), text_color=self.white)
        self.continue_button = Image(self.game_window, self.width - (self.width*.065), self.height -(self.height*.104), "Exploding_kittens/assets/images/correct_button.png", self.width*.06, self.height*.09)
        self.click_sound  = Sound("Exploding_kittens/assets/audio/button-202966.mp3")
        self.card_swip = Sound("Exploding_kittens/assets/audio/wind-swoosh-short-289744.mp3")
        self.oh_no_sound = Sound("Exploding_kittens/assets/audio/Oh No (Instrumental) - Kreepa(cut edition).mp3")
        self.dan_dan_dan_sound = Sound("Exploding_kittens/assets/audio/Dan Dan Dannnnnnnn!!! Sound Effect.mp3")
        self.explotion_sound = Sound("Exploding_kittens/assets/audio/medium-explosion-cat.mp3")

    def draw_intro_objects(self):
        self.intro_background.draw_image()
        self.exit_button.draw_image()
        self.choose_teams_box.draw_image(with_text=True)
        self.continue_button.draw_image()
    
    def change_txt_intro(self):
        self.choose_teams_box.innit_text(text= f"How many teams will play?: {self.numOfTeams}", text_color=self.white)

    def make_score_for_team(self):
        self.teamScores = []
        teams = self.demo_teams if self.demo else self.numOfTeams
        self.teamScores = [0] * teams

    def make_question(self):
        self.instruction = self.data[self.json_i]["Instructions"] if not self.demo else self.demo_instruction
        self.question = self.data[self.json_i]["Question"] if not self.demo else self.demo_question
        self.answer = self.data[self.json_i]["Answer"] if not self.demo else self.demo_answer
        self.json_i += not self.demo 

    # Main Functions
    def create_main_objects(self):
        if not self.demo:
            self.background = Image(self.game_window, 0, 0, "Exploding_kittens/assets/images/main_background.png", self.width, self.height)
            self.tag = Image(self.game_window, 0, 0, "Exploding_kittens/assets/images/Choose_a_letter_tag.png", self.width, self.height*.13, text="Choose a letter", fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.black)
        else:
            self.background = Image(self.game_window, 0, 0, "Exploding_kittens/assets/images/main_background.png", self.width, self.height, text="EXAMPLE", fontUrl=self.font_url, text_size=int(self.width*.11), text_color=self.grey)
            self.tag = Image(self.game_window, 0, 0, "Exploding_kittens/assets/images/Choose_a_letter_tag.png", self.width, self.height*.13, text="This is an example to show how the game works.", fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.black)
        self.make_letter_boxes()
        self.make_score_planks()
        
    def draw_main_objets(self):
        self.background.draw_image() if not self.demo else self.background.draw_image(with_text=True)
        self.tag.draw_image(with_text=True)
        self.exit_button.draw_image()
        for box in self.letter_box_list:
            box.draw_image(with_text=True)
        for plank in self.team_box_list:
            plank.draw_image(with_text=True)

    def make_letter_boxes(self):
        self.letter_box_list = []
        position_x, position_y = self.width*.043, self.height*.138
        spaceing_x, spaceing_y = self.width*.11, self.height*.195
        list = self.demo_letter_list if self.demo else self.abc_list
        for i, letter in enumerate(list):
            if i == 5 or i == 11 or i == 17:
                self.letter_box_list.append(Image(self.game_window, position_x, position_y, "Exploding_kittens/assets/images/letter_block.png", self.width*.102, self.height*.182, text=letter, fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.white))
                position_x = self.width*.043
                position_y += spaceing_y
            else:
                self.letter_box_list.append(Image(self.game_window, position_x, position_y, "Exploding_kittens/assets/images/letter_block.png", self.width*.102, self.height*.182, text=letter, fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.white))
                position_x += spaceing_x
        
    def make_score_planks(self):
        self.team_box_list = []
        x, y = self.width - (self.width*.278), self.height*.143
        spacing_y = self.height*.143
        teams = self.demo_teams if self.demo else self.numOfTeams
        for i in range(0, teams):
            if i == 0:
                self.team_box_list.append(Image(self.game_window, x, y, "Exploding_kittens/assets/images/Score_plank.png", self.width*.26, self.height*.13, text=f"Team {i+1}: {self.teamScores[i]}", fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.white))
            else:
                self.team_box_list.append(Image(self.game_window, x, y, "Exploding_kittens/assets/images/Score_plank.png", self.width*.26, self.height*.13, text=f"Team {i+1}: {self.teamScores[i]}", fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.black))
            y += spacing_y
    
    def update_scorebord(self):
        for i, plank in enumerate(self.team_box_list):
            if i == self.turn:
                plank.innit_text(text= f"Team {i+1}: {self.teamScores[i]}", text_color=self.white)
            else:
                plank.innit_text(text= f"Team {i+1}: {self.teamScores[i]}", text_color=self.black)
    
    def change_turn(self):
        teams = self.demo_teams if self.demo else self.numOfTeams
        if self.turn == teams-1:
            self.turn = 0
        else:
            self.turn += 1

    # Question Functions
    def create_question_objects(self):
        self.make_question()
        self.question_background = Image(self.game_window, 0, 0, "Exploding_kittens/assets/images/question_background.png", self.width, self.height)
        if self.is_image_path(self.question):
            path = self.resource_path(self.question)
            self.question_box = Image(self.game_window, self.width*.073, self.height*.09, "Exploding_kittens/assets/images/question_box.png", self.width-(self.width*.146), self.height-(self.height*.13), False)
            self.over_image = Image(self.game_window, self.width*.5, self.height*.5, path, (self.width-(self.width*.146))-100, (self.height-(self.height*.13))-100, True)
        else:
            self.question_box = Image(self.game_window, self.width*.073, self.height*.09, "Exploding_kittens/assets/images/question_box.png", self.width-(self.width*.146), self.height-(self.height*.13), False, text=f"{self.question}", fontUrl=self.font_url, text_size=int(self.width*.0366), text_color=self.grey)
        self.top_instructions = Image(self.game_window, self.width*.037, self.height*.052, "Exploding_kittens/assets/images/Top_instructions.png", self.width-(self.width*.073), self.height*.13, False, text=f"{self.instruction}", fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.white)
        self.answer_bar = Image(self.game_window, self.width*.11, self.height-(self.height*.13), "Exploding_kittens/assets/images/answer_bar.png", self.width-(self.width*.22), self.height*.13, False, text=f"{self.answer}", fontUrl=self.font_url, text_size=int(self.width*.029), text_color=self.white)
        self.incorrect_button = Image(self.game_window, self.width*.0073, self.height-(self.height*.104), "Exploding_kittens/assets/images/incorrect_button.png", self.width*.061, self.height*.091)
        self.correct_button = Image(self.game_window, self.width - (self.width*.066), self.height-(self.height*.104), "Exploding_kittens/assets/images/correct_button.png", self.width*.061, self.height*.091)
        self.correct_sound = Sound("Exploding_kittens/assets/audio/correct-6033.mp3")
        self.tada_sound = Sound("Exploding_kittens/assets/audio/tada-military-3-183975.mp3")

    def draw_question_objects(self):
        self.question_background.draw_image()
        if self.is_image_path(self.question):
            self.question_box.draw_image()
            self.over_image.draw_image()
        else:
            self.question_box.draw_image(with_text=True)
        self.top_instructions.draw_image(with_text=True)
        self.incorrect_button.draw_image()
        if self.show_answer:
            self.answer_bar.draw_image(with_text=True)
            self.correct_button.draw_image()

    def is_image_path(self, string):
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
        return string.lower().endswith(image_extensions)

    # Reward Functions
    def create_reward_objects(self):
        self.back_button = Image(self.game_window, self.width - (self.width*.066), self.height - (self.height*.104), "Exploding_kittens/assets/images/back_button.png", self.width*.061, self.height*.0911)
        random_chance_list = self.random_chance_list if not self.demo else self.demo_random_chance_list
        if random_chance_list[0] != 5:
            self.make_cards_list_objects()
            self.score_label = Text(self.game_window, self.width*.5, (self.height*.5)-(self.height*.195), "Total Points:", self.font_url, int(self.width*.0366), self.white)
            self.temp_score_text = Text(self.game_window, (self.width*.5)+(self.width*.073), self.height*.5, f"{self.temp_score}", self.font_url, int(self.width*.073), self.white, self.red, self.yellow)
            self.stop_button = Box(self.game_window, self.width*.5, (self.height*.5)+(self.height*.26), self.width*.22, self.height*.13, self.red, "STOP", self.font_url, int(self.width*.0366), self.white, True)
        elif random_chance_list[0] == 5:
            self.make_special_card_list_objects()
            self.P5_label = Text(self.game_window, self.width*.5, (self.height*.5)-(self.height*.22), "Take 5 Points", self.font_url, int(self.width*.0366), self.white)
            self.or_label = Text(self.game_window, (self.width*.5)+(self.width*.073), (self.height*.5)-(self.height*.091), "OR", self.font_url, int(self.width*.073), self.white, self.red, self.yellow)
            self.show_label = Text(self.game_window, self.width*.5, (self.height*.5)+(self.height*.182), "Show the card", self.font_url, int(self.width*.0366), self.white)

    def make_special_card_list_objects(self):
        self.random_num = random.randint(1,2) if not self.demo else self.demo_random_num
        self.card_list = []
        if self.random_num == 1:
            self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/special_cards/change.png", self.width*.226, self.height*.546, True))
        elif self.random_num == 2:
            self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/special_cards/Lose_all.png", self.width*.226, self.height*.546, True))
        self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/back_of_card.png", self.width*.226, self.height*.546, True))

    def make_cards_list_objects(self):
        self.card_list = []
        random_card_list = self.random_card_list if not self.demo else self.demo_random_card_list
        for num in random_card_list:
            if num == 1:
                self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/normal_cards/+1.png", self.width*.226, self.height*.546, True))
            elif num == 2:
                self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/normal_cards/+2.png", self.width*.226, self.height*.546, True))
            elif num == 3:
                self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/normal_cards/+3.png", self.width*.226, self.height*.546, True))
            elif num == 4:
                self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/normal_cards/+4.png", self.width*.226, self.height*.546, True))
            elif num == 5:
                self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/normal_cards/+5.png", self.width*.226, self.height*.546, True))
            elif num == 0:
                self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/normal_cards/bomb.png", self.width*.226, self.height*.546, True))
            elif num == 6:
                self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/normal_cards/nuclear.png", self.width*.226, self.height*.546, True))
        self.card_list.reverse()
        reversed_list = random_card_list[::-1]
        if self.demo:
            self.demo_random_card_list = reversed_list
        else:
            self.random_card_list = reversed_list
        self.card_list.append(Image(self.game_window, self.width*.25, self.height*.5, "Exploding_kittens/assets/images/cards/back_of_card.png", self.width*.226, self.height*.546, True))

    def draw_reward_objects(self):
        self.question_background.draw_image()
        self.back_button.draw_image()
        random_chance_list = self.random_chance_list if not self.demo else self.demo_random_chance_list
        if random_chance_list[0] != 5:
            for card in self.card_list:
                self.move_card(card)
            self.score_label.draw_text()
            self.temp_score_text.draw_text(True)
            self.stop_button.draw_box(True)
        elif random_chance_list[0] == 5:
            for card in self.card_list:
                self.move_card(card)
            if not self.change_card and self.random_num == 1:
                for plank in self.team_box_list:
                    plank.draw_image(with_text=True)
            else:
                self.P5_label.draw_text()
                self.or_label.draw_text(True)
                self.show_label.draw_text()
                
    def change_score_label(self):
        self.temp_score_text.innit_text(f"{self.temp_score}", self.white, self.red, self.yellow)

    def show_total_score(self):
        random_card_list = self.random_card_list if not self.demo else self.demo_random_card_list
        total_points = self.temp_score
        for points in random_card_list:
            if points != 0 or points != 6:
                total_points += points
        self.stop_button.change_text(f"{total_points}", self.white)
        self.change_card = False

    def move_card(self, card):
        if self.moving and card == self.card_list[-1]:
            x = card.x
            y = card.y
            x -= 60
            card.draw_image(x = x, y = y)
            if x <=  0:
                self.card_list.remove(card)
                self.moving = False
        elif self.change_size:
            size_x = card.size_x
            size_y = card.size_y
            size_x += 5
            size_y += 5
            card.scale_img(size_x, size_y)
            card.draw_image() 
            self.max_size -= 1
            if self.max_size <= 0:
                self.change_size = False
        elif self.shaking:
            if self.shake_dif % 2 == 0:
                card.rotate_image(8)
                card.draw_image()
            else:
                card.rotate_image(-8)
                card.draw_image()
            self.shake_dif -= 1
            if self.shake_dif <= 0:
                self.shaking = False
        else:
            card.draw_image()
    
    # Event Functions
    def intro_event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_sound.play_sound()
                exit_button_rect = self.exit_button.get_rectangle()
                con_button_rect = self.continue_button.get_rectangle()
                if exit_button_rect.collidepoint(event.pos):
                    self.isRunning = False
                    return
                elif con_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.set_volume(0.1)
                    self.active = False
                    self.demo = True
                    self.demo_run()
                    self.make_score_for_team()
                    self.create_main_objects()
                    return                
            if self.active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    self.click_sound.play_sound()
                    pygame.mixer.music.set_volume(0.1)
                    self.active = False
                    self.demo = True
                    self.demo_run()
                    self.make_score_for_team()
                    self.create_main_objects()
                    return
                elif event.key == pygame.K_BACKSPACE:  # Backspace key
                    self.click_sound.play_sound()
                    self.numOfTeams = 1
                    self.change_txt_intro()
                    return
                elif pygame.K_0 < event.key < pygame.K_7:  # Check for number keys
                    self.click_sound.play_sound()
                    self.numOfTeams = int(event.unicode)
                    self.change_txt_intro()
                    return
                
    def main_event_listener(self):
        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_sound.play_sound()
                button_rect = self.exit_button.get_rectangle()
                if button_rect.collidepoint(event.pos):
                    if not self.demo:
                        self.isRunning = False 
                    else:
                        self.page = "main"
                        self.demo = False
                        self.make_score_for_team()
                        self.create_main_objects()
                    return 
                for box in self.letter_box_list:
                    box_rect = box.get_rectangle()
                    if box_rect.collidepoint(event.pos):
                        self.create_question_objects()
                        self.show_answer = False
                        self.letter_box_list.remove(box)
                        if not self.demo:
                            self.page = "question" 
                        else: 
                            self.demo_page ="demo_question"
                        return
    
    def question_event_listener(self):
        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_sound.play_sound()
                wrong_button_rect = self.incorrect_button.get_rectangle()
                right_button_rect = self.correct_button.get_rectangle()
                if wrong_button_rect.collidepoint(event.pos):
                    self.change_turn()
                    self.update_scorebord()
                    if not self.demo:
                        self.page = "main"
                    else:
                        self.demo_page = "demo_main"
                    return
                elif right_button_rect.collidepoint(event.pos):
                    self.change_card = True
                    self.temp_score = 0
                    if not self.demo:
                        self.random_chance_list.pop(0)
                        self.make_random_lists(True)
                        self.create_reward_objects()
                        self.page = "reward"
                    else:
                        self.demo_random_chance_list.pop(0)
                        self.create_reward_objects()
                        self.demo_page = "demo_reward" 
                else:
                    if not self.show_answer:
                        self.correct_sound.play_sound()
                        self.show_answer = True

    def reward_event_listener(self):
        for event in pygame.event.get():
            random_chance_list = self.random_chance_list if not self.demo else self.demo_random_chance_list
            random_card_list = self.random_card_list if not self.demo else self.demo_random_card_list
            teams = self.numOfTeams if not self.demo else self.demo_teams
            if random_chance_list[0] != 5:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_rect = self.back_button.get_rectangle()
                    top_card = self.card_list[-1]
                    card_rect = top_card.get_rectangle()
                    stop_rect = self.stop_button.check_collide(event.pos)
                    if button_rect.collidepoint(event.pos):
                        self.click_sound.play_sound()
                        self.teamScores[self.turn] += self.temp_score
                        self.change_turn()
                        self.update_scorebord()
                        if not self.demo:
                            self.page = "main"
                        else: 
                            self.demo_page = "demo_main"
                            self.demo_random_card_list = self.demo_random_card_list2
                        return
                    elif self.change_card and card_rect.collidepoint(event.pos):
                        self.card_swip.play_sound()
                        self.moving = True
                        self.temp_score += random_card_list[-1]
                        if random_card_list[-1] == 0:
                            self.change_card = False
                            self.temp_score = 0
                            self.explotion_sound.play_sound()
                            self.shaking = True
                            self.shake_dif = 8
                        elif random_card_list[-1] == 6:
                            self.change_card = False
                            self.temp_score = 0
                            self.dan_dan_dan_sound.play_sound()
                            self.max_size = 18
                            self.change_size = True
                            for i in range(0, teams):
                                self.teamScores[i] = 0
                        self.random_card_list.pop(-1) if not self.demo else self.demo_random_card_list.pop(-1)
                        self.change_score_label()
                        return
                    elif stop_rect:
                        self.click_sound.play_sound()
                        self.show_total_score()
            elif random_chance_list[0] == 5:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_rect = self.back_button.get_rectangle()
                    top_card = self.card_list[-1]
                    card_rect = top_card.get_rectangle()
                    P5_text_rect = self.P5_label.get_rectangle()
                    if button_rect.collidepoint(event.pos) and self.change_card:
                        self.click_sound.play_sound()
                        if self.change_card:
                            self.temp_score = 5
                        self.teamScores[self.turn] += self.temp_score
                        self.change_turn()
                        self.update_scorebord()
                        if not self.demo:
                            self.page = "main"
                        else:
                            self.demo_page = "demo_main"
                            self.demo_random_num = self.demo_random_num2
                        return
                    elif button_rect.collidepoint(event.pos) and not self.change_card:
                        self.click_sound.play_sound()
                        self.change_turn()
                        self.update_scorebord()
                        if not self.demo:
                            self.page = "main"
                        else:
                            self.demo_page = "demo_main"
                            self.demo_random_num = self.demo_random_num2
                        return
                    elif self.change_card and card_rect.collidepoint(event.pos):
                        self.moving = True
                        self.change_card = False
                        if self.random_num == 2:
                            self.teamScores[self.turn] = 0
                            self.oh_no_sound.play_sound()
                        else:
                            self.tada_sound.play_sound()
                        return
                    elif not self.change_card and self.random_num == 1:
                        for i, plank in enumerate(self.team_box_list):
                            if i != self.turn:
                                plank_rect = plank.get_rectangle()
                                if plank_rect.collidepoint(event.pos):
                                    newscore = self.teamScores[i]
                                    oldscore = self.teamScores[self.turn]
                                    self.teamScores[i] = oldscore
                                    self.teamScores[self.turn] = newscore
                                    self.change_turn()
                                    self.update_scorebord()
                                    if not self.demo:
                                        self.page = "main"
                                    else:
                                        self.demo_page = "demo_main"
                                        self.demo_random_num = self.demo_random_num2
                                    return
                    elif P5_text_rect.collidepoint(event.pos):
                        self.click_sound.play_sound()
                        self.moving = True

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            base_path = os.path.dirname(sys.executable)  # PyInstaller builds
        except AttributeError:
            base_path = os.path.dirname(sys.argv[0])  # Folder containing the main script or executable
            print("Root path:", os.path.dirname(sys.argv[0]))

        return os.path.join(base_path, relative_path)

    def main_loop(self):
        while self.isRunning:
            if self.page == "intro":
                if not self.demo:
                    self.intro_event_listener()
                    self.draw_intro_objects()
                else:
                    if self.demo_page == "demo_main":
                        self.main_event_listener()
                        self.draw_main_objets()
                    elif self.demo_page == "demo_question":
                        self.question_event_listener()
                        self.draw_question_objects()
                    elif self.demo_page == "demo_reward":
                        self.reward_event_listener()
                        self.draw_reward_objects()
            elif self.page == "main":
                self.main_event_listener()
                self.draw_main_objets()
            elif self.page == "question":
                self.question_event_listener()
                self.draw_question_objects()
            elif self.page == "reward":
                self.reward_event_listener()
                self.draw_reward_objects()
            pygame.display.update()
            self.clock.tick(60)

def play_kitten_game(grade, lesson):
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        with open("error_log.txt", "a") as f:
            f.write("Mixer init failed:\n")
            f.write(traceback.format_exc())
    game = Game(grade, lesson)
    game.main_loop()
    pygame.quit()

# This Game I want to dedicate to God Who made it possible. Without His help I would not have gotten so far.