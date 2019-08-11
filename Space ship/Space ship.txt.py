import simplegui
import math
import random
wt = 800
ht = 600
ex=[wt/2,ht/2]
sc = 0
lives = 3
time = 0
tim=0
expl=False
splash=True
started = False
rock_group=set([])
missile_group=set([])
rmst=set([])
expl1=False
EXPLOSION_CENTER = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]
explosion_image = simplegui.load_image("D:\Document\Space ship\explosion_alpha.png")
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("D:\Document\Space ship\debris2_blue.png")
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("D:\Document\Space ship\background.png")
if splash==True:
    splash_info = ImageInfo([200, 150], [400, 300])
    splash_image = simplegui.load_image("D:\Document\Space ship\splash.png")
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("D:\Document\Space ship\double_ship.png")
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("D:\Document\Space ship\shot2.png")
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("D:\Document\Space ship\asteroid_blue.png")
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("D:\Document\Space ship\explosion.png")
soundtrack = simplegui.load_sound("D:\Document\Space ship\soundtrack.mp3")
missile_sound = simplegui.load_sound("D:\Document\Space ship\missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("D:\Document\Space ship\thrust.mp3")
explosion_sound = simplegui.load_sound("D:\Document\Space ship\explosion.mp3")
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()       
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % wt
        self.pos[1] = (self.pos[1] + self.vel[1]) % ht
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .25
            self.vel[1] += acc[1] * .25           
        self.vel[0] *= .96
        self.vel[1] *= .96
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()      
    def get_position(self):
        return self.pos    
    def increment_angle_vel(self):
        self.angle_vel += .05       
    def decrement_angle_vel(self):
        self.angle_vel -= .05       
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    def get_position(self):
        return self.pos
    def update(self):
        self.angle += self.angle_vel
        self.age += 1       
        self.pos[0] = (self.pos[0] + self.vel[0]) % wt
        self.pos[1] = (self.pos[1] + self.vel[1]) % ht
    def collide(self,other_object):
        global ex
        c1=self.get_position()
        c2=other_object.get_position()
        if distance(c1,c2)<(self.radius + other_object.radius):
            explosion_sound.play()
            ex=c2
            return True
        else:
            return False
def gr_group_collide():
    global sc,expl1
    remove_set = set([])
    rsm=set([])
    for ms in missile_group:
        for rck in rock_group:
            if rck.collide(ms):
                sc += 10
                remove_set.add(rck)
                rsm.add(ms)
                expl1=True
    if len(remove_set)>0:
        rock_group.difference_update(remove_set)
    if len(rsm)>0:
        missile_group.difference_update(rsm)
def group_collide():
    global lives, started, expl, ex
    remove_set = set([])
    for rck in rock_group:
         if rck.collide(my_ship):
            lives -= 1
            expl=True
            if lives==0:
                started=False
                soundtrack.pause()
                remove_set=rock_group.copy()
            remove_set.add(rck)
    rock_group.difference_update(remove_set)
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()      
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
def click(pos):
    global started, lives, sc
    lives=3
    sc=0
    center = [wt / 2, ht / 2]
    size = splash_info.get_size()
    inwt = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inht = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwt and inht:
        started = True
        soundtrack.rewind()
        soundtrack.play()
def draw(canvas):
    global time, splash, started, expl, tim, EXPLOSION_DIM, EXPLOSION_SIZE, EXPLOSION_CENTER, wt, ht, ex
    group_collide()
    gr_group_collide()
    time += 1
    wtime = (time / 4) % wt
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [wt / 2, ht / 2], [wt, ht])
    canvas.draw_image(debris_image, center, size, (wtime - wt / 2, ht / 2), (wt, ht))
    canvas.draw_image(debris_image, center, size, (wtime + wt / 2, ht / 2), (wt, ht))
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(sc), [680, 80], 22, "White")
    my_ship.draw(canvas)
    for r in rock_group:
        r.draw(canvas)
    for m in missile_group:
        remove_set = set([])
        m.draw(canvas)
        if m.age>m.lifespan:
            remove_set.add(m)
        missile_group.difference_update(rmst)
        missile_group.difference_update(remove_set)
    if expl:
        while tim<360:
            tim+=1
            explosion_index = [time % EXPLOSION_DIM[0], (time // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
            canvas.draw_image(explosion_image,[EXPLOSION_CENTER[0]+explosion_index[0]*EXPLOSION_SIZE[0],EXPLOSION_CENTER[1]+explosion_index[1]*EXPLOSION_SIZE[1]],EXPLOSION_SIZE,ex,EXPLOSION_SIZE)
        tim=0
    if expl1:
        while tim<360:
            tim+=1
            explosion_index = [time % EXPLOSION_DIM[0], (time // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
            canvas.draw_image(explosion_image,[EXPLOSION_CENTER[0]+explosion_index[0]*EXPLOSION_SIZE[0],EXPLOSION_CENTER[1]+explosion_index[1]*EXPLOSION_SIZE[1]],EXPLOSION_SIZE,ex,EXPLOSION_SIZE)
        tim=0
    my_ship.update()
    for r in rock_group:
        r.update()
    for m in missile_group:
        m.update()
    
    if lives == 0:
        splash=False
        canvas.draw_text('You Lose!!!', [150, 300], 122, "White")
    if not started:
        if splash==True:
            canvas.draw_image(splash_image, splash_info.get_center(), 
                              splash_info.get_size(), [wt / 2, ht / 2], 
                              splash_info.get_size())
def rock_spawner():
    global rock_group, started, sc
    if started:
        rock_pos = [random.randrange(0, wt), random.randrange(0, ht)]
        rock_vel = [random.randrange(-4,4) * .6 - .3, random.randrange(-4,4) * .6 - .3]
        if sc>250:
            rock_vel[0]*=2
            rock_vel[1]*=2
        rock_avel = random.random() * .2 - .1
        if len(rock_group)<12:
            if distance(rock_pos,my_ship.pos)>100:
                rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
def expl2():
    global expl
    if expl==True:
        expl=False
def expl3():
    global expl1
    if expl1==True:
        expl1=False
frame = simplegui.create_frame("Asteroids", wt, ht)
my_ship = Ship([wt / 2, ht / 2], [0, 0], 0, ship_image, ship_info)
a_missile = Sprite([2 * wt / 3, 2 * ht / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
soundtrack.play()
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)
timer2 = simplegui.create_timer(1750, expl2)
timer3 = simplegui.create_timer(1750, expl3)
timer.start()
frame.start()
timer2.start()
timer3.start()