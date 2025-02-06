import pygame
import sys

pygame.init()

#########################################
WIDTH, HEIGHT = 300, 300                #
LINE_WIDTH = 15                         #
BOARD_COLOR = (28, 170, 156)            #
LINE_COLOR = (23, 145, 135)             #
CIRCLE_COLOR = (239, 231, 200)          #
CROSS_COLOR = (66, 66, 66)              #
SPACE = 55                              #
FONT_SIZE = 40                          #
TEXT_COLOR = (255, 255, 255)            #
#########################################

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')
screen.fill(BOARD_COLOR)

font = pygame.font.Font(None, FONT_SIZE)

board = [[None]*3 for _ in range(3)]

def draw_board():
    screen.fill(BOARD_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT//3), (WIDTH, HEIGHT//3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2*HEIGHT//3), (WIDTH, 2*HEIGHT//3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH//3, 0), (WIDTH//3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*WIDTH//3, 0), (2*WIDTH//3, HEIGHT), LINE_WIDTH)

def draw_markers():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                draw_x(row, col)
            elif board[row][col] == 'O':
                draw_o(row, col)

def draw_x(row, col):
    x = col * WIDTH//3 + WIDTH//6
    y = row * HEIGHT//3 + HEIGHT//6
    pygame.draw.line(screen, CROSS_COLOR, (x - 50, y - 50), (x + 50, y + 50), LINE_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, (x + 50, y - 50), (x - 50, y + 50), LINE_WIDTH)

def draw_o(row, col):
    x = col * WIDTH//3 + WIDTH//6
    y = row * HEIGHT//3 + HEIGHT//6
    pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), 50, LINE_WIDTH)

def display_message(message):
    text = font.render(message, True, TEXT_COLOR)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

def check_winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def check_draw():
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                return False
    return True

def main():
    draw_board()
    current_player = 'X'
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row = y // (HEIGHT // 3)
                col = x // (WIDTH // 3)
                if board[row][col] is None:
                    board[row][col] = current_player
                    draw_markers()
                    winner = check_winner()
                    if winner:
                        message = f"Player {winner} wins!"
                        print(message)
                        display_message(message)
                        game_over = True
                    elif check_draw():
                        message = "It's a draw!"
                        print(message)
                        display_message(message)
                        game_over = True
                    current_player = 'O' if current_player == 'X' else 'X'
        pygame.display.flip()

if __name__ == "__main__":
    main()
