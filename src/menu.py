import pygame 
from pygame.locals import *   # for event MOUSE variables
import os   
import RPi.GPIO as GPIO
import sys
import time
import button
import subprocess
from servo_control import pen_lift

# Display on piTFT, Track mouse clicks on piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon')   
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB')     
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()

pygame.mouse.set_visible(False)

#create game window
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
options_img = pygame.image.load("button_options.png").convert_alpha()
quit_img = pygame.image.load("button_quit.png").convert_alpha()
back_img = pygame.image.load('button_back.png').convert_alpha()
auto_img = pygame.image.load('auto.png').convert_alpha()
manual_img = pygame.image.load('manual.png').convert_alpha()
rect_img = pygame.image.load('rect.PNG').convert_alpha()
tri_img = pygame.image.load('tri.PNG').convert_alpha()


#create button instances
options_button = button.Button(60, 20, options_img, 1)
quit_button = button.Button(100, 140, quit_img, 1)
back_button = button.Button(100, 120, back_img, 1)
manual_button = button.Button(80, 70, manual_img, 1)
auto_button = button.Button(200, 70, auto_img, 1)
rectangle_button = button.Button(60, 20, rect_img, 1)
tri_button = button.Button(60, 120, tri_img, 1)

pen_up = True


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
while run:

  screen.fill((52, 78, 91))

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      if options_button.draw(screen):
        menu_state = "options"
      if quit_button.draw(screen):
        run = False
    #check if the options menu is open
    if menu_state == "options":
      if manual_button.draw(screen):
        menu_state = "manual"
        print("manual")
      if auto_button.draw(screen):
        menu_state = "auto"
      #draw the different options buttons
      if back_button.draw(screen):
        menu_state = "main"
    if menu_state == "auto":
      if rectangle_button.draw(screen):
        subprocess.run(["python3", "rectangle.py"])
        print("Rectangle")
        menu_state = "main"
      if tri_button.draw(screen):
        subprocess.run(["python3", "triangle.py"])
        print("Triangle")
        menu_state = "main"
    if menu_state == "manual":
      # if (pen_up): 
      #   pen_lift(1)
      #   pen_up = False
      if rectangle_button.draw(screen):
        subprocess.run(["python3", "control_rect.py"])
        # pen_lift(0)
        # pen_up = True
        print("Rectangle")
        menu_state = "main"
      if tri_button.draw(screen):
        subprocess.run(["python3", "control_tri.py"])
        # pen_lift(0)
        # pen_up = True
        print("Triangle")
        menu_state = "main"

  else:
    draw_text("Begin", font, TEXT_COL, 100, 100)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONUP:
      game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()