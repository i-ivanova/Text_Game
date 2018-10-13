import pygame
import pygame_textinput
import pygame_button

DECISIONS = {"username": ""}
pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('The Escape Game')


def setup_front_page(pygame_screen):
	myfont = pygame.font.SysFont('purisa', 190, bold=True)
	title = myfont.render("SURVIVAL 2018", 1, (222, 247, 219))

	myfont = pygame.font.SysFont('tlwgtypo', 70)
	username = myfont.render("Nickname: ", 1, (238, 251, 218))

	title_x = (pygame_screen.get_width() - title.get_width())/2
	title_y = (pygame_screen.get_height() - title.get_height())/4

	pygame_screen.blit(title, (title_x, title_y))
	pygame_screen.blit(username, (title_x + 100, title_y + 400))

	return (title_x + 100 + username.get_width(), title_y + 400 + username.get_height())

def front_page():
	
	run = True
	clock = pygame.time.Clock()

	# initialise user input
	username_input = pygame_textinput.TextInput(text_color=(222, 247, 219),
												cursor_color=(238, 251, 218),
												font_family='tlwgtypo',
												font_size=50)

	# initialise buttons
	button_x, button_y = SCREEN.get_width(), SCREEN.get_height()
	font =  pygame.font.SysFont('tlwgtypo', 50)

	play_rect = (button_x / 10 * 7, button_y / 15 * 13,  button_x / 10 * 2, button_y / 15 * 1)
	exit_rect = (button_x / 10 * 1, button_y / 15 * 13,  button_x / 10 * 2, button_y / 15 * 1)
	play_button = pygame_button.PygButton(rect=play_rect, caption="Play", font=font, bgcolor=(113, 111, 143))
	exit_button = pygame_button.PygButton(rect=exit_rect, caption="Exit Game", font=font, bgcolor=(113, 111, 143))


	# run front_page
	while True:
		SCREEN.fill((18, 17, 44))
		username_x, username_y = setup_front_page(SCREEN)		
		events = pygame.event.get()
		for event in events:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				return

			# if user name is not empty and play_button is pressed start game
			if 'click' in play_button.handleEvent(event):
				if username_input.get_text() != "":
					start_game(username_input)
					return

			if 'click' in exit_button.handleEvent(event):
				return

		# constatly update
		username_input.update(events)
		SCREEN.blit(username_input.get_surface(), (username_x , username_y - 70))
		play_button.draw(SCREEN)
		exit_button.draw(SCREEN)
		pygame.display.update()

		clock.tick(30)

# start game
def start_game(username_input):
	"""
	TODO: Make the plot for the DECISIONS
	"""
	DECISIONS["username"] = username_input.get_text()
	SCREEN.fill((18, 17, 44))
	pygame.display.update()


if __name__ == "__main__":
	front_page()