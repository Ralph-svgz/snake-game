import pygame
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

class SnakeGame:
    def __init__(self, width=640, height=480, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        
        # Initialize Pygame for font support (display init happens in main usually, but we need fonts)
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 25)
        
        self.reset()

    def reset(self):
        self.direction = 'RIGHT'
        self.head = [self.width // 2, self.height // 2]
        self.snake = [self.head, 
                      [self.head[0] - self.block_size, self.head[1]],
                      [self.head[0] - 2*self.block_size, self.head[1]]]
        self.score = 0
        self.food = None
        self._place_food()
        self.game_over = False

    def _place_food(self):
        x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
        self.food = [x, y]
        if self.food in self.snake:
            self._place_food()

    def update(self, new_direction=None):
        if self.game_over:
            return

        # Update direction if valid (cannot reverse directly)
        if new_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        elif new_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif new_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif new_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'

        # Move head
        x, y = self.head
        if self.direction == 'RIGHT':
            x += self.block_size
        elif self.direction == 'LEFT':
            x -= self.block_size
        elif self.direction == 'UP':
            y -= self.block_size
        elif self.direction == 'DOWN':
            y += self.block_size
        
        self.head = [x, y]

        # Check collisions
        if (x < 0 or x >= self.width or 
            y < 0 or y >= self.height or 
            self.head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, self.head)

        # Check food
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

    def draw(self, surface):
        surface.fill(BLACK)
        
        # Draw Snake
        for pt in self.snake:
            pygame.draw.rect(surface, GREEN, pygame.Rect(pt[0], pt[1], self.block_size, self.block_size))
            
        # Draw Food
        pygame.draw.rect(surface, RED, pygame.Rect(self.food[0], self.food[1], self.block_size, self.block_size))
        
        # Draw Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, [0, 0])
        
        if self.game_over:
            msg = self.font.render("Game Over! Press R to Restart", True, WHITE)
            text_rect = msg.get_rect(center=(self.width/2, self.height/2))
            surface.blit(msg, text_rect)
