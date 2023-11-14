import pygame
import random
import time


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bird_midflap = pygame.image.load("yellowbird-midflap.png").convert_alpha()
        bird_midflap = pygame.transform.rotozoom(bird_midflap,0,1.3)
        bird_downflap = pygame.image.load("yellowbird-downflap.png").convert_alpha()
        bird_downflap = pygame.transform.rotozoom(bird_downflap, 0, 1.3)
        bird_upflap = pygame.image.load("yellowbird-upflap.png").convert_alpha()
        bird_upflap = pygame.transform.rotozoom(bird_upflap, 0, 1.3)
        self.bird_flight = [bird_midflap,bird_downflap,bird_upflap]
        self.bird_index = 0

        self.image = self.bird_flight[self.bird_index]
        self.rect = self.image.get_rect(center=(100,300))

        self.jump_sound = pygame.mixer.Sound("wing.wav")
        self.jump_sound.set_volume(0.11)
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 0:
            self.gravity = -7


    def gravity_function(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
        if self.rect.top <= 0:
            self.rect.top = 0

    def animation(self):
        self.bird_index += 0.1
        if self.bird_index >= len(self.bird_flight):
            self.bird_index = 0
        self.image = self.bird_flight[int(self.bird_index)]
    def update(self):
        self.player_input()
        if game_active or game_over:
            self.gravity_function()
        self.animation()


class Pipes(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        values = [200, 250, 300, 350, 400, 450]
        random_pos = random.choice(values)
        if type == "pipe1":
            pipe1 = pygame.image.load("pipe-green.png").convert_alpha()
            pipe1 = pygame.transform.rotozoom(pipe1, 0, 1.3)
            self.image = pipe1
            self.rect = self.image.get_rect(midtop=(400, random_pos))
            global pos
            pos = self.rect.y

        else:
            pipe2 = pygame.image.load("pipe-green.png").convert_alpha()
            pipe2 = pygame.transform.rotozoom(pipe2, 180, 1.3)
            pipe2 = pygame.transform.flip(pipe2, True, False)
            self.image = pipe2
            if pos == 200:
                self.rect = self.image.get_rect(midbottom=(400, 50))
            elif pos == 250:
                self.rect = self.image.get_rect(midbottom=(400, 100))
            elif pos == 300:
                self.rect = self.image.get_rect(midbottom=(400, 150))
            elif pos == 350:
                self.rect = self.image.get_rect(midbottom=(400, 200))
            elif pos == 400:
                self.rect = self.image.get_rect(midbottom=(400, 250))
            elif pos == 450:
                self.rect = self.image.get_rect(midbottom=(400, 300))

    def update(self):
        if game_active and pipe_timer != 0:
            self.rect.x -= 3
        self.destroy()
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

score_value = 0
def score_increase():
    global score_value
    score_value += 1
    font = pygame.font.Font("Pixeltype.ttf", 70)
    score_text = font.render(str(score_value), True, black)
    score_sound = pygame.mixer.Sound("point.wav")
    score_sound.set_volume(0.35)
    score_sound.play()

pygame.init()

display_width = 350
display_height = 600
x = (610,100)
black = (0,0,0)
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Not Flappy Bird")
clock = pygame.time.Clock()

score_font = pygame.font.Font("Pixeltype.ttf", 70)
score_text = score_font.render(str(score_value), True, black)
score_rect = score_text.get_rect(center=(175,50))

game_active = False
game_intro = True
game_over = False


player = pygame.sprite.GroupSingle()
player.add(Player())

pipe_group = pygame.sprite.Group()

background = pygame.image.load("background-day.png").convert_alpha()
background = pygame.transform.rotozoom(background,0,1.3)

start_message = pygame.image.load("message.png").convert_alpha()
start_message = pygame.transform.rotozoom(start_message,0,1.2)
start_message_rect = start_message.get_rect(center=(175,220))

gameover_message = pygame.image.load("gameover.png").convert_alpha()
gameover_message = pygame.transform.rotozoom(gameover_message,0,1)
gameover_message_rect = gameover_message.get_rect(center=(175,200))

ground = pygame.image.load("base.png").convert_alpha()
ground = pygame.transform.scale(ground, x)
ground_rect = ground.get_rect(midbottom=(175,600))


pipe1 = pygame.image.load("pipe-green.png").convert_alpha()
pipe1 = pygame.transform.rotozoom(pipe1,0,1.3)
pipe1_rect = pipe1.get_rect(midtop=(300, 300))

pipe2 = pygame.image.load("pipe-green.png")
pipe2 = pygame.transform.rotozoom(pipe2,180,1.3)
pipe2 = pygame.transform.flip(pipe2,True,False)
pipe2_rect = pipe2.get_rect(midbottom=(300, 150))

pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pipe_timer:
            if game_active:
                pipe_group.add(Pipes("pipe1"))
                pipe_group.add(Pipes("pipe2"))
        if event.type == pygame.KEYDOWN and pygame.K_SPACE and game_intro == True:
            game_active = True
            game_intro = False
            score_value = 0
        elif event.type == pygame.KEYDOWN and pygame.K_SPACE and game_over == True:
            pipe_group.empty()
            player.sprite.rect.y = 300
            pipe_timer = pygame.USEREVENT + 1
            game_intro = True
            game_active = False
            game_over = False
            score_value = 0


    if game_active:
        screen.blit(background,(0,0))
        pipe_group.draw(screen)
        pipe_group.update()
        pipe_hitbox = pygame.sprite.spritecollide(player.sprite,pipe_group,False)
        for pipes in pipe_hitbox:
            game_over = True

        if player.sprite.rect.bottom >= 500:
            game_over = True

        pipes_rect = pygame.sprite.Group.sprites(pipe_group)
        for pipe_location in pipes_rect:
            if player.sprite.rect.bottom <= pipe_location.rect.bottom and player.sprite.rect.top <= pipe_location.rect.top and player.sprite.rect.left >= pipe_location.rect.left and player.sprite.rect.right <= pipe_location.rect.right and player.sprite.rect.centerx == pipe_location.rect.centerx:
                score_increase()

        player.draw(screen)
        player.update()

        score_text = score_font.render(str(score_value), True, black)
        score_rect = score_text.get_rect(center=(175, 50))
        screen.blit(score_text, score_rect)

        ground_rect.x -= 3
        if ground_rect.left <= -100:
            ground_rect.right = 600
        screen.blit(ground,ground_rect)

        if game_over:
            ground_rect.x = 0
            pipe_timer = 0
            screen.blit(gameover_message,gameover_message_rect)


    if game_intro:
        screen.blit(background, (0, 0))
        screen.blit(start_message,start_message_rect)
        player.draw(screen)
        player.update()
        score_text = score_font.render(str(score_value), True, black)
        score_rect = score_text.get_rect(center=(175, 50))
        screen.blit(score_text, score_rect)



        ground_rect.x -= 3
        if ground_rect.left <= -100:
            ground_rect.right = 600
        screen.blit(ground, ground_rect)
    pygame.display.update()
    clock.tick(60)

