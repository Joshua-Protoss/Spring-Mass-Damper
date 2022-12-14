import pygame
import sys
import numpy as np
from numpy import sin, cos, pi
from numpy.linalg import inv
from pygame.locals import *
from spring import spring

# functions and classes
def F(t):
    #for matrix method --> F = np.zeros(4) F[1] = F0
    #F = np.zeros(4)
    #F[1] = F0
    F = F0
    if t>1:
        F = 0
        #matrix method F[1] = 0
        #F[1] = 0
    return F

def G(y,t):                                     #state_space method
    
    x1_d, x2_d, x1, x2 = y[0], y[1], y[2], y[3]

    x1_dd = (k1*x2+b1*x2_d-b1*x1_d-k1*x1) / m1
    x2_dd = (F(t)+k1*x1+b1*x1_d-(k1+k2)*x2-(b1+b2)*x2_d) / m2
    
    return np.array([x1_dd, x2_dd, x1_d, x2_d])

##def G(y,t):                                    #matrix method (undamped)
##    return A_inv.dot( F(t) - B.dot(y))

def RK4_step(y, t, dt):
    k1 = G(y, t)
    k2 = G(y+0.5*k1*dt, t+0.5*dt)
    k3 = G(y+0.5*k2*dt, t+0.5*dt)
    k4 = G(y+k3*dt, t+dt)
    
    return dt * (k1 + 2*k2 + 2*k3 + k4)/6

def update(point2, point3):
    mass1.update(point2)
    mass2.update(point3)
    s1.update(point1, point2)
    s2.update(point2, point3)
    
def render():
    screen.fill(WHITE)
    render_statics()
    s1.render()
    s2.render()
    mass1.render()
    mass2.render()

def render_statics():
    #floor and wall
    pygame.draw.line(screen, BLACK, (30, point1[1]+45), (770,point1[1]+45), 10)
    pygame.draw.line(screen, BLACK, (30, point1[1]-50), (30, point1[1]+50), 10)
    pygame.draw.line(screen, GRAY, (point1[0]+offset1, point1[1]+55), (point1[0]+offset1, point1[1]+70), 3)
    pygame.draw.line(screen, GRAY, (point1[0]+offset2, point1[1]+55), (point1[0]+offset2, point1[1]+70), 3)
class Mass():
    def __init__(self, position, color, width, height):
        self.pos = position
        self.color = color
        self.w = width
        self.h = height
        self.left = self.pos[0] - self.w/2
        self.top = self.pos[1] - self.h/2

    def render(self):
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.w, self.h))
        
    def update(self, position):
        self.pos = position
        self.left = self.pos[0] - self.w/2
        self.top = self.pos[1] - self.h/2

class Spring():
    def __init__(self, color, start, end, nodes, width, lead1, lead2):
        self.start = start
        self.end = end
        self.nodes = nodes
        self.width = width
        self.lead1 = lead1
        self.lead2 = lead2
        self.weight = 3
        self.color = color

    def update(self, start, end):
        self.start = start
        self.end = end
        self.x, self.y, self.p1, self.p2 = spring(self.start, self.end, self.nodes, self.width, self.lead1, self.lead2)
        self.p1 = (int(self.p1[0]), int(self.p1[1]))
        self.p2 = (int(self.p2[0]), int(self.p2[1]))
        
    def render(self):
        pygame.draw.line(screen, self.color, self.start, self.p1, self.weight)
        prev_point = self.p1
        for point in zip(self.x, self.y):
            pygame.draw.line(screen, self.color, prev_point, point, self.weight)
            prev_point = point
        pygame.draw.line(screen, self.color, self.p2, self.end, self.weight)
        
# setup
#w, h = 800, 480
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150, 150, 150)
RED = (255,0,0)
BLUE = (0,0,255)


#screen = pygame.display.set_mode((w,h))
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.fill(WHITE)
#pygame.display.update()
clock = pygame.time.Clock()

# parameters
F0 = 0.0
omega = 1.0
m1, m2 = 2.0, 1.0
k1, k2 = 2.0, 2.0
b1 = b2 = 0.9

dof = 2

delta_t = 0.1

#time = np.arange(0.0, 80.0, delta_t)

y = 100*np.array([0, 0, 3, 5])

# setup matrices
##K = np.array([[k1+k2,-k2],[-k2,k2]])
##M = np.array([[m1, 0],[0,m2]])
##I = np.identity(dof)
##
##A = np.zeros((2*dof,2*dof))
##B = np.zeros((2*dof,2*dof))
##
##
##A[0:2,0:2] = M
##A[2:4,2:4] = I
##
##B[0:2,2:4] = K
##B[2:4,0:2] = -I
##A_inv = inv(A)
t = 0

#Pygame and objects

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 38)
mass1 = Mass((150,100), RED, 120, 80)
mass2 = Mass((150,100), BLUE, 80, 80)
s1 = Spring(BLACK, (0,0), (0,0), 20, 50, 20, 70)
s2 = Spring(BLACK, (0,0), (0,0), 15, 30, 70, 50)

point1 = (35, 300)
offset1 = 300
offset2 = 550

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    point2 = point1[0] + offset1 + y[2], point1[1]
    point3 = point1[0] + offset2 + y[3], point1[1]
    update(point2, point3)
    render()
 
    t += delta_t
    y = y + RK4_step(y, t, delta_t)
    
    


    clock.tick(60)
    pygame.display.update()
