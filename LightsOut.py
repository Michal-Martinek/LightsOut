import pygame
import random

NODE_NUMBER = 3
NODE_SIZE = 120
NODE_SPACING = 25
BLOCK_SIZE = NODE_SIZE + NODE_SPACING
SCREEN_SIZE = NODE_NUMBER  * BLOCK_SIZE + NODE_SPACING

class LightsGrid:
    def generateNeighborRules(self):
        for x in range(self.size):
            for y in range(self.size):
                for neighborX in range(x-1, x+2):
                    for neighborY in range(y-1, y+2):
                        if 0 <= neighborX < self.size and 0 <= neighborY < self.size:
                            if (x == neighborX and y == neighborY) or random.random() >= 0.5:
                                self.neighborRules[y][x].append( (neighborX, neighborY) )

    def __init__(self, size: int):
        self.size = size
        self.grid = [[(random.random() < 0.5) for x in range(size)] for y in range(size)]
        self.neighborRules = [[[] for x in range(size)] for y in range(size)]
        self.generateNeighborRules()
        
    def drawGrid(self, display):
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                color = (255, 255, 0) if node else (0, 0, 255)
                pygame.draw.rect(display, color, (x * BLOCK_SIZE + NODE_SPACING, y * BLOCK_SIZE + NODE_SPACING, NODE_SIZE, NODE_SIZE))
    def click(self, pos):
        clicked = pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE
        remaining = pos[0] % BLOCK_SIZE, pos[1] % BLOCK_SIZE
        if (remaining[0] >= NODE_SPACING) and (remaining[1] >= NODE_SPACING):
            if (clicked[0] < self.size and clicked[1] < self.size):
                for x, y in self.neighborRules[clicked[1]][clicked[0]]:
                    self.grid[y][x] = not self.grid[y][x]

def main():
    display = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption('Lights Out')
    grid = LightsGrid(NODE_NUMBER)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                grid.click(pos)
        display.fill((255, 255, 255))
        grid.drawGrid(display)
        pygame.display.update()
        clock.tick(30)
    pygame.quit()

if __name__ == '__main__':
    main()