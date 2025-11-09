import pygame
import random
import json
from objectSandS import Image, Sound, Box, Text
import traceback
import sys
import os
import copy


class Game:
    def __init__(self, grade, lesson):
        info = pygame.display.Info()
        self.isRunning = True
        self.active = True
        self.moving = False
        self.changing_size = False
        self.demo = False
        self.teamsHaveChoosen = False
        self.grade = f"{grade}"
        self.lesson = f"{lesson}"
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.grey = (211, 211, 211)
        self.page = "intro"
        self.main_font_url_black = "Spots_and_spiders/assets/font/komika_display/KMKDSP__.ttf"
        self.main_font_url_white = "Spots_and_spiders/assets/font/komika_display/KMKDSPSH.ttf"
        self.special_font_url = "Spots_and_spiders/assets/font/badaboom_bb/BADABB__.TTF"
        self.abc_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X"]
        self.numOfTeams = 1
        self.turn = 0
        self.intro_num = 1
        self.board_num = 1
        self.characters = {}
        self.width, self.height = info.current_w, info.current_h  # Get screen resolution
        print(f"{self.width}, {self.height}")
        self.font_size = self.width//20
        self.game_window = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        # pygame.mixer.music.load("")
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        with open("Spots_and_spiders/assets/json/questions.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        self.data = data[self.grade][self.lesson]
        self.json_i = 0
        self.block_positions = {
            0: {0:  (25, self.height-125),},
            1: {0: (75, self.height-125),},
            2: {0: (125, self.height-125),},
            3: {0: (125, self.height-100),},
            4: {0: (125, self.height-50),},
            5: {0: (125, self.height-25),}
        }
        self.create_intro_objects()
    
    def positions(self):
       self.block_positions = {
            0: {0:  (25, self.height-125), 1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: (), 8: (), 9: (), 10: (), 11: (), 12: (), 13: (), 14: (), 15: (), 16: (), 17: (), 18: (), 19: (), 20: (), 21: (), 22: (), 23: (), 24: (), 25: (), 26: (), 27: (), 28: (), 29: (), 30: (), 31: (), 32: (), 33: (), 34: (), 35: (), 36: (), 37: (), 38: ()},
            1: {0: (75, self.height-125), 1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: (), 8: (), 9: (), 10: (), 11: (), 12: (), 13: (), 14: (), 15: (), 16: (), 17: (), 18: (), 19: (), 20: (), 21: (), 22: (), 23: (), 24: (), 25: (), 26: (), 27: (), 28: (), 29: (), 30: (), 31: (), 32: (), 33: (), 34: (), 35: (), 36: (), 37: (), 38: ()},
            2: {0: (125, self.height-125), 1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: (), 8: (), 9: (), 10: (), 11: (), 12: (), 13: (), 14: (), 15: (), 16: (), 17: (), 18: (), 19: (), 20: (), 21: (), 22: (), 23: (), 24: (), 25: (), 26: (), 27: (), 28: (), 29: (), 30: (), 31: (), 32: (), 33: (), 34: (), 35: (), 36: (), 37: (), 38: ()},
            3: {0: (125, self.height-100), 1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: (), 8: (), 9: (), 10: (), 11: (), 12: (), 13: (), 14: (), 15: (), 16: (), 17: (), 18: (), 19: (), 20: (), 21: (), 22: (), 23: (), 24: (), 25: (), 26: (), 27: (), 28: (), 29: (), 30: (), 31: (), 32: (), 33: (), 34: (), 35: (), 36: (), 37: (), 38: ()},
            4: {0: (125, self.height-50), 1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: (), 8: (), 9: (), 10: (), 11: (), 12: (), 13: (), 14: (), 15: (), 16: (), 17: (), 18: (), 19: (), 20: (), 21: (), 22: (), 23: (), 24: (), 25: (), 26: (), 27: (), 28: (), 29: (), 30: (), 31: (), 32: (), 33: (), 34: (), 35: (), 36: (), 37: (), 38: ()},
            5: {0: (125, self.height-25), 1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: (), 8: (), 9: (), 10: (), 11: (), 12: (), 13: (), 14: (), 15: (), 16: (), 17: (), 18: (), 19: (), 20: (), 21: (), 22: (), 23: (), 24: (), 25: (), 26: (), 27: (), 28: (), 29: (), 30: (), 31: (), 32: (), 33: (), 34: (), 35: (), 36: (), 37: (), 38: ()}
        } 

    # Intro Functions
    def create_intro_objects(self):
        self.intro_background1 = Image(self.game_window, 0, 0, "Spots_and_spiders/assets/images/Intro/Intro_background.png", self.width, self.height)
        self.intro_text1 = Image(self.game_window, self.width*.5, self.height*.5, "Spots_and_spiders/assets/images/Intro/Intro_text.png", self.width, 500, True)
        self.exit_button = Image(self.game_window, 0, self.height-100, "Spots_and_spiders/assets/images/Exit_button.png", 100, 100)
        self.intro_team_text = Box(self.game_window, self.width*.4, self.height-200, 700, 100, self.white, f"How many teams: {self.numOfTeams}", self.main_font_url_black, self.font_size, self.black)
        self.intro_background2 = Image(self.game_window, 0, 0, "Spots_and_spiders/assets/images/Intro/Intro_background2.png", self.width, self.height)
        self.intro_text2 = Image(self.game_window, self.width*.5, self.height*.5, "Spots_and_spiders/assets/images/Intro/Intro_text2.png", 800, 500, True)
        self.intro_background3 = Image(self.game_window, 0, 0, "Spots_and_spiders/assets/images/Intro/Intro_background3.png", self.width, self.height )
        self.intro_text3 = Image(self.game_window, self.width*.5, self.height*.5, "Spots_and_spiders/assets/images/Intro/Intro_text3.png", self.width-100, self.height-100, True)
        self.intro_background4 = Image(self.game_window, 0, 0, "Spots_and_spiders/assets/images/Intro/Intro_background4.png", self.width, self.height)
        self.intro_text4 = Image(self.game_window, self.width*.5, self.height*.5, "Spots_and_spiders/assets/images/Intro/Intro_text4.png", self.width-100, 400, True)
        


    def change_intro_team_text(self):
        self.intro_team_text.change_text(f"How many teams: {self.numOfTeams}")

    def draw_intro_objects(self):
        if self.intro_num == 1:
            self.intro_background1.draw_image()
            self.intro_text1.draw_image()
            self.exit_button.draw_image()
            self.intro_team_text.draw_box(True)
        elif self.intro_num == 2:
            self.intro_background2.draw_image()
            self.intro_text2.draw_image()
            self.exit_button.draw_image()
        elif self.intro_num == 3:
            self.intro_background3.draw_image()
            self.intro_text3.draw_image()
            self.exit_button.draw_image()
        elif self.intro_num == 4:
            self.intro_background4.draw_image()
            self.intro_text4.draw_image()
            self.exit_button.draw_image()

    # Board Functions
    def create_board_objects(self):
        if self.board_num == 1:
            self.board_background1 = Image(self.game_window, 0, 0, "Spots_and_spiders/assets/images/Intro/Intro_background3.png", self.width, self.height)
            self.create_character_objects1()
            self.next_button = Box(self.game_window, self.width-300, self.height-50, 300, 50, self.grey, "Next slide >", self.main_font_url_black, self.font_size-40, self.black, True)
        else:
            self.board_background2 = Image(self.game_window, 0, 0, "Spots_and_spiders/assets/images/Board_brackground.png", self.width, self.height)
            self.assign_characters()
            self.create_character_objects2()

    def create_character_objects1(self):
        self.showing_characters = {}
        for i in range(0, self.numOfTeams):
            character_list = []
            for filename in os.listdir("Spots_and_spiders/assets/images/Characters"):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                    image_path = os.path.join("Spots_and_spiders/assets/images/Characters", filename)
                    new_character = Image(self.game_window, 100, 100, image_path, 200, 200, True)
                    character_list.append(new_character)
            label1 = Text(self.game_window, 100, 100, f"Team {i+1}", self.main_font_url_black, self.font_size-15, self.white)
            label2 = Text(self.game_window, 100, 100, f"Team {i+1}", self.main_font_url_white, self.font_size-20, self.black)
            button = Box(self.game_window, 100, 100, 195, 100, self.black, "Select", self.main_font_url_black, self.font_size-20, self.white, True)
            self.showing_characters[f"{i}"] = (0, character_list, label1, label2, button, True)
        

    def create_character_objects2(self):
        pass

    def assign_characters(self):
        for i in range(self.numOfTeams):
            index, list, label1, label2, button, active = self.showing_characters[f"{i}"]
            character = list[index]
            character.scale_img(50, 50)
            self.characters[i] = {
                "character":  character,
                "position": 0,
                                  }


    def draw_board_objects(self):
        if self.board_num == 1:
            total_width = (200 * self.numOfTeams)
            w = ((self.width*.5) - (total_width*.5))+90
            h = self.height*.5
            self.board_background1.draw_image()
            self.exit_button.draw_image()
            for i in range(0, self.numOfTeams):
                index, list, label1, label2, button, active = self.showing_characters[f"{i}"] 
                character = list[index]
                label1.draw_text(x= w-100, y= h-200)
                label2.draw_text(x= w-100, y= h-200)
                character.draw_image(x= w, y= h)
                if active:
                    button.draw_box(True, x= w-100, y= h+120)
                w += 200
            if self.teamsHaveChoosen:
                self.next_button.draw_box(True)
        else:
            self.board_background2.draw_image()
            self.next_button.draw_box(True)
            for i in range(self.numOfTeams):
                character = self.characters[i]["character"]
                position = self.characters[i]["position"]
                x,y = self.block_positions[f"{i}.{position}"]
                character.draw_image(x = x, y = y)
    # Main Functions
    def create_main_objects(self):
        pass

    def draw_main_objects(self):
        pass

    # Question Functions
    def create_question_objects(self):
        pass

    def draw_question_objects(self):
        pass

    # Dice Functions
    def create_dice_objects(self):
        pass

    def draw_dice_objects(self):
        pass

    # Event functions
    def intro_event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                    return
            if self.intro_num == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exit_button_rect = self.exit_button.get_rectangle()
                    if exit_button_rect.collidepoint(event.pos):
                        self.isRunning = False
                        return
                    
                if self.active and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                        self.intro_num = 2
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.numOfTeams = 1
                        self.change_intro_team_text()
                        return
                    elif pygame.K_0 < event.key < pygame.K_7:
                        self.numOfTeams = int(event.unicode)
                        self.change_intro_team_text()
                        return
            elif self.intro_num == 4:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exit_button_rect = self.exit_button.get_rectangle()
                    if exit_button_rect.collidepoint(event.pos):
                        self.isRunning = False
                        return 
                    else:
                        self.page = "board"
                        self.create_board_objects()
                        return
                   
            elif self.intro_num < 4:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exit_button_rect = self.exit_button.get_rectangle()
                    if exit_button_rect.collidepoint(event.pos):
                        self.isRunning = False
                        return
                    else:
                        self.intro_num += 1 
                        return
            


    def board_event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                    return
            if self.board_num == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exit_button_rect = self.exit_button.get_rectangle()
                    if exit_button_rect.collidepoint(event.pos):
                        self.isRunning = False
                        return
                    for i in range(self.numOfTeams):
                        index, list, label1, label2, button, active = self.showing_characters[f"{i}"]
                        character = list[index]
                        character_rect = character.get_rectangle()
                        button_click = button.check_collide(event.pos)
                        if character_rect.collidepoint(event.pos) and active:
                            if index < len(list)-1:
                                index += 1
                                self.showing_characters[f"{i}"] = (index, list, label1, label2, button, active)
                            elif index == len(list)-1:
                                index = 0
                                self.showing_characters[f"{i}"] = (index, list, label1, label2, button, active)  
                        elif button_click and active:
                            active = False
                            for i1 in range(self.numOfTeams):
                                if i1 != i:
                                    index1, list1, label1_1, label2_1, button1, active1 = self.showing_characters[f"{i1}"]
                                    if active1:
                                        list1.pop(index)
                            self.showing_characters[f"{i}"] = (index, list, label1, label2, button, active)
                    count = 0
                    for i in range(self.numOfTeams):
                       inde, lis, labe1, labe2, butto, activ = self.showing_characters[f"{i}"]
                       if not activ:
                           count+=1
                    if count == self.numOfTeams:   
                        self.teamsHaveChoosen = True
                    if self.teamsHaveChoosen:
                        next_button_rect = self.next_button.check_collide(event.pos)
                        if next_button_rect:
                            self.board_num +=1
                            self.create_board_objects()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exit_button_rect = self.exit_button.get_rectangle()
                    if exit_button_rect.collidepoint(event.pos):
                        self.isRunning = False
                        return


    def main_event_listener(self):
        pass
 
    def question_event_listener(self):
        pass

    def dice_event_listener(self):
        pass


    def main_loop(self):
        while self.isRunning:
            if self.page == "intro":
                self.intro_event_listener()
                self.draw_intro_objects()
            elif self.page == "board":
                self.board_event_listener()
                self.draw_board_objects()
            elif self.page == "main_page":
                pass
            elif self.page == "question":
                pass
            elif self.page == "dice_page":
                pass
            
            pygame.display.update()
            self.clock.tick(60)
if __name__ == "__main__":        
    pygame.init()
    game = Game(6, 3.1)
    game.main_loop()
    pygame.quit()


# def play_S_and_S(grade, lesson):
#     pygame.init()
#     try:
#         pygame.mixer.init()
#     except Exception:
#         with open("error_log.txt", "a") as f:
#             f.write("Mixer init failed:\n")
#             f.write(traceback.format_exc())
#     try:
#         game = Game(grade, lesson)
#     except Exception:
#         with open("error_log.txt", "a") as f:
#             f.write("loading game error:\n")
#             f.write(traceback.format_exc())
#     game.main_loop()
#     pygame.quit()
