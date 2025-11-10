"""
Walk The Plank - Pygame

Place all your image and sound files in an `assets/` folder next to this script.
This script uses placeholder names for assets. Replace them with your real file names.

Features implemented:
- Two planks (Team 1 = top, Team 2 = bottom) each with 30 spaces.
- Turn system: players alternate turns.
- Slider bar: hold mouse on the slider to move the arrow; release to stop.
  The arrow selects one of six options.
- Options: move 1/2/3 spaces for the active player, drop barrel(s) on Team 1/Team 2/both.
- Barrel drops cause cracks. Each plank counts total barrels landed. Each time a barrel lands the script shows a crack sprite at a random space.
- When a plank reaches 10 barrels, it breaks: a shark eats the player, then the plank and player reset.
- Background waves and sharks move left/right to give motion.
- Simple animations for player running/standing and barrel falling and explosion.

Requirements:
- Python 3.10+
- pygame installed: pip install pygame

"""

import pygame
import random
from pathlib import Path
from walk_the_plank.objects import MovingSpriteShark, MovingSpriteWave, Plank, Player, PlankBreakSequence, BarrelDrop, Explosion, TreasureChestInteraction
import os, sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ---------- CONFIG ----------
FPS = 60
PLANK_SPACES = 30
BARREL_TO_BREAK = 10
ASSET_DIR = resource_path('walk_the_plank/assets')

# Asset names (replace these with your files)
ASSETS = {
    'bg_wave_1': 'wave1.png',
    'bg_wave_2': 'wave2.png',
    'bg_wave_3': 'wave3.png',
    'bg_wave_4': 'wave4.png',
    'shark': 'shark.png',
    'shark_bite': 'shark_bite.png',
    'deck_right': 'deck_right.png',
    'deck_left': 'deck_left.png',
    'plank': 'plank.png',
    'plank_broken_left': 'plank_broken_left.png',
    'plank_broken_right': 'plank_broken_right.png',
    'crack_1': 'crack1.png',
    'crack_2': 'crack2.png',
    'crack_3': 'crack3.png',
    'crack_4': 'crack4.png',
    'crack_5': 'crack5.png',
    'crack_6': 'crack6.png',
    'barrel_1': 'barrel1.png',
    'barrel_2': 'barrel2.png',
    'barrel_3': 'barrel3.png',
    'barrel_4': 'barrel4.png',
    'barrel_5': 'barrel5.png',
    'barrel_6': 'barrel6.png',
    'expl_1': 'expl1.png',
    'expl_2': 'expl2.png',
    'expl_3': 'expl3.png',
    'expl_4': 'expl4.png',
    'expl_5': 'expl5.png',
    'expl_6': 'expl6.png',
    'oct_1': 'oct1.png',
    'oct_2': 'oct2.png',
    'oct_3': 'oct3.png',
    'oct_4': 'oct4.png',
    'p1_stand': 'p1_stand.png',
    'p1_run': 'p1_run.png',
    'p2_stand': 'p2_stand.png',
    'p2_run': 'p2_run.png',
    'p1_fall': 'p1_fall.png',
    'p2_fall': 'p2_fall.png',
    'slider': 'slider.png',
    'pointer': 'pointer.png',
    'parrot': 'parrot.png',
    'question_bar':'question.png',
    'answer_bar':'answer.png',
    'chest_open':'chest_open.png',
    'chest_close': 'chest_close.png',
    'game_over': 'game_over.png',

}

SOUNDS = {
    'song':'background_music.mp3',
    'intro_sound':'walk_the_plank.mp3',
    'spinner_sound':'spinner_sound.mp3',
    'plank_walk': 'plank_walk.mp3',
    'plank_hit': 'plank_hit.wav',
    'barrel_sound_1': 'take_him_down.mp3',
    'water_splash_1': 'water_splash.mp3',
    'water_splash_2': 'water_splash2.mp3',
    'falling_sound': 'falling_sound.mp3',
    'bite_sound': 'bite_sound.mp3',
    'win_sound': 'win_sound.mp3',
    'scream':'scream.mp3',
    'attack_1': 'take_him_down.mp3',
    'attack_2': 'Yo_ho_ho.mp3',
    'attack_3': 'Land_ho.mp3',
    'attack_4': 'Hiyee.mp3',
    'attack_5': 'He_ho.mp3',
    'attack_6': 'Feed_to_shark.mp3',
    'attack_7': 'argh.mp3',
    'try_again': 'Try_again.mp3',
    'game_over': 'Game_over.mp3',
    'barrel_fall': 'barrel_fall.mp3',
    'parrot': 'parrot.wav',
    'chest_open': 'chest_opened.wav',
    'chest_close': 'chest_closed.wav',
    }

# ---------- PYGAME HELPERS ----------

def load_image(name, fallback_size=(50,50)):
    path = f"{ASSET_DIR}/images/{name}"
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except Exception:
        # create placeholder surface
        surf = pygame.Surface(fallback_size)
        surf.fill((200, 50, 50))
        return surf
    
def load_sound(name, fallback_volume=0.5):
    path = f"{ASSET_DIR}/sounds/{name}"
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(fallback_volume)
        return sound
    except Exception as e:
        print(f"⚠️ Could not load sound '{name}': {e}")
        # create a silent placeholder (tiny empty buffer)
        arr = pygame.mixer.Sound(buffer=b'\x00' * 4)
        arr.set_volume(0)
        return arr

# ---------- INITIALISE PYGAME ----------
class GamePlay:
    def __init__(self, grade, lesson):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_w, self.screen_h = self.screen.get_size()
        print(({self.screen_w}, {self.screen_h}))
        pygame.display.set_caption('Walk The Plank')
        self.font = pygame.font.SysFont(None, 26)
        pygame.mixer.init()  # initialise sound mixer

        pygame.mixer.music.load(f"{ASSET_DIR}/sounds/background_music.mp3")  # your music file
        pygame.mixer.music.set_volume(0.3)  # volume between 0.0 and 1.0
        pygame.mixer.music.play(-1)


        # load assets (with placeholders if missing)
        self.loaded = {k: load_image(v, fallback_size=(80,80)) for k,v in ASSETS.items()}
        self.sound_loaded = {k: load_sound(v) for k,v in SOUNDS.items()}

        # crack images array
        self.crack_images = [self.loaded[f'crack_{i}'] for i in range(1,7)]
        self.barrel_images = [self.loaded[f'barrel_{i}'] for i in range(1,7)]
        self.expl_images = [self.loaded[f'expl_{i}'] for i in range(1,7)]

        # create moving waves and sharks
        self.waves = []
        wave_img = self.loaded['bg_wave_1']
        for i in range(5):  # 5 waves at 0%, 25%, 50%, 75%, 100%
            y = int((self.screen_h - wave_img.get_height()) * (i / 4))  # distribute vertically
            x = 0
            self.waves.append(MovingSpriteWave(wave_img, x=x, y=y, screen_w=self.screen_w, screen_h=self.screen_h))
        self.overlay_box = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.overlay_box.fill((0, 0, 0, 100))  # RGBA -> (R, G, B, Alpha)
        self.sharks = []
        for i in range(4):  # 4 sharks
            y = int((self.screen_h - self.loaded['shark'].get_height()) * (i / 3))  # 0%, 33%, 66%, 100%
            x = 100 + i * 200
            speed = 30 + i * 10
            self.sharks.append(MovingSpriteShark(self.loaded['shark'], x=x, y=y, speed=speed, bounds=(0, self.screen_w - 150)))

        # planks positions
        plank_w = self.screen_w - (self.screen_w*.036)
        plank_h = self.screen_h*.083
        self.plank_top = Plank(self.screen_w*.026, self.screen_h*.278, plank_w, plank_h, team=1)
        self.plank_bottom = Plank(self.screen_w*.026, self.screen_h*.648, plank_w, plank_h, team=2)

        # players
        player1_run_image = pygame.transform.scale(self.loaded['p1_run'], (self.screen_w*.109, self.screen_h*.195))
        player1_stand_image = pygame.transform.scale(self.loaded['p1_stand'], (self.screen_w*.109, self.screen_h*.195))
        player2_run_image = pygame.transform.scale(self.loaded['p2_run'], (self.screen_w*.109, self.screen_h*.195))
        player2_stand_image = pygame.transform.scale(self.loaded['p2_stand'], (self.screen_w*.109, self.screen_h*.195))
        self.player1 = Player(1, player1_stand_image, player1_run_image)
        self.player2 = Player(2, player2_stand_image, player2_run_image)

        # UI slider
        # --- SLIDER SETUP ---
        self.slider_img = self.loaded['slider']
        self.pointer = self.loaded['pointer']

        # Always centred horizontally, near bottom
        self.slider_rect = self.slider_img.get_rect(midbottom=(self.screen_w / 2, self.screen_h))

        # Arrow setup
        self.arrow_dir = 1
        self.arrow_speed = 3000  # px per second while held oscillating
        self.arrow_pos = self.slider_rect.left  # start at the left edge of the slider
        self.arrow_moving = False

        # game state
        self.turn = 1  # 1 or 2
        self.movement_in_progress = False
        self.barrel_drops = []
        self.explosions = []
        self.break_sequences = []

        # parrot and chest objects
        parrot_image = self.loaded['parrot']
        self.parrot = pygame.transform.scale(parrot_image, (self.screen_w*.087, self.screen_h*.195))
        parrot_h = self.parrot.get_height()
        self.parrot_pos = (0, self.screen_h-parrot_h)
        self.chest_scene = TreasureChestInteraction(self.screen, self.loaded, self.sound_loaded, pygame.mixer.music, grade, lesson)
        self.parrot_clicked = False

        # game_over image
        self.game_over = False
        self.go_pic = self.loaded['game_over']

        self.sound_loaded['intro_sound'].set_volume(0.6)
        self.sound_loaded['intro_sound'].play()
        self.main_loop()
        pygame.quit()
        sys.exit()

# ---------- GAME LOOP ----------

    def pick_slider_option(self, px):
        """Return option 1–6 based on pointer X position along the slider."""
        segment_count = 6
        segment_w = self.slider_rect.w / segment_count

        # Distance from the start of the slider
        rel_x = px - self.slider_rect.left

        # Clamp to slider bounds
        rel_x = max(0, min(rel_x, self.slider_rect.w - 1))

        # Determine which segment the pointer is in
        slot = int(rel_x // segment_w) + 1

        return slot

    def perform_option(self, option):
        # options mapping:
        # 1 move 1, 2 barrel on team1, 3 move 2, 4 barrel on team2, 5 move 3, 6 barrel on both
        if option == 1:
            self.active_player().move_spaces(1)
            self.movement_in_progress = True
            self.sound_loaded['plank_walk'].play()
            self.active_plank().start_shake(1)
        elif option == 2:
            self.sound_loaded['barrel_fall'].play()
            attack_sound = self.sound_loaded[f'attack_{random.randint(1, 7)}']
            attack_sound.play()
            self.drop_barrel_on(self.plank_top)
        elif option == 3:
            self.active_player().move_spaces(2)
            self.movement_in_progress = True
            self.sound_loaded['plank_walk'].play()
            self.active_plank().start_shake(2)
        elif option == 4:
            self.sound_loaded['barrel_fall'].play()
            attack_sound = self.sound_loaded[f'attack_{random.randint(1, 7)}']
            attack_sound.play()
            self.drop_barrel_on(self.plank_bottom)
        elif option == 5:
            self.active_player().move_spaces(3)
            self.movement_in_progress = True
            self.sound_loaded['plank_walk'].play()
            self.active_plank().start_shake(3)
        elif option == 6:
            self.sound_loaded['barrel_fall'].play()
            attack_sound = self.sound_loaded[f'attack_{random.randint(1, 7)}']
            attack_sound.play()
            self.drop_barrel_on(self.plank_top)
            self.drop_barrel_on(self.plank_bottom)

    def active_plank(self):
        return self.plank_top if self.turn == 1 else self.plank_bottom

    def active_player(self):
        return self.player1 if self.turn == 1 else self.player2

    def drop_barrel_on(self, plank):
        # choose random space somewhere along plank (exclude very ends)
        idx = random.randint(2, PLANK_SPACES-3)
        img = random.choice(self.barrel_images)
        bd = BarrelDrop(img, plank, idx)
        self.barrel_drops.append(bd)
        # create explosion location when it lands (handled later)

    def reset_plank_and_player(self, plank):
        # find which player is on that plank and reset them
        if plank.team == 1:
            if plank.lives > 1:
                self.sound_loaded['try_again'].play() 
                self.player1.index = 0
                self.player1.moving = False
                plank.reset()
            else:
                self.sound_loaded['game_over'].play()
                plank.lives -= 1
                self.game_over = True

        else:
            if plank.lives > 1:
                self.sound_loaded['try_again'].play()
                self.player2.index = 0
                self.player2.moving = False
                plank.reset()
            else:
                self.sound_loaded['game_over'].play()
                plank.lives -= 1
                self.game_over = True

    def main_loop(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.slider_rect.collidepoint(event.pos):
                        self.arrow_moving = True
                        self.sound_loaded['spinner_sound'].play(-1)
                    elif self.parrot.get_rect(topleft=self.parrot_pos).collidepoint(event.pos):
                        self.chest_scene.click_parrot()
                        self.parrot_clicked = True
                    elif self.parrot_clicked and self.chest_scene.rect_chest.collidepoint(event.pos):
                        self.chest_scene.click_chest()
                        self.parrot_clicked = False
                    elif self.parrot_clicked and self.chest_scene.rect_question.collidepoint(event.pos):
                        self.chest_scene.click_question()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.arrow_moving:
                        self.arrow_moving = False
                        self.sound_loaded['spinner_sound'].stop()
                        # pick option
                        option = self.pick_slider_option(self.arrow_pos)
                        self.perform_option(option)
                        self.turn = 1 if self.turn == 2 else 2
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # allow keyboard control: start/stop arrow
                        if not self.arrow_moving:
                            self.arrow_moving = True
                            self.sound_loaded['spinner_sound'].play(-1)
                        else:
                            self.arrow_moving = False
                            self.sound_loaded['spinner_sound'].stop()
                            option = self.pick_slider_option(self.arrow_pos)
                            self.perform_option(option)
                            self.turn = 1 if self.turn == 2 else 2
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            if self.arrow_moving:
                # move back and forth across the slider
                self.arrow_pos += self.arrow_dir * self.arrow_speed * dt

                # Clamp the pointer CENTER within the slider bounds
                half_w = self.pointer.get_width() / 2
                if self.arrow_pos < self.slider_rect.left + half_w:
                    self.arrow_pos = self.slider_rect.left + half_w
                    self.arrow_dir *= -1
                elif self.arrow_pos > self.slider_rect.right - half_w:
                    self.arrow_pos = self.slider_rect.right - half_w
                    self.arrow_dir *= -1
            else:
                # relax arrow to last position if not moving
                pass

            # update moving background elements
            for s in self.sharks:
                s.update(dt)
            for w in self.waves:
                w.update(dt)
        

            # update players
            self.player1.update(dt)
            self.player2.update(dt)

            # update planks
            self.plank_top.update(dt)
            self.plank_bottom.update(dt)

            # Check if movement finished
            if self.movement_in_progress and not (self.player1.moving or self.player2.moving):
                self.movement_in_progress = False
                

            # --- CHECK IF PLAYER REACHED END OF PLANK ---
            for player, plank in [(self.player1, self.plank_top), (self.player2, self.plank_bottom)]:
                if player.index >= PLANK_SPACES - 1:
                    # Player reached the end
                    if 'win_sound' in self.sound_loaded:
                        self.sound_loaded['win_sound'].play()
                    else:
                        print("Reached the end!")

                    # Give player an extra life
                    if plank.lives < 6:
                        plank.lives += 1

                    # Reset player to start
                    player.index = 0
                    player.moving = False
                    player.move_target = None


            # update barrel drops
            for bd in self.barrel_drops:
                old_phase = getattr(bd, "old_phase", None)
                bd.update(dt)

                # Check for new impact
                if bd.phase == "impact" and old_phase != "impact":
                    self.sound_loaded['plank_hit'].play()
                    self.explosions.append(Explosion(self.expl_images, bd.x, bd.y))
                    self.sound_loaded['barrel_fall'].stop()

                # Check for water splash
                if bd.phase == "done" and old_phase != "done":
                    random.choice([
                        self.sound_loaded['water_splash_1'],
                        self.sound_loaded['water_splash_2']
                    ]).play()

                bd.old_phase = bd.phase

            self.barrel_drops = [b for b in self.barrel_drops if not b.done or (b.done and b in self.barrel_drops and False)]
            # we keep finished barrels but rely on plank cracks list; so remove finished barrel objects
            self.barrel_drops = [b for b in self.barrel_drops if not b.done]

            # update explosions
            for ex in self.explosions:
                ex.update(dt)
            self.explosions = [e for e in self.explosions if e.is_alive()]

            # update break sequences
            for seq in self.break_sequences:
                seq.update(dt)
            # remove finished sequences
            self.break_sequences = [s for s in self.break_sequences if not s.done]

            # check for broken planks and start break sequences
            for plank in (self.plank_top, self.plank_bottom):
                if plank.broken:
                    # only start one sequence per broken event
                    already = any(seq.plank is plank for seq in self.break_sequences)
                    if not already:
                        # find the player for this plank and fall image
                        player = self.player1 if plank.team == 1 else self.player2
                        fall_img = self.loaded['p1_fall'] if plank.team == 1 else self.loaded['p2_fall']
                        shark_img = self.loaded['shark_bite']
                        plank.visible = False
                        seq = PlankBreakSequence(self, plank, player, fall_img, shark_img)
                        self.break_sequences.append(seq)

            # update chest
            self.chest_scene.update()

            # Draw
            self.screen.fill((135, 206, 235))
            # draw waves
            # draw sharks behind water
            for s in self.sharks:
                s.draw(self.screen)
            self.screen.blit(self.overlay_box, (0, 0))
            for w in self.waves:
                w.draw(self.screen)
            # draw decks
            self.screen.blit(self.loaded['deck_right'], (-(self.loaded['deck_right'].get_width()*0.70), -5))
            self.screen.blit(self.loaded['deck_left'], (self.screen_w - (self.loaded['deck_left'].get_width()*0.30), -5))

            # draw planks
            if self.plank_top.visible: 
                self.plank_top.draw(self.screen, self.loaded['plank'], self.crack_images)
            if self.plank_bottom.visible: 
                self.plank_bottom.draw(self.screen, self.loaded['plank'], self.crack_images)

            # draw players
            if self.plank_top.visible:
                self.player1.draw(self.screen, self.plank_top.rect)
            if self.plank_bottom.visible:
                self.player2.draw(self.screen, self.plank_bottom.rect)

            # draw barrel drops
            for bd in self.barrel_drops:
                bd.draw(self.screen)

            # draw explosions
            for ex in self.explosions:
                ex.draw(self.screen)


            # --- DRAW SLIDER UI ---
            self.screen.blit(self.slider_img, self.slider_rect)

           # --- Keep arrow centered within the slider width ---
            half_w = self.pointer.get_width() / 2

            # Clamp the pointer's CENTER within the slider bounds
            self.arrow_pos = max(
                self.slider_rect.left + half_w,
                min(self.arrow_pos, self.slider_rect.right - half_w)
            )

            # Draw the pointer using its CENTER position
            self.screen.blit(
                self.pointer,
                (
                    int(self.arrow_pos - half_w),
                    self.slider_rect.centery - self.pointer.get_height() - 10
                )
            )

            # --- DRAW LIFE BOXES WITH CHARACTER ICONS ---

            # Box size and padding
            box_w, box_h = self.screen_w*.291, self.screen_h*.092
            padding = 20
            icon_spacing = self.screen_w*.041
            icon_scale = 0.4 

            # TEAM 1 (Top Left)
            pygame.draw.rect(self.screen, (133, 94, 66), (padding, padding, box_w, box_h), border_radius=10)
            pygame.draw.rect(self.screen, (101, 67, 33), (padding, padding, box_w, box_h), 2, border_radius=10)

            # Flip Team1 character image so it faces right
            char1_img = pygame.transform.flip(self.player1.stand, True, False)
            char1_img = pygame.transform.scale(
                char1_img,
                (int(char1_img.get_width() * icon_scale), int(char1_img.get_height() * icon_scale))
            )

            for i in range(self.plank_top.lives):
                x = padding + 15 + i * icon_spacing
                y = padding + (box_h - char1_img.get_height()) // 2
                self.screen.blit(char1_img, (x, y))

            # TEAM 2 (Top Right)
            pygame.draw.rect(self.screen, (133, 94, 66),
                            (self.screen_w - box_w - padding, padding, box_w, box_h),
                            border_radius=10)
            pygame.draw.rect(self.screen, (101, 67, 33),
                            (self.screen_w - box_w - padding, padding, box_w, box_h),
                            2, border_radius=10)

            # Team2 character faces right naturally
            char2_img = pygame.transform.scale(
                self.player2.stand,
                (int(self.player2.stand.get_width() * icon_scale),
                int(self.player2.stand.get_height() * icon_scale))
            )
            for i in range(self.plank_bottom.lives):
                x = self.screen_w - padding - (i + 1) * (char2_img.get_width() + 5)
                y = padding + (box_h - char2_img.get_height()) // 2
                self.screen.blit(char2_img, (x, y))

            # draw parrot
            self.screen.blit(self.parrot, self.parrot_pos)

            # draw chest
            self.chest_scene.draw()

            # draw game over image
            if self.game_over:
                rect = self.go_pic.get_rect(center=(self.screen_w//2, self.screen_h//2))
                self.screen.blit(self.go_pic, rect)

            # draw any active break sequences on top
            for seq in self.break_sequences:
                seq.draw(self.screen)

            pygame.display.flip()

def play_plank_game(grade, lesson):
    GamePlay(grade, lesson)
