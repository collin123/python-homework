import spyral

SIZE = (640, 480)
BG_COLOR = (0, 0, 0)

SPRITE_FILE = ''

def load_walking_animation(filename, direction, offset=None, size=None):
        offset = (offset or (0, 0))
        size = (size or (32, 32))
        walking_images = []
        direction_rows = {'down':0, 'left':1, 'right':2, 'up':3}
        assert(direction in direction_rows)
        direction = (direction_rows.get(direction) * size[1])

        img = spyral.Image(filename=filename)
        img.crop(((size[0] * 0) + offset[0], offset[1] + direction), size)
        walking_images.append(img)

        img = spyral.Image(filename=filename)
        img.crop(((size[0] * 1) + offset[0], offset[1] + direction), size)
        walking_images.append(img)

        img = spyral.Image(filename=filename)
        img.crop(((size[0] * 2) + offset[0], offset[1] + direction), size)
        walking_images.append(img)

        img = spyral.Image(filename=filename)
        img.crop(((size[0] * 1) + offset[0], offset[1] + direction), size)
        walking_images.append(img)

        return spyral.Animation('image', spyral.easing.Iterate(walking_images), 1.0, loop=True)

class Game(spyral.Scene):
        """
        A Scene represents a distinct state of your game. They could be menus,
        different subgames, or any other things which are mostly distinct.
        """
        def __init__(self):
                spyral.Scene.__init__(self, SIZE)
                self.background = spyral.Image(size=SIZE).fill(BG_COLOR)
                spyral.event.register("system.quit", spyral.director.quit)

                self.player_sprite = spyral.Sprite(self)
                walking_animation = load_walking_animation(SPRITE_FILE, 'right', ((32 * 3), 126))
                self.player_sprite.animate(walking_animation)

if __name__ == "__main__":
        spyral.director.init(SIZE) # the director is the manager for your scenes
        spyral.director.run(scene=Game()) # This will run your game. It will not return.
