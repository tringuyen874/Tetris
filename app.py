import pygame
import sys
import Score
import Grid
from GlobalVar import *
import Shape

import cv2
import numpy as np
from mss import mss
from PIL import Image
pygame.init()
pygame.font.init()
sct = mss()
frames = []

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('arial', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height()))
       
def pause(surface,clock, paused):
    font = pygame.font.SysFont('arial', 30, bold=True)
    resume_button_width = top_left_x + play_width / 2 - 70
    resume_button_height = top_left_y + play_height / 2 + 40
    new_game_button_width = resume_button_width
    new_game_button_height = resume_button_height + 80
    resume_text = font.render('Resume' , True , white)
    new_game_text = font.render('New game' , True , white)
    new_game_check = False

    while paused:
        # surface.fill(black)
        sound.stop()
        
        draw_text_middle(surface, "Paused",80, black)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                # quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked the resume button, unpause the game
                if resume_button_width <= mouse[0] <= resume_button_width + 40 and resume_button_height <= mouse[1] <= resume_button_height + 40:
                    paused = False
                # If the user clicked the new game button, unpause the game and set new_game_check to True
                if new_game_button_width <= mouse[0] <= new_game_button_height + 40 and new_game_button_height <= mouse[1] <= new_game_button_height + 40:
                    paused = False
                    new_game_check = True
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    paused = False   

        mouse = pygame.mouse.get_pos()
        if resume_button_width <= mouse[0] <= resume_button_width+140 and resume_button_height <= mouse[1] <= resume_button_height+40:
            pygame.draw.rect(surface,red,[resume_button_width,resume_button_height,140,40])
            pygame.draw.rect(surface,blue,[new_game_button_width,new_game_button_height,140,40])
		
        elif new_game_button_width <= mouse[0] <= new_game_button_width+140 and new_game_button_height <= mouse[1] <= new_game_button_height+40:
            pygame.draw.rect(surface,red,[new_game_button_width,new_game_button_height,140,40])
            pygame.draw.rect(surface,blue,[resume_button_width,resume_button_height,140,40])
        else:
            pygame.draw.rect(surface,blue,[resume_button_width,resume_button_height,140,40])
            pygame.draw.rect(surface,blue,[new_game_button_width,new_game_button_height,140,40])
        surface.blit(resume_text , (resume_button_width + 10,resume_button_height))
        surface.blit(new_game_text , (new_game_button_width + 10,new_game_button_height))
        pygame.display.update()
        clock.tick(15)
    return new_game_check   
    
def draw_window(surface, grid,user_text, score = 0, last_score = 0 , high_score = 0, high_score_name = ''):
    # surface.fill(black)
    play_area = pygame.Rect(top_left_x,top_left_y,play_width, play_height)
    surface.fill(black, play_area)
    font = pygame.font.SysFont('arial', 30)
    
    surface.blit(title, (top_left_x + play_width / 2 - (title.get_width() / 2), 20)) #middle of the screen (label,x,y)

    #Last_score
    lc = font.render('Last Score', 1, white)
    startX = top_left_x + play_width + 50
    startY = top_left_y + play_height / 2 - 100
    last_score_area = pygame.Rect(startX,startY + 160,150,80)
    surface.fill(gray, last_score_area)
    surface.blit(lc, (startX + 10, startY  + 160))
    
    label = font.render(str(last_score), 1, white)
    surface.blit(label, (startX + (150 - label.get_width()) / 2, startY + 160 + lc.get_height()))

    #Current_score
    label = font.render('Score' + ":  " + str(score), 1, white)
    startX = top_left_x - 200
    startY = top_left_y + play_height / 2 - 100 
    score_area = pygame.Rect(startX,startY + 160,150, label.get_height() + 10)
    surface.fill(gray, score_area)
    surface.blit(label, (startX + 10, startY  + 160))
    
    # Player name:
    label = font.render('Player' + ":  " + user_text, 1, white)
    startX = top_left_x - 200 # 50
    startY = top_left_y + play_height / 2 - 100 
    player_area = pygame.Rect(startX,startY + 100,150, label.get_height() + 10)
    surface.fill(gray, player_area)
    surface.blit(label, (startX + 10, startY  + 100))
    
    # High score
    hc = font.render('High Score:' , 1, white)
    startX = top_left_x - 200
    startY = top_left_y + 100
    high_score_area = pygame.Rect(startX,startY,150, 80)
    surface.fill(gray, high_score_area)
    surface.blit(hc, (startX + (150 - hc.get_width()) / 2, startY))
    
    label = font.render(str(high_score) + "("+ high_score_name + ")", 1, white)
    surface.blit(label, (startX + (150 - label.get_width()) / 2, startY + hc.get_height()))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            surface.blit(grid[y][x], (top_left_x + x * block_size, top_left_y + y * block_size))
    pygame.draw.rect(surface, red, (top_left_x, top_left_y,play_width,play_height), 4)

    Grid.draw_grid(surface, grid)
    
def setting_butt(font, window, clock, user_text):
    qm = pygame.image.load(f"Tetris/images/qm.png")
    qm = pygame.transform.scale(qm, (450,300))
    plus = pygame.image.load(f"Tetris/images/plus.png")
    plus = pygame.transform.scale(plus, (30,30))
    minus = pygame.image.load(f"Tetris/images/minus.png")
    minus = pygame.transform.scale(minus, (30,30))

    plusV = pygame.image.load(f"Tetris/images/plusV.png")
    plusV = pygame.transform.scale(plusV, (30,30))
    minusV = pygame.image.load(f"Tetris/images/minusV.png")
    minusV = pygame.transform.scale(minusV, (50,50))

    setting_menu = pygame.Rect(200, 200, 430, 300)

    save = pygame.image.load(f"Tetris/images/save.png")
    save = pygame.transform.scale(save, (30,30))
    level = 1
    volume = 50
    active = True
    while active:
        level_text = font.render('Level: ' + str(level),1, white)
        volume_text = font.render('Volume: ' + str(volume),1, white)
        window.blit(qm, (200,200))
        window.blit(level_text, (250,220))
        window.blit(volume_text, (250, 300))
        # pygame.draw.rect(window, black, input_rect)
        plus_rect = plus.get_rect()
        plus_x = 300 + level_text.get_width() - 10
        plus_y = 240
        plus_rect.x = plus_x
        plus_rect.y = plus_y
        plus_rect.width = 30
        plus_rect.height = 30
        window.blit(plus,plus_rect)

        minus_rect = minus.get_rect()
        minus_x = 300 + level_text.get_width() + 50
        minus_y = 240
        minus_rect.x = minus_x
        minus_rect.y = minus_y
        minus_rect.width = 30
        minus_rect.height = 30
        window.blit(minus,minus_rect)

        plusV_rect = plus.get_rect()
        plusV_x = 300 + volume_text.get_width() - 40
        plusV_y = 320
        plusV_rect.x = plusV_x
        plusV_rect.y = plusV_y
        plusV_rect.width = 30
        plusV_rect.height = 30
        window.blit(plusV,plusV_rect)

        minusV_rect = minusV.get_rect()
        minusV_x = 300 + volume_text.get_width() 
        minusV_y = 320
        minusV_rect.x = minusV_x
        minusV_rect.y = minusV_y
        minusV_rect.width = 30
        minusV_rect.height = 30
        window.blit(minusV,minusV_rect)

        save_rect = save.get_rect()
        save_x = 400
        save_y = 400
        save_rect.x = save_x
        save_rect.y = save_y
        save_rect.width = 30
        save_rect.height = 30
        window.blit(save,save_rect)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if plus_rect.collidepoint(mouse_x, mouse_y):
            plus = pygame.transform.scale(plus, (40,40))
        else:
            plus = pygame.transform.scale(plus, (30,30))
        if minus_rect.collidepoint(mouse_x, mouse_y):
            minus = pygame.transform.scale(minus, (40,40))
        else:
            minus = pygame.transform.scale(minus, (30,30))

        if plusV_rect.collidepoint(mouse_x, mouse_y):
            plusV = pygame.transform.scale(plusV, (40,40))
        else:
            plusV = pygame.transform.scale(plusV, (30,30))
        if minusV_rect.collidepoint(mouse_x, mouse_y):
            minusV = pygame.transform.scale(minusV, (40,40))
        else:
            minusV = pygame.transform.scale(minusV, (30,30))

        if save_rect.collidepoint(mouse_x, mouse_y):
            save = pygame.transform.scale(save, (60,60))
        else:
            save = pygame.transform.scale(save, (50,50))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if plus_rect.collidepoint(event.pos):
                    if level == 3:
                        pass
                    else:
                        level += 1
                if minus_rect.collidepoint(event.pos):
                    if level == 0:
                        pass
                    else:
                        level -= 1

                if plusV_rect.collidepoint(event.pos):
                    if volume == 1:
                        pass
                    else:
                        volume += 10
                if minusV_rect.collidepoint(event.pos):
                    if volume == 0:
                        pass
                    else:
                        volume -= 10

                if save_rect.collidepoint(event.pos):
                    active = False
                    main(window,user_text, clock,level/200, volume /100)
        pygame.display.update()
        clock.tick(15)
    sound.set_volume(volume / 100)
     
def question_button(window, clock):
    font = pygame.font.SysFont('arial', 30, bold=True)
    qm = pygame.image.load(f"Tetris/images/qm.png")
    qm = pygame.transform.scale(qm, (450,300))
    member = font.render('How to play ',1, white)
    save = pygame.image.load(f"Tetris/images/save.png")
    save = pygame.transform.scale(save, (30,30))
    arrow = pygame.image.load(f"Tetris/images/arrow.png")
    arrow = pygame.transform.scale(arrow, (100,40))
    nmt = font.render('Use arrow key to move ',1, white)
    nmv = font.render('and change shape form  ',1, white)
    tkl = font.render('Press ESC to pause ',1, white)
    active = True
    while active:
        window.blit(qm, (200,200))
        window.blit(member, (300,220))
        window.blit(nmt, (300,260))
        window.blit(arrow, (300,340))
        window.blit(nmv, (300,300))
        window.blit(tkl, (300,380))
        save_rect = save.get_rect()
        save_x = 400
        save_y = 430
        save_rect.x = save_x
        save_rect.y = save_y
        save_rect.width = 30
        save_rect.height = 30
        window.blit(save,save_rect)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if save_rect.collidepoint(mouse_x, mouse_y):
            save = pygame.transform.scale(save, (60,60))
        else:
            save = pygame.transform.scale(save, (50,50))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_rect.collidepoint(event.pos):
                    active = False
        pygame.display.update()
        clock.tick(15)

    pass 

def main_menu(window):
    # Create a "screen capture" object to capture video from the screen

    clock = pygame.time.Clock()
    color_active = pygame.Color(red)
    color_passive = pygame.Color(black)
    color_text_box = color_passive
    active = False
    user_text = ''
    font = pygame.font.SysFont('arial', 60, bold=True)
    label = font.render('Type name:', 1, black)
    input_rect = pygame.Rect(top_left_x + play_width / 2-120, top_left_y + play_height / 2 + 45, label.get_width() - 10, 60)
    # text_surface = font.render(user_text, True, blue)
    run = True
    setting = pygame.image.load(f"Tetris/images/setting.png")
    setting_rect = setting.get_rect()
    setting_x = top_left_x + play_width / 2-120
    setting_y = top_left_y + play_height / 2 + 120
    setting_rect.x = setting_x
    setting_rect.y = setting_y
    setting_rect.width = 60
    setting_rect.height = 60

    play = pygame.image.load(f"Tetris/images/play.png")
    # play = pygame.transform.scale(play, (60,60))
    play_rect = play.get_rect()
    play_x = top_left_x + play_width / 2 - 20
    play_y = top_left_y + play_height / 2 + 120
    play_rect.x = play_x
    play_rect.y = play_y
    play_rect.width = 60
    play_rect.height = 60

    question = pygame.image.load(f"Tetris/images/question.png")
    # question = pygame.transform.scale(question, (60,60))
    question_rect = question.get_rect()
    question_x = top_left_x + play_width / 2 + 80
    question_y = top_left_y + play_height / 2 + 120
    question_rect.x = question_x
    question_rect.y = question_y
    question_rect.width = 60
    question_rect.height = 60

    while run:

        window.blit(background_image, (0,0))
        window.blit(open_title, (100,150))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if play_rect.collidepoint(event.pos):
                    main(window,user_text, clock,new_level, new_volume)
                if setting_rect.collidepoint(event.pos):
                    setting_butt(font, window, clock, user_text)
                if question_rect.collidepoint(event.pos):
                    question_button(window, clock)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    user_text = user_text[:-1]
                    # record(window,user_text, clock,new_level,new_volume)
                    main(window,user_text, clock,new_level,new_volume)
        
        if setting_rect.collidepoint(mouse_x, mouse_y):
            setting = pygame.transform.scale(setting, (70,70))
        else:
            setting = pygame.transform.scale(setting, (60,60))
        if play_rect.collidepoint(mouse_x, mouse_y):
            play = pygame.transform.scale(play, (70,70))
        else:
            play = pygame.transform.scale(play, (60,60))
        if question_rect.collidepoint(mouse_x, mouse_y):
            question = pygame.transform.scale(question, (70,70))
        else:
            question = pygame.transform.scale(question, (60,60))

        window.blit(setting,setting_rect) 
        window.blit(play,play_rect) 
        window.blit(question,question_rect) 
        if active:
            color_text_box = color_active
        else:
            color_text_box = color_passive
            
        # Draw the textbox and label
        # pygame.draw.rect(window, color_text_box, input_rect)
        window.fill(color_text_box, input_rect)
        text_surface = font.render(user_text, True, white)
        window.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))
        window.blit(text_surface, (input_rect.x+5, input_rect.y))
        # input_rect.w = max(100, text_surface.get_width()+10)
        pygame.display.flip()
        clock.tick(60)

def watch_replay():
    # Set the frame rate of the replay
    frame_rate = 30
    new_size = (640, 480)
    # Display the frames in the list
    for frame in frames:
        resized_frame = cv2.resize(frame, new_size)
        cv2.imshow('replay', resized_frame)
        if cv2.waitKey(1000 // frame_rate) & 0xFF == ord('q'):
            break
    
    # Clean up
    cv2.destroyAllWindows()

def main(window, user_text, clock, new_level, new_volume):
    lastScore = Score.last_score()
    locked_position = {}
    grid = Grid.create_grid(locked_position)
    change_piece = False
    run  = True
    current_piece = Shape.get_shape()
    next_piece = Shape.get_shape()
    fall_time = 0  
    level_time = 0
    fall_speed = 0.27
    score = 0
    highScore, highScoreName = Score.high_score()
    sound.set_volume(new_volume)
    

    replay = pygame.image.load(f"Tetris/images/replay.png")
    #replay = pygame.transform.scale(replay, (60,60))
    replay_rect = replay.get_rect()
    replay_x = top_left_x + play_width / 2 - 60
    replay_y = top_left_y + play_height / 2 + 120
    replay_rect.x = replay_x
    replay_rect.y = replay_y
    replay_rect.width = 60
    replay_rect.height = 60

    quit = pygame.image.load(f"Tetris/images/quit.png")
    #quit = pygame.transform.scale(quit, (60,60))
    quit_rect = quit.get_rect()
    quit_x = top_left_x + play_width / 2 + 80
    quit_y = top_left_y + play_height / 2 + 120
    quit_rect.x = quit_x
    quit_rect.y = quit_y
    quit_rect.width = 60
    quit_rect.height = 60

    while run:
        #record screen
        sct_img = sct.grab(moniter)
        img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        frames.append(img_bgr)

        window.blit(background_image, (0,0))
        sound.play()
        grid = Grid.create_grid(locked_position)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # increase falling speed every 5 sec
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= new_level
    
        if fall_time / 1000 > fall_speed: # to fall slow
            fall_time = 0
            current_piece.y += 1
            if not(Shape.valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1 # Stop and stay
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sound.stop()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(Shape.valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(Shape.valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(Shape.valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(Shape.valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    newGame = pause(window, clock, paused)
                    if newGame == True:
                        run = False
                    
        shape_pos = Shape.convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece: # before change piece need to reset locked positions by giving them color
            for pos in shape_pos: # locked_position = {(1, 2): black, (2, 3): black, (3, 4): black, ...}
                x, y = pos
                if current_piece.shape == B:
                    for i in range(x - 1, x + 2):
                        for j in range(y - 1, y + 2):
                            locked_position[i,j] = black_image
                else:
                    locked_position[pos] = current_piece.color
            current_piece = next_piece
            next_piece = Shape.get_shape()
            change_piece = False
            value = Shape.clear_rows(grid,locked_position)
            if value == 2:
                score += value * 20
            elif value == 0:
                continue
            else:
                score += value * 10

        draw_window(window, grid, user_text, score, lastScore, highScore, highScoreName)
        Shape.draw_next_shapes(next_piece, window)
        pygame.display.update()

        if Shape.check_lost(locked_position):
            
            draw_text_middle(window, 'You Lost!', 80, white)
            pygame.display.update()
            Score.update_score(score)
            Score.update_high_score(score, user_text)
            sound.stop()
            check = True
            while check:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if replay_rect.collidepoint(event.pos):
                            watch_replay()
                        if quit_rect.collidepoint(event.pos):
                            check = False
                if replay_rect.collidepoint(mouse_x, mouse_y):
                    replay = pygame.transform.scale(replay, (70,70))
                else:
                    replay = pygame.transform.scale(replay, (60,60))

                if quit_rect.collidepoint(mouse_x, mouse_y):
                    quit = pygame.transform.scale(quit, (70,70))
                else:
                    quit = pygame.transform.scale(quit, (60,60))

                
                window.blit(replay, replay_rect)
                window.blit(quit, quit_rect)
                pygame.display.flip()
                clock.tick(60)

            
            # clock.tick(15)              
                
            run = False
    cv2.destroyAllWindows()

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(window)
