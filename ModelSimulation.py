import pygame
import os
import sys
import random
import time
import math
import threading

pygame.init()
simulation = pygame.sprite.Group()

screenWidth = 1400
screenHeight = 800
screenSize = (screenWidth, screenHeight)

background = pygame.image.load('images/mod_int.png')
surface = pygame.image.load('Gray.png')

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("SIMULATION")

redSignal = pygame.image.load('images/signals/red.png')
yellowSignal = pygame.image.load('images/signals/yellow.png')
greenSignal = pygame.image.load('images/signals/green.png')
font = pygame.font.Font(None, 30)

gap = 15

vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

x = {'right':0, 'down':755, 'left':1400, 'up':602}    
y = {'right':370, 'down':0, 'left':466, 'up':800}

defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
threshStop = {"right": [380, 380, 380], "down": [120, 120, 120], "left": [610, 610, 610], "up": [345, 345, 345]}
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}

signalCoods = [(530,230),(810,230),(810,570),(530,570)]

vehiclesCount = {"right": 0, "down": 0, "left": 0, "up": 0}
vehicles = {"right": [], "down": [], "left": [], "up": []}


class Vehicles(pygame.sprite.Sprite):
    def __init__(self, vechicleClass, direction):
        pygame.sprite.Sprite.__init__(self)
        path = "images/" + direction + "/" + vechicleClass + ".png"
        self.originalImage = pygame.image.load(path)
        self.currentImage = pygame.image.load(path)
        vehicles[direction].append(self)
        self.index = len(vehicles[direction]) - 1
        self.x = x[direction]
        self.y = y[direction]
        self.direction = direction
        vehiclesCount[direction] += 1
        self.crossed = 0

        if direction == "right":
            if(len(vehicles[direction]) > 1):
                self.stop = vehicles[direction][self.index - 1].stop - vehicles[direction][self.index - 1].currentImage.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]
            tmp = self.currentImage.get_rect().width + gap
            x[direction] -= tmp
            stops[direction] -= tmp
        elif direction == "left":
            if(len(vehicles[direction]) > 1):
                self.stop = vehicles[direction][self.index - 1].stop + vehicles[direction][self.index - 1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            tmp = self.currentImage.get_rect().width + gap
            x[direction] += tmp
            stops[direction] += tmp
        elif direction == "up":
            if(len(vehicles[direction]) > 1):
                self.stop = vehicles[direction][self.index - 1].stop + vehicles[direction][self.index - 1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            tmp = self.currentImage.get_rect().width + gap
            y[direction] += tmp
            stops[direction] += tmp
        elif direction == "down":
            if(len(vehicles[direction]) > 1):
                self.stop = vehicles[direction][self.index - 1].stop - vehicles[direction][self.index - 1].currentImage.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]
            tmp = self.currentImage.get_rect().width + gap
            y[direction] -= tmp
            stops[direction] -= tmp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.currentImage, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.currentImage.get_rect().width>stopLines[self.direction]): 
                self.crossed = 1
            else:
                if(self.x+self.currentImage.get_rect().width<=self.stop or self.crossed == 1):
                    self.x += 2.5
        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.currentImage.get_rect().height>stopLines[self.direction]): 
                self.crossed = 1
            else:
                if(self.x+self.currentImage.get_rect().width<=self.stop or self.crossed == 1):
                    self.y += 2.5
        if(self.direction=='left'):
            if(self.crossed==0 and self.x+self.currentImage.get_rect().width>stopLines[self.direction]): 
                self.crossed = 1
            else:
                if(self.x+self.currentImage.get_rect().width<=self.stop or self.crossed == 1):
                    self.x -= 2.5
        if(self.direction=='up'):
            if(self.crossed==0 and self.x+self.currentImage.get_rect().width>stopLines[self.direction]): 
                self.crossed = 1
            else:
                if(self.x+self.currentImage.get_rect().width<=self.stop or self.crossed == 1):
                    self.y -= 2.5
        



def generateVehicles():
    while True:
        vhc = random.randint(0, 4)
        Vehicles(vehicleTypes[vhc], directionNumbers[vhc])
        time.sleep(1)

def main():

    thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())    # Generating vehicles
    thread3.daemon = True
    thread3.start()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
        screen.blit(background, (0, 0))
        for i in range(0, 4):
            screen.blit(redSignal, signalCoods[i])

        for vehicle in simulation:  
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            # vehicle.render(screen)
            vehicle.move()

        pygame.display.update()


if __name__ == "__main__":
    main()