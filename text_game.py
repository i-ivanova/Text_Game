import pygame
import pygame_textinput
import pygame_button
import os

### Initial SetUp
club = {1: "Go to the Bar", 2: "Go to the Dancefloor", 3: "Go to a Hackathon", 4: "..."}
go_home = {1: "Bus", 2: "Taxi", 3: "Walk", 4: "Hitch-hike"}
bar_choices = {1:"Drink the shot", 2:"Leave the Bar", 3:"Drink it and take another", 4: "Waste his time talking"} 
dancefloor_coices = {1: "Call Kayla", 2: "Make Insta story", 3: "Take a break", 4: "All three"}

has_id = None
username = ""
age = 0

pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_w, screen_h = SCREEN.get_width(), SCREEN.get_height()
pygame.display.set_caption('The Escape Game')

call_flag = False
battery_life = 5
sobriety = 5

### Game

def load_image(path):
	image = pygame.image.load(path)
	return image

class Kayla(pygame.sprite.Sprite):
	def __init__(self, normal):
		super(Kayla, self).__init__()
		self.kayla_normal = load_image(os.path.join("Kayla", "normal.png"))

		self.kayla_images_dance = []
		self.images = ["kayla{}.png".format(str(x)) for x in range(1,7)]
		self.index = 0
		for name in self.images:
			stage = load_image(os.path.join("Kayla", name))
			self.kayla_images_dance.append(stage)

		self.image = self.kayla_images_dance[self.index]
		self.normal = normal
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN.get_width() // 2, SCREEN.get_height() / 7 * 4)


	def update(self):
		if self.normal:
			self.image = pygame.transform.scale(self.kayla_normal, (SCREEN.get_width() // 3, SCREEN.get_height()))
			return
		self._update_dance()
		
	def _update_dance(self):
		self.index += 1
		if self.index >= len(self.kayla_images_dance):
			self.index = 0
		self.image = self.kayla_images_dance[self.index]


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

def setup_crowd():
	BackGround = Background(os.path.join("Crowd", "dance_floor.png"), [0,0])
	crowds = []
	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 3, screen_h / 3]))

	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 11*2, screen_h / 10*4]))
	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 11*6, screen_h / 10*4]))

	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 9, screen_h / 10*5]))
	crowds.append(Crowd(os.path.join("Crowd", "crowd_dance.png"), [screen_w / 9*6, screen_h / 10*5]))
	return crowds


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
					username = username_input.get_text()
					intro()
					return
					

			if 'click' in exit_button.handleEvent(event):
				return

			# constatly update

		username_input.update(events)
		SCREEN.blit(username_input.get_surface(), (username_x , username_y - 70))
		play_button.draw(SCREEN)
		exit_button.draw(SCREEN)
		pygame.display.update()

def intro():
	SCREEN.fill((18, 17, 44))
	myfont = pygame.font.SysFont('tlwgtypo', 60, bold=True)
	line1 = myfont.render("Your friend Kayla has just broken",  1, (222, 247, 219))
	line2 = myfont.render("off a long term relationship.", 1, (222, 247, 219))
	line3 = myfont.render("To cheer herself up, she’s decided to go",  1, (222, 247, 219))
	line4 = myfont.render("out clubbing and has asked you", 1, (222, 247, 219))
	line5 = myfont.render("to come along and make sure",  1, (222, 247, 219))
	line6 = myfont.render("she doesn’t do anything stupid...", 1, (222, 247, 219))

	title_y = (screen_h - line1.get_height())/4

	button_x, button_y = SCREEN.get_width(), SCREEN.get_height()
	font =  pygame.font.SysFont('tlwgtypo', 50)

	next_rec = (button_x / 10 * 7, button_y / 15 * 13,  button_x / 10 * 2, button_y / 15 * 1)
	next_button = pygame_button.PygButton(rect=next_rec, caption="Next", font=font, bgcolor=(113, 111, 143))
	next_button.draw(SCREEN)
	pygame.display.update()

	while True:
		events = pygame.event.get()
		for event in events:
			# if user name is not empty and play_button is pressed start game
			if 'click' in next_button.handleEvent(event):
				main_location()
				return
	
		SCREEN.blit(line1, ((screen_w - line1.get_width())/2, title_y))
		SCREEN.blit(line2, ((screen_w - line2.get_width())/2, title_y + 80))
		SCREEN.blit(line3, ((screen_w - line3.get_width())/2, title_y + 160))
		SCREEN.blit(line4, ((screen_w - line4.get_width())/2, title_y + 240))
		SCREEN.blit(line5, ((screen_w - line5.get_width())/2, title_y + 320))
		SCREEN.blit(line6, ((screen_w - line6.get_width())/2, title_y + 400))
		next_button.draw(SCREEN)
		pygame.display.update()

def dead_walk():
	SCREEN.fill((18, 17, 44))

	myfont = pygame.font.SysFont('tlwgtypo', 90, bold=True)

	line1 = myfont.render("GAME OVER", 1, (222, 247, 219))

	myfont = pygame.font.SysFont('tlwgtypo', 60, bold=True)
	line2 = myfont.render("You were kiddnapped on the way home.",  1, (222, 247, 219))
	line3 = myfont.render("Next time cosider a taxi/bus.",  1, (222, 247, 219))


	title_y = (screen_h - line1.get_height())/3

	button_x, button_y = SCREEN.get_width(), SCREEN.get_height()
	font =  pygame.font.SysFont('tlwgtypo', 50)

	next_rec = (button_x / 10 * 7, button_y / 15 * 13,  button_x / 10 * 2, button_y / 15 * 1)
	exit_rect = (button_x / 10 * 1, button_y / 15 * 13,  button_x / 10 * 2, button_y / 15 * 1)
	restart = pygame_button.PygButton(rect=next_rec, caption="Restart", font=font, bgcolor=(113, 111, 143))
	exit_button = pygame_button.PygButton(rect=exit_rect, caption="Exit Game", font=font, bgcolor=(113, 111, 143))

	exit_button.draw(SCREEN)
	restart.draw(SCREEN)
	pygame.display.update()

	while True:
		events = pygame.event.get()
		for event in events:
			# if user name is not empty and play_button is pressed start game
			if 'click' in next_button.handleEvent(event):
				front_page()
				return

			if 'click' in exit_button.handleEvent(event):
				return
	
		SCREEN.blit(line1, ((screen_w - line1.get_width())/2, title_y))
		SCREEN.blit(line2, ((screen_w - line2.get_width())/2, title_y + 150))
		SCREEN.blit(line3, ((screen_w - line3.get_width())/2, title_y + 230))
		exit_button.draw(SCREEN)
		restart.draw(SCREEN)
		pygame.display.update()


def main_location():
	global battery_life, sobriety, club

	SCREEN.fill((18, 17, 44))
	pygame.display.update()

	BackGround = Background(os.path.join("Crowd", "dance_floor.png"), [0, 0])

	kayla_normal = Kayla(True)
	all_sprites = pygame.sprite.Group()
	crowds = setup_crowd()

	for crowd in crowds:
		all_sprites.add(crowd)
	all_sprites.add(kayla_normal)

	decisions = DecisionMakingBoxes((129, 123, 134), club)

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
				return dancefloor()

			if 'click' in decisions.decision3.handleEvent(event):
				sobriety -= 1
				continue

			if 'click' in decisions.decision4.handleEvent(event) and club[4] == "...":
				continue

			if 'click' in decisions.decision4.handleEvent(event) and club[4] == "Leave":
				return bus_stop()
				


		SCREEN.fill([255, 255, 255])
		SCREEN.blit(BackGround.image, BackGround.rect)
		kayla_normal.update()
		all_sprites.draw(SCREEN)
		decisions.draw(SCREEN)
		pygame.display.update()

# start game
def dancefloor():
	global sobriety, battery_life
	global club
	SCREEN.fill((18, 17, 44))
	pygame.display.update()

	BackGround = Background(os.path.join("Crowd", "dance_floor.png"), [0, 0])

	kayla_dance = Kayla(False)
	all_sprites = pygame.sprite.Group()
	crowds = setup_crowd()

	for crowd in crowds:
		all_sprites.add(crowd)
	all_sprites.add(kayla_dance)

	decisions = DecisionMakingBoxes((129, 123, 134), dancefloor_coices)


	while True:
		pygame.time.delay(150)
		events = pygame.event.get()
		for event in events:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				return

			if 'click' in decisions.decision1.handleEvent(event):
				battery_life -= 1
				club[4] = "Leave"
				return main_location()
				

			if 'click' in decisions.decision2.handleEvent(event):
				battery_life -= 1
				return main_location()
				

			if 'click' in decisions.decision3.handleEvent(event):
				return main_location()
				

			if 'click' in decisions.decision4.handleEvent(event):
				battery_life -= 2
				club[4] = "Leave"
				return main_location()
				

		SCREEN.fill([255, 255, 255])
		SCREEN.blit(BackGround.image, BackGround.rect)
		kayla_dance.update()
		all_sprites.draw(SCREEN)
		decisions.draw(SCREEN)
		pygame.display.update()

def bar():
	global sobriety, battery_life
	global bar_choices
	pass

def bus_stop():
	global sobriety, battery_life, go_home
	SCREEN.fill((18, 17, 44))
	pygame.display.update()

	print ("in busstop")
	BackGround = Background(os.path.join("Go_Home", "busstop.png"), [0, 0])

	kayla_normal = Kayla(True)
	all_sprites = pygame.sprite.Group()
	all_sprites.add(kayla_normal)

	decisions = DecisionMakingBoxes((129, 123, 134), go_home)


	while True:
		pygame.time.delay(150)
		events = pygame.event.get()
		for event in events:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				return

			if 'click' in decisions.decision1.handleEvent(event):
				if call_flag:
					print ("It's too late, there are no busses at this time, you shouldn't have partied.")
				else:
					pass

			if 'click' in decisions.decision2.handleEvent(event):
				if battery_life < 0:
					print ("You dont have battery to cal a Taxi")
				else:
					pass

			if 'click' in decisions.decision3.handleEvent(event):
				return dead_walk()

			if 'click' in decisions.decision4.handleEvent(event):
				return dead_walk()
				
		SCREEN.fill([255, 255, 255])
		SCREEN.blit(BackGround.image, BackGround.rect)
		kayla_dance.update()
		all_sprites.draw(SCREEN)
		decisions.draw(SCREEN)
		pygame.display.update()




if __name__ == "__main__":
	front_page()
