# A simple maze game: OOP practice

import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("#55646a")
wn.title("Maze Game")
wn.setup(700,700)

# loads game faster
wn.tracer(0)

wn.register_shape("swizleft.gif")
wn.register_shape("swizright.gif")
wn.register_shape("treasuresmall.gif")
wn.register_shape("wall.gif")
wn.register_shape("monster.gif")

# Create Pen
class Pen(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape("wall.gif")
		self.color("white")
		self.penup()
		self.speed(0)

# Enemies
class Enemy(turtle.Turtle):
	def __init__(self, x, y):
		turtle.Turtle.__init__(self)
		self.shape("monster.gif")
		self.penup()
		self.speed(0)
		self.gold = 25
		self.goto(x,y)
		# 
		self.direction = random.choice(["up", "down", "left", "right"])

	def move(self):
		if self.direction == "up":
			dx = 0
			dy = 24

		elif self.direction == "down":
			dx = 0
			dy = -24

		elif self.direction == "left":
			dx = -24
			dy = 0

		elif self.direction == "right":
			dx = 24
			dy = 0


		else:
			dx = 0
			dy = 0
		# move randomly unless player is close
		if self.is_close(player):
			# if player is to the left of enemy
			if player.xcor() < self.xcor():
				self.direction = "left"
			elif player.xcor()  > self.xcor():
				self.direction = "right"
			elif player.ycor() > self.ycor():
				self.direction = "up"
			elif player.ycor() < self.ycor():
				self.direction = "down"


		movetox = self.xcor() + dx
		movetoy = self.ycor() + dy

		if (movetox, movetoy) not in walls:
			self.goto(movetox, movetoy)
		else:
			self.direction = random.choice(["up", "down", "left", "right"])
		turtle.ontimer(self.move, t = random.randint(100,300))

	def is_close(self, other):
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt((a**2) + (b**2))
		if distance < 75:
			return True
		else:
			return False

# Create player 
class Player(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape("swizright.gif")
		self.color("blue")
		self.penup()
		self.speed(0)
		self.gold = 0
	# check if space has a wall. If not, move. if there is a wall, do nothing
	def move_right(self):
		if (player.xcor() + 24, player.ycor()) not in walls:
			self.shape("swizright.gif")
			self.goto(self.xcor() + 24, self.ycor())

	def move_left(self):
		if (player.xcor() - 24, player.ycor()) not in walls:
			self.shape("swizleft.gif")			
			self.goto(self.xcor() - 24, self.ycor())

	def move_up(self):
		if (player.xcor(), player.ycor() + 24) not in walls:
			self.goto(self.xcor(), self.ycor() + 24)

	def move_down(self):
		if (player.xcor(), player.ycor() - 24) not in walls:
					self.goto(self.xcor(), self.ycor() - 24)

	def isCollision(self, other):
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt(a**2 + b**2)

		if distance < 5:
			return True
		else:
			return False

class Treasure (turtle.Turtle):
	def __init__(self, x, y):
		turtle.Turtle.__init__(self)
		self.shape("treasuresmall.gif")
		self.color("gold")
		self.penup()
		self.speed(0)
		self.gold = 100
		self.goto(x, y)

	def destroy(self):
		self.goto(2000,2000)
		self.hideturtle()

# Create levels list
levels = [""]

# Define first level
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXP  T          XXXT  XXX",
"XXXX   XXXXX  E XXX   XXX",
"XXXX    XXXXXXXXXXX   XXX",
"XXXXX                  XX",
"XXXXXXXXXXXXXX   XXX  XXX",
"XXX E          XXXXXX  XX",
"XT XX   XXXX    XX  XX  X",
"X  XXX  XXXXX  XXX  XXXXX",
"X  XXX   XXXX       X  XX",
"X       XX     XXXXXX  XX",
"X   XX   XXXX          XX",
"X    XXXXXXX   XXXXXXE XX",
"XXX  X  XX     X  XXXXXXX",
"XXX  XXXXX  XXX        XX",
"XXX   XXXX      XXXXX  XX",
"XXX            XXXX  E XX",
"XXXE XXXXXXXXXXXT    XXXX",
"XXX XX  XXX   XXXX  XXXX",
"XXXXX  XX XXX        XXXX",
"XXXT    XX     XXX    XXX",
"XXXXXXX      XX    XXXXXX",
"XX    XXXXXXXXX  XXXXXXXX",
"XXX    XXXXX      XXXXXXX",
"XXXXX         XXXXX  XXXX"
]

treasures = []
enemies = []

levels.append(level_1)

# top left corner of maze is -288, 288
def setup_maze(level):
	for y in range(len(level)):
		for x in range(len(level[y])):
			# get character at each x,y coordinate
			character = level[y][x]
			screen_x = -288 + (x * 24)
			screen_y = 288 - (y * 24)

			# Check if its an X (representing a wall)
			if character == "X":
				pen.goto(screen_x, screen_y)

				# stamp puts it there permanently
				pen.stamp()
				walls.append((screen_x, screen_y))
			if character == "P":
				player.goto(screen_x, screen_y)

			if character == 'T':
				treasures.append(Treasure(screen_x,screen_y))

			if character == 'E':
				enemies.append(Enemy(screen_x, screen_y))

# create pen
pen = Pen()
player = Player()

# Create walls
walls = []

# key binds
turtle.listen()
turtle.onkey(player.move_left,"Left")
turtle.onkey(player.move_right,"Right")
turtle.onkey(player.move_up,"Up")
turtle.onkey(player.move_down,"Down")

setup_maze(levels[1])
wn.tracer(0)

for e in enemies:
	turtle.ontimer(e.move, t = 250)
 
while True:
	for treasure in treasures:
		if player.isCollision(treasure):
			# add how much gold is acquired to player's score
			player.gold += treasure.gold

			# destroy treasure
			treasure.destroy()

			# remove treasure from list
			treasures.remove(treasure)  

	for e in enemies:
		if player.isCollision(e):
			print("player dies!")
	wn.update()
