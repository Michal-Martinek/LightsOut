import pygame
import random
import time
import math
pygame.init()

NODE_NUMBER = 3
NODE_SIZE = 120
NODE_SPACING = 25
BLOCK_SIZE = NODE_SIZE + NODE_SPACING

HEADER_HEIGHT = 50
SCREEN_WIDTH = NODE_NUMBER  * BLOCK_SIZE + NODE_SPACING
SCREEN_HEIGHT = NODE_NUMBER  * BLOCK_SIZE + NODE_SPACING + HEADER_HEIGHT

SMILEY_POS = ((SCREEN_WIDTH - 40) // 2, (HEADER_HEIGHT - 40) // 2)
LABEL_POS = ((SCREEN_WIDTH - SMILEY_POS[0] - 120) // 2 + SMILEY_POS[0] + 40, 3)

# assets
IMAGE_BULB_LIT = pygame.image.load('Assets\\BulbLit.png')
IMAGE_BULB_LIT.set_colorkey((255, 255, 255))
IMAGE_BULB_DARK = pygame.image.load('Assets\\BulbDark.png')
IMAGE_BULB_DARK.set_colorkey((255, 255, 255))

IMAGE_WIN = pygame.image.load('Assets\\FaceWin.png')
IMAGE_WIN.set_colorkey((255, 255, 255))
IMAGE_GAME = pygame.image.load('Assets\\FaceGame.png')
IMAGE_GAME.set_colorkey((255, 255, 255))


class LightsGrid:
    def generateNeighborRules(self):
        for x in range(self.size):
            for y in range(self.size):
                for neighborX in range(x-1, x+2):
                    for neighborY in range(y-1, y+2):
                        if 0 <= neighborX < self.size and 0 <= neighborY < self.size:
                            if (x == neighborX and y == neighborY) or random.random() >= 0.5:
                                self.neighborRules[y][x].append( (neighborX, neighborY) )

    def generateGrid(self):
        numMoves = random.randint(2, self.size**2-1)
        bulbs = []
        for x in range(self.size):
            bulbs.extend( [(x, y) for y in range(self.size)] )
        moves = random.sample(bulbs, numMoves)
        for move in moves:
            self.toggleAt(move)
    def __init__(self, size: int):
        self.size = size
        self.grid = [[True for x in range(size)] for y in range(size)]
        self.neighborRules = [[[] for x in range(size)] for y in range(size)]
        self.generateNeighborRules()
        self.generateGrid()
        
    def drawGrid(self, display):
        for y, row in enumerate(self.grid):
            for x, bulb in enumerate(row):
                image = IMAGE_BULB_LIT if bulb else IMAGE_BULB_DARK
                display.blit(image, (x * BLOCK_SIZE + NODE_SPACING, y * BLOCK_SIZE + NODE_SPACING + HEADER_HEIGHT))

    def toggleAt(self, pos):
        for x, y in self.neighborRules[pos[1]][pos[0]]:
            self.grid[y][x] = not self.grid[y][x]
    def click(self, pos) -> bool:
        pos = [pos[0], pos[1] - HEADER_HEIGHT]
        if pos[1] < 0: return False
        clicked = pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE
        remaining = pos[0] % BLOCK_SIZE, pos[1] % BLOCK_SIZE
        if (remaining[0] >= NODE_SPACING) and (remaining[1] >= NODE_SPACING):
            if (clicked[0] < self.size and clicked[1] < self.size):
                self.toggleAt(clicked)
        return all([all(row) for row in self.grid])

def smileyClicked(pos) -> bool:
    return SMILEY_POS[0] <= pos[0] <= SMILEY_POS[0]+40 and SMILEY_POS[1] <= pos[1] <= SMILEY_POS[1]+40

def main():
    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Lights Out')
    grid = LightsGrid(NODE_NUMBER)
    clock = pygame.time.Clock()
    gameWon = False
    smileyFirstClicked = False

    gameStartTime = time.time()
    timeFont = pygame.font.SysFont('arial', 40, bold=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not gameWon:
                    gameWon = grid.click(event.pos)
                if smileyClicked(event.pos):
                    if smileyFirstClicked:
                        grid = LightsGrid(NODE_NUMBER)
                        gameWon = False
                        smileyFirstClicked = False
                        gameStartTime = time.time()
                    else: 
                        smileyFirstClicked = True

        display.fill((255, 255, 255))
        grid.drawGrid(display)

        pygame.draw.rect(display, (0, 0, 255), (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))
        display.blit((IMAGE_WIN if gameWon else IMAGE_GAME), SMILEY_POS)

        # time counter
        if not gameWon:
            dt = math.floor(time.time() - gameStartTime)
        minutes = dt // 60
        seconds = dt - 60 * minutes
        label = timeFont.render(f'{minutes}:{seconds:0>2}', False, (255, 0, 0))
        display.blit(label, LABEL_POS)

        pygame.display.update()
        clock.tick(30)
    pygame.quit()

if __name__ == '__main__':
    main()
