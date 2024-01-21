import pygame


# main function
def main():

    # initialize window
    screen = pygame.display.set_mode((1250, 1250))
    clock = pygame.time.Clock()

    # customize window
    pygame.display.set_caption("Chess")
    programIcon = pygame.image.load('icon.png')
    pygame.display.set_icon(programIcon)

    # make board
    surface = createBoard()
    board = [[0]*8, [0]*8, [0]*8, [0]*8, [0]*8, [0]*8, [0]*8, [0]*8]

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(pygame.Color(48, 46, 43))
        screen.blit(surface, (25, 25))
        x, y = getPos()

        if x != None:
            pygame.draw.rect(screen, (255, 0, 0, 50),
                             ((x * 150)+25, (y * 150)+25, 150, 150), 2)
        pygame.display.flip()
        clock.tick(60)


# gets the position of the mouse in terms of the board tile coordinates
def getPos():
    mX, mY = pygame.mouse.get_pos()
    if mX > 1225 or mY > 1225 or mX < 25 or mY < 25:
        return None, None  # out of bounds
    else:
        x = int((mX-25) / 150)
        y = int((mY-25) / 150)
        return x, y


# creates board surface
def createBoard():

    board = pygame.Surface((1200, 1200))

    # board colours
    green = (119, 149, 86)
    white = (235, 236, 208)

    # draw boards
    for y in range(0, 8, 2):
        for x in range(0, 8, 2):
            pygame.draw.rect(board, green, (150*x, 150*y, 150, 150))
            pygame.draw.rect(board, white, ((x + 1)*150, 150*y, 150, 150))
            pygame.draw.rect(
                board, green, ((x + 1)*150, (y + 1)*150, 150, 150))
            pygame.draw.rect(board, white, (150*x, (y + 1)*150, 150, 150))

    return board


if __name__ == '__main__':
    main()
