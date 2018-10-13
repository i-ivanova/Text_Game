import pygame
import pygame_textinput
import pygame_button
import round_rect as rr
import os

DECISIONS = {"username": ""}
pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_w, screen_h = SCREEN.get_width(), SCREEN.get_height()
pygame.display.set_caption('The Escape Game')

def load_image(path):
	image = pygame.image.load(path)
	return image

class Kayla(pygame.sprite.Sprite):
	def __init__(self):
		super(Kayla, self).__init__()
		kayla_images_dance = ["kayla{}.png".format(str(x)) for x in range(1,7)]
		self.index = 0
		self.images = []
		for name in kayla_images_dance:
			stage = load_image(os.path.join("Kayla", name))
			self.images.append(stage)
		self.image = self.images[self.index]
		self.normal = False
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN.get_width() / 2, SCREEN.get_height() / 7 * 4)

	def update(self):
		self.index += 1
		if self.index >= len(self.images):
			self.index = 0
		if self.normal:
			self.index = 1
		self.image = self.images[self.index]

class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		#call Sprite initializer
		super(Background, self).__init__()
		self.image = load_image(image_file)
		self.image = pygame.transform.scale(self.image, (SCREEN.get_width(), SCREEN.get_height()))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class Crowd(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		super(Crowd, self).__init__()
		self.image = load_image(image_file)
		#self.image = pygame.transform.scale(self.image, (SCREEN.get_width() // 3, SCREEN.get_height() // 3))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class DecisionMakingBoxes(pygame.sprite.Sprite):
	def __init__(self, color, captions):
		super(DecisionMakingBoxes, self).__init__()
		font = pygame.font.SysFont('tlwgtypo', 50)

		rect1 = (screen_w / 10 * 1, screen_h / 19 * 15,  screen_w / 10 * 4, screen_h / 12 * 1)
		rect2 = (screen_w / 15 * 8, screen_h / 19 * 15,  screen_w / 10 * 4, screen_h / 12 * 1)
		rect3 = (screen_w / 10 * 1, screen_h / 17 * 15,  screen_w / 10 * 4, screen_h / 12 * 1)
		rect4 = (screen_w / 15 * 8, screen_h / 17 * 15,  screen_w / 10 * 4, screen_h / 12 * 1)

		self.decision1 = pygame_button.PygButton(rect=rect1, caption=captions[1], font=font, bgcolor=color)
		self.decision2 = pygame_button.PygButton(rect=rect2, caption=captions[2], font=font, bgcolor=color)
		self.decision3 = pygame_button.PygButton(rect=rect3, caption=captions[3], font=font, bgcolor=color)
		self.decision4 = pygame_button.PygButton(rect=rect4, caption=captions[4], font=font, bgcolor=color)

	def draw(self, screen):
		self.decision1.draw(screen)
		self.decision2.draw(screen)
		self.decision3.draw(screen)
		self.decision4.draw(screen)


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


# start game
def start_game(username_input):
	"""
	TODO: Make the plot for the DECISIONS
	"""
	DECISIONS["username"] = username_input.get_text()
	SCREEN.fill((18, 17, 44))
	pygame.display.update()

	kayla_dance = Kayla()
	all_sprites = pygame.sprite.Group()
	BackGround = Background(os.path.join("Crowd", "dance_floor.png"), [0,0])
	crowds = []
	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 3, screen_h / 3]))

	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 11*2, screen_h / 10*4]))
	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 11*6, screen_h / 10*4]))

	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 9, screen_h / 10*5]))
	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 9*6, screen_h / 10*5]))

	for crowd in crowds:
		all_sprites.add(crowd)
	all_sprites.add(kayla_dance)

	test = {1: "Test", 2: "Text", 3: "For", 4: "Fun"}
	decisions = DecisionMakingBoxes((129, 123, 134), test)


	while True:
		pygame.time.delay(150)
		events = pygame.event.get()
		for event in events:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				return

			if 'click' in decisions.decision1.handleEvent(event):
				return

			if 'click' in decisions.decision2.handleEvent(event):
				return

			if 'click' in decisions.decision3.handleEvent(event):
				return

			if 'click' in decisions.decision4.handleEvent(event):
				return

		SCREEN.fill([255, 255, 255])
		SCREEN.blit(BackGround.image, BackGround.rect)
		kayla_dance.update()
		all_sprites.draw(SCREEN)
		decisions.draw(SCREEN)
		pygame.display.update()


if __name__ == "__main__":
	front_page()
