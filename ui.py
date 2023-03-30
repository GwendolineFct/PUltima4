
import graphics
from pygame import Surface
from graphics import gfx_draw_char


class TextArea():
    def __init__(self, width, height):
        self.buffer = [0] * (width * height)
        self.width = width
        self.height = height
        self.cursor = 28
        self.cursor_x = 0
        self.cursor_y = 0
        self.reversed = False
        self.attributes = 0
        self.clear()

    def reverse(self, reversed):
        self.reversed = bool(reversed)
        if self.reversed:
            self.attributes |= 256
        else:
            self.attributes &= ~256
        return self

    def clear(self):
        c = int(32 + self.attributes)
        self.buffer = [c] * (self.width * self.height)
        self.cursor_x = 0
        self.cursor_y = 0
        return self

    def scroll(self):
        dest = 0
        src = self.width
        for y in range(1, self.height):
            self.buffer[dest:dest+self.width] = self.buffer[src:src+self.width]
            dest = src
            src += self.width
        c = int(32 + self.attributes)
        self.buffer[dest:dest+self.width] = [c] * self.width
        return self

    def print(self, what):
        if isinstance(what, int):
            self.print(chr(what))
        for char in what:
            if char == '\n':
                self.newline()
                continue
            c = ord(char) % 256 + self.attributes
            self.buffer[self.cursor_x + self.cursor_y * self.width] = c
            self.cursor_x += 1
            if self.cursor_x == self.width:
                self.cursor_x = 0
                self.cursor_y += 1
                if self.cursor_y == self.height:
                    self.scroll()
                    self.cursor_y -= 1
        return self

    def newline(self):
        c = int(32 + self.attributes)
        while self.cursor_x < self.width:
            self.buffer[self.cursor_x + self.cursor_y * self.width] = c
            self.cursor_x += 1
        self.cursor_x = 0
        self.cursor_y += 1
        if self.cursor_y == self.height:
            self.scroll()
            self.cursor_y -= 1
        return self

    def render(self, surface: Surface, x: int, y: int):
        ptr = 0
        dy = y
        for _ in range(self.height):
            dx = x
            for _ in range(self.width):
                c = self.buffer[ptr] & 255
                gfx_draw_char(surface, dx, dy, c)
                ptr += 1
                dx += graphics.charset.char_width
            dy += graphics.charset.char_height

class Console(TextArea):

    def __init__(self, width, height):
        TextArea.__init__(self, width, height)
        self.prompt_x = 0
        self.prompt_y = 0
        self.showing_cursor = False

    def backspace(self):
        if self.cursor_x != self.prompt_x or self.cursor_y != self.prompt_y:
            if self.cursor_x > 0:
                self.cursor_x -= 1
            else:
                self.cursor_x = self.width - 1
                self.cursor_y -= 1
        return self

    def scroll(self):
        super().scroll()
        if self.prompt_y > 0:
            self.prompt_y -= 0
        return self

    def prompt(self):
        self.prompt_x = self.cursor_x
        self.prompt_y = self.cursor_y
        self.showing_cursor = True
        return self

    def hide_cursor(self):
        self.showing_cursor = False
        return self

    def animate(self):
        self.cursor -= 1
        if self.cursor >= 32:
            self.cursor = 28
        elif self.cursor < 28:
            self.cursor = 31

    def render(self, surface: Surface, x: int, y: int):
        super().render(surface, x, y)
        if self.showing_cursor:
            dx = x + self.cursor_x * graphics.charset.char_width
            dy = y + self.cursor_y * graphics.charset.char_height
            gfx_draw_char(surface, dx, dy, self.cursor)
