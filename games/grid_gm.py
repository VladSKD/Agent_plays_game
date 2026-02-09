import pygame
import random
import sys
import re
import lmstudio as lms

# 1. Ініціалізація моделі
# Порада: Qwen 2.5 (1.5B) значно краще впорається з цим лабіринтом
model = lms.llm("qwen/qwen3-vl-4b")

pygame.init()

TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 15, 10
WIDTH, HEIGHT = GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Collector: Epsilon-Greedy Learning")

WHITE, BLUE, GOLD, GRAY, BLACK = (240, 240, 240), (50, 100, 255), (255, 215, 0), (100, 100, 100), (0, 0, 0)
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

LEVEL_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,1,0,1,1,1,0,1,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,1,1,1,0,1,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

player_x, player_y = 1, 1

def spawn_coin():
    while True:
        x, y = random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)
        if LEVEL_MAP[y][x] == 0 and (x, y) != (player_x, player_y): return x, y

coin_x, coin_y = spawn_coin()
coins_collected = 0
moves_count = 0
last_ai_decision = "Waiting..."
move_history = [] 

# --- НАЛАШТУВАННЯ НАВЧАННЯ ---
EPSILON = 0.2  # 20% шанс випадкового ходу для виходу з циклу (Exploration)

running = True
while running:
    clock.tick(6)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 1. Стан оточення
    walls = []
    if LEVEL_MAP[player_y-1][player_x] == 1: walls.append("UP")
    if LEVEL_MAP[player_y+1][player_x] == 1: walls.append("DOWN")
    if LEVEL_MAP[player_y][player_x-1] == 1: walls.append("LEFT")
    if LEVEL_MAP[player_y][player_x+1] == 1: walls.append("RIGHT")

    possible_moves = [d for d in ["UP", "DOWN", "LEFT", "RIGHT"] if d not in walls]
    
    # Розрахунок відстані (Мангеттенська відстань)
    dist_now = abs(player_x - coin_x) + abs(player_y - coin_y)
    
    # Підказка для AI: які ходи реально наближають до цілі
    better_moves = []
    if coin_x > player_x and "RIGHT" not in walls: better_moves.append("RIGHT")
    if coin_x < player_x and "LEFT" not in walls: better_moves.append("LEFT")
    if coin_y > player_y and "DOWN" not in walls: better_moves.append("DOWN")
    if coin_y < player_y and "UP" not in walls: better_moves.append("UP")

    # 2. ПРИЙНЯТТЯ РІШЕННЯ (Epsilon-Greedy)
    dx, dy, decision = 0, 0, ""

    if random.random() < EPSILON:
        # ВИПАДКОВИЙ ХІД (щоб не зациклюватись)
        decision = random.choice(possible_moves) if possible_moves else ""
        last_ai_decision = f"EXPLORE: {decision}"
    else:
        # ЗАПИТ ДО AI
        history_context = "\n".join(move_history[-3:]) if move_history else "None"
        prompt = f"""
        POS: ({player_x}, {player_y}). TARGET: ({coin_x}, {coin_y}). Dist: {dist_now}
        WALLS: {walls}. AVAILABLE: {possible_moves}.
        HINT: Moves that reduce distance: {better_moves if better_moves else "Any"}.
        
        RECENT HISTORY (Avoid loops!):
        {history_context}
        
        Instruction: Choose ONE move from AVAILABLE to reach the coin.
        Decision:"""

        try:
            raw_response = str(model.respond(prompt)).upper()
            words = re.sub(r'[^A-Z]', ' ', raw_response).split()
            for word in reversed(words):
                if word in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    decision = word
                    break
            last_ai_decision = decision
        except:
            last_ai_decision = "Error"

    # 3. Виконання руху
    if decision == "LEFT": dx = -1
    elif decision == "RIGHT": dx = 1
    elif decision == "UP": dy = -1
    elif decision == "DOWN": dy = 1

    new_x, new_y = player_x + dx, player_y + dy
    
    if 0 <= new_y < GRID_HEIGHT and 0 <= new_x < GRID_WIDTH:
        if LEVEL_MAP[new_y][new_x] == 0:
            # Оновлюємо історію ПЕРЕД зміною позиції для розуміння циклів
            move_history.append(f"At ({player_x}, {player_y}) moved {decision} -> SUCCESS")
            player_x, player_y = new_x, new_y
            if dx != 0 or dy != 0: moves_count += 1
        else:
            move_history.append(f"At ({player_x}, {player_y}) tried {decision} -> HIT WALL")

    # Збір монети
    if player_x == coin_x and player_y == coin_y:
        coins_collected += 1
        coin_x, coin_y = spawn_coin()
        move_history.append("!!! COIN COLLECTED !!!")

    # 4. Малювання
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if LEVEL_MAP[y][x] == 1:
                pygame.draw.rect(screen, GRAY, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    pygame.draw.circle(screen, GOLD, (coin_x*TILE_SIZE + 20, coin_y*TILE_SIZE + 20), 10)
    pygame.draw.rect(screen, BLUE, (player_x*TILE_SIZE, player_y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    status_text = font.render(f"Coins: {coins_collected} | Decision: {last_ai_decision}", True, BLACK)
    screen.blit(status_text, (10, 10))
    pygame.display.flip()

pygame.quit()