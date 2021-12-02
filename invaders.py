import pygame
import os
import sys
import time
import random
from pygame import mixer

pygame.init()
icon = pygame.image.load(os.path.join("assets", "GameIcon.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("***** ***")
WIDTH, HEIGHT = 750, 750
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.mixer.init()

SHIP = pygame.image.load(os.path.join("assets", "SHIP.png"))
ZIOBRO = pygame.transform.scale(pygame.image.load(os.path.join("assets", "ZIOBRO.png")), (90, 95))
DUDA = pygame.transform.scale(pygame.image.load(os.path.join("assets", "DUDA.png")), (110, 115))
KACZOR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "KACZOR.png")), (90, 95))
LASER_YELLOW = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
HEART = pygame.transform.scale(pygame.image.load(os.path.join("assets", "heart.png")), (50,50))
BG1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
BG1_SHOP = pygame.transform.scale(BG1, (200,200))
BG0 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "black.jpg")), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "flappy.png")), (WIDTH, HEIGHT))
BG2_SHOP = pygame.transform.scale(BG2, (200,200))
BG3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sejm.jpg")), (WIDTH, HEIGHT))
BG3_SHOP = pygame.transform.scale(BG3, (200,200))
BG4 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "purple.jpg")), (WIDTH, HEIGHT))
BG4_SHOP = pygame.transform.scale(BG4, (200,200))
BG5 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue.png")), (WIDTH, HEIGHT))
BG5_SHOP = pygame.transform.scale(BG5, (200,200))
BG6 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "grass.jpg")), (WIDTH, HEIGHT))
BG6_SHOP = pygame.transform.scale(BG6, (200,200))
MACIEREWICZ = pygame.transform.scale(pygame.image.load(os.path.join("assets", "MACIEREWICZ.png")),(70,100))
SASIN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "SASIN.png")),(70,100))
BACKGROUND = 0
BALANCE = 1000
HIGHSCORE = 0
ODBLOKOWANE = []
ZABLOKOWANE = pygame.image.load(os.path.join("assets", "100.png"))

if os.path.isfile('save.txt'):
      with open('save.txt', 'r') as f:
            [BACKGROUND, BALANCE, HIGHSCORE] = f.readline().split(" ")
            BACKGROUND, BALANCE, HIGHSCORE = int(BACKGROUND), int(BALANCE), int(HIGHSCORE)
            ODBLOKOWANE = f.readline().split(',')
            ODBLOKOWANE = [int(x) for x in ODBLOKOWANE if x.strip()]
            print(ODBLOKOWANE)

BACKGROUNDS = [BG0, BG1, BG2, BG3, BG4, BG5, BG6]

class Laser:
      def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.mask = pygame.mask.from_surface(self.img)
      def draw(self, window):
            window.blit(self.img, (self.x, self.y))

      def move(self, vel):
            self.y += vel
      def off_screen(self, height):
            return not (self.y <= height and self.y >= 0)
      def collision(self, obj):
            return collide(obj, self)

class Ship:
      COOLDOWN = 30
      def __init__(self, x, y, health=100):
            self.x = x
            self.y = y
            self.health = health
            self.ship_img = None
            self.laser_img = None
            self.lasers = []
            self.cool_down_counter = 0

      def draw(self, window):
            for laser in self.lasers:
                  laser.draw(window)
            window.blit(self.ship_img, (self.x, self.y))

      def move_lasers(self, vel, obj):
            self.cooldown()
            for laser in self.lasers:
                  laser.move(vel)
                  if laser.off_screen(HEIGHT):
                        self.lasers.remove(laser)
                  elif laser.collision(obj):
                        obj.health -= 10
                        self.lasers.remove(laser)

      def cooldown(self):
            if self.cool_down_counter >= self.COOLDOWN:
                  self.cool_down_counter = 0
            elif self.cool_down_counter > 0:
                  self.cool_down_counter += 1

      def shoot(self):
            if self.cool_down_counter == 0:
                  laser = Laser(self.x, self.y, self.laser_img)
                  self.lasers.append(laser)
                  self.cool_down_counter = 1


      def get_width(self):
            return self.ship_img.get_width()
      def get_height(self):
            return self.ship_img.get_height()

class Player(Ship):
      def __init__(self, x, y, health=100):
            super().__init__(x, y, health)
            self.ship_img = SHIP
            self.laser_img = LASER_YELLOW
            self.mask = pygame.mask.from_surface(self.ship_img)
            self.max_health = health

      def move_lasers(self, vel, objs):
            self.cooldown()
            for laser in self.lasers:
                  laser.move(vel)
                  if laser.off_screen(HEIGHT):
                        self.lasers.remove(laser)
                  else:
                        for obj in objs:
                              if laser.collision(obj):
                                    objs.remove(obj)
                                    if laser in self.lasers:
                                          self.lasers.remove(laser)

      def healthbar(self, window):
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
      
      def draw(self, window):
            super().draw(window)
            self.healthbar(window)

class Enemy(Ship):
      COLOR_MAP = {
            "red":(DUDA, RED_LASER),
            "blue":(ZIOBRO, BLUE_LASER),  
            "green":(KACZOR, GREEN_LASER),
            "purple":(MACIEREWICZ, RED_LASER),
            "yellow":(SASIN, GREEN_LASER)
      }
      def __init__(self, x, y, color, health=100):
            super().__init__(x, y, health)
            self.ship_img, self.laser_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.ship_img)
      
      def move(self, vel):
            self.y += vel

      def shoot(self):
            if self.cool_down_counter == 0:
                  laser = Laser(self.x, self.y, self.laser_img)
                  self.lasers.append(laser)
                  self.cool_down_counter = 1

def collide(obj1, obj2):
      offset_x = obj2.x - obj1.x
      offset_y = obj2.y - obj1.y
      return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def save(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE):
      with open('save.txt', 'w') as f:
            f.write(str(BACKGROUND) + " " + str(BALANCE) + " " + str(HIGHSCORE))
            f.write('\n')
            for i in ODBLOKOWANE:
                  f.write(str(i) + ',')


def main(BACKGROUND, BALANCE, HIGHSCORE):

      mixer.music.load(os.path.join("music", "background.mp3"))
      mixer.music.play(-1)

      run = True
      FPS = 60
      level = 2010
      lives = 5
      main_font = pygame.font.Font(os.path.join("assets", "INVASION2000.ttf"), 40)
      lost_font = pygame.font.Font(os.path.join("assets", "INVASION2000.ttf"), 60)
      player_vel = 7
      player = Player(300, 650)

      enemies = []
      wave_length = 0
      enemy_vel = 2

      laser_vel = 5

      lost = False
      lost_count = 0

      bullet_sound = mixer.Sound(os.path.join("music", "laser.wav"))
      destroy_sound = mixer.Sound(os.path.join("music", "explosion.wav"))

      clock = pygame.time.Clock()

      def redraw_window(window):
            window.blit(BACKGROUNDS[BACKGROUND], (0,0))
            level_label = main_font.render(f"Rok: {level}", 1, (255, 255, 255))
            for enemy in enemies:
                  enemy.draw(window)
            player.draw(window)
            window.blit(level_label, (10, 10))
            if (lives >= 1):
                  window.blit(HEART, (WIDTH - HEART.get_width() - 5, 10))
                  if (lives >= 2):
                        window.blit(HEART, (WIDTH - HEART.get_width() * 2 - 5, 10))
                        if (lives >= 3):
                              window.blit(HEART, (WIDTH - HEART.get_width() * 3 - 5, 10))
                              if (lives >= 4):
                                    window.blit(HEART, (WIDTH - HEART.get_width() * 4 - 5, 10))
                                    if (lives == 5):
                                          window.blit(HEART, (WIDTH - HEART.get_width() * 5 - 5, 10))

            if lost:
                  lost_label = lost_font.render("PISOWCY WYGRALI", 1, (255,255,255))
                  window.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            pygame.display.update()

      while run:
            clock.tick(FPS)
            
            if lives <= 0 or player.health <= 0:
                  lost = True
                  lost_count += 1

            redraw_window(window)

            if lost:
                  if lost_count > FPS * 3:
                        run = False
                        BALANCE += (level - 2011) * 5
                        HIGHSCORE = max(HIGHSCORE, level)
                        
                  else:
                        continue

            if len(enemies) == 0:
                  level += 1
                  wave_length += 2
                  for i in range(wave_length):
                        enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red","blue","green","purple","yellow"]))
                        enemies.append(enemy)

            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        save(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE)
                        quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0: #left
                  player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #right
                  player.x += player_vel
            if keys[pygame.K_w] and player.y - player_vel > 0: #up
                  player.y -= player_vel
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: #down
                  player.y += player_vel
            if keys[pygame.K_SPACE]:
                  player.shoot()
                  bullet_sound.play()
            if keys[pygame.K_ESCAPE]:
                  main_menu(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE)

            for enemy in enemies[:]:
                  enemy.move(enemy_vel)
                  enemy.move_lasers(laser_vel, player)

                  if random.randrange(0, 110) == 1:
                        enemy.shoot()

                  if collide(enemy, player):
                        player.health -= 10
                        enemies.remove(enemy)
                        destroy_sound.play()

                  if enemy.y + enemy.get_height() > HEIGHT:
                        lives -= 1
                        enemies.remove(enemy)
                  
            player.move_lasers(-laser_vel, enemies)
      main_menu(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE)
def shop(BACKGROUND, ODBLOKOWANE, BALANCE):
      run = True
      balance_font = pygame.font.Font(os.path.join("assets", "INVASION2000.ttf"), 60)
      while run:
            window.blit(BACKGROUNDS[BACKGROUND], (0,0))
            if 1 in ODBLOKOWANE: 
                  window.blit(BG1_SHOP, (38, 50))
            else:
                  window.blit(ZABLOKOWANE, (38, 50))
            if 2 in ODBLOKOWANE:
                  window.blit(BG2_SHOP, (275, 50))
            else:
                  window.blit(ZABLOKOWANE, (275, 50))
            if 3 in ODBLOKOWANE:
                  window.blit(BG3_SHOP, (512, 50))
            else:
                  window.blit(ZABLOKOWANE, (512, 50))
            if 4 in ODBLOKOWANE:
                  window.blit(BG4_SHOP, (38, 300))
            else:
                  window.blit(ZABLOKOWANE, (38, 300))
            if 5 in ODBLOKOWANE:
                  window.blit(BG5_SHOP, (275, 300))
            else:
                  window.blit(ZABLOKOWANE, (275, 300))
            if 6 in ODBLOKOWANE:
                  window.blit(BG6_SHOP, (512, 300))
            else:
                  window.blit(ZABLOKOWANE, (512, 300))
            balance_label = balance_font.render(f"Balance: {BALANCE}", 1, (255,255,255))
            window.blit(balance_label, (WIDTH/2 - balance_label.get_width()/2, 600))
            pygame.display.update()
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        save(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE)
                        quit()
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if mouse[0] >= 38 and mouse[0] <= 238 and mouse[1] >= 50 and mouse[1] <= 250:
                              if 1 in ODBLOKOWANE:
                                    BACKGROUND = 1
                              elif BALANCE >= 100:
                                    BALANCE -= 100
                                    ODBLOKOWANE.append(1)
                        if mouse[0] >= 275 and mouse[0] <= 475 and mouse[1] >= 50 and mouse[1] <= 250:
                              if 2 in ODBLOKOWANE:
                                    BACKGROUND = 2
                              elif BALANCE >= 100:
                                    BALANCE -= 100
                                    ODBLOKOWANE.append(2)
                        if mouse[0] >= 512 and mouse[0] <= 712 and mouse[1] >= 50 and mouse[1] <= 250:
                              if 3 in ODBLOKOWANE:
                                    BACKGROUND = 3
                              elif BALANCE >= 100:
                                    BALANCE -= 100
                                    ODBLOKOWANE.append(3)
                        if mouse[0] >= 38 and mouse[0] <= 238 and mouse[1] >= 300 and mouse[1] <= 500:
                              if 4 in ODBLOKOWANE:
                                    BACKGROUND = 4
                              elif BALANCE >= 100:
                                    BALANCE -= 100
                                    ODBLOKOWANE.append(4)
                        if mouse[0] >= 275 and mouse[0] <= 475 and mouse[1] >= 300 and mouse[1] <= 500:
                              if 5 in ODBLOKOWANE:
                                    BACKGROUND = 5
                              elif BALANCE >= 100:
                                    BALANCE -= 100
                                    ODBLOKOWANE.append(5)
                        if mouse[0] >= 512 and mouse[0] <= 712 and mouse[1] >= 300 and mouse[1] <= 500:
                              if 6 in ODBLOKOWANE:
                                    BACKGROUND = 6
                              elif BALANCE >= 100:
                                    BALANCE -= 100
                                    ODBLOKOWANE.append(6)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                  main_menu(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE)
            


def main_menu(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE):
      mixer.music.load(os.path.join("music", "wii.mp3"))
      mixer.music.play(-1)
      title_font = pygame.font.Font(os.path.join("assets", "INVASION2000.ttf"), 40)
      bg_font = pygame.font.Font(os.path.join("assets", "INVASION2000.ttf"), 40)
      run = True
      while run:
            window.blit(BACKGROUNDS[BACKGROUND], (0,0))
            title_label = title_font.render("Press SPACE to begin...", 1, (255,255,255))
            bg_label = bg_font.render("shop", 1, (255,255,255))
            bg_label2 = bg_font.render(f"HIGH SCORE: {HIGHSCORE}", 1, (255,255,255))
            window.blit(bg_label2, (WIDTH/2 - bg_label2.get_width()/2, 200))
            pygame.draw.rect(window, (255,0,0), (WIDTH/2 - (bg_label.get_width() + 20) / 2, 450 - bg_label.get_height() / 2 + 20, bg_label.get_width() + 20, 50))
            window.blit(bg_label, (WIDTH/2 - bg_label.get_width()/2, 450))
            window.blit(title_label, (WIDTH/2 - title_label.get_width()/2,300))
            pygame.display.update()
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        save(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE)
                        run = False
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if mouse[0] >= WIDTH/2 - (bg_label.get_width() + 20) / 2 and mouse[0] <= WIDTH/2 - (bg_label.get_width() + 20) / 2 + bg_label.get_width() + 20:
                              if mouse[1] >= 450 - bg_label.get_height() / 2 + 10 and mouse[1] <= 450 - bg_label.get_height() / 2 + 10 + 50:
                                    shop(BACKGROUND, ODBLOKOWANE, BALANCE)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                  main(BACKGROUND, BALANCE, HIGHSCORE) 
      pygame.quit()

main_menu(BACKGROUND, ODBLOKOWANE, BALANCE, HIGHSCORE)


#ZAPISYWANIE
#sasin macierewicz
