import pygame
import math
import time
import json

class Body:
    def __init__(self, m=1, x=0, y=0, vx=0, vy=0, r=1, color='red', R = -1):
        self.m = m # body mass [kg]
        self.x = x # initial x coordinate [m]
        self.y = y # initial y coordinate [m]
        self.vx = vx # initial x velocity [m/s]
        self.vy = vy # initial y velocity [m/s]
        self.R = R # displayed circle radius [px]
        self.r = r # real body radius [m]
        self.color = color # displayed circle color
        self.ax = self.ay = 0 # initial body acceleration, 0


    def iterate(self, objects, params):
        self.ax = self.ay = 0
        G = params['G']
        T = params['T']
        for obj in objects:
            r = math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2)
            if r <= (self.r + obj.r):
                self.vx = (self.vx *self.m + obj.vx * obj.m) / (self.m + obj.m)
                self.vy = (self.vy *self.m + obj.vy * obj.m) / (self.m + obj.m)
                continue
            
            self.ax += G * obj.m * (obj.x - self.x) / math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2)**3
            self.ay += G * obj.m * (obj.y - self.y) / math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2)**3
        
        self.x += self.vx * T + self.ax * T**2 / 2
        self.y += self.vy * T + self.ay * T**2 / 2

        self.vx += self.ax * T
        self.vy += self.ay * T
    
    def get_r(self, params):
        if self.R != -1:
            return self.R
        return self.r / params['scale']

class System:
    def __init__(self, objects, params):
        self.objects = objects
        self.params = params
        self.t = 0

    def iterate(self):
        for i in range(len(self.objects)):
            obj = self.objects[i]
            obj.iterate(self.objects[:i] + self.objects[i+1:], self.params)
        self.t += self.params['T']

def convert(point, scale, DISPLAY): 
    return (round(point[0] / scale + DISPLAY[0]/2.0), round(-point[1] / scale + DISPLAY[1] / 2.0))

def main():
    pygame.init()
    DISPLAY = [1500,700]
    screen = pygame.display.set_mode(DISPLAY)
    running = True

    earth = Body(m=5.97E+24, x=150*10**9, y=0, vx=0, vy=29800, r = 6371*10**3, color='green', R=3)
    sun = Body(m=1.99E+30, x=0, y=0, vx=0, vy=0, r=696340*10**3, color='yellow', R=10)
    halley = Body(m=2.2E+4, x = 35.14*150E+9, vy = 910, color='white', R = 2)

    params = json.load(open('config.json', 'r'))

    solar_system = System([sun, earth, halley], params)
    n = 25
    count = 0
    screen.fill((255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if count % params['iterationsPerFrame'] == 0:
            screen.fill((5, 5, 150))
            for obj in solar_system.objects:
                pygame.draw.circle(screen, obj.color, convert((obj.x, obj.y), params['scale'], DISPLAY), obj.get_r(params))
            pygame.display.flip()

        solar_system.iterate()

        count += 1
        time.sleep(0.0001)

    pygame.quit()
    
if __name__ == '__main__':
    main()
