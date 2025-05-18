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

    def scale_img(self, size_x: int = None, size_y: int = None):
        if size_x is not None and size_y is not None:
            self.size_x = size_x
            self.size_y = size_y
        self.img = pygame.transform.scale(self.img, (self.size_x, self.size_y))
    
    def center_image(self, x = None, y = None):
        if x is None and y is None:
            img_rect = self.img.get_rect(center= (self.x, self.y))
        else:
            img_rect = self.img.get_rect(center= (x, y))
        self.img_rect = img_rect
    
    def draw_image(self, with_audio: bool = False, with_text:bool = False, x: int = None, y: int = None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        if self.centered:
            self.center_image()
            self.game_window.blit(self.img, self.img_rect)
        else:
            self.game_window.blit(self.img, (self.x, self.y))
        if with_audio:
            self.audio.play_sound()
        if with_text:
            self.text.draw_text()
    
    def innit_text(self, text: str = None, text_color: tuple= None):
        self.text.innit_text(text, text_color)

    def get_rectangle(self):
        if self.centered:
            rect = self.img.get_rect(center = (self.x, self.y))
        else:
            rect = self.img.get_rect(topleft = (self.x, self.y))
        return rect

    def rotate_image(self, degree):
        self.img = pygame.transform.rotate(self.img, degree)

class Text:
    def __init__(self, game_window, position_x: int, position_y: int, text: str, font_url: str, text_size: int, text_color: tuple, start_color = None, end_color = None):
        self.x = position_x
        self.y = position_y
        self.game_window = game_window
        self.font = pygame.font.Font(font_url, text_size)
        self.text = text
        self.text_color = text_color
        self.text_centerd = False
        if start_color is not None and end_color is not None:
            self.innit_text(start_color=start_color, end_color=end_color)
        else:
            self.innit_text()
        

    def innit_text(self, text: str = None, text_color: tuple= None, start_color = None, end_color = None):
        if text == None and text_color == None:
            self.text = self.font.render(self.text, True, self.text_color)
        elif text == None:
            self.text = self.font.render(self.text, True, text_color)
        elif text_color == None:
            self.text = self.font.render(text, True, self.text_color)
        else:
            self.text = self.font.render(text, True, text_color)
        if start_color is not None and end_color is not None:
            width, height = self.text.get_size()

            # Create the gradient surface
            self.gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)

            for y in range(height):
                # Calculate the interpolated colour
                r = start_color[0] + (end_color[0] - start_color[0]) * y // height
                g = start_color[1] + (end_color[1] - start_color[1]) * y // height
                b = start_color[2] + (end_color[2] - start_color[2]) * y // height

                pygame.draw.line(self.gradient_surface, (r, g, b), (0, y), (width, y))
            self.gradient_surface.blit(self.text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.text = None  # avoid drawing white text later
            
    
    def center_text(self, container_width, container_height):
        text_rect = self.text.get_rect(center = (self.x + container_width // 2, self.y + container_height // 2))
        self.text_rect = text_rect  # Store adjusted rect for drawing
        self.text_centerd = True

    def draw_text(self, with_gradient = False):
        if self.text_centerd:
            self.game_window.blit(self.text, self.text_rect)
        elif with_gradient:
            self.game_window.blit(self.gradient_surface, (self.x, self.y))
        else:
            self.game_window.blit(self.text, (self.x, self.y))

    def get_rectangle(self):
        rect = self.text.get_rect(topleft = (self.x, self.y))
        return rect
class Box:
    def __init__(self, game_window, position_x: int, position_y: int, size_x: int, size_y: int, box_color:tuple, text: str = None, fontUrl: str = None, text_size: int = None, text_color: tuple = None, centered: bool = False):
        self.x = position_x
        self.y = position_y
        self.game_window = game_window
        self.box_color = box_color
        self.box = pygame.Rect(self.x, self.y, size_x, size_y)
        if text != None and fontUrl != None and text_size != None and text_color != None:
            self.text_object = Text(self.game_window, self.x, self.y, text, fontUrl, text_size, text_color)
            if centered:
                self.text_object.center_text(size_x, size_y)
    
    def draw_box(self, with_text = False):
        pygame.draw.rect(self.game_window, self.box_color, self.box)
        if with_text == True:
            self.text_object.draw_text()
    
    def check_collide(self, pos):
        return self.box.collidepoint(pos)

    def change_text(self, text, text_color):
        self.text_object.innit_text(text, text_color)


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