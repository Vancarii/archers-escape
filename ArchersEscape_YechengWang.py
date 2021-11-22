# ~ Yecheng Wang
# ~ ARCHER'S ESCAPE
# ~ FINAL PROJECT
# ~ 2020-06-12

import math, random, sys
import pygame
from pygame.locals import *
from PIL import Image

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption("ARCHER'S ESCAPE")

Width = 800
Height = 500

WINDOW_SIZE = (Width, Height)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((340,200)) # used as the surface for rendering, which is scaled

#Fonts
font1 = pygame.font.Font('Font/DEADCRT.ttf', 40)
font2 = pygame.font.Font('Font/DEADCRT.ttf', 15)
font3 = pygame.font.Font('Font/DEADCRT.ttf', 12)
font4 = pygame.font.Font('Font/DEADCRT.ttf', 7)

#----------------------VARIABLES-------------------------
vertical_momentum = 0
horizontal_momentum = 0
air_timer = 0
crash_timer = 0
stepcounter = 0
stepdistance = 35
monsterposlist = []
score = 0
finishgame = False
endtext = 0
intro = True
playbtnclick = False
howtobtnclick = False
returntomain = 0
scorecounter = 0

Black = pygame.Color(0,0,0)
White = pygame.Color(255,255,255)

true_scroll = [0,0]

spike_img = pygame.image.load('Images/Spike.png').convert_alpha()
ground_img = pygame.image.load('Images/ground.png').convert_alpha()
coin_img = pygame.image.load('Images/Coin.png').convert_alpha()
downarrow_img = pygame.image.load('Images/DownArrow.png').convert_alpha()
ship_img = pygame.image.load('Images/Ship.png').convert_alpha()
audioon_img = pygame.image.load('Images/AudioOn.png').convert_alpha()
audioon_rect = audioon_img.get_rect()
audioon_rect.topleft = (770, 0)
audioon_shrunk = pygame.transform.scale(audioon_img, (16, 16))
audioon_shrunkrect = audioon_shrunk.get_rect()
audioon_shrunkrect.topleft = (300, 0)

player_img = pygame.image.load('Images/Archer.png').convert_alpha()
monster_img = pygame.image.load('Images/Monster.png').convert_alpha()
player_img.set_colorkey((255,255,255))
monster_rect = monster_img.get_rect()
player_rect = player_img.get_rect()
player_rect.y = 200

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[600,80,120,400]],[0.25,[500,10,70,400]],[0.25,[680,30,40,400]],[0.5,[300,40,40,400]],[0.5,[430,90,100,400]],[0.5,[600,80,120,400]],[0.5,[700,80,120,400]], [0.5,[900,40,40,400]]]

#-------------------------------------FUNCTIONS--------------------------------------------
#Open the map file and put it into a list
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def displaytext(word, center, font, color):
    text = font.render(word, True, color)
    text_rect = text.get_rect()
    text_rect.center = center
    return text, text_rect

def resetgame():
    pygame.time.wait(500)
    player_rect.x = 0
    player_rect.y = 200
    monsterposlist = []
    score = 0
    finishgame = False
    game_map = load_map('map')
    return score, finishgame, game_map

pygame.mixer.music.load("Music/ArchersThemeSong.wav")
pygame.mixer.music.play(-1)

#Menu screen
def game_intro(intro, playbtnclick, howtobtnclick):
    while intro == True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 > mouse[0] > 300 and 280 > mouse[1] > 220:
                    playbtnclick = True
                    intro = False
                if 500 > mouse[0] > 300 and 380 > mouse[1] > 320:
                    howtobtnclick = True
                    intro = False

        screen.fill(pygame.Color(80,8,13))
        titletext, titletext_rect = displaytext("ARCHER'S ESCAPE", (400, 150), font1, White)
        credittext, credittext_rect = displaytext('Game made by Yecheng Wang, Music produced by Xiuneng Wang', (207, 10), font4, White)
        soundtext, soundtext_rect = displaytext('please turn on sound', (690, 15), font4, White)

        #PLAY BUTTON
        #Have the button turn white when hovered over
        if 500 > mouse[0] > 300 and 280 > mouse[1] > 220:
            pygame.draw.rect(screen, White,((Width/2 - 100), (Height/2 - 30), 200, 60))
            playtext, playtext_rect = displaytext('Play', (400, 250), font2, Black)
        else:
            pygame.draw.rect(screen, Black,((Width/2 - 100), (Height/2 - 30), 200, 60))
            playtext, playtext_rect = displaytext('Play', (400, 250), font2, White)

        #HOW TO PLAY BUTTON
        if 500 > mouse[0] > 300 and 380 > mouse[1] > 320:
            pygame.draw.rect(screen, White,((Width/2 - 100), (Height/2 + 70), 200, 60))
            howtotext, howto_rect = displaytext('How to Play', (400, 350), font2, Black)
        else:
            pygame.draw.rect(screen, Black,((Width/2 - 100), (Height/2 + 70), 200, 60))
            howtotext, howto_rect = displaytext('How to Play', (400, 350), font2, White)

        screen.blit(soundtext, soundtext_rect)
        screen.blit(audioon_img, audioon_rect)
        screen.blit(playtext, playtext_rect)
        screen.blit(howtotext, howto_rect)
        screen.blit(titletext, titletext_rect)
        screen.blit(credittext, credittext_rect)
        pygame.display.update()
        clock.tick(15)
    return intro, playbtnclick, howtobtnclick

#How to play menu
def howtoplay(howtobtnclick, intro):
    while howtobtnclick == True:
        screen.fill((80,8,13))
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if 500 > mouse[0] > 300 and 460 > mouse[1] > 400:
                        intro = True
                        howtobtnclick = False

        #Back button, Have the button turn white and text turn black when mouse hovers
        if 500 > mouse[0] > 300 and 460 > mouse[1] > 400:
            pygame.draw.rect(screen, White,((Width/2 - 100), (Height - 100), 200, 60))
            backtext, backtext_rect = displaytext('Back', (400, 430), font2, Black)
        else:
            pygame.draw.rect(screen, Black,((Width/2 - 100), (Height - 100), 200, 60))
            backtext, backtext_rect = displaytext('Back', (400, 430), font2, White)

        titletext, titletext_rect = displaytext("ARCHER'S ESCAPE", (400, 75), font1, White)
        keystext, keystext_rect = displaytext("Use the keys 'UP', 'W', or 'SPACE' on the keyboard to jump", (400, 250), font3, White)
        story1, story1_rect = displaytext("Archer has landed on a planet with", (255, 150), font4, White)
        story2, story2_rect = displaytext("ANGRY MONSTERS", (500, 150), font2, (255, 0, 0))
        story3, story3_rect = displaytext("Your job is to get to your spaceship and fly home", (400, 200), font3, White)
        story4, story4_rect = displaytext("Avoid the spikes or they'll kill you", (400, 300), font3, White)
        story5, story5_rect = displaytext("Each coin will increase your score by 5", (400, 350), font3, White)
        screen.blit(story1, story1_rect)
        screen.blit(story2, story2_rect)
        screen.blit(story3, story3_rect)
        screen.blit(story4, story4_rect)
        screen.blit(story5, story5_rect)
        screen.blit(keystext, keystext_rect)
        screen.blit(titletext, titletext_rect)
        screen.blit(backtext, backtext_rect)
        pygame.display.update()
        clock.tick(15)
    return howtobtnclick, intro


#------------------------------------MAIN LOOP------------------------------------------
while True:

    #Calls the game intro function for the main menu splash screen
    if intro == True:
        intro, playbtnclick, howtobtnclick  = game_intro(intro, playbtnclick, howtobtnclick)
        score, finishgame, game_map = resetgame()
        print(howtobtnclick)

    #GAME LOOP
    while intro == False:
        while howtobtnclick == True:
            howtobtnclick, intro = howtoplay(howtobtnclick, intro)

        while playbtnclick == True:
            display.fill((80,8,13))

            #If the game ends then stop adding score
            if finishgame == False:
                scorecounter += 1
                if scorecounter > 70:
                    score += 1
                    scorecounter = 0

            #Allows for everything on the screen to scroll accross the screen
            #This code was found online and imported to my code
            true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
            true_scroll[1] += (player_rect.y-true_scroll[1]-106)/25
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            #BACKGROUND IMAGES
            pygame.draw.rect(display,(255,69,0),pygame.Rect(0,120,500,80))
            for background_object in background_objects:
                obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
                if background_object[0] == 0.5:
                    pygame.draw.rect(display,(219,112,147),obj_rect)
                else:
                    pygame.draw.rect(display,(139, 0, 139),obj_rect)

            #HANDLES DRAWING THE MAP
            #iterates through the map.txt file and checks for the numbers
            #According to the number in the file, draw a specific image in that position
            #Also creates a rect in specific places to check for collision
            #appends the ground tiles to a list (tile_rects) to check for collision on each side
            #if you hit the spike, the game resets
            #if you hit a coin, the score adds 5 and the coin disappears
            #if you hit the ship, the player disappears and the ship flies away
            tile_rects = []
            y = 0
            for layer in game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        display.blit(ground_img,(x*16-scroll[0],y*16-scroll[1]))
                        tile_rects.append(pygame.Rect(x*16,y*16,16,16))
                    if tile == '2':
                        display.blit(spike_img,(x*16-scroll[0],y*16-scroll[1]))
                        spike_rect = pygame.Rect(x*16,y*16,16,16)
                        if player_rect.colliderect(spike_rect):
                            print('spike')
                            score, finishgame, game_map = resetgame()
                    if tile == '3':
                        coin_rect = pygame.Rect(x*16,y*16,16,16)
                        if player_rect.colliderect(coin_rect):
                            game_map[y][x] = '0'
                            score += 5
                            scorecounter = 0
                        else:
                            display.blit(coin_img,(x*16-scroll[0],y*16-scroll[1]))
                    if tile == '4':
                        display.blit(downarrow_img,(x*16-scroll[0],y*16-scroll[1]))
                    if tile == '5':
                        display.blit(ship_img,(x*16-scroll[0],y*16-scroll[1]))
                        ship_rect = pygame.Rect(x*16,y*16,16,16)
                        if player_rect.colliderect(ship_rect):
                            game_map[y][x] = '0'
                            finishgame = True
                            vertical_momentum = -1
                            horizontal_momentum = 1
                    x += 1
                y += 1

            player_movement = [0,0]

            player_movement[1] += vertical_momentum
            player_movement[0] += horizontal_momentum

            #Sends the ground tiles to be checked if the player hits it
            player_rect,collisions = move(player_rect,player_movement,tile_rects)

            #LET THE MONSTER FOLLOW THE PLAYER
            if finishgame == False:
                #Append the players position to a monsterposlist
                playerpos = [player_rect.x, player_rect.y]
                monsterposlist.append(playerpos)

                #Have the monster ten steps behind the player
                if stepcounter < stepdistance:
                    monster_rect.x = -10
                    monster_rect.y = -10
                elif stepcounter >= stepdistance:
                    monster_rect.x = monsterposlist[stepcounter-stepdistance][0]
                    monster_rect.y = monsterposlist[stepcounter-stepdistance][1]
                stepcounter += 1

                #Checks to see if the player has hit the monster
                #reset if collided
                if player_rect.colliderect(monster_rect):
                    score, finishgame, game_map = resetgame()

                #Falling gravity
                vertical_momentum += 0.3
                if vertical_momentum > 3:
                    vertical_momentum = 3
                #Constant forward motion
                horizontal_momentum += 0.3
                if horizontal_momentum > 2:
                    horizontal_momentum = 2
                #If you hit the ground tile to the right, bounce backwards
                if collisions['right'] == True:
                    crash_timer += 1
                    horizontal_momentum = -3
                #If the player stands on the ground tile, stop falling
                if collisions['bottom'] == True:
                    air_timer = 0
                    vertical_momentum = 0
                else:
                    air_timer += 1

            if crash_timer > 6:
                crash_timer = 0
                horizontal_momentum = 2

            #In-game text
            scoreword, scoreword_rect = displaytext('SCORE ', (50, 15), font2, White)
            scoretext, score_rect = displaytext(str(score).upper(), (120, 15), font2, White)
            finishtext, finishtext_rect = displaytext('THANKS FOR PLAYING', (160, 50), font2, White)
            returntomaintext, returntomain_rect = displaytext('Returning to main menu...', (160, 70), font4, White)

            #Event Loop
            #Checks for jumping
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_SPACE or event.key == K_w:
                        if air_timer < 6:
                            vertical_momentum = -4.1

            #Displaying the end text after the player enters the ship
            if endtext > 80:
                display.blit(finishtext, finishtext_rect)
            if endtext > 120:
                display.blit(returntomaintext, returntomain_rect)
                if endtext > 160:
                    endtext = 80
                    returntomain += 1

            #Have the return to main menu text flash four times
            if returntomain == 3:
                returntomain = 0
                endtext = 0
                score, finishgame, game_map = resetgame()
                intro = True
                playbtnclick = False

            #Display the player during the game
            #and display the ship in position of the player when you collide with it
            if finishgame == False:
                display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            else:
                display.blit(ship_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                endtext += 1

            display.blit(scoreword, scoreword_rect)
            display.blit(scoretext, score_rect)
            display.blit(monster_img,(monster_rect.x-scroll[0], monster_rect.y-scroll[1]))
            screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
            pygame.display.update()
            clock.tick(60)
