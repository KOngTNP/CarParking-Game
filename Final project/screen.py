import arcade
from models import World, Spot
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 518

class MazeWindow(arcade.Window):
    def __init__(self, width, height):
        self.car_list = []
        super().__init__(width, height)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = arcade.load_texture("Wallpaper2.jpg")
        self.spot_sprite = Spot(100, 50, angle=0)
        self.spot_sprite.add_texture('car_move.png')
        self.world.add_car(self.spot_sprite)
        park_car_list = ['parking_car1.png','parking_car2.png']
        for i in self.world.car_park:
            self.car_list.append(ModelSprite(random.choice(park_car_list), model=i))

                                 
    def update(self, delta):
        self.world.update(delta)

    def on_draw(self): 
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        self.world.spot.draw()
        if self.world.state != self.world.STATE_FROZEN:
            arcade.draw_text(f"Time: {self.world.start_time:.0f}",23,450,arcade.color.RED,30)

        if self.world.state == self.world.STATE_FROZEN:
            
            arcade.draw_text(f"CAR PARKING GAME",210,440,arcade.color.RED,30)
            arcade.draw_text(f"Press any key to start",180,30,arcade.color.BLACK,15)
        for i in self.car_list:
            i.draw()
        if self.world.state == self.world.STATE_DEAD:
            self.background = arcade.load_texture("Wallpaper2END.jpg")
            if self.world.start_time < 15:
                ModelSprite('star_score3.png',model = self.world.win).draw()
                arcade.draw_text(f"You get 3 star!!!!!",300,250,arcade.color.BLUE,25)
                
            elif self.world.start_time < 20:
                ModelSprite('star_score2.png',model = self.world.win).draw()
                arcade.draw_text(f"You get 2 star!!!!!",300,250,arcade.color.BLUE,25)

            elif self.world.start_time >20:
                ModelSprite('star_score1.png',model = self.world.win).draw()
                arcade.draw_text(f"You get 1 star!!!!!",300,250,arcade.color.BLUE,25)

            arcade.draw_text(f"Thank you for playing",240,200,arcade.color.BLUE,30)
            arcade.draw_text("Press any key to restart.", 235, 150, arcade.color.BLACK, 30)
            self.world.die()
    def restart(self):
        self.car_list = []
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = arcade.load_texture("Wallpaper2.jpg")
        self.spot_sprite = Spot(100, 50, angle=0)
        self.spot_sprite.add_texture('car_move.png')
        self.world.add_car(self.spot_sprite)
        park_car_list = ['parking_car1.png','parking_car2.png']
        for i in self.world.car_park:
            self.car_list.append(ModelSprite(random.choice(park_car_list), model=i))

        
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if self.world.state == World.STATE_RESTART:
            self.restart()
        
        if not self.world.is_dead():
             self.world.start()
        
        
    
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        self.front_left = [self.right, self.top]
        self.front_rigt = [self.right, self.bottom]
        self.back_left = [self.left, self.top]
        self.back_right = [self.right, self.bottom]
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
 
    def draw(self):
        self.sync_with_model()
        super().draw()


def main():
    window = MazeWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()
    