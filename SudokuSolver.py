board = [
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

#prints the board
def print_board(board):
    for i in range (len(board)):
        if i % 3 == 0 and i != 0: #for every 3 rows create a dashed line
            print ("- - - - - - - - - - - - - -")
        for j in range (len(board[0])):
            if j % 3 == 0 and j != 0:
                print (" | ", end = "") #for every 3 columns create a | but continue on the same line
            if j == 8: #for the last element of a row just print the number and move to next line
                print(board[i][j])
            else: #if its not the last element of each row, print the number and continue on the same line
                print(str(board[i][j]) + " ", end = "")

#finds the next empty(0) cell and return its (row,col)
def find_empty(board):
    for i in range(len(board)):
        for j in range (len(board[0])):
            if board[i][j] == 0:
                return (i, j) 
    return None

#Checks if the value placed in the empty cell is valid
def valid(board, value, pos):
    #Check each row
    for i in range(len(board[0])):
        if board[pos[0]][i] == value and pos[1] != i:
            return False
            
    #Check each column
    for j in range(len(board)):
        if board[j][pos[1]] == value and pos[0] != j:
            return False

    #Check each box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range (box_y * 3, box_y * 3 + 3):
        for j in range (box_x * 3, box_x * 3 + 3):
            if board[i][j] == value and (i,j) != pos:
                return False
    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    else:
        x, y = empty

    for i in range(1,10):
        if valid(board, i, (x, y)):
            board[x][y] = i
            
            if solve(board):
                return True

            board[x][y] = 0

    return False

#Uncomment to see before
# print_board(board)
# print()
# print()
#Uncomment to see after
# solve(board)
# print_board(board)
