import pygame
import random
import json
from Pirates_of_the_classroom.objectPirates import Image, Sound, Box, Text
import traceback
import sys
import os


class Game:
    def __init__(self, grade, lesson, font_size):
        info = pygame.display.Info()
        self.grade = grade
        self.lesson = lesson
        self.page = "intro"
        self.isRunning = True
        self.width, self.height = info.current_w, info.current_h  # Get screen resolution
        print(f"width{self.width}, height{self.height}")
        self.rgb = (255, 255, 255)
        self.font_url = "Pirates_of_the_classroom/assets/font/FantaisieArtistique.ttf"
        self.game_window = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.font_size = font_size
        self.text_color = (221, 217, 195)
        self.box_color = (150, 75, 0)
        self.numOfTeams = 1
        self.teams = []
        self.teamsScore = []
        self.scoreText = []
        self.rps_boxs = []
        self.turn = 0
        self.active = True
        self.COIN_EVENT = pygame.USEREVENT + 1
        self.TREASURE_EVENT = pygame.USEREVENT + 2
        self.FIGHT_EVENT = pygame.USEREVENT + 3
        self.MINUS_EVENT = pygame.USEREVENT + 4
        self.RESET_EVENT = pygame.USEREVENT + 5
        pygame.mixer.music.load("Pirates_of_the_classroom/assets/audio/Pirates of The Caribbean- EPIC Music [ ezmp3.cc ].mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        with open("Pirates_of_the_classroom/assets/json/words.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)
        self.create_intro_objects()
        

# Intro Page Functions
    def create_intro_objects(self):
        self.intro_background_img = Image(self.game_window, 0, 0, "Pirates_of_the_classroom/assets/images/into_background.png", self.width, self.height)
        self.exit_button = Image(self.game_window, self.width-70, self.height-70, "Pirates_of_the_classroom/assets/images/exit_button.png", 50, 50)
        self.intro_text = Image(self.game_window, 10, self.height*.2, "Pirates_of_the_classroom/assets/images/intro_text.png", self.width - 20, 188)
        self.choose_teams_text = Text(self.game_window, self.width*.5-120, self.height*.5, f"How many teams?: {self.numOfTeams}", self.font_url , 40, self.text_color)
        self.click = Sound("Pirates_of_the_classroom/assets/audio/button-202966.mp3")

    def render_teams_text(self):
        self.choose_teams_text.innit_text(f"How many teams?: {self.numOfTeams}")

    def draw_images_intro(self):
        self.intro_background_img.draw_image()
        self.exit_button.draw_image()
        self.intro_text.draw_image()
        self.choose_teams_text.draw_text()

# Main Page Functions
    def create_main_objects(self):
        self.main_background_img = Image(self.game_window, 0, 0, "Pirates_of_the_classroom/assets/images/background.png", self.width, self.height)
        self.topMaps = [(self.width * .183, 10), (self.width *.29, 10), (self.width *.4, 10), (self.width * .51, 10), (self.width *.62, 10), (self.width *.73, 10)]
        self.planks = [(10, self.height *.17), (10, self.height *.325), (10, self.height *.48), (10, self.height *.64), (10, self.height *.79)]
        self.x_imgs = []
        self.word_img = []
        ii = 0
        for x, y in self.topMaps:
            if self.is_image_path(self.data[f"{self.grade}"][f"{self.lesson}"][ii]):
                full_path = self.resource_path(self.data[f"{self.grade}"][f"{self.lesson}"][ii])
                mini_dic = {}
                mini_dic["background"] = Image(self.game_window, x, y, "Pirates_of_the_classroom/assets/images/blank_map.png", self.width *.11, self.height *.156)
                mini_dic["forground"] = Image(self.game_window, x, y, self.data[f"{self.grade}"][f"{self.lesson}"][ii], (self.width *.11)-10, (self.height *.156)-10)
                self.word_img.append(mini_dic)
            else:
                self.word_img.append(Image(self.game_window, x, y, "Pirates_of_the_classroom/assets/images/blank_map.png", self.width *.11, self.height *.156, text=self.data[f"{self.grade}"][f"{self.lesson}"][ii], fontUrl=self.font_url, text_size=self.font_size, text_color=self.text_color))
            ii += 1
        for x, y in self.planks:
            if self.is_image_path(self.data[f"{self.grade}"][f"{self.lesson}"][ii]):
                full_path = self.resource_path(self.data[f"{self.grade}"][f"{self.lesson}"][ii])
                mini_dic = {}
                mini_dic["background"] = Image(self.game_window, x, y, "Pirates_of_the_classroom/assets/images/plank.png", self.width *.146, self.height *.13)
                mini_dic["forground"] = Image(self.game_window, x, y, full_path, self.width *.146, self.height *.13)
                self.word_img.append(mini_dic)
            else:
                self.word_img.append(Image(self.game_window, x, y, "Pirates_of_the_classroom/assets/images/plank.png", self.width *.146, self.height *.13, text=self.data[f"{self.grade}"][f"{self.lesson}"][ii], fontUrl=self.font_url, text_size=self.font_size, text_color=self.text_color))
            ii += 1
        self.make_button()
        self.scoreboard = Box(self.game_window, self.width - (self.width *.13), 10, self.width *.117, self.height - (self.height *.104), self.box_color)
        score_x = self.width-(self.width *.13)
        score_y = 10
        for i in range(0, self.numOfTeams):
            text = f"Team {i+1}: "
            self.teamsScore.append(0)
            if i == 0:
                self.teams.append((Text(self.game_window, score_x, score_y, text, self.font_url, 40, (255, 204, 0)),
                                   Text(self.game_window, score_x + 40, score_y + 40, f"{self.teamsScore[i]}", self.font_url, self.font_size, (255, 204, 0))))
            else:
                self.teams.append((Text(self.game_window, score_x, score_y, text, self.font_url, 40, self.text_color),
                                   Text(self.game_window, score_x + 40, score_y + 40, f"{self.teamsScore[i]}", self.font_url, self.font_size, self.text_color)))
            score_y += 120
        self.make_random_list()

    def is_image_path(self, string):
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
        return string.lower().endswith(image_extensions)

    def make_button(self):
        start_x, start_y = self.width *.183, self.height *.17  # Starting position for the grid
        img_width, img_height = self.width *.07,self.height *.13  # Image size
        spacing_x, spacing_y = self.width *.11, self.height *.155  # Spacing between images
        for i in range(30):  # 5 rows × 6 columns = 30 images
            # Calculate row and column
            col = i % 6  # 6 columns
            row = i // 6  # 5 rows
            
            x_pos = start_x + col * spacing_x
            y_pos = start_y + row * spacing_y
            
            self.x_imgs.append(Image(self.game_window, x_pos, y_pos, "Pirates_of_the_classroom/assets/images/x.png", img_width, img_height))   

    def make_random_list(self):
        self.random_prize = []
        for i in range(0, 32):
            random_prize = random.randint(-4, 5)
            self.random_prize.append(random_prize)

    def draw_images_main(self):
        self.main_background_img.draw_image()
        self.exit_button.draw_image()
        for img in self.word_img:
            if isinstance(img, dict):
                background_img = img["background"]
                forground_img = img["forground"]
                background_img.draw_image()
                forground_img.draw_image()
            else:
                img.draw_image(with_text= True)
        for img in self.x_imgs:
            img.draw_image()
        self.scoreboard.draw_box()
        for text, score in self.teams:
            text.draw_text()
            score.draw_text()

    def innitilise_scorebord(self):
        for i, objects in enumerate(self.teams):
            text, score = objects
            if i == self.turn:
                text.innit_text(text = f"Team {i+1}: ", text_color = (255, 204, 0))
                score.innit_text(f"{self.teamsScore[i]}", (255, 204, 0))
            else:
                text.innit_text(f"Team {i+1}: ", self.text_color)
                score.innit_text(f"{self.teamsScore[i]}", self.text_color)

    def render_score(self):
        if self.turn >= self.numOfTeams-1:
            self.turn = 0
        else:
            self.turn += 1 
        self.innitilise_scorebord()
        print(self.teamsScore) 

    # Rewards Page Functions
    def create_reward_objects(self):
        self.treasure_shine = Image(self.game_window, self.width*.5, self.height*.5, "Pirates_of_the_classroom/assets/images/treasure_shine.png", 600, 600, True, "Pirates_of_the_classroom/assets/audio/winning-218995.mp3", 0.4)
        self.treasure = Image(self.game_window, self.width*.5, self.height*.5, "Pirates_of_the_classroom/assets/images/treasure.png", 300, 300, True, "Pirates_of_the_classroom/assets/audio/pot-of-coins-275747.mp3")
        self.fight_instructions = Image(self.game_window, 50, 10, "Pirates_of_the_classroom/assets/images/fight_instructions.png", self.width-100, self.height *.13)
        self.fight_salavan = Image(self.game_window, self.width *.22, self.height *.26, "Pirates_of_the_classroom/assets/images/fight_salavan.png", self.width *.274, self.height *.445)
        self.fight_jack = Image(self.game_window, self.width *.51, self.height *.26, "Pirates_of_the_classroom/assets/images/fight_jack.png", self.width *.274, self.height *.445)
        self.fight_text = Image(self.game_window, self.width*.5, self.height *.78, "Pirates_of_the_classroom/assets/images/fight_text.png", self.width *.34, self.height *.22, True, "Pirates_of_the_classroom/assets/audio/draw-sword1-44724.mp3")
        starting_y = self.height *.17
        for teams in range(0, self.numOfTeams):
            self.rps_boxs.append(Box(self.game_window, self.width-190, starting_y, 170, 80, self.box_color, f"Team {teams+1}", self.font_url, 40, self.text_color, True))
            starting_y +=100
        self.reset_score_img = Image(self.game_window, 0, 0, "Pirates_of_the_classroom/assets/images/background_reset.png", self.width, self.height, False, "Pirates_of_the_classroom/assets/audio/evil-laugh-89423.mp3")

    def coin_event(self):
        self.coin_list = []
        self.i = 0
        self.coin_x = self.width *.5
        self.coin_y = self.height*.5
        pygame.time.set_timer(self.COIN_EVENT, 400)  # Trigger event every 400ms
    
    def treasure_event(self):
        self.isTreasure = True
        pygame.time.set_timer(self.TREASURE_EVENT, 400)
        
    def fight_event(self):
        self.isFight = True
        pygame.time.set_timer(self.FIGHT_EVENT, 400)

    def reset_event(self):
        self.isReset = True
        pygame.time.set_timer(self.RESET_EVENT, 400)
    
    def minus_event(self):
        self.minus_list = []
        self.i = 0
        self.boat_x = self.width * .5
        self.boat_y = self.height * .5
        cannon_sound = Sound("Pirates_of_the_classroom/assets/audio/cannon-fire-161072.mp3")
        cannon_sound.play_sound()
        pygame.time.set_timer(self.MINUS_EVENT, 1000)

    def draw_rewards_img(self):
        self.main_background_img.draw_image()
        self.exit_button.draw_image()
        if 0 < self.random_prize[1] < 5:
            if len(self.coin_list)> 0:
                for coin in self.coin_list:
                    coin.draw_image()
        elif self.random_prize[1] == 5:
            if not self.isTreasure:
                self.treasure_shine.draw_image()
                self.treasure.draw_image()
        elif self.random_prize[1] == 0:
            self.fight_instructions.draw_image()
            self.fight_jack.draw_image()
            self.fight_salavan.draw_image()
            for i, box in enumerate(self.rps_boxs):
                if i != self.turn:
                    box.draw_box(True)
            if not self.isFight:
                self.fight_text.draw_image()
        elif -4 < self.random_prize[1] < 0:
            if len(self.minus_list) > 0:
                for boat in self.minus_list:
                    boat.draw_image()
        elif self.random_prize[1] == -4:
            if not self.isReset:
                self.reset_score_img.draw_image()
                self.exit_button.draw_image()

    # Event functions
    def check_events_intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click.play_sound()
                button_rect = self.exit_button.get_rectangle()
                if button_rect.collidepoint(event.pos):  # Check if mouse clicks the button
                    self.isRunning = False
                    return  

            if self.active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    self.click.play_sound()
                    self.create_main_objects()
                    self.create_reward_objects()
                    self.page = "main" #start the game
                    self.active = False
                    pygame.mixer.music.set_volume(0.1)
                    return
                elif event.key == pygame.K_BACKSPACE:  # Backspace key
                    self.click.play_sound()
                    self.numOfTeams = 1  # Change the teams to default 1
                    self.render_teams_text()
                    return
                elif pygame.K_0 < event.key < pygame.K_7:  # Check for number keys
                    self.click.play_sound()
                    self.numOfTeams = int(event.unicode)
                    self.render_teams_text() 
                    return

    def check_events_main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click.play_sound()
                button_rect = self.exit_button.get_rectangle()
                if button_rect.collidepoint(event.pos):  # Check if mouse clicks the button
                    self.isRunning = False
                    return
                for img in self.x_imgs:  # Iterate over a copy of the list
                    button_rect = img.get_rectangle()
                    if button_rect.collidepoint(event.pos):
                        self.random_prize.pop(1)
                        if 0 < self.random_prize[1] < 5:
                            self.coin_event()
                        elif self.random_prize[1] == 5:
                            self.treasure_event()
                        elif self.random_prize[1] == 0:
                            self.fight_event()
                        elif -4 <self.random_prize[1] < 0:
                            self.minus_event()
                        elif self.random_prize[1] == -4:
                            self.reset_event()
                        self.page = "reward"
                        self.x_imgs.remove(img)  # Remove from list
                        return  # Stop after removing one item
                    
    def check_events_reward(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            
            if event.type == self.COIN_EVENT:
                if self.i < self.random_prize[1]:
                    coin = Image(self.game_window, self.coin_x, self.coin_y, "Pirates_of_the_classroom/assets/images/coin.png", 200, 200, True, "Pirates_of_the_classroom/assets/audio/coin-recieved-230517.mp3")
                    coin.draw_image(with_audio=True)
                    self.coin_list.append(coin)
                    self.i +=1
                    if self.i == 1:
                        self.coin_x-=220
                    elif self.i == 2:
                        self.coin_x+=440
                    elif self.i == 3:
                        self.coin_x-= 220
                        self.coin_y -= 220
                else:
                    pygame.time.set_timer(self.COIN_EVENT, 0)  # Stop event once all coins appear 
            elif event.type == self.TREASURE_EVENT:
                self.treasure_shine.draw_image(True)
                self.treasure.draw_image(True)
                pygame.time.set_timer(self.TREASURE_EVENT, 0)  # Stop event once all coins appear
                self.isTreasure = False
            elif event.type == self.FIGHT_EVENT:
                self.fight_text.draw_image(True)
                pygame.time.set_timer(self.FIGHT_EVENT, 0)
                self.isFight = False
            elif event.type == self.MINUS_EVENT:
                if self.i < abs(self.random_prize[1]):
                    boat = Image(self.game_window, self.boat_x, self.boat_y, "Pirates_of_the_classroom/assets/images/minus_img.png", 280, 262, True, "Pirates_of_the_classroom/assets/audio/explosion-312361.mp3")
                    boat.draw_image(with_audio=True)
                    self.minus_list.append(boat)
                    self.i +=1
                    if self.i == 1:
                        self.boat_x -=320
                    elif self.i == 2:
                        self.boat_x +=640
                    elif self.i == 3:
                        self.boat_x -= 320
                        self.boat_y -= 320
                else:
                    pygame.time.set_timer(self.MINUS_EVENT, 0)  # Stop event once all coins appear 
            elif event.type == self.RESET_EVENT:
                if self.isReset:
                    self.reset_score_img.draw_image(True)
                    pygame.time.set_timer(self.RESET_EVENT, 0)
                    self.isReset = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click.play_sound()
                button_rect = self.exit_button.get_rectangle()
                if button_rect.collidepoint(event.pos):  # Check if mouse clicks the button
                    if self.random_prize[1] != -4:
                        self.teamsScore[self.turn] += self.random_prize[1]
                    else:
                        for i in range(0, len(self.teamsScore)):
                            self.teamsScore[i] = 0
                    self.render_score()
                    self.page = "main"
                    return 
                elif self.random_prize[1] == 0:
                    for i, box in enumerate(self.rps_boxs):
                        if box.check_collide(event.pos):
                            self.teamsScore[i] -= 3
                            self.teamsScore[self.turn] +=3
                            self.render_score()
                            self.page = "main"
                            return   

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            base_path = os.path.dirname(sys.executable) # PyInstaller builds
        except AttributeError:
            base_path = os.path.dirname(sys.argv[0])  # Folder containing the main script or executable
            print("Root path:", os.path.dirname(sys.argv[0]))

        return os.path.join(base_path, relative_path)

    # Main Loop function
    def main_loop(self):
        while self.isRunning:
            if self.page == "main": 
                #event handler
                self.check_events_main()
                #draw images
                self.draw_images_main()
            elif self.page == "reward":
                #event handler
                self.check_events_reward()
                #draw images
                self.draw_rewards_img()
            elif self.page == "intro":
                #event handler
                self.check_events_intro()
                #draw images
                self.draw_images_intro()

            
            pygame.display.update()
            self.clock.tick(60)



def play_pirate_game(grade, lesson):
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        with open("error_log.txt", "a") as f:
            f.write("Mixer init failed:\n")
            f.write(traceback.format_exc())
    try:
        game = Game(grade, lesson, 40)
    except Exception:
        with open("error_log.txt", "a") as f:
            f.write("loading game error:\n")
            f.write(traceback.format_exc())
    game.main_loop()
    pygame.quit()

# This game I want to dedicate to God Who made it possible. Without His help I would not have gotten so far.