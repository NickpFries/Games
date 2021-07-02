import random
from kivy.core.audio import SoundLoader
from kivy import platform
from kivy.core.image import ImageLoader
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder


Builder.load_file("menu.kv")


def is_desktop():
    if platform in ('linux', 'win', 'macosx'):
        return True
    else:
        return False


class MainWidget(RelativeLayout):
    from transforms import transform, transform_perspective
    from user_actions import on_keyboard_up, on_keyboard_down, on_touch_up, on_touch_down, keyboard_closed

    menu_widget = ObjectProperty()
    pause = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 8
    V_LINES_SPACING = 0.4  # percentage in screen width
    vertical_lines = []

    H_NB_LINES = 10
    H_LINES_SPACING = 0.1  # percentage in screen height
    horizontal_lines = []
    current_y_loop = 0

    START_SPEED = 4
    START_SPEED_X = 12.8
    SPEED = START_SPEED
    SPEED_x = START_SPEED_X
    current_offset_y = 0
    current_offset_x = 0
    current_speed_x = 0
    speed_inc = 0

    NB_TILES = 56
    gen_line = True
    gen_num = 0
    tiles = []
    tiles_coordinates = []

    # Ship variables
    ship = ObjectProperty()
    SHIP_WIDTH = 0.1
    SHIP_HEIGHT = 0.035
    SHIP_BASE = 0.04
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]
    ship_hb = [(0, 0), (0, 0)]

    state_game_over = False
    state_game_start = False
    state_game_paused = False
    score_txt = StringProperty("SCORE: 0")

    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")
    pause_txt = StringProperty("Pause")
    exit_txt = StringProperty("E X I T")

    sound_begin = None
    sound_galaxy = None
    sound_impact = None
    sound_voice = None
    sound_music1 = None
    sound_restart = None
    music_time = 0

    sensorEnabled = False
    tilt = StringProperty("0")

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W:" + str(self.width) + "H:" + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.pre_fill_tiles_coordinates()
        self.generate_land()
        self.init_ship()
        self.init_audio()

        # Enable or disable keyboard input
        if is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

        self.sound_galaxy.play()
        self.sound_music1.play()

    def reset_game(self):
        self.current_y_loop = 0
        self.current_offset_y = 0
        self.current_offset_x = 0
        self.current_speed_x = 0
        self.gen_num = 0
        self.gen_line = True
        self.SPEED = self.START_SPEED
        self.SPEED_x = self.START_SPEED_X

        self.tiles_coordinates = []
        self.pre_fill_tiles_coordinates()
        self.generate_land()

        self.state_game_over = False

    def init_audio(self):
        self.sound_begin = SoundLoader.load("assets/begin.wav")
        self.sound_galaxy = SoundLoader.load("assets/galaxy.wav")
        self.sound_impact = SoundLoader.load("assets/gameover_impact.wav")
        self.sound_voice = SoundLoader.load("assets/gameover_voice.wav")
        self.sound_music1 = SoundLoader.load("assets/music1.wav")
        self.sound_restart = SoundLoader.load("assets/restart.wav")
        self.sound_music1.volume = 1
        self.sound_begin.volume = .25
        self.sound_galaxy.volume = .25
        self.sound_voice.volume = .25
        self.sound_restart.volume = .25
        self.sound_impact.volume = .5

        self.sound_music1.loop = True
        pass
    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def init_ship(self):
        with self.canvas:
            Color(1, 0, 0, 1)
            self.ship = Triangle()

    def update_ship(self):
        ship_w = self.SHIP_WIDTH * self.width
        ship_h = self.SHIP_HEIGHT * self.height
        x1 = self.center_x - (ship_w / 2)
        y1 = self.SHIP_BASE * self.height
        x2 = x1 + ship_w / 2
        y2 = y1 + ship_h
        x3 = x1 + ship_w
        y3 = y1
        self.ship_coordinates[0] = (x1, y1)
        self.ship_coordinates[1] = (x2, y2)
        self.ship_coordinates[2] = (x3, y3)

        self.ship_hb[0] = (self.center_x, y1)
        self.ship_hb[1] = (self.center_x, y2)

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)

        for i in range(0, 2):
            ship_x, ship_y = self.ship_hb[i]
            if xmin <= ship_x <= xmax and ymin <= ship_y <= ymax:
                return True
        return False

    def pre_fill_tiles_coordinates(self):
        # starting tiles in straight line
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_land(self):
        # clean coordinates out of screen
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        # Generate Land
        while len(self.tiles_coordinates) < self.NB_TILES:
            if self.gen_num >= 60:
                self.gen_line = not self.gen_line
                self.gen_num = 0
            if self.gen_line:
                self.generate_tiles_coordinates()
            else:
                self.generate_tile_land()

    def generate_tile_land(self):

        last_y = 0
        last_x = 0
        left_isle = -int(self.V_NB_LINES / 2) + 1

        gen_all = True

        # take the next values of x, y from the previous tile
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_y = last_coordinates[1] + 1
            last_x = last_coordinates[0]

        # Generate tiles if there aren't enough already
        for i in range(len(self.tiles_coordinates), self.NB_TILES):

            # Start land off with two rows of all tile
            if self.gen_num < 2:
                for x in range(left_isle, left_isle + self.V_NB_LINES - 1):
                    self.tiles_coordinates.append((x, last_y))
                last_y += 1
                self.gen_num += 1

            # Begin generating random holes in land
            elif 2 <= self.gen_num < 56:

                # Randomly pick tiles to be holes
                r1 = random.randint(left_isle, left_isle + self.V_NB_LINES)
                if not gen_all:
                    r2 = random.randint(left_isle, left_isle + self.V_NB_LINES)
                    r3 = random.randint(left_isle, left_isle + self.V_NB_LINES)
                    while r2 == r1 + 1 or r2 == r1 - 1:
                        r2 = random.randint(left_isle, left_isle + self.V_NB_LINES)
                    while r3 == r2 + 1 or r3 == r2 - 1 or r3 == r1 - 1 or r3 == r1 + 1:
                        r3 = random.randint(left_isle, left_isle + self.V_NB_LINES)

                for x in range(left_isle+1, left_isle + self.V_NB_LINES - 2):

                    if (gen_all and not (x == r1)) or (not gen_all and (not (x == r1) and not (x == r2) and not (x == r3))):
                        self.tiles_coordinates.append((x, last_y))
                last_y += 1
                gen_all = not gen_all
                self.gen_num += 1

            # No more holes generate, narrow down the land back to single tile
            elif self.gen_num == 56:
                for x in range(left_isle+1, left_isle + self.V_NB_LINES-1):
                    self.tiles_coordinates.append((x, last_y))
                last_y += 1
                self.gen_num += 1
            elif self.gen_num == 57:
                for x in range(-2, 3):
                    self.tiles_coordinates.append((x, last_y))
                last_y += 1
                self.gen_num += 1
            elif self.gen_num == 58:
                for x in range(-1, 2):
                    self.tiles_coordinates.append((x, last_y))
                last_y += 1
                self.gen_num += 1
            elif self.gen_num == 59:
                self.tiles_coordinates.append((0, last_y))
                last_y += 1
                self.gen_num += 1

    def generate_tiles_coordinates(self):

        last_y = 0
        last_x = 0

        # take the next values of x, y from the previous tile
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_y = last_coordinates[1] + 1
            last_x = last_coordinates[0]

        # Generate tiles if there aren't enough already
        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            if self.gen_num < 60:
                self.tiles_coordinates.append((last_x, last_y))
                # Currently on far right path, can't shift right
                if last_x >= int(self.V_NB_LINES / 2 - 1):
                    r = random.randint(-1, 0)
                # Currently on far left path
                elif last_x <= -int(self.V_NB_LINES / 2) + 1:
                    r = random.randint(0, 1)
                # Not on either edge
                else:
                    r = random.randint(-1, 1)

                # right shift of path    #
                #                       ##
                if r == 1:
                    last_x += 1
                    self.tiles_coordinates.append((last_x, last_y))
                    last_y += 1
                    self.gen_num += 1
                    self.tiles_coordinates.append((last_x, last_y))
                # left shift of path    #
                #                       ##
                if r == -1:
                    last_x += -1
                    self.tiles_coordinates.append((last_x, last_y))
                    last_y += 1
                    self.gen_num += 1
                    self.tiles_coordinates.append((last_x, last_y))
                self.gen_num += 1
                last_y += 1

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_vertical_lines(self):
        start_index = -int(self.V_NB_LINES / 2) + 1
        for i in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        start_index = -int(self.V_NB_LINES / 2) + 1
        end_index = start_index + self.V_NB_LINES - 1
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)
            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update(self, dt):
        # print("dt: ", str(dt * 60))
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        if self.sensorEnabled:
            self.tilt = str(AccelerometerTest.get_acceleration(self, dt))

        # Game is running
        if not self.state_game_over and self.state_game_start and not self.state_game_paused:
            self.current_offset_y += self.SPEED * 0.001 * self.height * time_factor
            # self.current_offset_x += self.SPEED_x * time_factor

            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "SCORE: " + str(self.current_y_loop - 1)
                if self.speed_inc >= time_factor * 40:
                    self.speed_inc = 0
                    self.SPEED += 0.4
                    self.SPEED_x = self.SPEED * (self.START_SPEED_X / self.START_SPEED)
                    print("SPEED INCREASED")
                self.speed_inc += 1
                self.generate_land()

            self.current_offset_x += self.current_speed_x * self.width * 0.001 * time_factor

        # Ship Crashed
        if not self.check_ship_collision() and not self.state_game_over:
            self.sound_impact.play()
            self.sound_music1.stop()
            Clock.schedule_once(self.game_over_voice, 1)
            self.state_game_over = True
            self.menu_title = "G A M E    O V E R"
            self.menu_button_title = "RESTART"
            self.menu_widget.opacity = 1
            print("Game Over")

    def game_over_voice(self, dt):
        if self.state_game_over:
            self.sound_voice.play()

    def on_menu_button_pressed(self):
        self.reset_game()
        self.state_game_start = True
        self.menu_widget.opacity = 0
        if self.menu_button_title == "RESTART":
            self.sound_restart.play()
            self.sound_music1.play()
        else:
            self.sound_begin.play()

    def pause_pressed(self):
        if self.menu_widget.opacity == 0:
            self.state_game_paused = not self.state_game_paused
            if self.state_game_paused:
                self.music_time = self.sound_music1.get_pos()
                self.sound_music1.stop()
                self.pause_txt = "Resume"
            else:
                self.sound_music1.play()
                self.pause_txt = "Pause"


class GalaxyApp(App):
    pass


GalaxyApp().run()
