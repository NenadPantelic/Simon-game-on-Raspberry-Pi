from time import *
import RPi.GPIO as GPIO
import random,os
class Simon():

	def __init__(self):

		self.name = raw_input("Enter your name:")
		print ("Hi " + self.name + ".The game will start now!")
		print("Good luck!")
		self.points = 0
		self.level = 1
		self.colors = {"red":18,"yellow":23,"green":24}
		GPIO.setmode(GPIO.BCM)
		self.game = True
		
	def ioChoice(self,choice):
		if (choice == 0):
			GPIO.setup(18,GPIO.OUT)
			GPIO.setup(23,GPIO.OUT)
			GPIO.setup(24,GPIO.OUT)
		else:
			GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
			GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
			GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		
	def lightOn(self,color):
		self.ioChoice(0)
		GPIO.output(self.colors[color],GPIO.HIGH)
		sleep(.03)

	def lightsOff(self):
		self.ioChoice(0)
		for color in self.colors:
			GPIO.output(self.colors[color],GPIO.LOW)
		sleep(.03)
	def looser(self):
		print("You reached " + str(self.level) + " level and scored " + str(self.points) + " points!")
		for i in range(3):
			for color in ("red","yellow","green"):
				self.lightOn(color)
				sleep(.06)
			self.lightsOff()
			sleep(.06)
		print ("You lost! Game over")
	def winner(self):
		q = None
		while (not q):
			q = raw_input()
			self.lightOn("red")
			self.lightOn("yellow")
			self.lightOn("green")
			sleep(.06)
			print("Congratulations! You wooon!")
			print("---Press any key for the end---")
	def choice(self):

		self.ioChoice(1)
		prevColor = [False,False,False]
		currentColor = [0,0,0]
		colors = ["red","yellow","green"]
		gpios = [18,23,24]
		
		while (not currentColor[0] and not currentColor[1] and not currentColor[2]):
			
			currentColor[0] = GPIO.input(18)
			currentColor[1] = GPIO.input(23)
			currentColor[2] = GPIO.input(24)
		if(currentColor[0]):
			prevColor[0] = GPIO.input(18)
			while(prevColor[0] == currentColor[0]):
				prevColor[0] = GPIO.input(18)
		if(currentColor[1]):
			prevColor[1] = GPIO.input(23)
			while(prevColor[1] == currentColor[1]):
				prevColor[1] = GPIO.input(23)
		if(currentColor[2]):	
			prevColor[2] = GPIO.input(24)
			while(prevColor[2] == currentColor[2]):
				prevColor[2] = GPIO.input(24)

		for i in range(3):
			prevColor[i] = GPIO.input(gpios[i])
			if (currentColor[i]):
				
				print ("Your choice: " + colors[i])
				sleep(.03)
				return colors[i]
	
	def randCombination(self):
		combination = []
		for i in range(self.level):
			combination.append(random.choice(self.colors.keys()))
			self.lightOn(combination[i])
			sleep(.3)
			self.lightsOff()
			sleep(0.3)
		print(combination)
		return combination
	def playGame(self):
		if (self.level >= 100):
			self.game = False
			winner()
			return
		
		while (self.game):
			print("\n----------------")
			print("Level: " + str(self.level))
			print("-----------------")
			combination = self.randCombination()
			num = 0
			while (num < self.level):
				user_choice = self.choice()
				if (combination[num] != user_choice):
					print("Wrong!\n")
					self.looser()
					self.game = False
					return
				else:
					print("Correct!")
					print("Point for you!\n")
					self.points += 1
				num += 1
			self.level += 1
			sleep(1)


simon = Simon()
simon.playGame()
GPIO.cleanup()
