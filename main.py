import pygame
from sys import exit
from random import randint, choice
import json



class Player(pygame.sprite.Sprite):
    """
       Represents the player character in the game.

       Attributes:
           image: The current image of the player.
           rect: The rectangular area of the player sprite.
           gravity: The current gravity affecting the player.
       """
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('jump.mp3')
        self.jump_sound.set_volume(0.5)

        self.high_score = self.load_high_score()

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    @staticmethod
    def load_high_score(file="high_scores.json") -> int:
        try:
            with open(file, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except (IOError, json.JSONDecodeError):
            return 0
    @staticmethod
    def save_high_score(score: int, file="high_scores.json"):
        try:
            with open(file, "w") as f:
                json.dump({"high_score": score}, f)
        except IOError:
            print("Error saving high score.")

    def display_high_score(self, screen, test_font):
        """Display the high score on the screen."""
        high_score_surf = test_font.render(f'High Score: {self.high_score}', False, (111, 196, 169))
        high_score_rect = high_score_surf.get_rect(center=(600, 280))
        screen.blit(high_score_surf, high_score_rect)

    def update_high_score(self, score: int):
        """Check if the current score is a new high score and save it."""
        if score > self.high_score:
            self.high_score = score
            self.save_high_score(self.high_score)



class Obstacle(pygame.sprite.Sprite):
    """
    Represents an obstacle in the game

    Attributes:
        image: The current image of the obstacle, depending on its type (fly or snail)
        rect: the rectangular area of the obstacle sprite, used for pos and collisions
        frames: A list of frames for animating the obstacles
        animation_index: The current frame index used for animation
        speed: The speed at which the obstacle moves across the screen
    """
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load('Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        self.speed = speed
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 10
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collisoin_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True




#variables
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Serbi Space Run')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Pixeltype.ttf', 50)  # font type , font size
game_active = False
start_time = 0
score = 0
speed = 5
#bg_music = pygame.mixer.Sound('music.wav')
#bg_music.play(loops = -1)
blink = True
blink_start_time = 0
blink_interval = 350
#high_score = load_high_score("high_scores.json")


#Groups
player = pygame.sprite.GroupSingle() #group single that contains sprite
player.add(Player())

obstacle_group = pygame.sprite.Group()

high_score = player.sprite.high_score

# surfaces
sky_surface = pygame.image.load('Sky.png').convert()
ground_surface = pygame.image.load('ground.png').convert()
pink_surface = pygame.image.load('Sky_Pink.png').convert()
grey_surface = pygame.image.load('Sky_Grey.png').convert()
# list of bgs
#backgrounds = [sky_surface, pink_surface, grey_surface]

# intro screen image
player_stand = pygame.image.load('player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # scale and rotate
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_title_surf = test_font.render('Serbi\'s Space Run', False, (111, 196, 169))
game_title_rect = game_title_surf.get_rect(center=(400, 80))

game_msg = test_font.render('Press space to run', False, (111, 196, 169))
game_msg_rect = game_msg.get_rect(center=(400, 340))

# timer!
obstacle_timer = pygame.USEREVENT + 1 #avoids conflict with events
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():  # get us all events
        if event.type == pygame.QUIT:
            pygame.quit()  # opposite of pygame.init
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['snail','snail', 'snail', 'snail', 'fly'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:
        screen.blit(sky_surface, (0, 0))  # 0 from left ,0from top
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        if score % 15 == 0 and score > 0:
            speed += 5
            last_speed_update = score
            print(f'Speed increased to: {speed}')
            screen.blit(pink_surface, (0, 0))
            level_up_surf = test_font.render("Level Up!", False, (255, 0, 0))
            level_up_rect = level_up_surf.get_rect(center=(400, 200))
            screen.blit(level_up_surf, level_up_rect)



        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        game_active = collisoin_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        player.sprite.display_high_score(screen, test_font)

        #player.update_high_score(score)
        #player.display_high_score(screen)

        #high_score_surf = test_font.render(f'High Score: {high_score}', False, (111, 196, 169))
        #high_score_rect = high_score_surf.get_rect(center=(600, 280))
        #screen.blit(high_score_surf, high_score_rect)

        score_msg = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_msg_rect = score_msg.get_rect(center=(200, 280))
        screen.blit(score_msg, score_msg_rect)
        screen.blit(game_title_surf, game_title_rect)

        if score == 0:
            current_time = pygame.time.get_ticks()
            if current_time - blink_start_time >= blink_interval:
                blink = not blink
                blink_start_time = current_time
            if blink:
                screen.blit(game_msg, game_msg_rect)

        else:
            screen.blit(score_msg, score_msg_rect)

    pygame.display.update()
    clock.tick(60)

    if score > high_score:
        high_score = score
        player.sprite.update_high_score(high_score)
