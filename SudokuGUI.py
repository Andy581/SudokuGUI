import pygame
from SudokuSolver import valid, solve
import time
import json
import requests
pygame.font.init()

#CONSTANTS
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (128,128,128)
RED = (255,0,0)
BLUE = (0,0,255)
WIDTH, HEIGHT = 540, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

FPS = 60
#Initial Board
gameBoard = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

class Grid:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.selected = None
        self.cubes = [[Cubes(gameBoard[i][j], i, j, width, height) for j in range(cols)] for i in range (rows)]
        self.model = None
        self.isSelected = False

    #Update model for solver
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    #Update grid to correspond with model
    def update_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                gameBoard[i][j] = self.model[i][j]

    #Place a value in the empty cell and update both the grid and the model
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()
            self.update_grid()

        if valid(self.model, val, (row,col)) and solve(self.model):
            return True
        else:
            self.cubes[row][col].set(0)
            self.cubes[row][col].setTemp(0)
            self.update_model()
            self.update_grid()
            return False

    #draws the grid lines and the numbers
    def draw(self, win):
        gap = self.width / 9
        for i in range(10):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, BLACK, (0, i*gap), (self.width, i * gap), thick)
            pygame.draw.line(win, BLACK, (i*gap, 0 ), (i*gap, self.height), thick)
        
        #Calls on the function to draw each square
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw_board(win)
    
    #if press backspace, delete the temporary(blue) number
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].setTemp(0)

    #Adds a temporary number to the grid
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].setTemp(val)

    #Make sure only one is selected for highlighting in draw function
    def select(self, row, col):
        for i in range (self.rows):
            for j in range (self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    #Turns mouse coordinates into grid positions
    def click(self, pos):
        gap = self.width / 9
        if pos[0] <= self.width and pos[1] <= self.height:
            x = pos[0] // gap
            y = pos[1] // gap
            self.isSelected = True
            self.select(int(y), int(x))
            return (int(y), int(x)) #row, col
        else:
            return None

    #If press tab, move to the next empty position
    def next_empty(self, pos):
        gap = self.width / 9
        for a in range(self.rows):
            if a == pos[0]:
                for b in range(pos[1], self.cols):
                    if b > pos[1]:
                        if gameBoard[a][b] == 0:
                            return (b * gap , a * gap)
            elif a > pos[0]:
                for b in range(self.cols):
                    if gameBoard[a][b] == 0:
                        return (b * gap ,a * gap)
        for a in range(self.rows):
            for b in range(self.cols):
                if gameBoard[a][b] == 0:
                    return (b * gap, a * gap)

    #If press up arrow key, move to the next 0 above it
    def go_up(self,pos):
        gap = self.width / 9
        for a in range(pos[0]-1, -1, -1):
            if gameBoard[a][pos[1]] == 0:
                return (pos[1] * gap, a * gap)
        for a in range(self.rows - 1, -1, -1):
            if gameBoard[a][pos[1]] == 0:
                return (pos[1] * gap, a * gap)
    
    #If press down arrow key, move to the next 0 below it
    def go_down(self,pos):
        gap = self.width / 9
        for a in range(pos[0] + 1, self.rows):
            if gameBoard[a][pos[1]] == 0:
                return (pos[1] * gap, a * gap)
        for a in range(self.rows):
            if gameBoard[a][pos[1]] == 0:
                return (pos[1] * gap, a * gap)
    
    #If press left arrow key, move to the next 0 in the left direction
    def go_left(self, pos):
        gap = self.width / 9
        for a in range(pos[1]-1, -1, -1):
            if gameBoard[pos[0]][a] == 0:
                return (a * gap, pos[0] * gap)
        for a in range(self.cols-1, -1,-1):
            if gameBoard[pos[0]][a] == 0:
                return (a * gap, pos[0] * gap)

    #If press right arrow key, move to the next 0 in the right direction
    def go_right(self, pos):
        gap = self.width / 9
        for a in range(pos[1] + 1, self.cols):
            if gameBoard[pos[0]][a] == 0:
                return (a * gap, pos[0] * gap)
        for a in range(self.cols):
            if gameBoard[pos[0]][a] == 0:
                return (a * gap, pos[0] * gap)
    
    #Solve the entire sudoku board
    def solve_grid(self, win):
        if solve(gameBoard):
            for i in range(self.rows):
                for j in range(self.cols):
                    val = gameBoard[i][j]
                    self.cubes[i][j].set(val)
            self.update_model()
            self.update_grid()


class Cubes:
    rows = 9
    cols = 9
    
    def __init__(self, value, row, col , width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.temp = 0
    
    #Draw each number and highlights selected square
    def draw_board(self, win):
        font = pygame.font.SysFont("arial", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (BLUE))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = font.render(str(self.value), 0, (BLACK))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            if gameBoard[self.row][self.col] == 0:
                pygame.draw.rect(win, RED, (x,y,gap,gap),3)
    
    #Set the values to the cubes
    def set(self, value):
        self.value = value

    #Set the temp values to the cubes
    def setTemp(self, temp):
        self.temp = temp

#Gets board from API
def get_new_board(board):
    response = requests.get("http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=1")
    data = response.json()
    for a in range(9):
        for b in range(9):
            gameBoard[a][b] = 0
    for i in range(40):
        x = data["squares"][i]["x"]
        y = data["squares"][i]["y"]
        value = data["squares"][i]["value"]
        gameBoard[x][y] = value

#Redraw the entire application
def redraw_window(win, board, strikes):
    fnt = pygame.font.SysFont("comicsans", 40)
    win.fill(WHITE)
    #Draw solve button
    pygame.draw.rect(win,BLACK, (360,550,180,50), 3)
    solve_button = fnt.render("Solve", 1, BLACK)
    win.blit(solve_button,(420,560))
    #Draw New Game button
    pygame.draw.rect(win, BLACK, (180,550,180,50), 3)
    new_game_button = fnt.render("New Game", 1 , BLACK)
    win.blit(new_game_button,(200, 560))
    # Draw Strikes
    text = fnt.render("X: ", 1, RED)
    win.blit(text, (20, 560))
    text = fnt.render(str(strikes), 1 , BLACK)
    win.blit(text, (50,560))
    # Draw grid/board
    board.draw(win)


def main():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    board = Grid(9,9,540,540)
    solve_button = pygame.Rect(360,550,180,50)
    new_game_button = pygame.Rect(180,550,180,50)
    key = None
    strikes = 0
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if solve_button.collidepoint(pos):
                    board.solve_grid(WIN)
                if new_game_button.collidepoint(pos):
                    get_new_board(gameBoard)
                    strikes = 0
                    board = Grid(9,9,540,540)
                clicked = board.click(pos)
                key = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if board.isSelected:
                    if event.key == pygame.K_TAB:
                        empty = board.next_empty(clicked)
                        clicked = board.click(empty)
                        key = None
                    if event.key == pygame.K_UP:
                        empty = board.go_up(clicked)
                        clicked = board.click(empty)
                        key = None
                    if event.key == pygame.K_DOWN:
                        empty = board.go_down(clicked)
                        clicked = board.click(empty)
                        key = None
                    if event.key == pygame.K_LEFT:
                        empty = board.go_left(clicked)
                        clicked = board.click(empty)
                        key = None
                    if event.key == pygame.K_RIGHT:
                        empty = board.go_right(clicked)
                        clicked = board.click(empty)
                        key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None
                
        if board.selected and key != None:
            board.sketch(key)
        redraw_window(WIN, board, strikes)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()