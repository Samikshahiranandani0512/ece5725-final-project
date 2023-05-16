import pygame 
from pygame.locals import *   # for event MOUSE variables
import os   
import RPi.GPIO as GPIO
import sys
import time


# Display on piTFT, Track mouse clicks on piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon')   
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB')     
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()

pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0,255,0
size = width, height = 320, 240 

screen = pygame.display.set_mode((320, 240))
button_font = pygame.font.Font(None, 25)
text_font = pygame.font.Font(None, 20)

# Erase the Work space
screen.fill(BLACK)  
speed_const = 1

CIRCLE = (160, 120)
QUIT_BUTTON = (280, 200)
START_BUTTON = (50, 200)
LEFT_HEADING = (40, 70)
RIGHT_HEADING = (240, 70)

running = False

start_time = time.time()

current_color = RED

def draw_display(display, x, y):             
    # for my_text, text_pos in buttons.items():  
    line_space = 0 
    col_space = 60
    print_display = display.copy()
    print_display.reverse()
    for item in print_display:  
        text_surface = text_font.render(item['command'], True, WHITE)   
        rect = text_surface.get_rect(center=(x, y+line_space))
        screen.blit(text_surface, rect)
        text_num = text_font.render(item['time'], True, WHITE)   
        rect_num = text_num.get_rect(center=(x+col_space, y+line_space))
        line_space += 30
        screen.blit(text_num, rect_num)
        pygame.display.update()

def draw_button():       
    if running: 
        button_text = "STOP" 
        current_color = RED
    else: 
        button_text = "RESUME"
        current_color = GREEN
    text_surface = button_font.render(button_text, True, WHITE)   
    pygame.draw.circle(screen, current_color,[160, 120], 40) 
    rect = text_surface.get_rect(center=CIRCLE)
    quit_text = button_font.render("QUIT", True, WHITE)   
    quit_rect = quit_text.get_rect(center=QUIT_BUTTON)
    heading1 = text_font.render("Left History", True, WHITE)   
    heading1_rect = heading1.get_rect(center=LEFT_HEADING)
    screen.blit(heading1, heading1_rect)
    heading2 = text_font.render("Right History", True, WHITE)   
    heading2_rect = heading2.get_rect(center=RIGHT_HEADING)
    screen.blit(heading2, heading2_rect)
    start_text = button_font.render("START", True, WHITE)   
    start_rect = start_text.get_rect(center=START_BUTTON)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    screen.blit(text_surface, rect)
    pygame.display.flip()

    for event in pygame.event.get():                  
        if(event.type is MOUSEBUTTONUP):            
            pos = pygame.mouse.get_pos() 
            x,y = pos
            if (x < CIRCLE[0] + 40 and x > CIRCLE[0] - 40 and y < CIRCLE[1] + 40 and y > CIRCLE[1] - 40): 
                
                if (running): 
                    stop_motor(pwm_left)
                    stop_motor(pwm_right)
                    stop_start = time.time() - start_time
                else: 
                    if (stop_start):
                        stop_elapsed = time.time() - start_time - stop_start

                    left_state = left_queue[1]['command']
                    if (left_state == 'Clockwise'):
                        run_clockwise(pwm_left, 100)
                    elif (left_state == 'CClockwise'): 
                        run_counterclockwise(pwm_left, 100)
                    right_state = right_queue[1]['command']
                    if (right_state == 'Clockwise'):
                        run_clockwise(pwm_right, 100)
                    elif (right_state == 'CClockwise'): 
                        run_counterclockwise(pwm_right, 100)
                    


                running = not running
                print("Detected button")
                draw_button()