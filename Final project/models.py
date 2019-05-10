import arcade.key
import math
from time import time
import random

MOVEMENT_SPEED = 4
DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

class Spot(arcade.Sprite):
    def __init__(self, x=0, y=0, angle=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y
        self.angle = 0
        self.v_angle = 0
        self.v = 0
        
        self.left_key = False
        self.right_key = False
        self.up_down = False
    
    def add_texture(self, file_name):
        self.append_texture(arcade.load_texture(file_name))
        self.set_texture(0)
        self.a = [self.right, self.top]
        self.b = [self.right, self.bottom]
        self.c = [self.left, self.top]
        self.d = [self.left, self.bottom]
        self.spot_list = [self.a,self.b,self.c,self.d]
        self.diagonal = math.sqrt(((self._get_width()-20)//2)**2 + ((self._get_height()-20)//2)**2)

    def move(self):
        self.center_x += self.v * math.cos(math.radians(self.angle))
        self.center_y += self.v * math.sin(math.radians(self.angle))

        self.spot_list[0][0] = self._get_center_x() + self.diagonal * math.cos(math.radians(20+self.angle))
        self.spot_list[0][1] = self._get_center_y() + self.diagonal *  math.sin(math.radians(20+self.angle))

        self.spot_list[1][0] = self._get_center_x() + self.diagonal * math.cos(math.radians(160+self.angle))
        self.spot_list[1][1] = self._get_center_y() + self.diagonal *  math.sin(math.radians(160+self.angle))
        
        self.spot_list[2][0] = self._get_center_x() + self.diagonal * math.cos(math.radians(200+self.angle))
        self.spot_list[2][1] = self._get_center_y() + self.diagonal *  math.sin(math.radians(200+self.angle))

        self.spot_list[3][0] = self._get_center_x() + self.diagonal * math.cos(math.radians(340+self.angle))
        self.spot_list[3][1] = self._get_center_y() + self.diagonal *  math.sin(math.radians(340+self.angle))
           
    def angle_car(self):
        if self.up_down == True :
            self.angle += self.v_angle

    def update(self, delta):
        self.move()
        self.angle_car()
        if self.is_hit_mid_obs() == True:
            self.v = 0
            
    def is_hit_mid_obs(self):
        for spot in self.spot_list:
            if 40 <= spot[0] <= 520 and 243<= spot[1] <= 308:
                return True
            elif 780 <= spot[0] <= 800 and 38<= spot[1] <= 478:
                return True
            elif 50 <= spot[0] <= 190 and 308<= spot[1] <= 433 or 350 <= spot[0] <= 500 and 308<= spot[1] <= 433:
                return True 
            elif 50 <= spot[0] <= 190 and 128<= spot[1] <= 248 or 350 <= spot[0] <= 500 and 128<= spot[1] <= 350:
                return True 
            elif 650 <= spot[0] <= 770 and 53<= spot[1] <= 123 or 650 <= spot[0] <= 770 and 188<= spot[1] <= 253:
                return True
        return False

car_park_x  = [80, 155, 385,460]
car_park_y = [710]
class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3
    STATE_RESTART = 4

    def __init__(self, width, height):
        self.state = World.STATE_FROZEN
        self.car_park = []
        self.width = width
        self.height = height
        self.time = 0
        self.start_time = 0
        self.spot = None
        self.win = Score(self,800//2,380)

        for i in car_park_x:
            self.car_park.append(Parking_car(self, i,190,90))
            self.car_park.append(Parking_car(self, i,370,90))
        
        for i in car_park_y:
            self.car_park.append(Parking_car(self,i,220,0))
            self.car_park.append(Parking_car(self, i,85,0))

    def add_car(self, car):
        self.spot = car
        
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.spot.v = 3
            self.spot.up_down = True
        elif key == arcade.key.LEFT:
            self.spot.left_key = True
            self.spot.v_angle = 2
        elif key == arcade.key.RIGHT:
            self.spot.right_key = True
            self.spot.v_angle = -2
        elif key == arcade.key.DOWN:
            self.spot.up_down = True
            self.spot.v = -2
        if self.state == World.STATE_DEAD:
            self.restart()
    
    def on_key_release(self,key,key_modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.spot.right_key = False
            self.spot.left_key = False
            self.spot.v_angle = 0
            
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.spot.up_down = False
            self.spot.v = 0

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD, World.STATE_RESTART]:
            return
        self.spot.update(delta)
        if 275 <= self.spot.spot_list[0][0] <= 350 and 308 <= self.spot.spot_list[0][1] <= 430 and 275 <= self.spot.spot_list[1][0] <= 350 and 308 <= self.spot.spot_list[1][1] <= 430 and 275 <= self.spot.spot_list[2][0] <= 350 and 308 <= self.spot.spot_list[2][1] <= 430 and 275 <= self.spot.spot_list[3][0] <= 350 and 308 <= self.spot.spot_list[3][1] <= 430:
            self.die()
        if self.state == World.STATE_STARTED:
            self.start_time= time() - self.time

    def start(self):
        self.state = World.STATE_STARTED
        if self.time == 0:
            self.time = time()
    def freeze(self):
        self.state = World.STATE_FROZEN
    def is_started(self):
        return self.state == World.STATE_STARTED
    def die(self):
        self.state = World.STATE_DEAD
    def is_dead(self):
        return self.state == World.STATE_DEAD
    def restart(self):
        self.state = World.STATE_RESTART

class Parking_car:
    def __init__(self,world,x,y,angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = angle

class Score:
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0
    
