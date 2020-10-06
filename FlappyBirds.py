"""
The Classic Flappy Birds With an AI mode Bulit in
Using Libraries Like Pygame,neat-python,random,tkinter with pixel perfect Collision.
"""
import pygame
import os
import sys
import neat
import pickle
import random
import tkinter as tk
from tkinter import ttk,messagebox
#Intializing Pygame Module
pygame.init()
#Intializing Tkinter
root=tk.Tk()
root.title('Bird Selection Window')
root.geometry('601x338')
pygame.display.set_caption('Flappy Birds')
#Declaring Height and Width of Window
SCREEN=WIDTH,HEIGHT=288,512
CLOCK=pygame.time.Clock()
normal_speed=True
Generation_Count=0
font=pygame.font.Font('Fonts/FlappyBirdy.ttf',36)
#Creating A Bird Class
class birds:
	bird_velocity=4
	def __init__(self,bird_color):
		#Intializing Parameters Required
		self.bird_images=[pygame.image.load(f"sprites/{bird_color}bird-midflap.png").convert_alpha(),pygame.image.load(f"sprites/{bird_color}bird-upflap.png").convert_alpha(),pygame.image.load(f"sprites/{bird_color}bird-downflap.png").convert_alpha()]
		self.bird_position=[20,140]
		self.tilt=0
		self.current_bird_image=0
		self.frame_count=0
		self.flapping=False
		self.pressed=False
	def move(self):
		#Checking Whether The User Or AI has Pressed Jump
		if(self.pressed):
		#For The Next 15 Frames we're Changing The Tilting of Bird
			if(self.frame_count<15):
				self.frame_count+=1
			if(self.frame_count<10):
				self.bird_position[1]-=birds.bird_velocity
				self.tilt=25
			if(self.frame_count==15):
				self.frame_count=0
				self.pressed=False
			if(10<=self.frame_count<=15):
				self.tilt-=6
			self.flapping=True
		elif(not self.pressed):
			self.bird_position[1]+=birds.bird_velocity
			self.tilt=-45
			self.flapping=False
		#Changing Current bird Image
		if(self.current_bird_image==2 or not self.flapping):
			self.current_bird_image=0
		else:
			self.current_bird_image+=1
	@property
	def get_mask(self):
		return pygame.mask.from_surface(pygame.transform.rotate(self.bird_images[self.current_bird_image],self.tilt))
	
	#Drawing The Tilted Bird Image
	def draw(self):
	 	DISPLAY.blit(pygame.transform.rotate(self.bird_images[self.current_bird_image],self.tilt),self.bird_position)
class pipe:
	#We choose it to be 2Pixels per tick But you can change it if you want.
	pipe_velocity=2
	def __init__(self,pipe_color,intial_pipe_position):
		#Again Loading in all of the images
		self.bottom_pipe_image=pygame.image.load(f"sprites/pipe-{pipe_color}.png").convert_alpha()
		self.top_pipe_image=pygame.transform.flip(pygame.image.load(f"sprites/pipe-{pipe_color}.png").convert_alpha(),False,True)
		self.pipe_positions=intial_pipe_position #[[2,3],[2,4]]
	def move(self):
		#Changing the pipe x position
		self.pipe_positions[0][0]-=pipe.pipe_velocity
		self.pipe_positions[1][0]-=pipe.pipe_velocity
	@staticmethod
	def collision(pipes,bird):
		#Checking The collsion Between Bird and base or if bird is out of the background
		if(bird.bird_position[1]+bird.bird_velocity>base.base_current_position[1]-pygame.transform.rotate(bird.bird_images[bird.current_bird_image],bird.tilt).get_height()+6 or bird.bird_position[1]+bird.bird_velocity<0):
			return True
		#This if statement is because bird is likely not near a pipe if the pipes are less than 2. You can remove this statement if you want.
		if(len(pipes)>=2):
			for i in range(len(pipes)): 
				#Checking the Collsion between Each Pipe And bird
				if(bird.get_mask.overlap(pipes[i].get_mask_bottom,(pipes[i].pipe_positions[0][0]-bird.bird_position[0],pipes[i].pipe_positions[0][1]-bird.bird_position[1]))!=None or bird.get_mask.overlap(pipes[i].get_mask_top,(pipes[i].pipe_positions[1][0]-bird.bird_position[0],pipes[i].pipe_positions[1][1]-bird.bird_position[1]))!=None):
					return True
			return False
	@property
	def get_mask_bottom(self):
		#Getting the mask of the pipe
		return pygame.mask.from_surface(self.bottom_pipe_image)
	@property
	def get_mask_top(self):
		#Although they would be same we just did that to be absolutely sure
		return pygame.mask.from_surface(self.top_pipe_image)
	@staticmethod
	def get_new_pipe_position(position,intial=False):
		#Choosing the random number for the pipes
		temp=random.randint(150,340)
		if(intial):
			pipe_positions=[[200,temp]]
			pipe_positions.append([200,temp-440])
		else:
			#Horizontal Distance Between The Pipes
			pipe_gap=160
			#Getting a random Bottom Pipe
			pipe_positions=[[position[0]+pipe_gap,temp]]
			#Creating The Top Pipe With 120 Pixels Gap Between Both Pipes
			pipe_positions.append([position[0]+pipe_gap,temp-440])
		return pipe_positions
#Background Class and base class Should be self explantory
class background_class:
	def __init__(self,background_time):
		self.background=pygame.image.load(f"sprites/background-{background_time}.png")
		self.game_over=pygame.image.load(f"sprites/gameover.png")
	@property
	def get_mask(self):
		return pygame.mask.from_surface(self.background)
class base_class:
	def __init__(self):
		self.base_image=pygame.image.load('sprites/base.png')
		self.base_current_position=[0,400]
	def move(self):
		if(self.base_current_position[0]<=-48):
			self.base_current_position[0]=0
		else:
			self.base_current_position[0]-=2
	@property
	def get_mask(self):
		return pygame.mask.from_surface(self.base_image)
class score_counter():
	def __init__(self):
		self.score_images=[pygame.image.load(f"Fonts/{i}.png").convert_alpha() for i in range(10)]
		self.score=0
	def display_score(self):
		score_position=288-self.score_images[0].get_width()
		#Looping through each digit in The Score and displaying it in top right corner
		for temp in str(self.score)[::-1]:
			DISPLAY.blit(self.score_images[int(temp)],(score_position,0))
			score_position-=self.score_images[0].get_width()
	def display_Gen(self,Gen):
		Gen_position=0
		#Looping through each digit in Generation and displaying it in top left corner
		for temp in str(Gen):
			DISPLAY.blit(self.score_images[int(temp)],(Gen_position,0))
			Gen_position+=self.score_images[0].get_width()
	@staticmethod
	def check_score(bird,pipes):
		#Checking Whether the bird crossed the 0th or 1st pipe
		if(len(pipes)>=1):	
			if(bird.bird_position[0]==pipes[0].pipe_positions[0][0] or bird.bird_position[0]==pipes[1].pipe_positions[0][0]):
				return True
		return False
def draw(birds,background,pipes,base,score,show_generation=False,gameover=False):
	if(gameover):
		label=font.render('Press Space To Continue',True,(255,255,255))
		DISPLAY.blit(label,(0,80))
		DISPLAY.blit(background.game_over,(0,0))
		return
	DISPLAY.blit(background.background,(0,0))
	for pipe in pipes:
		DISPLAY.blit(pipe.bottom_pipe_image,pipe.pipe_positions[0])
		DISPLAY.blit(pipe.top_pipe_image,pipe.pipe_positions[1])
	for bird in birds:
		bird.draw()
	DISPLAY.blit(base.base_image,base.base_current_position)
	if(show_generation):
		score.display_Gen(Generation_Count)
	score.display_score()
def move(birds,pipes,base):
	for bird in birds:
		bird.move()
	base.move()
	for pipe in pipes:
		pipe.move()
class GUI:
	def __init__(self):
		#Simple Stuff just creating Buttons and labels etc
		self.flappy_image=tk.PhotoImage(file='sprites/Untitled.png')
		self.a=tk.Label(root,image=self.flappy_image)
		self.a.place(relwidth=1,relheight=1)
		self.labels=[tk.Label(text='Which Color of Bird You Want:',bg='skyblue1'),tk.Label(text='Training Mode:',bg='skyblue1'),tk.Label(text='Which Color of Pipes You Want:',bg='skyblue1')]
		self.choices=[ttk.Combobox(root,width=30,textvariable=tk.StringVar()),ttk.Combobox(root,width=30,textvariable=tk.StringVar()),ttk.Combobox(root,width=30,textvariable=tk.StringVar())]
		self.choices[0]['values']=('Blue','Red','Yellow')
		self.choices[1]['values']=('True','False')
		self.choices[2]['values']=('Red','Green')
		for i in range(3):
			self.labels[i].place(x=10,y=30+i*60)
			self.choices[i].current(0)
			self.choices[i].place(x=250,y=30+i*60)
		self.start_button=tk.Button(text='Start',command=self.start,height=3,width=8,bg='pale green')
		self.start_button.place(x=520,y=280)
	def start(self):
		#Defined These in Global As they are gonna be used later
		global pipe_color,bird_color,background_time,DISPLAY
		bird_color,background_time,pipe_color=self.choices[0].get(),'Day',self.choices[2].get()
		DISPLAY=pygame.display.set_mode(SCREEN)
		if(self.choices[1].get()=='True'):
			#Loading The Config File
			config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,'config.txt')
			p=neat.Population(config)
			#Adding Two Reporters You can remove Them If you want to
			p.add_reporter(neat.StdOutReporter(True))
			stats=neat.StatisticsReporter()
			p.add_reporter(stats)
			p.add_reporter(neat.Checkpointer(25))
			best=p.run(neural_network,1000)
			#Saving The best Bird in Winner.pickle File in directory
			with open('Winner.pickle','wb+') as f:
				pickle.dump(best,f)
		else:
			gameloop()
		root.quit()
def gameloop():
	#Intialzing Classes and Some Useful Variables
	global base,background_time
	bird=[birds(bird_color)]
	background=background_class(background_time)
	base=base_class()
	pipes=[pipe(pipe_color,pipe.get_new_pipe_position(None,intial=True))]
	score=score_counter()
	day_night_counter=0
	gameover=False
	while True:
		if(gameover==True):
			for event in pygame.event.get():
				if(event.type==pygame.QUIT):
					sys.exit()
				#Checking If User Wants To play Again or not
				elif(event.type==pygame.KEYDOWN):
					if(event.key==pygame.K_SPACE):
						gameover=False
						#Intialzing Them All of The parameter To default Values
						day_night_counter=0
						background=background_class('Day')
						bird=[birds(bird_color)]
						pipes=[pipe(pipe_color,pipe.get_new_pipe_position(None,intial=True))]
						score=score_counter()
			draw(bird,background,pipes,base,score,gameover=True)
			pygame.display.update()
		else:
			for event in pygame.event.get():
				if(event.type==pygame.QUIT):
					sys.exit()
				elif(event.type==pygame.KEYDOWN):
					if(event.key==pygame.K_SPACE):
						bird[0].pressed=True
						#Changing The bird Velocity the Rest Of the Gameloop Should be Pretty Self Explonatory
						bird[0].bird_position[1]-=8
						bird[0].frame_count=0
			draw(bird,background,pipes,base,score)
			move(bird,pipes,base)
			if(len(pipes)<3):
				pipes.append(pipe(pipe_color,pipe.get_new_pipe_position(pipes[len(pipes)-1].pipe_positions[0])))
			if(pipes[0].pipe_positions[0][0]<-52):
				pipes.pop(0)
			pygame.display.update()
			if(pipe.collision(pipes,bird[0])):
				gameover=True
			if(score.check_score(bird[0],pipes)):
				score.score+=1
			if(day_night_counter>9):
				day_night_counter=0
				if(background_time=='Day'):
					background=background_class('Night')
					background_time='Night'
				else:
					backround=background_class('Day')
					background_time='Day'
			day_night_counter+=0.01
		CLOCK.tick(30)
def neural_network(genomes,config):
	global base,bird,normal_speed,background_time,Generation_Count
	Generation_Count+=1
	net,bird_genomes,bird,score,day_night_counter=[],[],[],score_counter(),0
	for genome_id,genome in genomes:
		#Creating The List of Birds And their Respective Genomes
		genome.fitness=0
		bird_genomes.append(genome)
		net.append(neat.nn.FeedForwardNetwork.create(genome,config))
		bird.append(birds(bird_color))
	background=background_class(background_time)
	base=base_class()
	pipes=[pipe(pipe_color,pipe.get_new_pipe_position(None,intial=True))]
	while True:
		if(len(bird)==0):
			break
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				sys.exit()
			elif(event.type==pygame.KEYDOWN):
				if(event.key==pygame.K_SPACE):
					#Increases The Tick Count So that you Don't have to watch it getting Trained For a long time
					if normal_speed:
						normal_speed=False
					else:
						normal_speed=True
		draw(bird,background,pipes,base,score,show_generation=True)
		move(bird,pipes,base)
		#Checking Which Pipe is Next For Birds
		if(bird[0].bird_position[0]>pipes[0].pipe_positions[0][0]+pipes[0].top_pipe_image.get_width()-15):
			current_pipe=1
		else:
			current_pipe=0
		for i in range(len(bird)):
			#Calculating The Jump Value For which Birds Gonna Jump or not
			jump=net[i].activate((bird[i].bird_position[1],abs(bird[i].bird_position[0]-pipes[current_pipe].pipe_positions[0][1])))
			#We Choose 0.5 Because That worked best for us. You can Use Something Else Based On result you Want to see
			if(jump[0]>0.5):
				bird[i].pressed=True
		if(day_night_counter>9):
			day_night_counter=0
			if(background_time=='Day'):
				background=background_class('Night')
				background_time='Night'
			else:
				backround=background_class('Day')
				background_time='Day'
		day_night_counter+=0.01
		if(len(pipes)<3):
			pipes.append(pipe(pipe_color,pipe.get_new_pipe_position(pipes[len(pipes)-1].pipe_positions[0])))
		if(pipes[0].pipe_positions[0][0]<-52):
			pipes.pop(0)
		pygame.display.update()
		#Intializing The list Where we gonna Store indexes of Birds we want to be deleted
		to_be_deleted=[]
		for i in range(len(bird)):	
			#Checking Whether The Bird Collided With A Pipe or base if yes Then we're decreasing it's fitness
			if(pipe.collision(pipes,bird[i])):
				to_be_deleted.append(i)
				bird_genomes[i].fitness-=5
		#Deleting the Birds Which Collided With Pipes
		for i in to_be_deleted[::-1]:
			bird.pop(i)
			bird_genomes.pop(i)
			net.pop(i)
		score_registered=False
		for i in range(len(bird_genomes)):
			#we're increasing the fitness of bird which survived for each Frame by 0.1points
			bird_genomes[i].fitness+=0.1
			temp=score.check_score(bird[i],pipes)
			if(bird_genomes[i].fitness>5000):
				return
			if(temp):
				#if A bird crossed the Pipe Then We're increasing it's Fitness by 5points
				bird_genomes[i].fitness+=5
				if(score_registered==False):	
					#Just Making Sure We don't Count Score Multiple Times
					score_registered=True
		if(score_registered):
			score.score+=1
		if(normal_speed):
			#For Slow Train
			CLOCK.tick(30)
temp=GUI()
root.mainloop()
