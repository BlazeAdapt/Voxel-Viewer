import pygame
import numpy as np
import cv2
from numba import njit,prange
import math

color_map=cv2.imread('C1W.png')
height_map=cv2.resize(cv2.imread('D1.png',cv2.IMREAD_GRAYSCALE),(1024, 1024),interpolation=cv2.INTER_LINEAR)
height=1080
width=1920

posx = 435.0
posy = 245.0
ht = 75.0
pane = 0.0
rot = 0.0
screenh=1080
velx = 0
vely = 0
velz=0

acch=25
friction=12.5
g=0.25
vjump=3
airborne=False
jcooldown=0


@njit(cache=True,parallel=True,fastmath=True)
def drawimg(color_map, height_map, posx, posy, ht,pane,rot):
    viewlen=1920
    viewh=1080
    dbig = viewlen//2
    frame = np.zeros((1920, 1080, 3), dtype=np.uint8)
    angle=math.tan(pane)
    for x in prange(viewlen):
        horizon=0
        num=x/viewlen
        for y in range(viewh):
            frame[x,y, 0] = 135
            frame[x,y, 1] = 150
            frame[x,y, 2] = 255
        for dist in range(1,dbig):
            length=(0.5-num)*dist*2
            my = int(posy - (length * math.sin(rot) + dist * math.cos(rot))) % 1024
            mx = int(posx + (dist * math.sin(rot) - length * math.cos(rot))) % 1024
            yend=screenh-(screenh / 2 - dbig * angle+ (ht - height_map[my, mx]) * dbig / dist)
            if yend<horizon:
                yend=horizon
            yend=min(yend,screenh)
            b, g, r = color_map[my, mx]

            for k in range(horizon,int(yend)):
                frame[x, screenh-k, 0] = r
                frame[x, screenh-k, 1] = g
                frame[x, screenh-k, 2] = b
            horizon=yend
            if horizon>=screenh-1:
                break
    return frame
def update_screen():
    global surf
    frame = drawimg(color_map, height_map, posx, posy, ht,pane,rot)
    surf = pygame.surfarray.make_surface(frame)
pygame.init()
pygame.mixer.init()
walksound= pygame.mixer.Sound('walksound.wav')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Voxel Viewer")
clock = pygame.time.Clock()
running = True
surf = pygame.surfarray.make_surface(drawimg(color_map, height_map, posx, posy, ht,pane,rot))
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            dx, dy = event.rel

            rot+=dx/100
            pane+=dy/100
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
    if keys[pygame.K_s]:
        vely-= acch
    if keys[pygame.K_w]:
        vely+=acch
    if keys[pygame.K_a]:
        velx -= acch
    if keys[pygame.K_d]:
        velx += acch
    if not vely==0:
        vely-=friction*(abs(vely)/vely)
    if not velx==0:
        velx-=friction*(abs(velx)/velx)
    if keys[pygame.K_q]:
        velmax=200
    else:
        velmax=100
    vely=min(velmax,max(-velmax,vely))
    velx=min(velmax,max(-velmax,velx))
    posx+=(vely*math.sin(rot)+ velx*math.cos(rot))/100
    posy+=(velx*math.sin(rot)- vely*math.cos(rot))/100
    posx = (posx + 1024) % 1024
    posy = (posy + 1024) % 1024
    if keys[pygame.K_UP]:
        pane -= 0.1
    if keys[pygame.K_DOWN]:
        pane += 0.1
    if keys[pygame.K_p]:
        ht += 2
    if keys[pygame.K_l]:
        ht -= 2
    airborne = ht >= height_map[int(posy), int(posx)] + 11
    if keys[pygame.K_LEFT]:
        rot -= 0.1
    if keys[pygame.K_RIGHT]:
        rot += 0.1
    if keys[pygame.K_SPACE] and not airborne and not jcooldown:
        velz+=vjump
        jcooldown=10
    velz-= g

    if not airborne and jcooldown>0:
        jcooldown-=1

    ht=max(height_map[int(posy),int(posx)]+10.0,ht+velz)
    if ht<=height_map[int(posy),int(posx)]+10:
        velz=0
        airborne=False
    pane = max(-math.pi/3, min(math.pi/3, pane))
    #if height_map[int(posy),int(posx)] > ht:
    update_screen()

    if (velx or vely) and walksound.get_num_channels()==0:
        walksound.play(fade_ms=500)
    if (not (velx or vely) and walksound.get_num_channels()>0):
        walksound.fadeout(500)
    if airborne:
        walksound.set_volume(0.1)
    else:
        walksound.set_volume(1)
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()