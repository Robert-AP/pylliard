#imports
import pygame
from pygame.locals import *
import sys
from ball import Ball
from input import Mouse
from math import sqrt
from board import Board, Hole
import time
import json


# constants
pygame.init()
FPS_CLOCK = pygame.time.Clock()
DISPLAY_SIZE = (640, 360)
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE)
RES = [31.22, 36, 581.81, 288]

COLORS = {
    'black': (0, 0, 0),
    'brown': (150, 75, 0),
    'white': (255, 255, 255),
    'purple': (128, 0, 128),
    'green': (38, 130, 35),
    'blue': (0, 0, 180),
    'light_brown': (189, 154, 122)
}

TICKRATE = 60

RESTITUTION = 0.8

BALL_RADIUS = 9
BALLS = []
ball_data = [{
    'color': COLORS['white'],
    'position': [260, 180],
    'velocity': [0, 0]
}, {
    'color': COLORS['purple'],
    'position': [340, 180],
    'velocity': [0, 0]
}, {
    'color': COLORS['purple'],
    'position': [355, 170],
    'velocity': [0, 0]
}, {
    'color': COLORS['purple'],
    'position': [370, 200],
    'velocity': [0, 0]
}, {
    'color': COLORS['purple'],
    'position': [385, 190],
    'velocity': [0, 0]
}, {
    'color': COLORS['purple'],
    'position': [385, 150],
    'velocity': [0, 0]
}, {
    'color': COLORS['purple'],
    'position': [400, 220],
    'velocity': [0, 0]
}, {
    'color': COLORS['purple'],
    'position': [400, 160],
    'velocity': [0, 0]
}, {
    'color': COLORS['blue'],
    'position': [355, 190],
    'velocity': [0, 0]
}, {
    'color': COLORS['blue'],
    'position': [370, 160],
    'velocity': [0, 0]
}, {
    'color': COLORS['blue'],
    'position': [385, 210],
    'velocity': [0, 0]
}, {
    'color': COLORS['blue'],
    'position': [385, 170],
    'velocity': [0, 0]
}, {
    'color': COLORS['blue'],
    'position': [400, 200],
    'velocity': [0, 0]
}, {
    'color': COLORS['blue'],
    'position': [400, 180],
    'velocity': [0, 0]
}, {
    'color': COLORS['blue'],
    'position': [400, 140],
    'velocity': [0, 0]
}, {
    'color': COLORS['black'],
    'position': [370, 180],
    'velocity': [0, 0]
}]
delta_x = 0
delta_y = 0

HOLE_RADIUS = 20
hole_data = [[35, 35], [320, 35], [610, 35], [35, 325], [320, 325], [615, 320]]
HOLES = []

mouse = Mouse()
board = Board()

mouse_check = False
start_time = 0
clicked = False

FONTS = {
    1: pygame.font.Font('freesansbold.ttf', 10),
    2: pygame.font.Font('freesansbold.ttf', 11),
    3: pygame.font.Font('freesansbold.ttf', 18),
    4: pygame.font.Font('freesansbold.ttf', 30)
}
f = open("data.json", )
data = json.load(f)

p1_score = 0
p2_score = 0
player_data = {'player': 1, 'color': COLORS['blue'], 'score': p1_score}


#helper functions


def get_dot_product(u, v):
    return u[0] * v[0] + u[1] * v[1]  # u = velocity of ball a, v = velocity of ball b


def get_unit(v):
    magv = sqrt(v[0] * v[0] + v[1] * v[1])  # magnitude of v
    return [v[0] / magv,v[1] / magv]  #returns initial velocities divided by magnitude


def get_projection(u, v):
    #projection of u in direction v
    k = get_dot_product(u, get_unit(v))
    return [k * v[0], k * v[1]]


def get_direction_of_perpendicular(a, b):
    if a[0] == b[0]:
        return [1, 0]
    if a[1] == b[1]:
        return [0, 1]
    m = -(b[0] - a[0]) / (b[1] - a[1])
    return get_unit([1, m])


def collide(a, u, b, v):
    # ball at a with  velocity u, ball at b with velocity v
    dir_perp = get_direction_of_perpendicular(a, b)  #gets direction of perpendicular of a and b
    uparallel = get_projection(u, dir_perp)  #gets projection of u in the direction of the perpendicular(parallel of u)
    vparallel = get_projection(v, dir_perp)  # //v
    uperpendicular = [(u[0] - uparallel[0]) * RESTITUTION,(u[1] - uparallel[1]) * RESTITUTION]  #gets perpendicular of u
    vperpendicular = [(v[0] - vparallel[0]) * RESTITUTION,(v[1] - vparallel[1]) * RESTITUTION]  # //v
    newu = [uparallel[0] + vperpendicular[0], uparallel[1] + vperpendicular[1]]  # returns the new direction for u
    newv = [vparallel[0] + uperpendicular[0], vparallel[1] + uperpendicular[1]]  # //v
    return newu, newv


#
def set_player_text():
    text = "Player " + str(player_data['player'])
    text_box = FONTS[3].render(text, True, player_data['color'])
    text_rect = text_box.get_rect()
    text_rect.center = (200, 20)
    DISPLAY.blit(text_box, text_rect)



def swap_player():
    global FONTS

    if player_data['player'] == 1:
        player_data['player'] = 2
        player_data['color'] = COLORS['purple']
        player_data['score'] = p2_score
    else:
        player_data['player'] = 1
        player_data['color'] = COLORS['blue']
        player_data['score'] = p1_score

    set_player_text()


game_over = False


def setup():
    pygame.display.set_caption("    Pylliard")
    pygame.init()
    create_balls(ball_data)
    create_holes(hole_data)


def create_balls(ball_data):

    for ball_datum in ball_data:

        ball = Ball(ball_datum['color'], ball_datum['position'], BALL_RADIUS,
                    ball_datum['velocity'])
        BALLS.append(ball)


def create_holes(hole_data):

    for hole_datum in hole_data:

        hole = Hole(hole_datum, DISPLAY)
        HOLES.append(hole)

    for hole in HOLES:
        hole.hole_draw(DISPLAY)



def collide_hole(HOLES, BALLS):
    ball_potted = False
    global p1_score
    global p2_score
    n = 0
    for ball in BALLS:

        for hole in HOLES:
            
            if ball.ball.collidepoint(hole.center):
                if ball_data[n]['color'] == player_data['color']:
                    BALLS.remove(ball)
                    if player_data['score'] == p1_score:
                        p1_score += 10
                    elif player_data['score'] == p2_score:
                        p2_score += 10
                        print("SAME COLOR BALL REMOVED")
                        n = 0
                        ball_potted = True

                elif ball_data[n]['color'] != player_data['color']:
                    if ball_data[n]['color'] != COLORS['black'] and ball_data[n]['color'] != COLORS['white']:
                        BALLS.remove(ball)
                        print("OPPOSITE COLOR BALL REMOVED")
                        if player_data['score'] == p1_score:
                            p2_score += 10
                            p1_score -= 10

                        elif player_data['score'] == p2_score:
                            p1_score += 10
                            p2_score -= 10

                        swap_player()
                        n = 0
                        ball_potted = True
                    elif ball_data[n]['color'] == COLORS['black'] or ball_data[n]['color'] == COLORS['white']:
                        BALLS.remove(ball)
                        print("WHITE OR BLACK BALL REMOVED")
                        swap_player()
                        ball_potted = True
                        win_screen(click)
        n += 1
    return ball_potted


def white_ball_checker(BALLS, mouse_data):
    global start_time
    global clicked
    global mouse_check
    global delta_x
    global delta_y
    time_passed = False
    if ball_data[0]['velocity'][0] == 0 and ball_data[0]['velocity'][1] == 0:
        for event in pygame.event.get():
            if BALLS[0].ball.collidepoint(
                    mouse_data["pos"]) and event.type == MOUSEBUTTONDOWN:
                mouse_check = True

                pygame.mouse.get_rel()
            elif mouse_check == True and event.type == MOUSEBUTTONUP:
                delta_x, delta_y = pygame.mouse.get_rel()
                start_time = time.time()
                clicked = True
                mouse_check = False

    elif time.time() - start_time > 1 and clicked:
        delta_x, delta_y = 0, 0
        time_passed = True

    return delta_x, delta_y, time_passed


def change_white_velocity(ball_data, delta_x, delta_y):
    ball_data[0]['velocity'][0] = -round(delta_x/ RESTITUTION/8, 2)
    ball_data[0]['velocity'][1] = -round(delta_y/ RESTITUTION/8, 2)
    

def update():
    global FONTS
    board.draw_table()

    for hole in HOLES:

        hole.hole_draw(DISPLAY)

    for ball in BALLS:

        ball.ball_draw(DISPLAY)
        ball.update(RES, BALLS)
        ball.ball_move()
    mouse_data = mouse.get_mouse_data()
    delta_x, delta_y, time_passed = white_ball_checker(BALLS, mouse_data)
    change_white_velocity(ball_data, delta_x, delta_y)

    ball_counter = 0
    balls_stopped = False

    font = FONTS[3]
    text = font.render("Player " + str(player_data['player']) + ":  " + str(player_data['score']), True, player_data['color'])
    text_rect = text.get_rect()
    text_rect.center = (200, 20)
    DISPLAY.blit(text, text_rect)

    for i in range(len(BALLS) - 1):
        for j in range(i + 1, len(BALLS)): 
            
            if sqrt((ball_data[i]['position'][0] + ball_data[i]['velocity'][0] - ball_data[j]['position'][0] - ball_data[j]['velocity'][0])**2 + (ball_data[i]['position'][1] + ball_data[i]['velocity'][1] - ball_data[j]['position'][1] - ball_data[j]['velocity'][1])**2) <= BALLS[i].radius + BALLS[j].radius -2:
                
                a = [ball_data[i]['position'][0], ball_data[i]['position'][1]]
                u = [ball_data[i]['velocity'][0], ball_data[i]['velocity'][1]]
                b = [ball_data[j]['position'][0], ball_data[j]['position'][1]]
                v = [ball_data[j]['velocity'][0], ball_data[j]['velocity'][1]]
                [[ball_data[i]['velocity'][0], ball_data[i]['velocity'][1]],[ball_data[j]['velocity'][0],ball_data[j]['velocity'][1]]] = collide(a, u, b, v)

        
        if ball_data[i]['velocity'][0] == 0 and ball_data[i]['velocity'][1] == 0:
            ball_counter += 1
        if ball_data[i]['velocity'][0] == -0.0 and ball_data[i]['velocity'][1] == -0.0:
            ball_counter += 1
        if ball_counter == len(BALLS):
            balls_stopped = True

            

    if not collide_hole(HOLES, BALLS) and time_passed and balls_stopped:
        swap_player()
        balls_stopped = False
        ball_counter = 0


    game_over_check()

    for event in pygame.event.get():

        if event.type == QUIT:

            pygame.quit()
            sys.exit()

    pygame.display.update()
    FPS_CLOCK.tick(TICKRATE)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    text_rect = textobj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(textobj, text_rect)


def game_over_check():
    if player_data['score'] >= 50:
        win_screen(click)


# A variable to check for the status later
click = False


def win_screen(click):
    global FONTS
    font = FONTS[4]
    while True:
        pygame.display.set_caption("    Pylliard")
        DISPLAY.fill((0, 190, 255))
        draw_text(
            "Player " + str(player_data['player']) + " has won with: " +
            str(player_data['score']) + " score", font, (0, 0, 0), DISPLAY,
            180, 40)

        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(200, 220, 200, 50)

        if back_button.collidepoint((mx, my)):
            if click:
                main_menu(click)
        pygame.draw.rect(DISPLAY, (255, 170, 0), back_button)
        font = FONTS[3]
        draw_text('BACK TO MENU', font, (255, 255, 255), DISPLAY, 235, 235)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


# Main container function that holds the buttons and game functions
def main_menu(click):
    while True:
        pygame.display.set_caption("    Pylliard")
        DISPLAY.fill((0, 190, 255))
        font = FONTS[4]
        draw_text('Main Menu', font, (0, 0, 0), DISPLAY, 217, 40)

        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(200, 100, 200, 50)
        button_2 = pygame.Rect(200, 180, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                run_how_to_play(click)
        pygame.draw.rect(DISPLAY, (255, 170, 0), button_1)
        pygame.draw.rect(DISPLAY, (255, 0, 0), button_2)

        #writing text on top of button
        font = FONTS[3]
        draw_text('PLAY', font, (255, 255, 255), DISPLAY, 270, 115)
        draw_text('HOW TO PLAY', font, (255, 255, 255), DISPLAY, 240, 195)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def run_how_to_play(click):
    global FONTS
    while True:
        pygame.display.set_caption("    Pylliard")
        DISPLAY.fill((0, 190, 255))
        font = FONTS[4]
        draw_text('How To Play', font, (0, 0, 0), DISPLAY, 210, 40)

        font = FONTS[2]
        draw_text(data['htp']['subtitle'], font, (0, 0, 0), DISPLAY, 10, 80)
        draw_text('Rules:', font, (0, 0, 0), DISPLAY, 10, 100)
        draw_text(data['htp']['1'], font, (0, 0, 0), DISPLAY, 10, 120)

        font = FONTS[1]
        draw_text(data['htp']['2'], font, (0, 0, 0), DISPLAY, 10, 140)

        font = FONTS[2]
        draw_text(data['htp']['3'], font, (0, 0, 0), DISPLAY, 10, 160)
        draw_text(data['htp']['4'], font, (0, 0, 0), DISPLAY, 10, 180)
        draw_text(data['htp']['5'], font, (0, 0, 0), DISPLAY, 10, 200)

        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(200, 220, 200, 50)

        if back_button.collidepoint((mx, my)):
            if click:
                main_menu(click)
        pygame.draw.rect(DISPLAY, (255, 170, 0), back_button)
        font = FONTS[3]
        draw_text('BACK TO MENU', font, (255, 255, 255), DISPLAY, 235, 235)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def game():
    setup()

    while not game_over:
        update()
    if game_over:
        win_screen()


run_how_to_play(click)
# game()
#in case the menu isn't working properly, run the game function instead of run_how_to_play