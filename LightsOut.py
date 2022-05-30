import pygame
import random
import time
import math
from typing import Union

class Parameters:
    def __init__(self, nodeNumber):
        # screen layout
        self.NODE_NUMBER = nodeNumber
        self.NODE_SIZE = 120 if nodeNumber < 5 else 60
        self.NODE_SPACING = 25 if nodeNumber < 5 else 13
        self.BLOCK_SIZE = self.NODE_SIZE + self.NODE_SPACING
        self.HEADER_HEIGHT = 50
        self.SCREEN_WIDTH = self.NODE_NUMBER  * self.BLOCK_SIZE + self.NODE_SPACING
        self.SCREEN_HEIGHT = self.NODE_NUMBER  * self.BLOCK_SIZE + self.NODE_SPACING + self.HEADER_HEIGHT

        # images
        self.IMAGE_BULB_LIT = pygame.image.load('Assets\\BulbLit.png')
        if self.NODE_NUMBER >= 5:
            self.IMAGE_BULB_LIT = pygame.transform.scale(self.IMAGE_BULB_LIT, (60, 60))
        self.IMAGE_BULB_LIT.set_colorkey((255, 255, 255))
        self.IMAGE_BULB_DARK = pygame.image.load('Assets\\BulbDark.png')
        if self.NODE_NUMBER >= 5:
            self.IMAGE_BULB_DARK = pygame.transform.scale(self.IMAGE_BULB_DARK, (60, 60))
        self.IMAGE_BULB_DARK.set_colorkey((255, 255, 255))
        self.IMAGE_WIN = pygame.image.load('Assets\\FaceWin.png')
        self.IMAGE_WIN.set_colorkey((255, 255, 255))
        self.IMAGE_GAME = pygame.image.load('Assets\\FaceGame.png')
        self.IMAGE_GAME.set_colorkey((255, 255, 255))
        self.IMAGE_TIMER_BOX = pygame.image.load('Assets\\TimerBox.png')
        self.IMAGE_TIMER_BOX.set_colorkey((255, 255, 255))
        self.IMAGE_DROPDOWN_ARROW = pygame.image.load('Assets\\DropdownArrow.png')
        self.IMAGE_DROPDOWN_ARROW.set_colorkey((255, 255, 255))

        # header graphics
        self.SMILEY_POS = ((self.SCREEN_WIDTH - 40) // 2, (self.HEADER_HEIGHT - 40) // 2)
        self.SMILEY_RECT = pygame.Rect((*self.SMILEY_POS, self.IMAGE_WIN.get_width(), self.IMAGE_WIN.get_height()))
        self.LABEL_POS = ((3 * self.SCREEN_WIDTH) // 4 - 40, 3)
        self.TIMER_POS = (self.LABEL_POS[0] - 9, self.LABEL_POS[1])

        self.DROPDOWN_POS = (self.SMILEY_POS[0] // 2 - 40, 3)
        self.DROPDOWN_RECT_UP = pygame.Rect((*self.DROPDOWN_POS, 80, 44))
        self.DROPDOWN_ARROW_POS = (self.DROPDOWN_POS[0] + 45, self.DROPDOWN_POS[1] + 17)
        self.DROPDOWN_RECT_DOWN = pygame.Rect((*self.DROPDOWN_RECT_UP[:3], 8 * self.DROPDOWN_RECT_UP[3] - 27))
        self.DROPDOWN_NUM_POS_FUNC = lambda i: (self.DROPDOWN_POS[0] + 13, self.DROPDOWN_POS[1] + i * 40)

        self.FONT = pygame.font.SysFont('arial', 40, bold=True)

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
        # TODO: sometimes it generates board which is already solved
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
        
    def drawGrid(self, display, params: Parameters):
        posY = params.HEADER_HEIGHT + params.NODE_SPACING
        for row in self.grid:
            posX = params.NODE_SPACING
            for bulb in row:
                image = params.IMAGE_BULB_LIT if bulb else params.IMAGE_BULB_DARK
                display.blit(image, (posX, posY))
                posX += params.BLOCK_SIZE
            posY += params.BLOCK_SIZE

    def toggleAt(self, pos):
        for x, y in self.neighborRules[pos[1]][pos[0]]:
            self.grid[y][x] = not self.grid[y][x]
    def click(self, pos, params: Parameters) -> bool:
        pos = [pos[0], pos[1] - params.HEADER_HEIGHT]
        if pos[1] < 0: return False
        clicked = pos[0] // params.BLOCK_SIZE, pos[1] // params.BLOCK_SIZE
        remaining = pos[0] % params.BLOCK_SIZE, pos[1] % params.BLOCK_SIZE
        if (remaining[0] >= params.NODE_SPACING) and (remaining[1] >= params.NODE_SPACING):
            if (clicked[0] < self.size and clicked[1] < self.size):
                self.toggleAt(clicked)
        return all([all(row) for row in self.grid])

def timerConstructor(display, params: Parameters):
    startTime = time.time()
    timePassed = 0
    def timerDrawerWrapper(gameWon):
        nonlocal timePassed
        if not gameWon:
            timePassed = math.floor(time.time() - startTime)
        label = params.FONT.render(f'{timePassed // 60:0>2}:{timePassed % 60:0>2}', False, (255, 0, 0))
        display.blit(params.IMAGE_TIMER_BOX, params.TIMER_POS)
        display.blit(label, params.LABEL_POS)
    return timerDrawerWrapper


def drawDropdown(display, dropped, params: Parameters):
    pygame.draw.rect(display, (255, 255, 255), params.DROPDOWN_RECT_DOWN if dropped else params.DROPDOWN_RECT_UP, border_radius=5)
    pygame.draw.rect(display, (0, 0, 0), params.DROPDOWN_RECT_DOWN if dropped else params.DROPDOWN_RECT_UP, 3, border_radius=5)
    if dropped:
        for i in range(8):
            label = params.FONT.render(str(i + 2), False, (0, 0, 0))
            display.blit(label, params.DROPDOWN_NUM_POS_FUNC(i))
    else:
        label = params.FONT.render(str(params.NODE_NUMBER), False, (0, 0, 0))
        display.blit(label, params.DROPDOWN_NUM_POS_FUNC(0))
        display.blit(params.IMAGE_DROPDOWN_ARROW, params.DROPDOWN_ARROW_POS)

def dropdownClicked(pos, params: Parameters, dropped: bool) -> Union[bool, int]:
    if dropped:
        for i in range(8):
            rect = pygame.Rect(*params.DROPDOWN_NUM_POS_FUNC(i), 80, 44)
            if rect.collidepoint(pos): return i + 2
        return -1
    return params.DROPDOWN_RECT_UP.collidepoint(pos)

def game():
    def gameRestart():
        nonlocal params, display, grid, clock, timerDrawer, gameWon, smileyFirstClicked, droppedDown, running
        params = Parameters(nodeNumber)
        display = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT))
        pygame.display.set_caption('Lights Out')
        grid = LightsGrid(params.NODE_NUMBER)
        clock = pygame.time.Clock()
        timerDrawer = timerConstructor(display, params)
        gameWon = False
        smileyFirstClicked = False
        droppedDown = False
        running = True
    
    nodeNumber = 3
    # NOTE: doing this for the scope definition of these variables before actually initializing
    params = display = grid = clock = timerDrawer = gameWon = smileyFirstClicked = droppedDown = running = None
    
    pygame.init()
    gameRestart()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if res := dropdownClicked(event.pos, params, droppedDown):
                    droppedDown = not droppedDown
                    if isinstance(res, int) and res >= 2 and droppedDown is not True:
                        nodeNumber = res
                        gameRestart()
                else:
                    if not gameWon:
                        gameWon = grid.click(event.pos, params)
                    if params.SMILEY_RECT.collidepoint(event.pos):
                        if smileyFirstClicked:
                            gameRestart()
                        else: 
                            smileyFirstClicked = True

        display.fill((255, 255, 255))
        grid.drawGrid(display, params)

        pygame.draw.rect(display, (0, 0, 255), (0, 0, params.SCREEN_WIDTH, params.HEADER_HEIGHT))
        display.blit((params.IMAGE_WIN if gameWon else params.IMAGE_GAME), params.SMILEY_POS)

        timerDrawer(gameWon)
        drawDropdown(display, droppedDown, params)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    game()
