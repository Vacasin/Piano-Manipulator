#设计一个基于pygame和music21的钢琴模拟器
import os
import pygame
from pygame.locals import *
import sys
import music21
pygame.init()


piano_display = [
    "la", " ", "si",
    "do", " ", "re", " ", "mi", "fa", " ", "so", " ", "la", " ", "si",
    "do", " ", "re", " ", "mi", "fa", " ", "so", " ", "la", " ", "si",
    "do", " ", "re", " ", "mi", "fa", " ", "so", " ", "la", " ", "si",
    "do", " ", "re", " ", "mi", "fa", " ", "so", " ", "la", " ", "si",
    "do", " ", "re", " ", "mi", "fa", " ", "so", " ", "la", " ", "si",
    "do", " ", "re", " ", "mi", "fa", " ", "so", " ", "la", " ", "si",
    "do", " ", "re", " ", "mi", "fa", " ", "so", " ", "la", " ", "si",
    "do"
]

# 定义了一个列表来存储钢琴键的名称
piano_notes = [
    "A0", "A#0", "B0",
    "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1",
    "A1", "A#1", "B1",
    "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2",
    "A2", "A#2", "B2",
    "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3",
    "A3", "A#3", "B3",
    "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4",
    "A4", "A#4", "B4",
    "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5",
    "A5", "A#5", "B5",
    "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6",
    "A6", "A#6", "B6",
    "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7",
    "A7", "A#7", "B7",
    "C8"
]

# 通过音符索引按键
# 代码通过循环，将每个音符名称作为键，将该音符在键盘中的索引作为值，存储在notes_index字典中
notes_index = {}
index = 0
for note in piano_notes:
    notes_index[note] = index
    index += 1

# 定义了一些常量，如期望的帧速率、键盘的位置和大小、键之间的距离等
FPS = 60  # desired framerate in frames per second. try out other values !
KEYBOARDX = 5   # Top left of the full keyboard
KEYBOARDY = 5   # Top left of the full keyboard
KEYBETWEEN = 0  # distance between the key
# height of white key (useful for put the text at the right distance
KEY_HEIGHT = 0
DISTKEY_TEXT = 10  # distance between the key and the text with the name of the key below
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 通过将键盘键码与Unicode字符相映射，为每个键码创建了一个字典，并创建了另一个字典来将Unicode字符映射到钢琴键
QWERTY_SCANCODE_UNICODE = dict(zip([  # correspondance azerty keyboard with its scancode
    49, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
    23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
    38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 51,
    50, 94, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62
], [
    '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
    'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '\\',
    'lsh', '<', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'rsh'
]))


unicode_to_note = dict(zip(
    [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'rsh'
    ],
    [  # correspondance azerty keyboard with its scancode
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5",
        "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6",
    ]))
print(unicode_to_note)


def nameof(n):
    a = n.name + str(n.octave)
    if "--" in a:                 # order matters
        b = a.replace("B--", "A")
        b = b.replace("A--", "G")  # chain b.replace not a.replace
        b = b.replace("G--", "F")
        b = b.replace("E--", "D")
        b = b.replace("D--", "C")
        return b
    elif "-" in a:
        b = a.replace("C-", "B")
        b = b.replace("D-", "C#")  # chain b.replace not a.replace
        b = b.replace("E-", "D#")
        b = b.replace("F-", "E")
        b = b.replace("G-", "F#")
        b = b.replace("A-", "G#")
        b = b.replace("B-", "A#")
        return b
    elif "##" in a:
        b = a.replace("C##", "D")
        b = b.replace("D##", "E")  # chain b.replace not a.replace
        b = b.replace("F##", "G")
        b = b.replace("G##", "A")
        b = b.replace("A##", "B")
        return b
    elif "E#" in a:
        b = a.replace("E#", "F")
        return b
    elif "B#" in a:
        b = a.replace("B#", "C")
        return b
    else:
        return a


nameOffset = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11
}
# DEFINING THE KEYBOARD SETTING:
# we use 'freesound_med' folder with 4 octaves: C2 to G5
# Create the list of note filenames, sorted according to classic notation c, db, d, eb, etc...
pygame.mixer.pre_init(44100, -16, 2, 4096)  # setup mixer to avoid sound lag
music_order = ['c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab', 'a', 'bb', 'b']
note_sounds = {}  # list of all the note filename
for note in piano_notes:
    note_sounds[note] = pygame.mixer.Sound(
        os.path.join("./piano-keys", "{}.ogg".format(note)))
with open('computer_typewriter.kb', 'r') as f:
    KEY_ASCII = f.read().split('\n')


class Hand(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((150, 200))
        self.image.fill((255, 255, 255))

        # pygame.draw.rect(self.image, [255, 255, 255], [10, 10, 10, 10], 0)
        # self.init_finger()

        # 手掌所在位置
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 180

        # 右手手掌
        self.finger_up_down = [True, True, True, True, True]
        self.finger_y = [50, 20, 0, 15, 30]
        self.finger_offset = 2
        self.finger_length = 150
        self.finger_width = 30
        self.up_color = [237, 186, 163]
        self.down_color = [0, 186, 163],
        self.all_fingers = [None]*5

        # 建立所有钢琴键索引位置
        self.piano_index_positon_item = [15, 30, 45, 60, 75, 105, 120, 135, 150, 165, 180, 195]
        self.piano_len = 30*7
        self.piano_index_position = []

        # 手掌心
        pygame.draw.rect(self.image, self.up_color, [0+10, self.finger_length+10, 5*self.finger_width-2*10, 50], 0)

        # 前两个 offset
        self.global_offset = 60
        self.piano_index_position = [15, 30, 45]
        # 中间
        for i in range(7):
            offset = i * self.piano_len + self.global_offset
            for item in self.piano_index_positon_item:
                self.piano_index_position.append(offset + item)
        # 结尾
        self.piano_index_position.append(self.piano_index_position[-1]+30)
        self.hand_index_position = [15, 45, 75, 105, 135]


    def display(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        offset = 2
        finger_len = 150
        finger_width = 30
        for finger_index, up_down in enumerate(self.finger_up_down):
            if(up_down):
                # 没有按压琴键的情况
                self.all_fingers[finger_index] = pygame.draw.rect(self.image, self.up_color, [
                                                                  finger_index*finger_width+offset, self.finger_y[finger_index], self.finger_width-2*self.finger_offset, self.finger_length-self.finger_y[finger_index]], 0)
            else:
                # 按压琴键的情况
                self.all_fingers[finger_index] = pygame.draw.rect(self.image, self.down_color, [
                                                                  finger_index*finger_width+offset, self.finger_y[finger_index], self.finger_width-2*self.finger_offset, self.finger_length-self.finger_y[finger_index]], 0)

    def press_finger(self, finger_index):
        self.finger_up_down[finger_index] = False

    def release_finger(self, finger_index):
        self.finger_up_down[finger_index] = True

    def move(self, finger_index, piano_index):

        piano_position = self.piano_index_position[piano_index]
        finger_position = self.hand_index_position[finger_index]

        hand_position = piano_position - finger_position
        self.rect.x = hand_position

# 左手手掌
class LHand(Hand):
    def __init__(self) -> None:
        super().__init__()
        self.finger_y = [30, 15, 0, 20, 50]
        # self.finger_y = self.finger_y.reverse()

        self.rect.x = 500


# Create the Key sprites:
class Key(pygame.sprite.Sprite):
    keyobj_list = []

    def __init__(self, name, keyevent):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.color = self.name.split('_')[1]
        self.image = pygame.image.load(os.path.join(
            'pythonpiano_pictures', self.name+'_unpressed.png'))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()  # need to be defined for the group updates!
        self.width = self.image.get_width()
        # name of the key returned by 'pygame.event.scancode' = Key code number
        self.keyevent = keyevent
        self.pressed = False
        Key.keyobj_list.append(self)
        self.rect.x = 0  # temporary, the position of the key is '0'
        self.rect.y = KEYBOARDY
        self._layer = 0  # the order with which the key is drawn
        # Preloading of the key picture for faster load
        self._img_down = pygame.image.load(os.path.join(
            'pythonpiano_pictures', self.name+'_pressed.png'))
        self._img_up = pygame.image.load(os.path.join(
            'pythonpiano_pictures', self.name+'_unpressed.png'))

    def update(self):
        if self.pressed:
            self.image = self._img_down
#             print("the key {} is being pressed".format(self.keyevent))
        else:
            self.image = self._img_up


class Game(object):
    def __init__(self):
        # Qwerty or Azerty keyboard depending on command line arguments:
        if len(sys.argv) == 1:
            SCANCODE_UNICODE = QWERTY_SCANCODE_UNICODE
        elif len(sys.argv) > 2:
            print(
                "You need to provide only one argument: for example: 'python pypiano.pi azerty'")
            sys.exit()
        else:
            arg = sys.argv[1].upper()
            if arg == "QWERTY":
                SCANCODE_UNICODE = QWERTY_SCANCODE_UNICODE
            elif arg == "AZERTY":
                SCANCODE_UNICODE = AZERTY_SCANCODE_UNICODE
            else:
                print("Not a valid argument. Valid example: 'python pypiano.pi azerty'")
                sys.exit()

        # Draw the background:
        self.screen = pygame.display.set_mode(
            (1500, 600))  # set screensize of pygame window
        self.background = pygame.Surface(
            self.screen.get_size())  # create empty pygame surface
        # fill the background white color (red,green,blue)
        self.background.fill((255, 255, 255))
        # Useless if it's not a sprite...:
#         self.background = self.background.convert()  #convert Surface object to make blitting faster

        # Create all the sprites beforehand:
        # Position of key for one octave:
        key_octave = ['key_white_Left', 'key_black', 'key_white_Middle', 'key_black',
                      'key_white_Right', 'key_white_Left', 'key_black', 'key_white_Middle', 'key_black',
                      'key_white_Middle', 'key_black', 'key_white_Right']
        music_octave = ['C', 'C#', 'D', 'D#', 'E',
                        'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        # each key must have a reference to the keyboard ascii with their correct position:
        keyevent_idx = 0
        keyboardx_position = KEYBOARDX
        # assign groups for the Sprite:
        self.keysprites = pygame.sprite.LayeredUpdates()

        # 添加手
        self.rhand = Hand()
        self.lhand = LHand()

        self.display_font_size = 18
        self.white_y = 135
        self.black_y = 200
        self.group_colors = [
            (31, 119, 180),   # 蓝色
            (255, 127, 14),   # 橙色
            (44, 160, 44),    # 绿色
            (214, 39, 40),    # 红色
            (148, 103, 189),  # 紫色
            (140, 86, 75),    # 棕色
            (227, 119, 194),  # 粉色
            (127, 127, 127),  # 灰色
            (188, 189, 34)    # 黄色
        ]
        self.display_offset = -4
        # 左边三个
        self.group = 0
        for key in key_octave[9:]:
            key_obj = Key(key, KEY_ASCII[keyevent_idx])
            
            # Draw the keys:
            if key_obj.color == 'white':
                key_obj.rect.x = keyboardx_position
                keyboardx_position += key_obj.width + KEYBETWEEN
                # 绘制标识符号
                note_name = piano_display[keyevent_idx]
                note_position = self.rhand.piano_index_position[keyevent_idx]
                print(keyevent_idx, note_name, note_position)
                ft = pygame.font.SysFont("Console", self.display_font_size)
                note_display = ft.render("{}".format(
                    note_name), True, self.group_colors[self.group])
                self.background.blit(
                    note_display, (note_position+self.display_offset, self.white_y))
            elif key_obj.color == 'black':
                key_obj.rect.x = keyboardx_position - key_obj.width/4
                key_obj._layer = 1
                note_name = piano_display[keyevent_idx]
                note_position = self.rhand.piano_index_position[keyevent_idx]
                print(keyevent_idx, note_name, note_position)
                ft = pygame.font.SysFont("Console", self.display_font_size)
                note_display = ft.render("{}".format(
                    note_name), True, self.group_colors[self.group])
                self.background.blit(
                    note_display, (note_position+self.display_offset, self.black_y))
            
            keyevent_idx += 1
            self.background.blit(key_obj.image, key_obj.rect)
            self.keysprites.add(key_obj)  # add the key sprite to the group

        self.group = 1
        for i in range(7):
            for idx, key in enumerate(key_octave):
                key_obj = Key(key, KEY_ASCII[keyevent_idx])
                
                # Draw the keys:
                if key_obj.color == 'white':
                    key_obj.rect.x = keyboardx_position
                    keyboardx_position += key_obj.width + KEYBETWEEN
                    # 绘制标识符号
                    note_name = piano_display[keyevent_idx]
                    note_position = self.rhand.piano_index_position[keyevent_idx]
                    print(keyevent_idx, note_name, note_position)
                    ft = pygame.font.SysFont("Console", self.display_font_size)
                    note_display = ft.render("{}".format(
                        note_name), True, self.group_colors[self.group])
                    self.background.blit(
                        note_display, (note_position+self.display_offset, self.white_y))
                elif key_obj.color == 'black':
                    key_obj.rect.x = keyboardx_position - key_obj.width/4
                    key_obj._layer = 1
                    note_name = piano_display[keyevent_idx]
                    note_position = self.rhand.piano_index_position[keyevent_idx]
                    print(keyevent_idx, note_name, note_position)
                    ft = pygame.font.SysFont("Console", self.display_font_size)
                    note_display = ft.render("{}".format(
                        note_name), True, self.group_colors[self.group])
                    self.background.blit(
                        note_display, (note_position+self.display_offset, self.black_y))
                
                keyevent_idx += 1
                self.background.blit(key_obj.image, key_obj.rect)
                self.keysprites.add(key_obj)  # add the key sprite to the group

            self.group += 1

        # 右边一个
        for key in key_octave[:1]:
            key_obj = Key(key, KEY_ASCII[keyevent_idx])
            
            # Draw the keys:
            if key_obj.color == 'white':
                key_obj.rect.x = keyboardx_position
                keyboardx_position += key_obj.width + KEYBETWEEN
                # 绘制标识符号
                note_name = piano_display[keyevent_idx]
                note_position = self.rhand.piano_index_position[keyevent_idx]
                print(keyevent_idx, note_name, note_position)
                ft = pygame.font.SysFont("Console", self.display_font_size)
                note_display = ft.render("{}".format(
                    note_name), True, self.group_colors[self.group])
                self.background.blit(
                    note_display, (note_position+self.display_offset, self.white_y))
            elif key_obj.color == 'black':
                key_obj.rect.x = keyboardx_position - key_obj.width/4
                key_obj._layer = 1
                note_name = piano_display[keyevent_idx]
                note_position = self.rhand.piano_index_position[keyevent_idx]
                print(keyevent_idx, note_name, note_position)
                ft = pygame.font.SysFont("Console", self.display_font_size)
                note_display = ft.render("{}".format(
                    note_name), True, self.group_colors[self.group])
                self.background.blit(
                    note_display, (note_position+self.display_offset, self.black_y))
            
            keyevent_idx += 1
            self.background.blit(key_obj.image, key_obj.rect)
            self.keysprites.add(key_obj)  # add the key sprite to the group
        print("piano len:", len(self.keysprites))
        # 添加手

        self.keysprites.add(self.rhand)
        self.keysprites.add(self.lhand)

        # draw the background on screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()                        # then flip it

        self.clock = pygame.time.Clock()  # create a pygame clock object

        self.pause = False

    def indexOf(self, n):
        index = nameof(n)
        if("#" in index):
            name = index[:2]
            octave = int(index[2:])
        else:
            name = index[:1]
            octave = int(index[1:])

        index = (octave-1) * 12 + nameOffset[name]
        return index

    def _moveHand(self, side, t):
        if(side == 1):
            engagedkeys = self.engagedkeysR
            engagedfingers = self.engagedfingersR
            H = self.rh
            hand = self.rhand
        else:
            engagedkeys = self.engagedkeysL
            engagedfingers = self.engagedfingersL
            H = self.lh
            hand = self.lhand

        # 释放按键
        for i, n in enumerate(H.noteseq):
            start, stop, f = n.time, n.time+n.duration, n.fingering
            if isinstance(f, str):
                continue
            # release key
            if f and stop <= t <= stop+self.dt and engagedkeys[i]:
                engagedkeys[i] = False
                engagedfingers[f] = False
                index = notes_index[nameof(n)]
                hand.release_finger(n.fingering-1)
                note_sounds[nameof(n)].fadeout(500)

                for keyobj in Key.keyobj_list:
                    if keyobj.keyevent == str(index):
                        keyobj.pressed = False

        # 按下按键
        for i, n in enumerate(H.noteseq):
            start, stop, f = n.time, n.time+n.duration, n.fingering
            if isinstance(f, str):
                print('Warning: cannot understand lyrics:', f, 'skip note', i)
                continue
            if f and start <= t < stop and not engagedkeys[i] and not engagedfingers[f]:
                # press key
                if i >= len(H.fingerseq):
                    return
                engagedkeys[i] = True
                engagedfingers[f] = True
                index = notes_index[nameof(n)]
                # move hand and control hand
                print("real:", n)
                print(nameof(n), notes_index[nameof(n)], n.fingering-1, piano_display[index])

                hand.press_finger(n.fingering-1)
                hand.move(n.fingering-1, notes_index[nameof(n)])
                note_sounds[nameof(n)].play()
                for keyobj in Key.keyobj_list:
                    if keyobj.keyevent == str(index):
                        keyobj.pressed = True

    def run(self, rh, lh, name="unknow"):

        # 显示当前播放的音乐
        ft = pygame.font.SysFont("Comic Sans MS", 30)
        self.play_text = ft.render(
            "♪ Playing: {} ♪".format(name), True, (123, 123, 123))
        self.play_text1 = ft.render('Enjoy it!', True, (123, 123, 123))
        text_rect = self.play_text.get_rect(center=(750, 450))
        img = pygame.image.load("images/playerrobot.png")
        img1=pygame.transform.scale(img, (200, 200))
        self.screen.blit(img1, (20, 390))
        self.screen.blit(self.play_text, (1000,520))
        self.screen.blit(self.play_text1, (250, 470))
        pygame.display.update()
        print("Starting Event loop")
        running = True
        self.rh = rh
        self.lh = lh
        self.dt = 0.05
        if(self.rh):
            self.engagedkeysR = [False]*len(self.rh.noteseq)
            self.engagedfingersR = [False]*6  # element 0 is dummy
        if(self.lh):
            self.engagedkeysL = [False]*len(self.lh.noteseq)
            self.engagedfingersL = [False]*6
        t = 0.0

        while running:

            if(not self.pause):
                # 控制手指和键盘的动作
                if(self.rh):
                    self._moveHand(1, t)
                if(self.lh):
                    self._moveHand(-1, t)
                t += self.dt
            else:
                pass

            # do not go faster than this framerate
            milliseconds = self.clock.tick(FPS)

            # handle pygame events -- if user closes game, stop running
            running = self.handlerEvents()

            # update our sprites
            for keysprite in self.keysprites:
                keysprite.update()

            self.keysprites.clear(self.screen, self.background)
            dirty = self.keysprites.draw(self.screen)

            pygame.display.update(dirty)

            # self.screen.blit(self.background, (0, 0))
            # self.lhand.display(self.screen)
            # self.rhand.display(self.screen)

            # print the framerate into the pygame window title
            pygame.display.set_caption(
                "FPS: {:.2f} Python Piano".format(self.clock.get_fps()))

        print("Good Bye!")
        sys.exit()

    def handlerEvents(self):
        # 相关事件
        # Event checker:
        for event in pygame.event.get():

            if event.type in (KEYDOWN, KEYUP):
                key = str(event.scancode)
                print(event)

            if event.type == QUIT:
                return False  # pygame window closed by user

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False  # user pressed ESC
                if event.key == K_SPACE:
                    self.pause = not self.pause

                if event.unicode in unicode_to_note.keys():
                    note = unicode_to_note[event.unicode]
                    note_sounds[note].play()
                    Key.keyobj_list[notes_index[note]].pressed = True

            elif event.type == KEYUP:
                if event.unicode in unicode_to_note.keys():
                    note = unicode_to_note[event.unicode]
                    note_sounds[note].fadeout(500)
                    Key.keyobj_list[notes_index[note]].pressed = False
        return True


if __name__ == "__main__":
    game = Game()
    game.run(None, None)
