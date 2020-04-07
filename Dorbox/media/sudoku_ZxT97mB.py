# Sudoku By Dor Avissara

board = [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],

    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],

    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9]
]
nums_set = {1,2,3,4,5,6,7,8,9}

def print_board(board):
    for i in range(9):
        for j in range(9):
            if j != 5 and j != 2:
                print board[i][j],
            else:
                print str(board[i][j]) + " | ",
        print
        if (i == 5 or i == 2):
            print "-------------------------"

def cell_emptys(board, row , col): # finding the possible numbers in a specific row and col (finding the cell)
    ls = []
    for i in range(0, 3):
        for j in range(0, 3):
            ls.append(board[(row / 3) * 3 + i][(col / 3) * 3 + j])  
    return list(nums_set - set(ls))


def used_in_row(board, row, num): # checking if num is in row
    for i in range(9):
        if board[row][i] == num:
            return True
    return False

def used_in_col(board, col, num): # checking if num is in column
    for i in range(9):
        if board[i][col] == num:
            return True
    return False

def used_in_cell(board, row, col, num): # checking if num is in cell
    for i in range(0, 3):
        for j in range(0, 3):
            if num == board[(row / 3) * 3 + i][(col / 3) * 3 + j]:
                return True
    return False   

def can_put(board, row, col, num): # checing if can put a specific number in a specific position
    return not used_in_row(board, row, num) and not used_in_col(board, col, num) and not used_in_cell(board, row, col, num)

def finished_game(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
    return True
def find_empty_place(board): 
    for i in range(9): # finding the first empty place
        for j in range(9):
            if board[i][j] == 0:
                return i,j

def solve_game(board):
    if finished_game(board): return True

    row, col = find_empty_place(board) # finding the first empty place
  
    for num in cell_emptys(board, row , col): # going through each possible move

        if(can_put(board, row, col, num)): 
            board[row][col] = num

            if(solve_game(board)): # keeping the recurions
                return True

            board[row][col] = 0 # didn't finished the game so reseting the value

    return False  # if nothing of the possible moves succeeded returns false and doing the backstrack


board2=[[3,0,6,5,0,8,4,0,0], 
          [5,2,0,0,0,0,0,0,0], 
          [0,8,7,0,0,0,0,3,1], 
          [0,0,3,0,1,0,0,8,0], 
          [9,0,0,8,6,3,0,0,5], 
          [0,5,0,0,9,0,6,0,0], 
          [1,3,0,0,0,0,2,5,0], 
          [0,0,0,0,0,0,0,7,4], 
          [0,0,5,2,0,6,3,0,0]] 

print solve_game(board2)
print print_board(board2)
raw_input()
