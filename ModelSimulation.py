import pygame
import os
import sys
import random
import time
import math
import threading

pygame.init()
simulation = pygame.sprite.Group()

black = (0, 0, 0)
white = (255, 255, 255)

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

noOfSignals = 4
gap = 15
currentGreen = 0
currentYellow = 0
nextGreen = (currentGreen + 1) % noOfSignals

defaultRed = 150
defaultYellow = 5
defaultGreen = 20

vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

x = {'right':0, 'down':755, 'left':1400, 'up':602}    
y = {'right':370, 'down':0, 'left':466, 'up':800}

xLane = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}    
yLane = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}

defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
threshStopLane = {"right": [380, 380, 380], "down": [120, 120, 120], "left": [610, 610, 610], "up": [345, 345, 345]}
threshStop = {"right": 380, "down": 120, "left": 610, "up": 345}
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}

signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

vehiclesCount = {"right": 0, "down": 0, "left": 0, "up": 0}
vehicles = {"right": [], "down": [], "left": [], "up": []}

signals = []

detectionTime = 4

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = "30"
        self.totalGreenTime = 0

class Vehicles(pygame.sprite.Sprite):
    def __init__(self, vechicleClass, direction):
        pygame.sprite.Sprite.__init__(self)
        vehicles[direction].append(self)
        self.index = len(vehicles[direction]) - 1
        path = "images/" + direction + "/" + vechicleClass + ".png"
        self.originalImage = pygame.image.load(path)
        self.currentImage = pygame.image.load(path)
        self.x = x[direction]
        self.y = y[direction]
        self.direction = direction
        vehiclesCount[direction] += 1
        self.crossed = 0

        if direction == "right":
            if(len(vehicles[direction]) > 1 and vehicles[direction][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][self.index - 1].stop - vehicles[direction][self.index - 1].currentImage.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]
            tmp = self.currentImage.get_rect().width + gap
            x[direction] -= tmp
            stops[direction] -= tmp
        elif direction == "left":
            if(len(vehicles[direction]) > 1 and vehicles[direction][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][self.index - 1].stop + vehicles[direction][self.index - 1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            tmp = vehicles[direction][self.index - 1].currentImage.get_rect().width + gap
            x[direction] += tmp
            stops[direction] += tmp
        elif direction == "up":
            if(len(vehicles[direction]) > 1 and vehicles[direction][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][self.index - 1].stop + vehicles[direction][self.index - 1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            tmp = vehicles[direction][self.index - 1].currentImage.get_rect().width + gap
            y[direction] += tmp
            stops[direction] += tmp
        elif direction == "down":
            if(len(vehicles[direction]) > 1):
                self.stop = vehicles[direction][self.index - 1].stop - vehicles[direction][self.index - 1].currentImage.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]
            tmp = vehicles[direction][self.index - 1].currentImage.get_rect().width + gap
            y[direction] -= tmp
            stops[direction] -= tmp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.currentImage, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.currentImage.get_rect().width>stopLines[self.direction]): 
                self.crossed = 1
                if(self.x + self.currentImage.get_rect().width > 1300):
                    vehicles[self.direction].pop(self.index)
            else:
                if(self.x+self.currentImage.get_rect().width<=self.stop or (currentGreen==0 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.x+self.currentImage.get_rect().width<(vehicles[self.direction][self.index-1].x - gap)):
                    self.x += 2.5
        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.currentImage.get_rect().height>stopLines[self.direction]): 
                self.crossed = 1
                if(self.y + self.currentImage.get_rect().height > 750):
                    vehicles[self.direction].pop(self.index)
            else:
                if((self.y+self.currentImage.get_rect().height<=self.stop or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.currentImage.get_rect().height<(vehicles[self.direction][self.index-1].y - gap))):
                    self.y += 2.5
        if(self.direction=='left'):
            if(self.crossed==0 and self.x<stopLines[self.direction]): 
                self.crossed = 1
                if(self.x < 100):
                    vehicles[self.direction].pop(self.index)
            else:
                if((self.x>=self.stop or self.crossed == 1 or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.index-1].x + vehicles[self.direction][self.index-1].currentImage.get_rect().width + gap))):
                    self.x -= 2.5
        if(self.direction=='up'):
            if(self.crossed==0 and self.y<stopLines[self.direction]): 
                self.crossed = 1
                if(self.y < 100):
                    vehicles[self.direction].pop(self.index)
            else:
                if((self.y>=self.stop or self.crossed == 1 or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.index-1].y + vehicles[self.direction][self.index-1].currentImage.get_rect().height + gap))):
                    self.y -= 2.5
        
def countVc():
    vcl0 = 0
    vcl1 = 0
    vcl2 = 0
    vcl3 = 0
    for i in range(0, 4):
        if(currentGreen != i):
            if(i == 0):
                vcl0 = len(vehicles[directionNumbers[i]])
            elif(i == 1):
                vcl1 = len(vehicles[directionNumbers[i]])
            elif(i == 2):
                vcl2 = len(vehicles[directionNumbers[i]])
            else:
                vcl3 = len(vehicles[directionNumbers[i]])
    return vcl0, vcl1, vcl2, vcl3

def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen)
    signals.append(ts1)
    ts2 = TrafficSignal(defaultRed, defaultYellow, defaultGreen)
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen)
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen)
    signals.append(ts4)
    repeat()

def setTime():
    l0, l1, l2, l3 = countVc()
    mx = max(l0, l1, l2, l3)
    nextGreen = -1
    if(mx == l0):
        nextGreen = 0
    elif(mx == l1):
        nextGreen = 1
    elif(mx == l2):
        nextGreen = 2
    else:
        nextGreen = 3
    signals[nextGreen].green = 10

def repeat():
    global currentYellow, currentGreen, nextGreen
    while(signals[currentGreen].green > 0):
        updateValues()
        l0, l1, l2, l3 = countVc()
        mx = max(l0, l1, l2, l3)
        if(mx == l0):
            nextGreen = 0
        elif(mx == l1):
            nextGreen = 1
        elif(mx == l2):
            nextGreen = 2
        else:
            nextGreen = 3
        if(signals[nextGreen].red == detectionTime):
            thread = threading.Thread(name="detection",target=setTime, args=())
            thread.daemon = True
            thread.start()
        time.sleep(1)
    currentYellow = 1

    stops[directionNumbers[currentGreen]] = defaultStop[directionNumbers[currentGreen]]
    for vehicle in vehicles[directionNumbers[currentGreen]]:
        vehicle.stop = defaultStop[directionNumbers[currentGreen]]

    while(signals[currentGreen].yellow>0):
        updateValues()
        time.sleep(1)
    currentYellow = 0

    signals[currentGreen].green = defaultGreen
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen
    nextGreen = (currentGreen + 1) % noOfSignals
    signals[nextGreen].red = signals[currentGreen].yellow+signals[currentGreen].green
    repeat()
 
def updateValues():
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                signals[i].green-=1
                signals[i].totalGreenTime+=1
            else:
                signals[i].yellow-=1
        else:
            signals[i].red-=1

def generateVehicles():
    run = True
    while run:
        vhc = random.randint(0, 3)
        Vehicles(vehicleTypes[vhc], directionNumbers[vhc])
        time.sleep(1.25)

def main():

    thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())
    thread3.daemon = True
    thread3.start()

    thread2 = threading.Thread(name="initialization",target=initialize, args=())
    thread2.daemon = True
    thread2.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
        screen.blit(background, (0, 0))
        for i in range(0, 4):
            if(i==currentGreen):
                if(currentYellow==1):
                    if(signals[i].yellow==0):
                        signals[i].signalText = "STOP"
                    else:
                        signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    if(signals[i].green==0):
                        signals[i].signalText = "SLOW"
                    else:
                        signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if(signals[i].red<=10):
                    if(signals[i].red==0):
                        signals[i].signalText = "GO"
                    else:
                        signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])
            signalTexts = ["","","",""]

        for i in range(0,noOfSignals):  
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods[i]) 

        for vehicle in simulation:  
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            vehicle.move()

        pygame.display.update()


if __name__ == "__main__":
    main()