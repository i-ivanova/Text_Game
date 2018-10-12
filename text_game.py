import pygame
import logging
pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

x, y, width, height, vel = 50, 50, 40, 60, 5

fonts = pygame.font.get_fonts()
i = 0

run = True
while run:
	pygame.time.delay(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
		myfont = pygame.font.SysFont('purisa', 50)

		# render text
		label = myfont.render("SOME TEXT", 1, (255, 255, 255))
		win.blit(label, (100, 100))

	if keys[pygame.K_SPACE]:
		win.fill((0,0,0))
		pygame.display.flip()

	pygame.display.update()

pygame.quit()


