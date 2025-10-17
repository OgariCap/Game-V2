

import pygame
import sys
import random
import math


pygame.init()


WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe + Punishment Wheel")


pygame_icon = pygame.image.load('icon.png')  
pygame.display.set_icon(pygame_icon)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
GRAY  = (230, 230, 230)


font_big = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 30)


state = "menu"


start_button = pygame.Rect(200, 250, 200, 80)


board = [""] * 9   
player = "X"
winner = None
game_over = False


GRID_SIZE = 400
GRID_X = (WIDTH - GRID_SIZE) // 2
GRID_Y = (HEIGHT - GRID_SIZE) // 2
CELL_SIZE = GRID_SIZE // 3


wheel_items = [
    "Do 10 Pushups", "Sing a Song", "Dance", "Tell a Joke",
    "Drink Water", "Do 5 Squats", "Act Like a Cat", "Clap 10 Times"
]
angle_per_item = 360 / len(wheel_items)
rotation = 0
spinning = False
spin_speed = 0
selected_item = None
center = (WIDTH // 2, HEIGHT // 2)
radius = 200


wheel_colors = [
    (255, 204, 102), (102, 204, 255),
    (255, 153, 204), (153, 255, 153)
] * 2




def draw_menu():
    """Draws the start menu screen"""
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, start_button)
    text = font_big.render("START", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 265))


def draw_board():
    """Draws the 3x3 Tic Tac Toe grid and pieces"""
    screen.fill(GRAY)


    for i in range(1, 3):
        pygame.draw.line(screen, BLACK,
                         (GRID_X, GRID_Y + i * CELL_SIZE),
                         (GRID_X + GRID_SIZE, GRID_Y + i * CELL_SIZE), 5)
        pygame.draw.line(screen, BLACK,
                         (GRID_X + i * CELL_SIZE, GRID_Y),
                         (GRID_X + i * CELL_SIZE, GRID_Y + GRID_SIZE), 5)

 
    for i in range(9):
        row, col = divmod(i, 3)
        x = GRID_X + col * CELL_SIZE + CELL_SIZE // 2
        y = GRID_Y + row * CELL_SIZE + CELL_SIZE // 2
        if board[i] != "":
            mark = font_big.render(board[i], True, BLACK)
            mark_rect = mark.get_rect(center=(x, y))
            screen.blit(mark, mark_rect)


def draw_wheel():
    """Draws the punishment wheel"""
    for i, item in enumerate(wheel_items):
        start_angle = math.radians(i * angle_per_item + rotation)
        end_angle = math.radians((i + 1) * angle_per_item + rotation)

        pygame.draw.polygon(screen, wheel_colors[i % len(wheel_colors)], [
            center,
            (center[0] + radius * math.cos(start_angle),
             center[1] + radius * math.sin(start_angle)),
            (center[0] + radius * math.cos(end_angle),
             center[1] + radius * math.sin(end_angle))
        ])

    
        text_angle = math.radians(i * angle_per_item + angle_per_item / 2 + rotation)
        x = center[0] + math.cos(text_angle) * (radius / 1.5)
        y = center[1] + math.sin(text_angle) * (radius / 1.5)
        text = font_small.render(item, True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    
    pygame.draw.polygon(screen, BLACK, [
        (center[0], center[1] - radius - 15),
        (center[0] - 15, center[1] - radius + 15),
        (center[0] + 15, center[1] - radius + 15)
    ])




def check_winner():
    """Checks if someone won or if it's a tie"""
    global winner, game_over
    win_combos = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a, b, c in win_combos:
        if board[a] == board[b] == board[c] != "":
            winner = board[a]
            game_over = True
            return
    if "" not in board:
        winner = "Tie"
        game_over = True


def handle_click(pos):
    """Handles what happens when the mouse is clicked"""
    global state, player, board, winner, game_over
    global spinning, spin_speed, selected_item

    if state == "menu":
        if start_button.collidepoint(pos):
            
            board = [""] * 9
            player = "X"
            winner = None
            game_over = False
            state = "game"

    elif state == "game":
        if not game_over:
            if GRID_X <= pos[0] <= GRID_X + GRID_SIZE and GRID_Y <= pos[1] <= GRID_Y + GRID_SIZE:
                col = (pos[0] - GRID_X) // CELL_SIZE
                row = (pos[1] - GRID_Y) // CELL_SIZE
                idx = int(row * 3 + col)
                if board[idx] == "":
                    board[idx] = player
                    check_winner()
                    if not game_over:
                        player = "O" if player == "X" else "X"
        else:
            state = "wheel"
            selected_item = None

    elif state == "wheel":
        if not spinning and selected_item is None:
            spin_speed = random.uniform(15, 25)
            spinning = True
        elif not spinning and selected_item is not None:
            state = "menu"


def update_wheel():
    """Makes the wheel spin and slow down"""
    global rotation, spin_speed, spinning, selected_item
    if spinning:
        rotation += spin_speed
        spin_speed *= 0.97
        if spin_speed < 0.3:
            spinning = False
            index = int(((360 - rotation % 360) % 360) // angle_per_item)
            selected_item = wheel_items[index]



clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    screen.fill(WHITE)

    if state == "menu":
        draw_menu()

    elif state == "game":
        draw_board()
        if game_over:
            msg = font_big.render(f"{winner} Wins!" if winner != "Tie" else "It's a Tie!", True, RED)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 80))
            hint = font_small.render("Click anywhere to spin the punishment wheel!", True, BLACK)
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 40))

    elif state == "wheel":
        draw_wheel()
        update_wheel()
        if selected_item:
            result = font_big.render(f"Result: {selected_item}", True, BLACK)
            screen.blit(result, (WIDTH//2 - result.get_width()//2, HEIGHT - 150))
            hint = font_small.render("Click anywhere to return to menu", True, BLACK)
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 110))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
