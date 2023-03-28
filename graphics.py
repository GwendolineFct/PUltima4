
from pygame import Color, Surface

from options import Options
from file_io import read_file
from lzw import lzw_decompress



class TileSet:
    tile_width: int
    tile_height: int
    surface: Surface

    def __init__(self, tile_width, tile_height) -> None:
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.surface = Surface((tile_width, 256 * tile_height))

    def __getitem__(self, tile_no: int) -> Surface:
        offset = tile_no * self.tile_height
        return self.surface.subsurface((0, offset, self.tile_width, self.tile_height))

    def draw_tile(self, surface: Surface, x: int, y, tile_no: int) -> None:
        offset = tile_no * self.tile_height
        surface.blit(self.surface, (x,y), (0, offset, self.tile_width, self.tile_height))

class CharSet(TileSet):
    char_width: int
    char_height: int

    def __init__(self) -> None:
        super().__init__(8, 8)
        self.char_width = self.tile_width
        self.char_height = self.tile_height

    def draw_char(self, surface: Surface, x: int, y: int, char) -> None:
        if isinstance(char, str):
            char = ord(char[0])
        self.draw_tile(surface, x, y, char)

class Shapes(TileSet):
    _temp: Surface
    _elapsed_time: 0

    def __init__(self) -> None:
        super().__init__(16, 16)
        self._temp = Surface((16, 16))
        self._elapsed_time = 0

    def animate(self, elapsed_time) -> None:
        self._elapsed_time += elapsed_time
        while self._elapsed_time >= 125:
            self._elapsed_time -= 125
            for i in (0, 1, 2, 68, 69, 70, 71):
                self._scroll_shape(i)

    def draw_shape(self, surface: Surface, x: int, y: int, shape_no: int) -> None:
        self.draw_tile(surface, x, y, shape_no)

    def _scroll_shape(self, tile_no: int) -> None:
        offset = tile_no * self.tile_height
        self._temp.blit(self.surface, (0,1), (0, offset, self.tile_width, self.tile_height-1))
        self._temp.blit(self.surface, (0,0), (0, offset+self.tile_height-1, self.tile_width, 1))
        self.surface.blit(self._temp, (0, offset))


charset: CharSet = None
shapes: Shapes = None

CGA_PALETTE = [
    Color("0x000000"), # Black
    Color("0x00AAAA"), # Cyan
    Color("0xAA00AA"), # Magenta
    Color("0xAAAAAA"), # Grey
]

EGA_PALETTE = [
    Color("0x000000"), # Black
    Color("0x0000AA"), # Blue
    Color("0x00AA00"), # Green
    Color("0x00AAAA"), # Cyan
    Color("0xAA0000"), # Red
    Color("0xAA00AA"), # Magenta
    Color("0xAA5500"), # Brown
    Color("0xAAAAAA"), # Light gray
    Color("0x555555"), # Dark gray
    Color("0x5555FF"), # Bright blue
    Color("0x55FF55"), # Bright green
    Color("0x55FFFF"), # Bright cyan
    Color("0xFF5555"), # Bright red
    Color("0xFF55FF"), # Bright magenta
    Color("0xFFFF55"), # Bright yellow
    Color("0xFFFFFF"), # White
]

VGA_PALETTE = [ Color ] * 256


def gfx_init():
    global charset, shapes
    gfx_load_vga_palette()
    charset = gfx_load_charset()
    shapes = gfx_load_shapes()

def gfx_draw_tile(surface: Surface, x: int, y: int, shape_no: int):
    global shapes
    shapes.draw_shape(surface, x, y, shape_no)

def gfx_draw_char(surface: Surface, x: int, y: int, char: int):
    global charset
    if isinstance(char, str):
        char = ord(char[0])
    char &= 0x7f
    charset.draw_tile(surface, x, y, char)

def gfx_draw_string(surface, x, y, string:str):
    global charset
    start_x = x
    newline = chr(0x0A)
    for c in string:
        if c == newline:
            x = start_x
            y += charset.char_height
        else:
            charset.draw_char(surface, x, y, c)
            x += charset.char_width

def gfx_animate_shapes(elapsed_time: int):
    global shapes
    shapes.animate(elapsed_time)

def gfx_load_rle_image(filename: str) -> Surface:
    if Options.mode == "VGA":
        return gfx_load_rle_vga_image(filename.upper())
    return gfx_load_rle_ega_image(filename.upper())

def gfx_load_rle_ega_image(filename: str) -> Surface:
    buffer = read_file(f"{filename}.EGA")
    surface = Surface((320, 200))
    offset = 0
    x = 0
    y = 0
    end = len(buffer)
    while offset < end:
        n = 1
        c = buffer[offset] & 0xFF
        offset += 1
        if c == 0x02:
            n = buffer[offset] & 0xFF
            offset += 1
            c = buffer[offset] & 0xFF
            offset += 1
        c1 = EGA_PALETTE[c // 16]
        c2 = EGA_PALETTE[c % 16]
        for _ in range(n):
            surface.set_at((x ,y), c1)
            x += 1
            surface.set_at((x ,y), c2)
            x += 1
            if x >= 320:
                y += 1
                x = 0

    return surface

def gfx_load_rle_ega_image(filename: str) -> Surface:
    buffer = read_file(f"{filename}.EGA")
    surface = Surface((320, 200))
    offset = 0
    x = 0
    y = 0
    end = len(buffer)
    while offset < end:
        n = 1
        c = buffer[offset] & 0xFF
        offset += 1
        if c == 0x02:
            n = buffer[offset] & 0xFF
            offset += 1
            c = buffer[offset] & 0xFF
            offset += 1
        c1 = EGA_PALETTE[c // 16]
        c2 = EGA_PALETTE[c % 16]
        for _ in range(n):
            surface.set_at((x ,y), c1)
            x += 1
            surface.set_at((x ,y), c2)
            x += 1
            if x >= 320:
                y += 1
                x = 0

    return surface

def gfx_load_rle_vga_image(filename: str) -> Surface:
    buffer = read_file(f"{filename}.VGA")
    surface = Surface((320, 200))
    offset = 0
    x = 0
    y = 0
    end = len(buffer)
    while offset < end:
        c = buffer[offset] & 0xFF
        offset += 1
        if c == 0x02:
            n = buffer[offset] & 0xFF
            offset += 1
            c = buffer[offset] & 0xFF
            offset += 1
        else:
            n = 1
        c = VGA_PALETTE[c]
        for _ in range(n):
            surface.set_at((x ,y), c)
            x += 1
            if x == 320:
                y += 1
                x = 0
    return surface

def gfx_load_lzw_image(filename) -> Surface:
    buffer = read_file(f"{filename.upper()}.EGA")
    buffer = lzw_decompress(buffer)
    surface = Surface((320, 200))
    x = 0
    y = 0
    for byte in buffer:
        surface.set_at((x,y), EGA_PALETTE[byte // 16])
        x += 1
        surface.set_at((x,y), EGA_PALETTE[byte % 16])
        x += 1
        if x >= 320:
            y += 1
            x = 0
    return surface

def gfx_load_vga_palette():
    buffer = read_file("U4VGA.PAL")
    pointer = 0
    for c in range(0, 256):
        r = (buffer[pointer+0] << 2) & 0xFF
        g = (buffer[pointer+1] << 2) & 0xFF
        b = (buffer[pointer+2] << 2) & 0xFF
        VGA_PALETTE[c] =  Color(r,g,b)
        pointer += 3


def gfx_load_charset() -> CharSet:
    if Options.mode == "VGA":
        return gfx_load_vga_charset()
    return gfx_load_ega_charset()

def gfx_load_shapes() -> Shapes:
    if Options.mode == "VGA":
        return gfx_load_vga_shapes()
    return gfx_load_ega_shapes()

def gfx_load_ega_charset() -> CharSet:
    charset = CharSet()
    buffer = read_file("CHARSET.EGA")
    pointer = 0
    y = 0
    x = 0
    for c in range(0, 128):
        for _ in range(0, 8):
            x = 0
            for _ in range(0, 4):
                byte = buffer[pointer]
                pointer += 1
                charset.surface.set_at((x,y), EGA_PALETTE[byte // 16])
                x += 1
                charset.surface.set_at((x,y), EGA_PALETTE[byte % 16])
                x += 1
            y += 1
    return charset

def gfx_load_vga_charset() -> CharSet:
    charset = CharSet()
    buffer = read_file("CHARSET.VGA")
    pointer = 0
    y = 0
    x = 0
    for c in range(0, 128):
        for _ in range(0, 8):
            x = 0
            for _ in range(0, 8):
                byte = buffer[pointer]
                pointer += 1
                charset.surface.set_at((x,y), VGA_PALETTE[byte])
                x += 1
            y += 1
    return charset

def gfx_load_ega_shapes() -> Shapes:
    shapeset = Shapes()
    buffer = read_file("SHAPES.EGA")
    pointer = 0
    y = 0
    x = 0
    for c in range(0, 256):
        for _ in range(0, 16):
            x = 0
            for _ in range(0, 8):
                byte = buffer[pointer]
                pointer += 1
                shapeset.surface.set_at((x,y), EGA_PALETTE[byte // 16])
                x += 1
                shapeset.surface.set_at((x,y), EGA_PALETTE[byte % 16])
                x += 1
            y += 1
    return shapeset

def gfx_load_vga_shapes() -> Shapes:
    shapeset = Shapes()
    buffer = read_file("SHAPES.VGA")
    pointer = 0
    y = 0
    x = 0
    for c in range(0, 256):
        for _ in range(0, 16):
            x = 0
            for _ in range(0, 16):
                byte = buffer[pointer]
                pointer += 1
                shapeset.surface.set_at((x,y), VGA_PALETTE[byte])
                x += 1
            y += 1
    return shapeset

