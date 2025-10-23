import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Defense")

# Load assets
background = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bear_img = pygame.transform.scale(pygame.image.load("bear.png"), (80, 80))
arrow_img = pygame.transform.scale(pygame.image.load("arrow.png"), (20, 40))
enemy_img = pygame.transform.scale(pygame.image.load("enemy.png"), (60, 60))
balloon_img = pygame.transform.scale(pygame.image.load("balloon.png"), (50, 70))

# Load sounds and adjust volume
hit_sound = pygame.mixer.Sound("hit.wav")
hit_sound.set_volume(0.1)
pop_sound = pygame.mixer.Sound("pop.wav")
pop_sound.set_volume(0.1)

# Fonts
font = pygame.font.SysFont("Arial Black", 36)
small_font = pygame.font.SysFont("Arial Black", 24)

# Clock
clock = pygame.time.Clock()

# Game variables
score = 0
arrow_speed = -10
enemy_speed = 3
start_time = 0
hearts = 3

# Classes
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = arrow_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += arrow_speed
        if self.rect.y < -40:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        side = random.choice(["left", "right"])
        y = random.randint(50, HEIGHT - 200)
        if side == "left":
            self.rect = self.image.get_rect(center=(0, y))
            self.direction = 1
        else:
            self.rect = self.image.get_rect(center=(WIDTH, y))
            self.direction = -1

    def update(self):
        self.rect.x += self.direction * enemy_speed
        if self.rect.x < -60 or self.rect.x > WIDTH + 60:
            self.kill()

# Functions
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def start_screen():
    screen.blit(background, (0, 0))
    draw_text("Balloon Defense", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 3)
    draw_text("Press ENTER to Start", small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def game_over_screen(final_score, play_time):
    screen.blit(background, (0, 0))
    draw_text("Game Over", font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 3)
    draw_text(f"Score: {final_score}", small_font, (255, 255, 0), screen, WIDTH // 2, HEIGHT // 2)
    draw_text(f"Time: {play_time:.1f} sec", small_font, (255, 255, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("Press ENTER to Restart", small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 80)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Main game loop
running = True
while running:
    start_screen()
    score = 0
    hearts = 3
    start_time = pygame.time.get_ticks()
    bear_rect = bear_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    balloon_rect = balloon_img.get_rect(center=(bear_rect.centerx, bear_rect.top - 50))
    arrows = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    spawn_timer = 0

    playing = True
    while playing:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arrow = Arrow(bear_rect.centerx, bear_rect.top)
                    arrows.add(arrow)
                    pop_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bear_rect.left > 0:
            bear_rect.x -= 5
        if keys[pygame.K_RIGHT] and bear_rect.right < WIDTH:
            bear_rect.x += 5

        balloon_rect.centerx = bear_rect.centerx
        balloon_rect.bottom = bear_rect.top - 10

        spawn_timer += 1
        if spawn_timer > 60:
            enemy = Enemy()
            enemies.add(enemy)
            spawn_timer = 0

        arrows.update()
        enemies.update()

        for arrow in arrows:
            hit_enemies = pygame.sprite.spritecollide(arrow, enemies, True)
            if hit_enemies:
                arrow.kill()
                score += 1
                hit_sound.play()

        for enemy in enemies:
            if enemy.rect.colliderect(balloon_rect):
                hearts -= 1
                enemy.kill()
                if hearts <= 0:
                    playing = False

        screen.blit(background, (0, 0))
        screen.blit(bear_img, bear_rect)
        screen.blit(balloon_img, balloon_rect)
        arrows.draw(screen)
        enemies.draw(screen)
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        draw_text(f"Score: {score}", small_font, (255, 255, 0), screen, WIDTH - 100, 30)
        draw_text(f"Time: {elapsed_time:.1f}s", small_font, (255, 255, 0), screen, WIDTH - 100, 60)
        draw_text(f"Hearts: {hearts}", small_font, (255, 0, 0), screen, WIDTH - 100, 90)
        pygame.display.flip()

    game_over_screen(score, elapsed_time)