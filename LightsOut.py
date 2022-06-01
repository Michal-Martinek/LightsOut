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
        self.IMAGE_HINT = pygame.image.load('Assets\\HintIcon.png')
        self.IMAGE_HINT.set_colorkey((255, 255, 255))
        self.IMAGE_HINTED_LIT = pygame.image.load('Assets\\HintedLit.png')
        self.IMAGE_HINTED_LIT.set_colorkey((255, 255, 255))
        self.IMAGE_HINTED_DARK = pygame.image.load('Assets\\HintedDark.png')
        self.IMAGE_HINTED_DARK.set_colorkey((255, 255, 255))

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

        # game mechanics
        self.HINT_TIME_INTERVAL = 10

class LightsGrid:
    def generateNeighborRules(self):
        for y in range(self.size):
            for x in range(self.size):
                for neighborY in range(y-1, y+2):
                    for neighborX in range(x-1, x+2):
                        if 0 <= neighborX < self.size and 0 <= neighborY < self.size:
                            if (x == neighborX and y == neighborY) or random.random() >= 0.5:
                                self.neighborRules[y][x].append( (neighborY, neighborX) )
    def generateGrid(self):
        # TODO: sometimes it generates board which is already solved
        numMoves = random.randint(2, self.size**2-1)
        bulbs = []
        for y in range(self.size):
            bulbs.extend( [(y, x) for x in range(self.size)] )
        movesToSolve = random.sample(bulbs, numMoves)
        for move in movesToSolve:
            self.toggleAt(move)
    def __init__(self, size: int):
        self.size = size
        self.grid = [[True for x in range(size)] for y in range(size)]
        self.hinted = [[False for x in range(size)] for y in range(size)]
        self.neighborRules = [[[] for x in range(size)] for y in range(size)]
        self.clicked = [[False for x in range(size)] for y in range(size)]
        self.generateNeighborRules()
        self.generateGrid()
    def drawGrid(self, display, params: Parameters):
        images = [params.IMAGE_BULB_DARK, params.IMAGE_BULB_LIT, params.IMAGE_HINTED_DARK, params.IMAGE_HINTED_LIT]
        posY = params.HEADER_HEIGHT + params.NODE_SPACING
        for rows in zip(self.grid, self.hinted):
            posX = params.NODE_SPACING
            for lit, hinted in zip(*rows):
                image = images[lit + 2 * hinted]
                display.blit(image, (posX, posY))
                posX += params.BLOCK_SIZE
            posY += params.BLOCK_SIZE
    def toggleAt(self, pos):
        if self.hinted[pos[0]][pos[1]]: return
        self.clicked[pos[0]][pos[1]] = not self.clicked[pos[0]][pos[1]]
        for y, x in self.neighborRules[pos[0]][pos[1]]:
            self.grid[y][x] = not self.grid[y][x]
    def isWon(self):
        return all([all(row) for row in self.grid])
    def click(self, pos, params: Parameters):
        pos = [pos[1] - params.HEADER_HEIGHT, pos[0]]
        if pos[0] < 0: return False
        clicked = pos[0] // params.BLOCK_SIZE, pos[1] // params.BLOCK_SIZE
        remaining = pos[0] % params.BLOCK_SIZE, pos[1] % params.BLOCK_SIZE
        if (remaining[0] >= params.NODE_SPACING) and (remaining[1] >= params.NODE_SPACING):
            if (clicked[0] < self.size and clicked[1] < self.size):
                self.toggleAt(clicked)
    def dropHint(self):
        # test
        return self.dropHintNostrict()
        enmueratedRules = [(y, x, self.neighborRules[y][x]) for x in range(self.size) for y in range(self.size)]
        lamda = lambda rule: len(rule[2]) * (not self.hinted[rule[0]][rule[1]] and self.clicked[rule[0]][rule[1]])
        y, x, mostRules = max(enmueratedRules, key=lamda)
        if self.hinted[y][x] or not self.clicked[y][x]: return self.dropHintNostrict()
        self.toggleAt((y, x))
        self.hinted[y][x] = True
    def dropHintNostrict(self):
        notHintedBulbs = [(y, x) for y in range(self.size) for x in range(self.size) if not self.hinted[y][x]]
        y, x = random.choice(notHintedBulbs)
        if self.clicked[y][x]:
            self.toggleAt((y, x))
        self.hinted[y][x] = True



def timerConstructor(display, startTime, params: Parameters):
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
        nonlocal params, display, grid, clock, gameStartTime, timerDrawer, gameWon, smileyFirstClicked, droppedDown, running, hintAvailable
        params = Parameters(nodeNumber)
        display = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT))
        pygame.display.set_caption('Lights Out')
        grid = LightsGrid(params.NODE_NUMBER)
        clock = pygame.time.Clock()
        gameStartTime = time.time()
        timerDrawer = timerConstructor(display, gameStartTime, params)
        gameWon = False
        smileyFirstClicked = False
        droppedDown = False
        running = True
        hintAvailable = False
        restartHintTimer()

    nodeNumber = 3
    hintEventId = pygame.event.custom_type()
    restartHintTimer: function = lambda: pygame.time.set_timer(pygame.event.Event(hintEventId), params.HINT_TIME_INTERVAL * 1000, loops=1)
    # NOTE: doing this for the scope definition of these variables before actually initializing
    params: Parameters = None
    grid: LightsGrid = None
    display  = clock = gameStartTime = timerDrawer = gameWon = smileyFirstClicked = droppedDown = running = hintAvailable = None
    
    pygame.init()
    gameRestart()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if res := dropdownClicked(event.pos, params, droppedDown):
                    droppedDown = not droppedDown
                    if isinstance(res, int) and res >= 2 and droppedDown is not True:
                        nodeNumber = res
                        gameRestart()
                else:
                    if not gameWon:
                        grid.click(event.pos, params)
                        gameWon = grid.isWon()
                    if params.SMILEY_RECT.collidepoint(event.pos):
                        if smileyFirstClicked:
                            if hintAvailable:
                                grid.dropHint()
                                gameWon = grid.isWon()
                                smileyFirstClicked = False
                                hintAvailable = False
                                restartHintTimer()
                            else:
                                gameRestart()
                        else: 
                            smileyFirstClicked = True
            elif event.type == hintEventId:
                hintAvailable = True
        
        display.fill((255, 255, 255))
        grid.drawGrid(display, params)

        pygame.draw.rect(display, (0, 0, 255), (0, 0, params.SCREEN_WIDTH, params.HEADER_HEIGHT))
        smileyImg = params.IMAGE_WIN if gameWon else (params.IMAGE_HINT if hintAvailable else params.IMAGE_GAME)
        display.blit(smileyImg, params.SMILEY_POS)

        timerDrawer(gameWon)
        drawDropdown(display, droppedDown, params)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    game()
