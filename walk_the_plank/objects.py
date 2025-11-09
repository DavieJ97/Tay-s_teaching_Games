import pygame
import sys, os
import random
from pathlib import Path
import math
import time
import json

# ---------- CONFIG ----------
FPS = 60
PLANK_SPACES = 30
BARREL_TO_BREAK = 10

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ---------- GAME OBJECTS ----------
class MovingSpriteWave:
    def __init__(self, image, x, y, screen_w, screen_h, speed=3, amplitude=50):
        self.image = image
        self.start_x = x
        self.x = x
        self.y = y
        self.speed = speed
        self.amplitude = amplitude
        self.time = 0
        self.screen_w = screen_w
        self.screen_h = screen_h

    def update(self, dt):
        # Move back and forth smoothly using sine wave motion
        self.time += dt * self.speed
        self.x = self.start_x + math.sin(self.time) * self.amplitude

    def draw(self, surf):
        scaled_image = pygame.transform.scale(self.image, (self.screen_w, self.screen_h*.25))
        surf.blit(scaled_image, (int(self.x), int(self.y)))

class MovingSpriteShark:
    def __init__(self, image, x, y, speed=1, bounds=(0, 0)):
        # keep original as provided and make a guaranteed flipped copy
        self.original_image = image.convert_alpha()
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)

        # choose default: we will pick the image to draw from dir every frame
        self.x = x
        self.y = y
        self.speed = speed
        self.dir = 1  # 1 = moving right, -1 = moving left
        self.left_bound, self.right_bound = bounds

        # debug flag (set True while testing)
        self.debug_print = False

    def update(self, dt):
        # move
        self.x += self.speed * self.dir * dt

        # bounce and change direction if hit bounds
        if self.x <= self.left_bound:
            self.x = self.left_bound
            self.dir = 1
            if self.debug_print: print("Shark hit left bound -> dir=1 (right)")

        elif self.x >= self.right_bound:
            self.x = self.right_bound
            self.dir = -1
            if self.debug_print: print("Shark hit right bound -> dir=-1 (left)")


    def draw(self, surf):
        img_to_draw = self.original_image if self.dir > 0 else self.flipped_image

        surf.blit(img_to_draw, (int(self.x), int(self.y)))

        # optional debug: draw a small red dot at the x,y anchor
        if self.debug_print:
            pygame.draw.circle(surf, (255,0,0), (int(self.x), int(self.y)), 4)


class Player:
    def __init__(self, team, stand_img, run_img):
        self.team = team  # 1 = top, 2 = bottom
        self.stand = stand_img
        self.run = run_img
        self.index = 0.0  # 0..PLANK_SPACES-1 (0 at right side, moves left)
        self.moving = False
        self.move_target = None
        self.move_speed = 5.0  # spaces per second

    def world_pos(self, plank_rect):
        # compute pixel position on plank for current index
        space_w = plank_rect.w / PLANK_SPACES
        x = plank_rect.right - (self.index + 0.5) * space_w
        y = plank_rect.top-(plank_rect.h * 0.25) if self.team == 1 else plank_rect.bottom-(plank_rect.h * 1.25) 
        return int(x - 32), int(y - 32)

    def move_spaces(self, n):
        self.move_target = min(PLANK_SPACES - 1, self.index + n)
        self.moving = True

    def update(self, dt):
        if self.moving and self.move_target is not None:
            step = self.move_speed * dt
            if self.index < self.move_target:
                self.index += step
                if self.index >= self.move_target:
                    self.index = self.move_target
                    self.moving = False
                    self.move_target = None

    def draw(self, surf, plank_rect):
        x, y = self.world_pos(plank_rect)
        image = self.run if self.moving else self.stand
        rect = image.get_rect()
        # shift so that (x, y) is the bottom-right corner
        surf.blit(image, (x - rect.width//2, y - rect.height//2))


class Plank:
    def __init__(self, x, y, w, h, team):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_y = y
        self.team = team
        self.barrel_count = 0
        self.cracks = []
        self.broken = False
        self.visible = True
        self.lives = 3

        # shaking state
        self.shake_timer = 0
        self.shake_duration = 0
        self.shake_cycles = 0
        self.shake_intensity = 0.8  # pixels to rotate back and forth
        self.shake_angle = 0

    def start_shake(self, cycles: int):
        """Start shaking animation based on number of movement spaces."""
        self.shake_timer = 0
        self.shake_cycles = cycles
        self.shake_duration = cycles * 0.25  # total duration
        self.shake_angle = 0

    def update(self, dt):
        """Update plank shaking animation."""
        if self.shake_timer < self.shake_duration:
            self.shake_timer += dt
            # determine progress (0–1)
            progress = self.shake_timer / self.shake_duration
            # oscillate back and forth
            angle = self.shake_intensity * math.sin(progress * self.shake_cycles * math.pi * 4)
            self.shake_angle = angle
        else:
            self.shake_angle = 0  # stop shaking
    
    def add_barrel(self, space_idx): 
        # add a crack at space 
        self.barrel_count += 1 
        crack_img_idx = (self.barrel_count - 1) % 6 
        self.cracks.append((space_idx, crack_img_idx)) 
        if self.barrel_count >= BARREL_TO_BREAK: 
            self.broken = True

    def reset(self): 
        self.barrel_count = 0 
        self.cracks = [] 
        self.broken = False
        self.visible = True
        self.lives -= 1

    def draw(self, surf, plank_img, crack_images):
        # Rotate and scale the plank
        scaled = pygame.transform.scale(plank_img, (self.rect.w, self.rect.h))
        rotated = pygame.transform.rotate(scaled, self.shake_angle)
        new_rect = rotated.get_rect(center=self.rect.center)
        surf.blit(rotated, new_rect.topleft)

        # draw cracks on top (unrotated for now)
        space_w = self.rect.w / PLANK_SPACES
        for (sidx, cidx) in self.cracks:
            x = self.rect.right - (sidx + 0.5) * space_w
            y = self.rect.top
            surf.blit(crack_images[cidx], (int(x - crack_images[cidx].get_width()/2), int(y)))

class BarrelDrop:
    def __init__(self, img, plank, space_index):
        self.img = img
        self.plank = plank
        self.space_index = space_index

        # Compute X position along the plank
        space_w = self.plank.rect.w / PLANK_SPACES
        self.x = self.plank.rect.right - (space_index + 0.5) * space_w

        # Start above the plank
        self.y = self.plank.rect.top - 150

        self.vel_y = 0
        self.gravity = 600  # how fast it falls
        self.angle = 0
        self.rotation_speed = 0
        self.phase = "falling"
        self.done = False

    def update(self, dt):
        if self.phase == "falling":
            # Apply gravity
            self.vel_y += self.gravity * dt
            self.y += self.vel_y * dt

            # Check for plank impact
            if self.y >= self.plank.rect.top - self.img.get_height() / 2:
                self.phase = "impact"
                self.vel_y = -120  # small upward bounce
                self.rotation_speed = 360  # degrees per second
                self.plank.add_barrel(self.space_index)

        elif self.phase == "impact":
            # slight bounce upward
            self.y += self.vel_y * dt
            self.vel_y += self.gravity * dt

            if self.vel_y > 0:
                self.phase = "falling_water"

        elif self.phase == "falling_water":
            # fall into water
            self.angle += self.rotation_speed * dt
            self.y += self.vel_y * dt
            self.vel_y += self.gravity * dt

            # off-screen? -> splash and done
            if self.y > self.plank.rect.bottom + 300:
                self.phase = "done"
                self.done = True

    def draw(self, surf):
        if not self.done:
            rotated = pygame.transform.rotate(self.img, self.angle)
            rect = rotated.get_rect(center=(self.x, self.y))
            surf.blit(rotated, rect)



class Explosion:
    def __init__(self, images, x, y, ttl=0.6):
        self.images = images
        self.x = x
        self.y = y
        self.time = 0.0
        self.ttl = ttl

    def update(self, dt):
        self.time += dt

    def draw(self, surf):
        # pick frame by time
        if self.time < self.ttl:
            idx = int((self.time / self.ttl) * len(self.images))
            idx = min(idx, len(self.images)-1)
            img = self.images[idx]
            surf.blit(img, (int(self.x - img.get_width()/2), int(self.y - img.get_height()/2)))

    def is_alive(self):
        return self.time < self.ttl

class PlankBreakSequence:
    """
    Handles the cinematic when a plank breaks:
      - split plank halves rotate and fall
      - player swaps to fall image and rotates 180 while falling
      - shark rises, collides and both descend together
      - calls back to the game to reset plank/player
    """
    def __init__(self, game, plank, player, fall_image, shark_image):
        self.game = game                # reference to GamePlay (to call reset at end)
        self.plank = plank
        self.player = player
        self.fall_image = fall_image
        self.shark_image = shark_image

        # timings (seconds)
        self.t_split = 0.7    # plank halves split and rotate
        self.t_player = 0.6   # player fall / rotate
        self.t_shark = 1.0    # shark rise + take down
        self.time = 0.0
        self.phase = "split"  # split -> player -> shark -> done
        self.done = False

        # create left/right half rects and images scaled to plank size
        w = self.plank.rect.w // 2
        h = self.plank.rect.h
        # load broken halves from game assets (fallback to scaled plank if missing)
        left_img = game.loaded['plank_broken_left']
        right_img = game.loaded['plank_broken_right']
        if left_img is None:
            left_img = pygame.transform.scale(game.loaded['plank'], (w, h))
        else:
            left_img = pygame.transform.scale(left_img, (w, h))
        if right_img is None:
            right_img = pygame.transform.scale(game.loaded['plank'], (w, h))
        else:
            right_img = pygame.transform.scale(right_img, (w, h))

        self.left_img = left_img
        self.right_img = right_img

        # halves start positions
        self.left_pos = pygame.Rect(self.plank.rect.left, self.plank.rect.top, w, h)
        self.right_pos = pygame.Rect(self.plank.rect.left + w, self.plank.rect.top, w, h)

        # animation state
        self.left_angle = 0.0
        self.right_angle = 0.0
        self.left_offset_y = 0.0
        self.right_offset_y = 0.0

        # player fall state
        # note: we sample player's world position once to anchor the falling animation start
        px, py = self.player.world_pos(self.plank.rect)
        self.player_start_x = px
        self.player_start_y = py
        self.player_rot = 0.0
        self.player_fall_y = self.player_start_y

        # shark movement
        self.shark_x = px
        # shark starts below the plank bottom
        self.shark_start_y = self.plank.rect.bottom + int(self.game.screen_h * 0.25)
        self.shark_y = self.shark_start_y
        self.shark_peak_y = self.plank.rect.bottom - int(self.plank.rect.h * 0.2)  # where shark emerges
        self.played_bite_sound = False
        self.played_fall_sound = False

        # disable normal control for this player until done
        self.player.moving = False
        self.plank.broken = False  # prevent re-triggering while animating

    def update(self, dt):
        if self.done:
            return
        self.time += dt

        if self.phase == "split":
            p = min(self.time / self.t_split, 1.0)
            # angles and vertical offsets: rotate away and drop a bit
            self.left_angle = -30 * p
            self.right_angle = 30 * p
            self.left_offset_y = 120 * p
            self.right_offset_y = 120 * p

            if p >= 1.0:
                # move to player fall phase
                self.phase = "player"
                self.time = 0.0
                # play a plank-break/bite sound if available
                if 'bite_sound' in self.game.sound_loaded:
                    self.game.sound_loaded['bite_sound'].play()

        elif self.phase == "player":
            p = min(self.time / self.t_player, 1.0)
            # rotate player to 180 and move down
            self.player_rot = 180 * p
            self.player_fall_y = self.player_start_y + (self.plank.rect.h * 0.9) * p

            # play falling sound once at start of this phase
            if not self.played_fall_sound:
                if 'falling_sound' in self.game.sound_loaded:
                    self.game.sound_loaded['falling_sound'].play()
                self.played_fall_sound = True

            if p >= 1.0:
                self.phase = "shark"
                self.time = 0.0

        elif self.phase == "shark":
            p = min(self.time / self.t_shark, 1.0)
            # shark rises to peak then both descend
            # first half: shark rise, second half: joint descent
            if p < 0.5:
                up = p / 0.5
                self.shark_y = self.shark_start_y - (self.shark_start_y - self.shark_peak_y) * up
                # player continues to drop a little
                self.player_fall_y += (self.plank.rect.h * 0.25) * dt
            else:
                down_p = (p - 0.5) / 0.5
                # both go down together off-screen
                fall_distance = self.game.screen_h * 1.2
                self.shark_y = self.shark_peak_y + fall_distance * down_p
                self.player_fall_y = self.player_start_y + self.plank.rect.h * 1.6 + fall_distance * down_p

            # play bite sound at the moment shark reaches peak (only once)
            if not self.played_bite_sound and self.time >= (self.t_shark * 0.25):
                if 'bite_sound' in self.game.sound_loaded:
                    self.game.sound_loaded['bite_sound'].play()
                self.played_bite_sound = True

            if p >= 1.0:
                self.phase = "done"
                self.done = True
                # final cleanup: reset plank and player using game's reset function
                # small delay would be possible, but we call reset now
                self.game.reset_plank_and_player(self.plank)

    def draw(self, surf):
        # draw left half rotated and shifted
        left_rot = pygame.transform.rotate(self.left_img, self.left_angle)
        left_rect = left_rot.get_rect(center=(self.left_pos.centerx, self.left_pos.centery + self.left_offset_y))
        surf.blit(left_rot, left_rect.topleft)

        # draw right half rotated and shifted
        right_rot = pygame.transform.rotate(self.right_img, self.right_angle)
        right_rect = right_rot.get_rect(center=(self.right_pos.centerx, self.right_pos.centery + self.right_offset_y))
        surf.blit(right_rot, right_rect.topleft)

        # draw falling player (on top)
        # pick appropriate fall image (player is team-specific)
        img = self.fall_image
        rot_img = pygame.transform.rotate(img, self.player_rot)
        rrect = rot_img.get_rect(center=(self.player_start_x, int(self.player_fall_y)))
        surf.blit(rot_img, rrect.topleft)

        # draw shark if in shark or later phases
        if self.phase in ("shark", "done"):
            srect = self.shark_image.get_rect(center=(self.shark_x, int(self.shark_y)))
            surf.blit(self.shark_image, srect.topleft)

class TreasureChestInteraction:
    def __init__(self, screen, assets, sounds, bg_music, grade, lesson):
        self.screen = screen
        self.assets = assets  # self.loaded
        self.sounds = sounds  # self.sounds_loaded
        self.bg_music = bg_music 

        # Load questions once
        with open(resource_path("walk_the_plank/assets/json/questions.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
            self.questions = data[f"{grade}"][f"{lesson}"]

        self.current_question = None

        # State control
        self.state = "IDLE"
        self.timer = 0
        self.alpha = 0  # for fade-in background
        self.visible = False

        # Positions
        self.screen_w, self.screen_h = self.screen.get_size()
        self.chest_pos = (self.screen_w // 2, self.screen_h // 2)
        self.question_pos = (self.screen_w // 2, 100)
        self.answer_pos = (self.screen_w // 2, self.screen_h-100)

        # Bars animation
        self.q_offset = 80  # start off-screen
        self.a_offset = 80

        # Rects (for click detection)
        self.rect_chest = None
        self.rect_question = None
        self.rect_answer = None

        # Text for bars
        self.question_text = "What is 2 + 2?"
        self.answer_text = "4"

        # Font
        self.font = pygame.font.Font(resource_path("walk_the_plank/assets/fonts/Noto_Sans_KR/NotoSansKR-VariableFont_wght.ttf"), 60)  # Default font, size 60

        # Blur overlay (semi-transparent dark layer)
        self.overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)

    def load_random_question(self):
        selected = random.choice(self.questions)
        self.questions.remove(selected)  # 🔹 delete used question

        self.current_question = selected
        self.question_text = selected["question"]
        self.answer_text = selected["answer"]

    def click_parrot(self):
        """Trigger when parrot is clicked"""
        if self.state == "IDLE":
            self.load_random_question()
            self.state = "CHEST_APPEARING"
            self.timer = time.time()
            self.visible = True
            self.alpha = 0
            self.sounds['parrot'].play()


    def click_question(self):
        """Trigger when question bar clicked"""
        if self.state == "QUESTION_SHOWING":
            self.state = "ANSWER_SHOWING"
            self.timer = time.time()

    def click_chest(self):
        """Trigger when chest clicked (close everything)"""
        if self.state in ("QUESTION_SHOWING", "ANSWER_SHOWING"):
            self.state = "CLOSING"
            self.timer = time.time()

    def update(self):
        now = time.time()

        if self.state == "CHEST_APPEARING":
            # Fade in background and chest
            self.alpha = min(180, self.alpha + 8)
            if now - self.timer > 0.5:
                self.state = "CHEST_OPENING"
                self.timer = now
                self.bg_music.set_volume(0.1)

        elif self.state == "CHEST_OPENING":
            # show chest open after delay
            if now - self.timer > 0.5:
                self.state = "QUESTION_SHOWING"
                self.timer = now
                self.sounds['chest_open'].play()

        elif self.state == "QUESTION_SHOWING":
            # animate question bar sliding up
            self.q_offset = max(0, self.q_offset - 8)

        elif self.state == "ANSWER_SHOWING":
            # animate answer bar sliding up
            self.a_offset = max(0, self.a_offset - 8)

        elif self.state == "CLOSING":
            # retract question and answer bars
            self.q_offset = min(80, self.q_offset + 10)
            self.a_offset = min(80, self.a_offset + 10)
            if self.q_offset == 80 and self.a_offset == 80:
                self.state = "DISAPPEARING"
                self.timer = now
            self.sounds['chest_close'].play()

        elif self.state == "DISAPPEARING":
            # fade out
            self.alpha = max(0, self.alpha - 8)
            if self.alpha == 0:
                self.state = "IDLE"
                self.visible = False
                self.sounds['chest_close'].stop()
                self.bg_music.set_volume(0.3)

    def draw_text_centered(self, text, pos, colour=(255, 255, 255)):
        """Helper to draw text centered with a light shadow for clarity."""
        text_surf = self.font.render(text, True, colour)
        text_rect = text_surf.get_rect(center=pos)

        # Shadow (draw slightly offset)
        shadow_surf = self.font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(pos[0] + 2, pos[1] + 2))
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(text_surf, text_rect)

    def draw(self):
        if not self.visible:
            return

        # draw blurred background overlay
        self.overlay.fill((50, 30, 10, self.alpha))
        self.screen.blit(self.overlay, (0, 0))

        # chest
        chest_img = (
            pygame.transform.scale(self.assets["chest_open"], (self.screen_w*.219, self.screen_h*.325))
            if self.state in ("QUESTION_SHOWING", "ANSWER_SHOWING", "CLOSING")
            else pygame.transform.scale(self.assets["chest_close"],(self.screen_w*.219, self.screen_h*.325))
        )
        chest_rect = chest_img.get_rect(center=self.chest_pos)
        self.screen.blit(chest_img, chest_rect)
        self.rect_chest = chest_rect

        # question bar
        q_img = pygame.transform.scale(self.assets["question_bar"], (self.screen_w, self.screen_h*.195))
        q_rect = q_img.get_rect(center=(self.question_pos[0], self.question_pos[1] - self.q_offset))
        if self.state in ("QUESTION_SHOWING", "ANSWER_SHOWING", "CLOSING"):
            self.screen.blit(q_img, q_rect)
            self.draw_text_centered(self.question_text, q_rect.center)
        self.rect_question = q_rect

        # answer bar
        a_img = pygame.transform.scale(self.assets["answer_bar"],(self.screen_w, self.screen_h*.195))
        a_rect = a_img.get_rect(center=(self.answer_pos[0], self.answer_pos[1] + self.a_offset))
        if self.state in ("ANSWER_SHOWING", "CLOSING"):
            self.screen.blit(a_img, a_rect)
            self.draw_text_centered(self.answer_text, a_rect.center)
        self.rect_answer = a_rect