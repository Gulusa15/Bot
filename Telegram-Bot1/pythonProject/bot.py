import pygame
import random
import telegram
from pygame.examples.go_over_there import screen

# Инициализировать Pygame и Telegram
pygame.init()
bot = telegram.Bot(token='7096643200:AAEUIJK05tuRj5MNkqvGtFRlJ-NxMpr_tUQ')

# Определяем игровые переменные
bw, bh = 20, 20
board_w, board_h = 10, 20
board_x, board_y = 70, 70
screen_w, screen_h = board_x + board_w * bw + bw * 5, board_y + board_h * bh + bh * 5
colors = {
    0: (0, 0, 0),
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 0, 255),
    6: (0, 255, 255),
    7: (200, 150, 50)
}
tetriminos = {
    1: [(-1, 0), (0, 0), (1, 0), (2, 0)],  # I
    2: [(-1, 1), (-1, 0), (0, 0), (1, 0)],  # J
    3: [(1, 1), (-1, 0), (0, 0), (1, 0)],  # L
    4: [(-1, 0), (0, 0), (0, 1), (1, 1)],  # O
    5: [(0, -1), (0, 0), (-1, 0), (1, -1)],  # S
    6: [(-1, -1), (-1, 0), (0, 0), (1, 0)],  # T
    7: [(0, -1), (0, 0), (-1, 1), (1, 0)]  # Z
}
board = [[0] * board_w for _ in range(board_h)]
tetrimino = None
game_over = False


# Определение функций
def get_tetrimino():
    return {
        "id": random.randint(1, 7),
        "pos": (board_w // 2 - 2, 0),
        "rot": 0
    }


def draw_board():
    for i in range(board_h):
        for j in range(board_w):
            pygame.draw.rect(screen, colors[board[i][j]], (board_x + j * bw + bw, board_y + i * bh + bh, bw, bh))


def draw_tetrimino(tetrimino):
    for block in tetriminos[tetrimino["id"]]:
        x, y = block[0] + tetrimino["pos"][0], block[1] + tetrimino["pos"][1]
        # Rotate block using rotation matrix
        if tetrimino["rot"] == 1:
            x, y = -y, x
        elif tetrimino["rot"] == 2:
            x, y = -x, -y
        elif tetrimino["rot"] == 3:
            x, y = y, -x
        x, y = x + tetrimino["pos"][0], y + tetrimino["pos"][1]
        pygame.draw.rect(screen, colors[tetrimino["id"]], (board_x + x * bw + bw, board_y + y * bh + bh, bw, bh))


def check_collision(tetrimino):
    for block in tetriminos[tetrimino["id"]]:
        x, y = block[0] + tetrimino["pos"][0], block[1] + tetrimino["pos"][1]
        if x < 0 or x >= board_w or y >= board_h or (y >= 0 and board[y][x]):
            return True
    return False


def add_tetrimino(tetrimino):
    for block in tetriminos[tetrimino["id"]]:
        x, y = block[0] + tetrimino["pos"][0], block[1] + tetrimino["pos"][1]
        board[y][x] = tetrimino["id"]


def remove_full_rows():
    full_rows = [i for i in range(board_h) if all(board[i])]
    if full_rows:
        for i in full_rows[::-1]:
            del board[i]
        board.extend([[0] * board_w for _ in range(len(full_rows))])


def restart_game():
    global board, tetrimino, game_over
    board = [[0] * board_w for _ in range(board_h)]
    tetrimino = get_tetrimino()
    game_over = False


def handle_message(message):
    global tetrimino, game_over
    if message.text == '/start':
        bot.send_message(message.chat.id, "Добро пожаловать! Введите 'r', чтобы перезапустить игру или 'p', чтобы начать играть.")
    elif message.text == 'r' and not game_over:
        restart_game()
        bot.send_message(message.chat.id, "Игра перезапущена!")
    elif message.text == 'p' and not game_over:
        restart_game()
        bot.send_message(message.chat.id, "Игра началась!")
        game_over = False
    elif not game_over:
        # Handle user input for game controls
        if message.text == 'a':
            tetrimino["pos"] = (tetrimino["pos"][0] - 1, tetrimino["pos"][1])
        elif message.text == 'd':
            tetrimino["pos"] = (tetrimino["pos"][0] + 1, tetrimino["pos"][1])
        elif message.text == 's':
            while not check_collision(tetrimino):
                tetrimino["pos"] = (tetrimino["pos"][0], tetrimino["pos"][1] + 1)
            add_tetrimino(tetrimino)
            remove_full_rows()
            tetrimino = get_tetrimino()
            if check_collision(tetrimino):
                game_over = True
                bot.send_message(message.chat.id, "Игра окончена!")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, перезапустите игру, набрав "r", или начните играть, набрав 'p'")


# Основной игровой цикл
while True:
    # Обрабатывать входящие сообщения из Telegram
    updates = bot.get_updates()
    for update in updates:
        handle_message(update.message)

    # Обновить состояние игры
    if not game_over:
        tetrimino = get_tetrimino()

    # Рендеринг игровой графики
    screen.fill((255, 255, 255))
    draw_board()
    draw_tetrimino(tetrimino)
    pygame.display.flip()

    # Дождитесь следующего кадра
    pygame.time.wait(1000 // 3)