import arcade
from models import World, Spot

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
class MazeWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.WHITE)
 
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.spot_sprite = ModelSprite('pacman.png', model=self.world.spot)
                                 
    def update(self, delta):
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()

        self.spot_sprite.draw()

    def on_key_press(self, key, key_modifiers):
         self.world.on_key_press(key, key_modifiers)


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()


def main():
    window = MazeWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()
    