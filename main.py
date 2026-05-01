from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

textures = {
    'grass': load_texture('assets/grass.png'),
    'bricks': load_texture('assets/bricks.png'),
    'dirt': load_texture('assets/dirt.png'),
    'oak': load_texture('assets/oak.png'),
    'sand': load_texture('assets/send.png'),
    'stone': load_texture('assets/stone.png'),
    'wood': load_texture('assets/wood.png'),
    'wool': load_texture('assets/wool.png'),
    'foliage': load_texture('assets/foliage.png'),
    'obsidian': load_texture('assets/obsidian.png'),
    'cobblestone': load_texture('assets/cobblestone.png'),
    'lava': load_texture('assets/lava.png')
}

sky_texture = load_texture('assets/sky.png')

hotbar_slots = [textures['grass'], textures['dirt'], textures['stone'], textures['wood'], textures['bricks']]
active_slot = 0
inventory_open = False
selected_texture_to_assign = None


def update():
    global active_slot

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if not inventory_open:
        for i in range(5):
            if held_keys[str(i + 1)]:
                active_slot = i

    update_hotbar_ui()


def input(key):
    global active_slot, inventory_open, selected_texture_to_assign

    if key == 'e':
        inventory_open = not inventory_open
        inventory_menu.enabled = inventory_open
        instruction_text.enabled = False
        selected_texture_to_assign = None
        mouse.visible = inventory_open
        mouse.locked = not inventory_open
        player.enabled = not inventory_open

    if not inventory_open:
        if key == 'scroll up': active_slot = (active_slot + 1) % 5
        if key == 'scroll down': active_slot = (active_slot - 1) % 5

    if inventory_open and selected_texture_to_assign:
        if key in ('1', '2', '3', '4', '5'):
            index = int(key) - 1
            hotbar_slots[index] = selected_texture_to_assign
            selected_texture_to_assign = None
            instruction_text.enabled = False


instruction_text = Text(
    text='Select slot 1-5 to assign...',
    origin=(0, 0), y=0.4, scale=2,
    color=color.yellow, enabled=False
)


inventory_menu = Entity(parent=camera.ui, enabled=False)
bg = Entity(parent=inventory_menu, model='quad', scale=(0.8, 0.6), color=color.black66, z=1)


def prepare_assign(tex):
    global selected_texture_to_assign
    selected_texture_to_assign = tex
    instruction_text.enabled = True


for i, (name, tex) in enumerate(textures.items()):
    b = Button(
        parent=inventory_menu,
        model='quad',
        texture=tex,
        scale=0.1,
        position=(-0.3 + (i % 4) * 0.2, 0.2 - (i // 4) * 0.2),
        color=color.gray,
        highlight_color=color.white,
        pressed_color=color.white
    )
    b.on_click = Func(prepare_assign, tex)

hotbar_ui = Entity(parent=camera.ui, position=(0, -0.45))
slot_visuals = []

for i in range(5):
    Entity(parent=hotbar_ui, model='quad', scale=0.11, position=(-0.3 + i * 0.15, 0), color=color.black33, z=0.1)

    s = Entity(
        parent=hotbar_ui,
        model='quad',
        texture=hotbar_slots[i],
        scale=0.1,
        position=(-0.3 + i * 0.15, 0),
        color=color.white
    )
    slot_visuals.append(s)


def update_hotbar_ui():
    for i in range(5):
        slot_visuals[i].texture = hotbar_slots[i]
        if i == active_slot:
            slot_visuals[i].scale = 0.12
            slot_visuals[i].color = color.white
        else:
            slot_visuals[i].scale = 0.1
            slot_visuals[i].color = color.gray


class Sky(Entity):
    def __init__(self):
        super().__init__(parent=scene, model='sphere', scale=200, texture=sky_texture, double_sided=True)


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui, model='cube', scale=(0.2, 0.3), color=color.gray,
            rotation=Vec3(150, -10, 0), position=Vec2(0.4, -0.4)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)
        self.rotation = Vec3(90, -10, 0)

    def passive(self):
        self.rotation = Vec3(150, -10, 0)
        self.position = Vec2(0.4, -0.4)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=textures['grass']):
        super().__init__(
            parent=scene, position=position, model='cube', origin_y=0.5,
            texture=texture, color=color.white, highlight_color=color.light_gray
        )

    def input(self, key):
        if self.hovered and not inventory_open:
            if key == 'right mouse down':
                Voxel(position=self.position + mouse.normal, texture=hotbar_slots[active_slot])
            if key == 'left mouse down':
                destroy(self)


for z in range(15):
    for x in range(15):
        Voxel(position=(x, 0, z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()