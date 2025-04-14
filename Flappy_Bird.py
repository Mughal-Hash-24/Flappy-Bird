import pygame
import math
import random

pygame.init()
clock = pygame.time.Clock()

win_res = (800, 600)

window = pygame.display.set_mode(win_res)

bg_color = (150, 220, 255)

font = pygame.font.SysFont("Arial", 45)
def score_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    window.blit(screen_text, [x, y])

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (200, win_res[1] / 2)
        self.vel = 0
        self.acc = 0.2
        self.draw()  # Call the draw method during initialization

    def draw(self):
        pygame.draw.circle(self.image, (255, 0, 0), (25, 25), 25)
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect

    def update(self):
        if self.rect.y >= 0 and self.rect.y <= win_res[1]-55:
            self.vel += self.acc
            self.rect.y += self.vel

    def jump(self):
        self.vel = -6

class Obstacles():
    def __init__(self, x, y, width, height, gap):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gap = gap
        self.vel = 3
    
    def draw(self, win):
        pygame.draw.rect(win, (0,0,255), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, (0,0,255), (self.x, self.y + self.height + self.gap, self.width, self.height))

    def update(self):
        self.x -= self.vel

def game_loop():

    score = 0

    bird = Bird()

    obstacles = []

    obstacle_spawn_timer = pygame.time.get_ticks()
    obstacle_spawn_interval = 3000  # Time interval in milliseconds (2 seconds)

    obstacle = Obstacles(790, 0, 100, random.randint(200, 400), 200)
    obstacles.append(obstacle)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird)

    game_over = False
    running = True
    while running:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
            score_screen("Game Over! Press Enter to restart", (0,0,0),120, win_res[1]/2-30)


        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        bird.jump()

            if bird.rect.y <= 0 or bird.rect.y >= win_res[1] - 50:
                game_over = True

            current_time = pygame.time.get_ticks()
            
            # Check if it's time to spawn a new obstacle
            if current_time - obstacle_spawn_timer >= obstacle_spawn_interval:
                obstacle_spawn_timer = current_time
                new_obstacle = Obstacles(790, 0, 100, random.randint(200, 380), 200)
                obstacles.append(new_obstacle)
                score += 1

            window.fill(bg_color)

            for obs in obstacles:
                top_obs_rect = pygame.Rect(obs.x, obs.y, obs.width, obs.height)
                bottom_obs_rect = pygame.Rect(obs.x, obs.y + obs.height + obs.gap, obs.width, obs.height)
                
                if bird.rect.colliderect(top_obs_rect) or bird.rect.colliderect(bottom_obs_rect):
                    game_over = True

            for obs in obstacles.copy():
                if obs.x + obs.width < 0:
                    obstacles.remove(obs)

            for obs in obstacles:
                obs.draw(window)
                obs.update()

            all_sprites.draw(window)

            score_screen("Score: "+str(score), (0,0,0),10, 10)

            all_sprites.update()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

game_loop()