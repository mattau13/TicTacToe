import math
import pygame
import time

pygame.init()

#  AI = "X" and User = "O"

#  Create Window
window = pygame.display.set_mode((512, 512))
pygame.display.set_caption("TicTacToe")
window.blit(pygame.image.load("Board.png").convert(), (0, 0))

pygame.display.update()

#  Load Images
x_image = pygame.image.load("X.png").convert_alpha()
o_image = pygame.image.load("O.png").convert_alpha()

#  Determine Start
ai_turn = int(input("Who starts? \"0\" = User, \"1\" = AI ")) == 1

#  Remaining Moves + Evaluation Functions


def moves_left(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return True
    return False


def evaluate(board):
    #  Check Rows
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            if board[i][0] == "X":
                return 10
            elif board[i][0] == "O":
                return -10

    #  Check Columns
    for j in range(3):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j]:
            if board[0][j] == "X":
                return 10
            elif board[0][j] == "O":
                return -10

    #  Check Negative Diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == "X":
            return 10
        elif board[0][0] == "O":
            return -10

    #  Check Positive Diagonal
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == "X":
            return 10
        elif board[0][2] == "O":
            return -10
    return 0


#  Minimax Function


def minimax(board, depth, ai_move):
    score = evaluate(board)

    #  Check Win
    if score == 10 or score == -10:
        return score

    #  Check Tie
    if not moves_left(board):
        return 0

    if ai_move:
        maximum = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = "X"
                    maximum = max(maximum, minimax(board, depth+1, not ai_move))
                    board[i][j] = None
        return maximum
    else:
        minimum = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = "O"
                    minimum = min(minimum, minimax(board, depth+1, not ai_move))
                    board[i][j] = None
        return minimum

#  Game Functionality


def find_move(board):
    max_value = -math.inf
    move = [-1, -1]
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = "X"
                value = minimax(board, 0, False)
                board[i][j] = None
                if value > max_value:
                    move[0] = i
                    move[1] = j
                    max_value = value
    return move


def convert_coord(pos):
    return int(math.floor(pos[0]/(512/3))), int(math.floor(pos[1]/(512/3)))


def find_coords(pos):
    x, y = 0, 0

    if pos[0] == 0:
        x = 0
    elif pos[0] == 1:
        x = 170
    elif pos[0] == 2:
        x = 340

    if pos[1] == 0:
        y = 0
    elif pos[1] == 1:
        y = 170
    elif pos[1] == 2:
        y = 340

    return x, y


def draw_board(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j])
            if board[i][j] == "X":
                window.blit(x_image, find_coords((i, j)))
            elif board[i][j] == "O":
                window.blit(o_image, find_coords((i, j)))
    pygame.display.update()
    print("drawn")

if __name__ == '__main__':
    game_board = [[None] * 3 for i in range(3)]
    move_count = 0
    # draw_board(game_board)
    while move_count < 9:
        if not ai_turn:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    coord = convert_coord(pygame.mouse.get_pos())
                    if game_board[coord[0]][coord[1]] is None:
                        game_board[coord[0]][coord[1]] = "O"
                        ai_turn = True
                        move_count += 1
        elif ai_turn:
            move = find_move(game_board)
            if game_board[move[0]][move[1]] is None:
                game_board[move[0]][move[1]] = "X"
            move_count += 1
            print("")
            ai_turn = False
        draw_board(game_board)

        if abs(evaluate(game_board)) == 10:
            break


    input("Any improvement ideas?")



