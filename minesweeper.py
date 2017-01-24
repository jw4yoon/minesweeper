import random
import pygame
from pygame.locals import *
pygame.init()

#python version: 2.7.13
#pygame 1.9.1

# 20 by 20 grid
def make_board():
    board = [[0 for x in range(20)] for y in range(20)] # x is vertical y is horizontal
    return board

def create_bomb(board, n):
    for num in range(n):
        bomb_exist = False
        while bomb_exist == False:
            x = random.randint(0, 19)
            y = random.randint(0, 19)
            if board[x][y] != 9: # 9 indicates the bomb
                board[x][y] = 9
                bomb_exist = True
    return board        

def check_near_bomb(board):
    for x in range(20):
        for y in range(20):
            if board[x][y] != 9:
                if x != 0 and y != 0 and board[x-1][y-1] == 9: #check up left
                    board[x][y] += 1
                if x != 0 and board[x-1][y] == 9: # check up
                    board[x][y] += 1
                if x != 0 and y != 19 and board[x-1][y+1] == 9: #check up right
                    board[x][y] += 1
                if y != 0 and board[x][y-1] == 9: #check left
                    board[x][y] += 1
                if y != 19 and board[x][y+1] == 9: #check right
                    board[x][y] += 1
                if x != 19 and y != 0 and board[x+1][y-1] == 9: #check bottom left
                    board[x][y] += 1
                if x != 19 and board[x+1][y] == 9: #check bottom
                    board[x][y] += 1
                if x != 19 and y != 19 and board[x+1][y+1] == 9: #check bottom right
                    board[x][y] += 1
    return board

def initial_board(num_bomb): #create the initial board
    board = check_near_bomb(create_bomb(make_board(), num_bomb))
    return board

class Board:
    'Fields: board'
    def __init__(self, board):
        self.board = board
    def __repr__(self):
        printboard(self.board)

class Box:
    def __init__(self, x, y, w, h, board, ij):
        self.rect = pygame.rect.Rect(x, y, w, h)
        i, j = ij
        self.val = board[i][j]
        self.x = x
        self.y = y
        self.visible = False
        self.flag = False

def restart_game(bombs):
    game(bombs)

def zero_clicked(lst_sqr, square): #if a zero tile is clicked, call this
    #function recursively until we face non-zero tiles and make those zero tiles
    # all visible
    square.visible = True
    i = square.x // 20
    j = square.y // 20
    if len(lst_sqr) > i+1:
        if lst_sqr[i+1][j].visible == False and lst_sqr[i+1][j].flag == False:
            lst_sqr[i+1][j].visible = True
            if lst_sqr[i+1][j].val == 0:
                zero_clicked(lst_sqr, lst_sqr[i+1][j])
        if len(lst_sqr) > j+1:
            if lst_sqr[i+1][j+1].visible == False and lst_sqr[i+1][j+1].flag == False:
                lst_sqr[i+1][j+1].visible = True
                if lst_sqr[i+1][j+1].val == 0:
                    zero_clicked(lst_sqr, lst_sqr[i+1][j+1])
        if j-1 >= 0:
            if lst_sqr[i+1][j-1].visible == False and lst_sqr[i+1][j-1].flag == False:
                lst_sqr[i+1][j-1].visible = True
                if lst_sqr[i+1][j-1].val == 0:
                    zero_clicked(lst_sqr, lst_sqr[i+1][j-1])
    if i-1 >= 0:
        if lst_sqr[i-1][j].visible == False and lst_sqr[i-1][j].flag == False:
                        lst_sqr[i-1][j].visible = True
                        if lst_sqr[i-1][j].val == 0:
                            zero_clicked(lst_sqr, lst_sqr[i-1][j])
        if len(lst_sqr) > j+1:
            if lst_sqr[i-1][j+1].visible == False and lst_sqr[i-1][j+1].flag == False:
                lst_sqr[i-1][j+1].visible = True
                if lst_sqr[i-1][j+1].val == 0:
                    zero_clicked(lst_sqr, lst_sqr[i-1][j+1])
        if j-1 >= 0:
            if lst_sqr[i-1][j-1].visible == False and lst_sqr[i-1][j-1].flag == False:
                lst_sqr[i-1][j-1].visible = True
                if lst_sqr[i-1][j-1].val == 0:
                    zero_clicked(lst_sqr, lst_sqr[i-1][j-1])
    if j-1 >= 0:
        if lst_sqr[i][j-1].visible == False and lst_sqr[i][j-1].flag == False:
            lst_sqr[i][j-1].visible = True
            if lst_sqr[i][j-1].val == 0:
                zero_clicked(lst_sqr, lst_sqr[i][j-1])
    if len(lst_sqr) > j+1:
        if lst_sqr[i][j+1].visible == False and lst_sqr[i][j+1].flag == False:
            lst_sqr[i][j+1].visible = True
            if lst_sqr[i][j+1].val == 0:
                zero_clicked(lst_sqr, lst_sqr[i][j+1])    
        

def game(bombs):
    #load images
    zero = pygame.image.load("zero.bmp") # empty tile
    one = pygame.image.load("one.bmp")
    two = pygame.image.load("two.bmp")
    three = pygame.image.load("three.bmp")
    four = pygame.image.load("four.bmp")
    five = pygame.image.load("five.bmp")
    six = pygame.image.load("six.bmp")
    seven = pygame.image.load("seven.bmp")
    eight = pygame.image.load("eight.bmp")
    nine = pygame.image.load("bombclick.bmp") # we've set 9 as bomb
    flag = pygame.image.load("flag.bmp")
    bombflag = pygame.image.load("bombflag.bmp")
    bomb = pygame.image.load("bomb.bmp")
    unopened = pygame.image.load("unopened.bmp")
    
    lst_num = [zero, one, two, three, four, five, six, seven, eight, nine]
    
    b = Board(initial_board(bombs))
    w = h = len(b.board) * 20
    screen = pygame.display.set_mode((w, h))
    
    lst_sqr = [[] for num in range(20)]
    for num in range(0, 20 * 20, 20): 
        for num2 in range(0, 20 * 20, 20):
            lst_sqr[num//20] += [Box(num, num2, 20, 20, b.board, 
                                     (num//20, num2//20))]
            screen.blit(unopened, (num, num2)) # cover the entire screen
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #if r was pressed, then restart
                    running = False
                    restart_game(bombs)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # if left click was inputed
                    for i in lst_sqr:
                        for j in i:
                            r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            # get position of the mouse
                            if j.rect.colliderect(r): # if the position of the
                                # mouse is the current position
                                if j.flag == False:
                                    if j.val == 9: #if a bomb was clicked
                                        print("Game Over")
                                        running = False
                                    j.visible = True # show tile(number)
                                    if j.val == 0:
                                        j.visible = zero_clicked(lst_sqr, j)
                                        j.visible = True
                elif event.button == 3: # if right click was inputed
                    for i in lst_sqr:
                        for j in i:
                            r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            if j.rect.colliderect(r):
                                j.flag = not j.flag
        for i in lst_sqr:
            for j in i:
                if j.visible == True:
                    screen.blit(zero, (j.x, j.y))
                    screen.blit(lst_num[j.val], (j.x, j.y))
                if j.flag == True:
                    screen.blit(flag, (j.x, j.y))
                if j.flag == False and j.visible == False:
                    screen.blit(unopened, (j.x, j.y))
        count = 0
        for i in lst_sqr:
            for j in i:
                if j.visible == True and j.val != 9:                    
                    count += 1
            if count == 20 * 20 - bombs and bombs != 400: # if there are no more empty tiles
                running = False
                print("Congratulations!")
        pygame.display.update()
        
    for i in lst_sqr:
        for j in i:
            if j.val == 9 and j.flag == True: #if the bomb was flagged
                screen.blit(bombflag, (j.x, j.y))
            elif j.val == 9 and j.visible == False: #if the bomb wasn't clicked
                screen.blit(bomb, (j.x, j.y))            
            elif j.val == 9: # if bomb
                screen.blit(nine, (j.x, j.y))            
    pygame.display.update()
        
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
                    restart_game(bombs)
                    
print("Press 'r' to restart the game")
bombs = int(input("Enter the number of bombs (1 to 400): "))
game(bombs)