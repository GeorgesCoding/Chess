import pygame

# initialize window
pygame.init()
screen = pygame.display.set_mode((1200,1200))
pygame.display.set_caption("Chess")

# change to custom icon
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

# create board object
board = pygame.Surface((1200, 1200))
board.fill((31, 31, 31))

# draw board
for y in range(0,8, 2):
    for x in range(0, 8, 2):
        pygame.draw.rect(board, (211, 255, 155), (150*x, 150*y, 150, 150))
        pygame.draw.rect(board, (235, 236, 208), ((x + 1)*150, 150*y, 150, 150))
        pygame.draw.rect(board, (211, 255, 155), ((x + 1)*150, (y + 1)*150, 150, 150))
        pygame.draw.rect(board, (235, 236, 208), (150*x, (y + 1)*150, 150, 150))

# add board to window
screen.blit(board, (0,0))

pygame.display.flip()

# main loop
running = True
while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False