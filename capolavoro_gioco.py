import pygame
import random
import sys

pygame.init()

# screen impostazioni
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colori
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Direzzioni
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameState:
    START = 0
    PLAYING = 1
    GAME_OVER = 2


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow()

    def move(self):
        head = self.body[0]
        x, y = head[0] + self.direction[0], head[1] + self.direction[1]
        self.body.insert(0, (x, y))
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        x, y = tail[0] - self.direction[0], tail[1] - self.direction[1]
        self.body.append((x, y))

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def controlla_collisione(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if len(self.body) != len(set(self.body)):
            return True
        return False

    def check_food(self, food_pos):
        if self.body[0] == food_pos:
            return True
        return False

    def check_obstacle_collision(self, obstacle_pos):
        if obstacle_pos in self.body:
            return True
        return False


class Obstacle:
    def __init__(self):
        self.pos = (0, 0)

    def spawn(self, food_pos):
        while True:
            x = random.randint(max(1, food_pos[0] - 3), min(GRID_WIDTH - 2, food_pos[0] + 3))
            y = random.randint(max(1, food_pos[1] - 3), min(GRID_HEIGHT - 2, food_pos[1] + 3))
            if (x, y) != food_pos and (x, y) not in snake.body:
                self.pos = (x, y)
                return

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def genera_cibo():
    while True:
        food_pos = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
        if food_pos not in snake.body:
            return food_pos


def home_menu():
    font = pygame.font.Font(None, 24)
    title_text = font.render("Mangia il verde evitando gli ostacoli in rosso", True, WHITE)
    start_text = font.render("Press Space to Start", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    SCREEN.fill(BLACK)
    SCREEN.blit(title_text, title_rect)
    SCREEN.blit(start_text, start_rect)
    pygame.display.flip()


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def show_game_over_screen(score):
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press Space to Play Again", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    SCREEN.fill(BLACK)
    SCREEN.blit(game_over_text, game_over_rect)
    SCREEN.blit(score_text, score_rect)
    SCREEN.blit(restart_text, restart_rect)
    pygame.display.flip()


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# funzione del gioco
def main():
    vel = pygame.time.Clock()
    game_state = GameState.START
    score = 0
    ostacolo = Obstacle()

    while True:
        if game_state == GameState.START:
            score = 0
            obstacle_pos = (-1, -1)
            home_menu()
            game_state = GameState.PLAYING

        elif game_state == GameState.PLAYING:
            global snake
            snake = Snake()
            pos_di_cibo = genera_cibo()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            snake.change_direction(UP)
                        elif event.key == pygame.K_DOWN:
                            snake.change_direction(DOWN)
                        elif event.key == pygame.K_LEFT:
                            snake.change_direction(LEFT)
                        elif event.key == pygame.K_RIGHT:
                            snake.change_direction(RIGHT)

                snake.move()
                if snake.controlla_collisione():
                    game_state = GameState.GAME_OVER
                    break
                if snake.check_food(pos_di_cibo):
                    snake.grow()
                    pos_di_cibo = genera_cibo()
                    score += 1
                    ostacolo.spawn(pos_di_cibo)

                if snake.check_obstacle_collision(ostacolo.pos):
                    game_state = GameState.GAME_OVER
                    break

                SCREEN.fill(BLACK)
                pygame.draw.rect(SCREEN, GREEN, (pos_di_cibo[0] * CELL_SIZE, pos_di_cibo[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                for part in snake.body:
                    pygame.draw.rect(SCREEN, WHITE, (part[0] * CELL_SIZE, part[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                
                ostacolo.draw(SCREEN)

                font = pygame.font.Font(None, 24)
                score_text = font.render(f"Score: {score}", True, WHITE)
                SCREEN.blit(score_text, (10, 10))

                pygame.display.flip()
                vel.tick(10)  # snake velocita

        elif game_state == GameState.GAME_OVER:
            show_game_over_screen(score)
            game_state = GameState.START

if __name__ == "__main__":
    main()
