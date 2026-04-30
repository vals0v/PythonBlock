from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

grass_texture = load_texture('assets/grass.png')
bricks_texture = load_texture('assets/bricks.png')
dirt_texture = load_texture('assets/dirt.png')
oak_texture = load_texture('assets/oak.png')
send_texture = load_texture('assets/send.png')
stone_texture = load_texture('assets/stone.png')
wood_texture = load_texture('assets/wood.png')
sky_texture = load_texture('assets/sky.png')
wool_texture = load_texture('assets/wool.png')
foliage_texture = load_texture('assets/foliage.png')
obsidian_texture = load_texture('assets/obsidian.png')
water1_texture = load_texture('assets/water1.png')
lava_texture = load_texture('assets/lava.png')
cobblestone_texture = load_texture('assets/cobblestone.png')

current_texture = grass_texture


def update():
    global current_texture

    if held_keys['1']: current_texture = grass_texture
    if held_keys['2']: current_texture = dirt_texture
    if held_keys['3']: current_texture = oak_texture
    if held_keys['4']: current_texture = send_texture
    if held_keys['5']: current_texture = stone_texture
    if held_keys['6']: current_texture = wood_texture
    if held_keys['7']: current_texture = bricks_texture
    if held_keys['8']: current_texture = wool_texture
    if held_keys['9']: current_texture = foliage_texture
    if held_keys['0']: current_texture = obsidian_texture
    if held_keys['-']: current_texture = water1_texture
    if held_keys['=']: current_texture = lava_texture
    if held_keys[']']: current_texture = cobblestone_texture

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            scale=150,
            texture=sky_texture,
            double_sided=True
        )


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='cube',
            scale=(0.2, 0.3),
            color=color.gray,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.4)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)
        self.rotation = Vec3(90, -10, 0)

    def passive(self):
        self.rotation = Vec3(150, -10, 0)
        self.position = Vec2(0.4, -0.4)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            highlight_color=color.light_gray
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                # Mouse normal allows placing blocks on the side of others
                Voxel(position=self.position + mouse.normal, texture=current_texture)
            if key == 'left mouse down':
                destroy(self)



for z in range(30):
    for x in range(30):
        voxel = Voxel(position=(x, 0, z))


player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()