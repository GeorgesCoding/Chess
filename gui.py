import pygame

def main():

   # initialize window
   screen = pygame.display.set_mode((1200,1200))
   clock = pygame.time.Clock()

   # customize window
   pygame.display.set_caption("Chess")
   programIcon = pygame.image.load('icon.png')
   pygame.display.set_icon(programIcon)

   # make board
   board = createBoard()

   # main loop
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
      
      screen.blit(board,(0,0))
      pygame.display.flip()
      clock.tick(60)
   
def createBoard():

   # create board surface
   board = pygame.Surface((1200, 1200))

   # board colours
   green = (119, 149, 86)
   white = (235, 236, 208)

   # draw board
   for y in range(0,8, 2):
      for x in range(0, 8, 2):
        pygame.draw.rect(board, green, (150*x, 150*y, 150, 150))
        pygame.draw.rect(board, white, ((x + 1)*150, 150*y, 150, 150))
        pygame.draw.rect(board, green, ((x + 1)*150, (y + 1)*150, 150, 150))
        pygame.draw.rect(board, white, (150*x, (y + 1)*150, 150, 150))

   return board

if __name__ == '__main__':
   main()