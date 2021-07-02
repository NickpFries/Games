from kivy.uix.relativelayout import RelativeLayout
from plyer import accelerometer


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.current_speed_x = self.SPEED_x
    elif keycode[1] == 'right':
        self.current_speed_x = -self.SPEED_x
    return True


def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0
    return True


def on_touch_down(self, touch):
    if not self.state_game_over and self.state_game_start and not self.state_game_paused:
        if touch.x < self.width / 2:
            self.current_speed_x = self.SPEED_x
        else:
            self.current_speed_x = self.SPEED_x * -1
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch):
    self.current_speed_x = 0
    return True


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_down=self.on_keyboard_up)
    self._keyboard = None
