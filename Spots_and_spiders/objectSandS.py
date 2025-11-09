import pygame


class Image:
    def __init__(self, game_window, position_x:int, position_y:int, img_url:str, size_x:int, size_y:int, centered : bool = False, audio_url: str = None, volume: float = 1.0, text: str = None, fontUrl: str = None, text_size: int = None, text_color: tuple = None):
        self.x = position_x
        self.y = position_y
        self.size_x = size_x
        self.size_y = size_y
        self.game_window = game_window
        self.img = pygame.image.load(img_url)
        self.centered = centered
        self.scale_img()
        if audio_url is not None:
            self.audio = Sound(audio_url, volume)
        if text is not None:
            self.text = Text(self.game_window, self.x, self.y, text, fontUrl, text_size, text_color)
            self.text.center_text(self.size_x, self.size_y)
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)   

    def scale_img(self, size_x: int = None, size_y: int = None):
        if size_x is not None and size_y is not None:
            self.img = pygame.transform.scale(self.img, (size_x, size_y))
        else:
            self.img = pygame.transform.scale(self.img, (self.size_x, self.size_y))
    
    def center_image(self, x, y):
        img_rect = self.img.get_rect(center= (x, y))
        self.img_rect = img_rect
    
    def draw_image(self, with_audio: bool = False, with_text:bool = False, x: int = None, y: int = None):
        if x is not None and y is not None:
            self.x = x
            self.y = y

        if self.centered:
            self.center_image(self.x, self.y)
            self.rect = self.img_rect
            self.game_window.blit(self.img, self.img_rect)
        else: 
            self.game_window.blit(self.img, (self.x, self.y))

        if with_audio:
            self.audio.play_sound()
        if with_text:
            self.text.draw_text()

    def get_rectangle(self):
        return self.rect

class Text:
    def __init__(self, game_window, position_x: int, position_y: int, text: str, font_url: str, text_size: int, text_color: tuple):
        self.x = position_x
        self.y = position_y
        self.game_window = game_window
        self.font = pygame.font.Font(font_url, text_size)
        self.text = text
        self.text_color = text_color
        self.text_centerd = False
        self.innit_text()
        

    def innit_text(self, text: str = None, text_color: tuple= None):
        if text == None and text_color == None:
            self.text = self.font.render(self.text, True, self.text_color)
        elif text == None:
            self.text = self.font.render(self.text, True, text_color)
        elif text_color == None:
            self.text = self.font.render(text, True, self.text_color)
        else:
            self.text = self.font.render(text, True, text_color)
    
    def center_text(self, container_width, container_height):
        text_rect = self.text.get_rect(center = (self.x + container_width // 2, self.y + container_height // 2))
        self.text_rect = text_rect  # Store adjusted rect for drawing
        self.text_centerd = True

    def draw_text(self, x: int = None, y: int = None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        if self.text_centerd:
            self.game_window.blit(self.text, self.text_rect)
        else:
            self.game_window.blit(self.text, (self.x, self.y))

class Box:
    def __init__(self, game_window, position_x: int, position_y: int, size_x: int, size_y: int, box_color:tuple, text: str = None, fontUrl: str = None, text_size: int = None, text_color: tuple = None, centered: bool = False):
        self.x = position_x
        self.y = position_y
        self.game_window = game_window
        self.box_color = box_color
        self.size_x = size_x
        self.size_y = size_y
        self.centered = centered
        self.box = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        if text != None and fontUrl != None and text_size != None and text_color != None:
            self.text_color = text_color
            self.text_object = Text(self.game_window, self.x, self.y, text, fontUrl, text_size, text_color)
            
    
    def draw_box(self, with_text = False, x: int = None, y: int = None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        self.box = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        pygame.draw.rect(self.game_window, self.box_color, self.box)
        if with_text == True:
            if self.centered:
                self.text_object.center_text(self.size_x, self.size_y)
            self.text_object.draw_text(self.x, self.y)
    
    def check_collide(self, pos):
        return self.box.collidepoint(pos)
    
    def change_text(self, new_text):
        self.text_object.innit_text(new_text, self.text_color)



class Sound:
    def __init__(self, audio_url: str, volume: float = 1):
        self.song = pygame.mixer.Sound(audio_url)
        self.change_volume(volume=volume)

    def play_sound(self):
        self.song.play()

    def stop_sound(self):
        self.song.stop()

    def change_volume(self, volume):
        self.song.set_volume(volume)