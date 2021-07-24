import pygame
import os
import random
from pygame import mixer

pygame.font.init()
mixer.init()
mixer.music.load(os.path.join("assets", "music.wav"))
mixer.music.play(-1)

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("TTT Inception")
WIDTH = WIN.get_width()
HEIGHT = WIN.get_height()

# Load Images
IMAGE_O = pygame.image.load(os.path.join("assets", "Omark.png"))
IMAGE_X = pygame.image.load(os.path.join("assets", "Xmark.png"))

# Background
BG = pygame.transform.scale((pygame.image.load(os.path.join("assets", "Board.png")).convert()), (HEIGHT, HEIGHT))

# Mini Board
IMAGE_BOARD = pygame.transform.scale((pygame.image.load(os.path.join("assets", "Board.png")).convert()),
                                     (int(HEIGHT / 4), int(HEIGHT / 4)))


class MiniBoard:

    def __init__(self, num, x, y):
        self.x = x
        self.y = y
        self.num = num

        self.spaces = [[0, 0, 0],  # 0 = empty, 1 = X, 2 = O
                       [0, 0, 0],
                       [0, 0, 0]]

        self.status = "play"  # can be play, draw, 1, 2

    def draw(self):
        WIN.blit(IMAGE_BOARD, (self.x, self.y))
        for row in range(0, 3):
            for col in range(0, 3):
                if self.spaces[row][col] == 1:
                    WIN.blit(IMAGE_X, (
                        (self.x + IMAGE_BOARD.get_width() * (0.1 + row / 3) - row * 0.03 * IMAGE_BOARD.get_height()),
                        (self.y + IMAGE_BOARD.get_height() * (0.1 + col / 3)) - col * 0.03 * IMAGE_BOARD.get_height())
                             )
                elif self.spaces[row][col] == 2:
                    WIN.blit(IMAGE_O, (
                        (self.x + IMAGE_BOARD.get_width() * (0.1 + row / 3) - row * 0.03 * IMAGE_BOARD.get_height()),
                        (self.y + IMAGE_BOARD.get_height() * (0.1 + col / 3)) - col * 0.03 * IMAGE_BOARD.get_height())
                             )


class MainBoard:

    def __init__(self):
        self.boards = [[None, None, None],
                       [None, None, None],
                       [None, None, None]]
        self.spaces = [[0, 0, 0],  # 0 means playable, 1 means player 1 won, 2 means player 2 won, -1 means draw
                       [0, 0, 0],
                       [0, 0, 0]]
        self.x = (WIDTH - HEIGHT) / 2
        self.y = 0
        for num in range(0, 9):
            row = num % 3
            col = int(num / 3)

            # Create the MiniBoards and get them centered in their spaces
            self.boards[row][col] = MiniBoard(num,
                                              self.x + int(
                                                  (BG.get_height() * (row / 3 + 0.07)) - row * 0.03 * BG.get_height()),
                                              self.y + int(
                                                  (BG.get_height() * (col / 3 + 0.07)) - col * 0.03 * BG.get_height())
                                              )

    def draw(self):
        for row in range(0, 3):
            for col in range(0, 3):
                if self.boards[row][col].status == "play":
                    self.boards[row][col].draw()
                elif self.boards[row][col].status == "1":
                    WIN.blit(pygame.transform.scale(IMAGE_X, (int(HEIGHT / 6), int(HEIGHT / 6))), (
                        (self.x + HEIGHT * (0.1 + row / 3) - row * 0.03 * HEIGHT),
                        (self.y + HEIGHT * (0.1 + col / 3)) - col * 0.03 * HEIGHT)
                             )
                elif self.boards[row][col].status == "2":
                    WIN.blit(pygame.transform.scale(IMAGE_O, (int(HEIGHT / 6), int(HEIGHT / 6))), (
                        (self.x + HEIGHT * (0.1 + row / 3) - row * 0.03 * HEIGHT),
                        (self.y + HEIGHT * (0.1 + col / 3)) - col * 0.03 * HEIGHT)
                             )


def main(tp):
    # Variables
    two_player = tp
    cpu_turn = False
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    board = MainBoard()
    cur_mark = 1  # 1 is X, 2 is O
    mini_view = False
    mini_board = None

    def render():
        # Display Background
        pygame.draw.rect(WIN, [255, 255, 255], [0, 0, WIDTH, HEIGHT], 0)
        WIN.blit(BG, ((WIDTH - HEIGHT) / 2, 0))

        # Determine whether to render single board or all boards
        if mini_view:
            single_board(mini_board)
        else:

            # Display Turn
            turn_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.05))
            if cur_mark == 1:
                turn = 'X'
            else:
                turn = 'O'
            turn_label = turn_font.render(f"Player Turn: {turn}", 1, (0, 0, 0))
            menu_label = turn_font.render("Press m to exit to menu", 1, (0, 0, 0))
            WIN.blit(turn_label, (WIDTH / 90, HEIGHT / 90))
            WIN.blit(menu_label, (WIDTH / 90, HEIGHT * 0.9))
            # Draw MainBoard
            board.draw()

        pygame.display.update()

    while run:
        # Tick method
        clock.tick(FPS)
        render()
        square_clicked = None
        keys = pygame.key.get_pressed()

        # Exit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Determine which square was clicked on and assign to square_clicked
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if board.x <= pos[0] <= board.x + BG.get_height() / 3 \
                        and board.y <= pos[1] <= board.y + BG.get_height() / 3:
                    # First square selected
                    square_clicked = 0
                elif board.x + BG.get_height() / 2.8 <= pos[
                    0] <= board.x + BG.get_height() / 2.8 + BG.get_height() / 3.6 \
                        and board.y <= pos[1] <= board.y + BG.get_height() / 3:
                    # Second square selected
                    square_clicked = 1
                elif board.x + BG.get_height() / 1.5 <= pos[0] <= board.x + BG.get_height() / 1.5 + BG.get_height() / 3 \
                        and board.y <= pos[1] <= board.y + BG.get_height() / 3:
                    # Third square selected
                    square_clicked = 2
                elif board.x <= pos[0] <= board.x + BG.get_height() / 3 and \
                        board.y + BG.get_height() / 2.8 <= pos[
                    1] <= board.y + BG.get_height() / 2.8 + BG.get_height() / 3.6:
                    # Fourth square selected
                    square_clicked = 3
                elif board.x + BG.get_height() / 2.8 <= pos[
                    0] <= board.x + BG.get_height() / 2.8 + BG.get_height() / 3.6 and \
                        board.y + BG.get_height() / 2.8 <= pos[
                    1] <= board.y + BG.get_height() / 2.8 + BG.get_height() / 3.6:
                    # Fifth square selected
                    square_clicked = 4
                elif board.x + BG.get_height() / 1.5 <= pos[
                    0] <= board.x + BG.get_height() / 1.5 + BG.get_height() / 3 and \
                        board.y + BG.get_height() / 2.8 <= pos[
                    1] <= board.y + BG.get_height() / 2.8 + BG.get_height() / 3.6:
                    # Sixth square selected
                    square_clicked = 5
                elif board.x <= pos[0] <= board.x + BG.get_height() / 3 and \
                        board.y + BG.get_height() / 1.5 <= pos[
                    1] <= board.y + BG.get_height() / 1.5 + BG.get_height() / 3:
                    # 7th square selected
                    square_clicked = 6
                elif board.x + BG.get_height() / 2.8 <= pos[
                    0] <= board.x + BG.get_height() / 2.8 + BG.get_height() / 3.6 and \
                        board.y + BG.get_height() / 1.5 <= pos[
                    1] <= board.y + BG.get_height() / 1.5 + BG.get_height() / 3:
                    # 8th square selected
                    square_clicked = 7
                elif board.x + BG.get_height() / 1.5 <= pos[
                    0] <= board.x + BG.get_height() / 1.5 + BG.get_height() / 3 and \
                        board.y + BG.get_height() / 1.5 <= pos[
                    1] <= board.y + BG.get_height() / 1.5 + BG.get_height() / 3:
                    # 9th square selected
                    square_clicked = 8

        # Check for CPU turn
        if not two_player and cpu_turn:
            board_played = cpu_move(board, cur_mark)
            cpu_turn = False
            # Check if MiniBoard was won, if True check if MainBoard was won
            if check_win(board_played, cur_mark):
                board_played.status = f"{cur_mark}"
                board.spaces[board_played.num % 3][int(board_played.num / 3)] = cur_mark
                if check_win(board, cur_mark):
                    win_menu(cur_mark, board, tp)

            # Check if the MiniBoard is a draw
            else:
                mini_draw = True
                for s in range(0, 9):
                    if board_played.spaces[s % 3][int(s / 3)] == 0:
                        mini_draw = False
                        break
                if mini_draw:
                    board_played.status = "draw"
                    board.spaces[board_played.num % 3][int(board_played.num / 3)] = -1

            # Check if whole board is now full
            game_draw = True
            for i in range(0, 9):
                if board.spaces[i % 3][int(i / 3)] == 0:
                    game_draw = False
                    break
            if game_draw:
                tie_breaker(board, tp)
            if cur_mark == 1:
                cur_mark = 2
            else:
                cur_mark = 1
            continue

        # Return to main view
        if mini_view and keys[pygame.K_ESCAPE]:
            mini_view = False
            mini_board = None

        # Return to menu
        if not mini_view and keys[pygame.K_m]:
            run = False
            start_menu()

        # Zoom in on board clicked on
        elif not mini_view and square_clicked is not None:
            if board.boards[square_clicked % 3][int(square_clicked / 3)].status != "play":
                continue
            mini_view = True
            mini_board = board.boards[square_clicked % 3][int(square_clicked / 3)]

        # Place X or O mark and check for wins, draws
        elif mini_view and square_clicked is not None:
            if mini_board.spaces[square_clicked % 3][int(square_clicked / 3)] != 0:
                continue
            mini_board.spaces[square_clicked % 3][int(square_clicked / 3)] = cur_mark
            cpu_turn = True

            # Check if MiniBoard was won, if True check if MainBoard was won
            if check_win(mini_board, cur_mark):
                mini_board.status = f"{cur_mark}"
                board.spaces[mini_board.num % 3][int(mini_board.num / 3)] = cur_mark
                if check_win(board, cur_mark):
                    win_menu(cur_mark, board, tp)

            # Check if the MiniBoard is a draw
            else:
                mini_draw = True
                for s in range(0, 9):
                    if mini_board.spaces[s % 3][int(s / 3)] == 0:
                        mini_draw = False
                        break
                if mini_draw:
                    mini_board.status = "draw"
                    board.spaces[mini_board.num % 3][int(mini_board.num / 3)] = -1

            # Check if whole board is now full
            game_draw = True
            for i in range(0, 9):
                if board.spaces[i % 3][int(i / 3)] == 0:
                    game_draw = False
                    break
            if game_draw:
                tie_breaker(board, tp)

            # Toggle Player Turn
            if cur_mark == 1:
                cur_mark = 2
            else:
                cur_mark = 1
            mini_view = False
            mini_board = None

    quit()


# Decided where the CPU player will move
def cpu_move(board, mark):
    if mark == 1:
        opp_mark = 2
    else:
        opp_mark = 1

        # 1 out of 20 chance CPU makes "mistake" and plays randomly
        mistake = random.randint(1, 20)
        if mistake == 1:
            # CPU makes mistake
            print("MISTAKE")
            r_board = random.randint(0, 8)
            r_space = random.randint(0, 8)
            # Re-pick random numbers as long as the spot is unplayable
            while board.spaces[r_board % 3][int(r_board / 3)] != 0 or \
                    board.boards[r_board % 3][int(r_board / 3)].spaces[r_space % 3][int(r_space / 3)] != 0:
                r_board = random.randint(0, 8)
                r_space = random.randint(0, 8)
            board.boards[r_board % 3][int(r_board / 3)].spaces[r_space % 3][int(r_space / 3)] = mark
            return board.boards[r_board % 3][int(r_board / 3)]

        # Play to win game if possible
        for i in range(0, 9):
            if board.spaces[i % 3][int(i / 3)] != 0:
                continue
            mini_board = board.boards[i % 3][int(i / 3)]
            for j in range(0, 9):
                if mini_board.spaces[j % 3][int(j / 3)] != 0:
                    continue
                mini_board.spaces[j % 3][int(j / 3)] = mark
                if check_win(mini_board, mark):
                    board.spaces[i % 3][int(i / 3)] = mark
                    if check_win(board, mark):
                        board.spaces[i % 3][int(i / 3)] = 0
                        return mini_board
                    else:
                        board.spaces[i % 3][int(i / 3)] = 0
                        mini_board.spaces[j % 3][int(j / 3)] = 0
                else:
                    mini_board.spaces[j % 3][int(j / 3)] = 0

        # Play to stop opponent from winning game if possible
        for i in range(0, 9):
            if board.spaces[i % 3][int(i / 3)] != 0:
                continue
            mini_board = board.boards[i % 3][int(i / 3)]
            for j in range(0, 9):
                if mini_board.spaces[j % 3][int(j / 3)] != 0:
                    continue
                mini_board.spaces[j % 3][int(j / 3)] = opp_mark
                if check_win(mini_board, opp_mark):
                    board.spaces[i % 3][int(i / 3)] = opp_mark
                    if check_win(board, opp_mark):
                        board.spaces[i % 3][int(i / 3)] = 0
                        mini_board.spaces[j % 3][int(j / 3)] = mark
                        return mini_board
                    else:
                        board.spaces[i % 3][int(i / 3)] = 0
                        mini_board.spaces[j % 3][int(j / 3)] = 0
                else:
                    mini_board.spaces[j % 3][int(j / 3)] = 0

    # Will play to win a mini board if possible
    for i in range(0, 9):
        if board.spaces[i % 3][int(i / 3)] != 0:
            continue
        mini_board = board.boards[i % 3][int(i / 3)]
        for j in range(0, 9):
            if mini_board.spaces[j % 3][int(j / 3)] != 0:
                continue
            mini_board.spaces[j % 3][int(j / 3)] = mark
            if check_win(mini_board, mark):
                return mini_board
            else:
                mini_board.spaces[j % 3][int(j / 3)] = 0

    # Will play to try to prevent other player from winning a mini board
    for i in range(0, 9):
        if board.spaces[i % 3][int(i / 3)] != 0:
            continue
        mini_board = board.boards[i % 3][int(i / 3)]
        for j in range(0, 9):
            if mini_board.spaces[j % 3][int(j / 3)] != 0:
                continue
            mini_board.spaces[j % 3][int(j / 3)] = opp_mark
            if check_win(mini_board, opp_mark):
                mini_board.spaces[j % 3][int(j / 3)] = mark
                return mini_board
            else:
                mini_board.spaces[j % 3][int(j / 3)] = 0

    # Check for moves that cause two separate ways to get 3 in a row
    for i in range(0, 9):
        if board.spaces[i % 3][int(i / 3)] != 0:
            continue
        mini_board = board.boards[i % 3][int(i / 3)]

        # Find spot to make first move in
        for j in range(0, 9):
            if mini_board.spaces[j % 3][int(j / 3)] != 0:
                continue
            mini_board.spaces[j % 3][int(j / 3)] = mark

            # Check if there are two possible moves that can be made afterwards to win
            for k in range(0, 9):
                if mini_board.spaces[k % 3][int(k / 3)] != 0:
                    continue
                mini_board.spaces[k % 3][int(k / 3)] = mark
                if check_win(mini_board, mark):
                    mini_board.spaces[k % 3][int(k / 3)] = 0
                    for l in range(0, 9):
                        if mini_board.spaces[l % 3][int(l / 3)] != 0 or l == k:
                            continue
                        mini_board.spaces[l % 3][int(l / 3)] = mark
                        if check_win(mini_board, mark):
                            mini_board.spaces[l % 3][int(l / 3)] = 0
                            return mini_board
                        else:
                            mini_board.spaces[l % 3][int(l / 3)] = 0
                mini_board.spaces[k % 3][int(k / 3)] = 0
            mini_board.spaces[j % 3][int(j / 3)] = 0

    # Check for moves that causes two separate ways to get 3 in a row for opponent
    for i in range(0, 9):
        if board.spaces[i % 3][int(i / 3)] != 0:
            continue
        mini_board = board.boards[i % 3][int(i / 3)]

        # Find spot to make first move in
        for j in range(0, 9):
            if mini_board.spaces[j % 3][int(j / 3)] != 0:
                continue
            mini_board.spaces[j % 3][int(j / 3)] = opp_mark

            # Check if there are two possible moves that can be made afterwards to win
            for k in range(0, 9):
                if mini_board.spaces[k % 3][int(k / 3)] != 0:
                    continue
                mini_board.spaces[k % 3][int(k / 3)] = opp_mark
                if check_win(mini_board, opp_mark):
                    mini_board.spaces[k % 3][int(k / 3)] = 0
                    for l in range(0, 9):
                        if mini_board.spaces[l % 3][int(l / 3)] != 0 or l == k:
                            continue
                        mini_board.spaces[l % 3][int(l / 3)] = opp_mark
                        if check_win(mini_board, opp_mark):
                            mini_board.spaces[l % 3][int(l / 3)] = 0
                            mini_board.spaces[j % 3][int(j / 3)] = mark
                            return mini_board
                        else:
                            mini_board.spaces[l % 3][int(l / 3)] = 0
                mini_board.spaces[k % 3][int(k / 3)] = 0
            mini_board.spaces[j % 3][int(j / 3)] = 0

    # Last case: Play in random spot
    r_board = random.randint(0, 8)
    r_space = random.randint(0, 8)
    # Re-pick random numbers as long as the spot is unplayable
    while board.spaces[r_board % 3][int(r_board / 3)] != 0 or \
            board.boards[r_board % 3][int(r_board / 3)].spaces[r_space % 3][int(r_space / 3)] != 0:
        r_board = random.randint(0, 8)
        r_space = random.randint(0, 8)
    board.boards[r_board % 3][int(r_board / 3)].spaces[r_space % 3][int(r_space / 3)] = mark
    return board.boards[r_board % 3][int(r_board / 3)]


def win_menu(player, board, tp):
    run = True
    title_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.3))
    small_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.05))
    title_label = title_font.render(f"Player {player} Won!", 1, (100, 100, 0))
    quit_label = small_font.render("Press m for Menu", 1, (0, 0, 0))
    replay_label = small_font.render("Press r to Play Again", 1, (0, 0, 0))
    while run:

        # Exit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Render Labels
        pygame.draw.rect(WIN, [255, 255, 255], [0, 0, WIDTH, HEIGHT], 0)
        WIN.blit(BG, ((WIDTH - HEIGHT) / 2, 0))
        board.draw()

        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT * 0.2))
        WIN.blit(quit_label, (WIDTH / 90, HEIGHT * 0.8))
        WIN.blit(replay_label, (WIDTH / 90, HEIGHT * 0.9))
        pygame.display.update()

        # Handle Key Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            start_menu()
        if keys[pygame.K_r]:
            main(tp)

    pass


def tie_breaker(board, tp):
    run = True
    title_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.3))
    small_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.05))
    quit_label = small_font.render("Press m for Menu", 1, (0, 0, 0))
    replay_label = small_font.render("Press r to Play Again", 1, (0, 0, 0))

    # Determine Tie Breaker
    # Whoever won most mini boards wins Tie Breaker
    count = 0
    for tb in range(0, 9):
        if board.spaces[tb % 3][int(tb / 3)] == 1:
            count += 1
        elif board.spaces[tb % 3][int(tb / 3)] == 2:
            count -= 1
    if count > 0:
        title_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.15))
        title_label = title_font.render("Player 1 Won by Tie Breaker!", 1, (100, 100, 0))
    elif count < 0:
        title_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.15))
        title_label = title_font.render("Player 2 Won by Tie Breaker!", 1, (100, 100, 0))
    else:
        title_label = title_font.render("It's a Draw!", 1, (100, 100, 0))

    while run:

        # Exit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Render Labels
        pygame.draw.rect(WIN, [255, 255, 255], [0, 0, WIDTH, HEIGHT], 0)
        WIN.blit(BG, ((WIDTH - HEIGHT) / 2, 0))
        board.draw()

        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT * 0.2))
        WIN.blit(quit_label, (WIDTH / 90, HEIGHT * 0.8))
        WIN.blit(replay_label, (WIDTH / 90, HEIGHT * 0.9))
        pygame.display.update()

        # Handle Key Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            start_menu()
        if keys[pygame.K_r]:
            main(tp)
    pass


def check_win(board, player):
    # Returns 0 if no one has won, 1 or 2 if someone has won
    for r in range(0, 3):

        # Check horizontal win
        if board.spaces[r][0] == player:
            if board.spaces[r][1] == player:
                if board.spaces[r][2] == player:
                    return True

        # Check vertical win
        if board.spaces[0][r] == player:
            if board.spaces[1][r] == player:
                if board.spaces[2][r] == player:
                    return True

    # Check Diagonals
    if board.spaces[1][1] == player:
        if (board.spaces[0][0] == player and board.spaces[2][2] == player) or \
                (board.spaces[0][2] == player and board.spaces[2][0] == player):
            return True

    return False


def single_board(board):
    board_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.05))
    board_label = board_font.render(f"Board Number {board.num + 1}", 1, (0, 0, 0))
    esc_label = board_font.render("Press ESC to see all boards.", 1, (0, 0, 0))
    WIN.blit(board_label, (WIDTH / 90, HEIGHT / 90))
    WIN.blit(esc_label, (WIDTH / 90, HEIGHT * 0.9))
    height = BG.get_height()
    x = (WIDTH - HEIGHT) / 2
    y = 0
    for row in range(0, 3):
        for col in range(0, 3):
            if board.spaces[row][col] == 1:
                WIN.blit(pygame.transform.scale(IMAGE_X, (int(HEIGHT / 6), int(HEIGHT / 6))), (
                    (x + height * (0.1 + row / 3) - row * 0.03 * height),
                    (y + height * (0.1 + col / 3)) - col * 0.03 * height)
                         )
            elif board.spaces[row][col] == 2:
                WIN.blit(pygame.transform.scale(IMAGE_O, (int(HEIGHT / 6), int(HEIGHT / 6))), (
                    (x + height * (0.1 + row / 3) - row * 0.03 * height),
                    (y + height * (0.1 + col / 3)) - col * 0.03 * height)
                         )


def start_menu():
    title_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.3))
    small_font = pygame.font.SysFont("comicsans", int(HEIGHT * 0.05))
    title_label = title_font.render("X-O Duel", 1, (210, 160, 0))
    small_label = small_font.render("Play 2-Player Game", 1, (255, 255, 255))
    single_player_label = small_font.render("Play against CPU", 1, (255, 255, 255))
    quit_label = small_font.render("Press q to quit", 1, (255, 255, 255))
    run = True
    while run:
        keys = pygame.key.get_pressed()
        pygame.draw.rect(WIN, [80, 80, 224], [0, 0, WIDTH, HEIGHT], 0)
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT * 0.2))
        WIN.blit(quit_label, (WIDTH / 90, HEIGHT * 0.9))
        WIN.blit(small_label, (WIDTH / 2 - small_label.get_width() / 2, HEIGHT * 0.6))
        WIN.blit(single_player_label, (WIDTH / 2 - single_player_label.get_width() / 2, HEIGHT * 0.75))
        # Rectangle around 2 player game button
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(WIDTH / 2 - small_label.get_width() / 1.8, HEIGHT * 0.565, small_label.get_width() * 1.1, HEIGHT * 0.1), 2)
        # Rectangle around CPU Game button
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(WIDTH / 2 - small_label.get_width() / 1.8, HEIGHT * 0.72, small_label.get_width() * 1.1, HEIGHT * 0.1), 2)
        pygame.display.update()

        if keys[pygame.K_q]:
            quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # 2 player game
                if WIDTH / 2 - small_label.get_width() / 1.8 <= pos[0] <= \
                        WIDTH / 2 - small_label.get_width() / 1.8 + small_label.get_width() * 1.1 \
                        and HEIGHT * 0.565 <= pos[1] <= HEIGHT * 0.665:
                    run = False
                    WIN.fill((255, 255, 255))
                    main(True)
                # 1 player game
                if WIDTH / 2 - small_label.get_width() / 1.8 <= pos[0] <= \
                        WIDTH / 2 - small_label.get_width() / 1.8 + small_label.get_width() * 1.1 \
                        and HEIGHT * 0.72 <= pos[1] <= HEIGHT * 0.82:
                    run = False
                    WIN.fill((255, 255, 255))
                    main(False)


start_menu()
