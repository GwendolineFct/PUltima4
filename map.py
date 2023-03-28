import globals
from constants import *
from file_io import read_file

class Mobile: ...
class Map: ...

class Mobile:
    x: int
    y: int
    z: int
    tile: int
    behaviour: int
    convIndex: int

    def __init__(self, tile=-1, x=0, y=0, z=0, behaviour=-1, convIndex = -1):
        self.tile = tile
        self.x = x
        self.y = y
        self.z = z
        self.behaviour = behaviour
        self.convIndex = convIndex

    def can_move(self, dx: int, dy: int, map: Map, exclude_pos: list[tuple[int]] = []):
        tx = self.x + dx
        ty = self.y + dy

        if (tx, ty, self.z) in exclude_pos:
            return False
        dest_tile = map[(tx, ty, self.z)]
        if not (tx, ty) in map:
            return False

        for mobile in map.mobiles:
            if mobile.x == tx and mobile.y == ty and mobile.z == self.z:
                return False

        if TILE_GHOST_1 <= self.tile <= TILE_GHOST_4 or TILE_PHANTOM_1 <= self.tile <= TILE_PHANTOM_4:
            return True

        if TILE_PIRATE_SHIP_WEST <= self.tile <= TILE_PIRATE_SHIP_SOUTH:
            return dest_tile <= TILE_MEDIUM_WATER
        if TILE_NIXIE_1 <= self.tile <= TILE_STORM_2:
            return dest_tile <= TILE_SHALLOW_WATER

        if dest_tile in (TILE_TOWN, TILE_VILLAGE, TILE_CASTLE, TILE_SHRINE, TILE_LCB_WEST, TILE_LCB_EAST, TILE_LCB_ENTRANCE, TILE_RUINS, TILE_MOONGATE_1, TILE_MOONGATE_2, TILE_MOONGATE_3, TILE_MOONGATE_4):
            return False

        if dest_tile in globals.avatar_exe.walkable_tiles:
            return True

        if TILE_DRAGON_1 <= self.tile and dest_tile <= TILE_SHALLOW_WATER:
            return True

        return False

class Map:

    width: int
    height: int
    depth: int
    wraps: bool
    default_tile: int
    tiles: bytes
    width_height: int
    mobiles: list[Mobile]

    def __init__(self, width: int, height: int, depth: int, tiles: bytes, wraps: bool, default_tile: int) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.wraps = wraps
        self.tiles = tiles
        self.default_tile = default_tile
        self.width_height = width * height
        self.mobiles = [Mobile() for _ in range(32)]

    def __contains__(self, pos: tuple) -> bool:
        x = pos[0]
        y = pos[1]
        z = pos[2] if len(pos) > 2 else 0
        if self.wraps:
            x %= self.width
            y %= self.height
        return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.height

    def __getitem__(self, pos: tuple) -> int:
        x = pos[0]
        y = pos[1]
        z = pos[2] if len(pos) > 2 else 0
        if self.wraps:
            x = (x + self.width) % self.width
            y = (y + self.height) % self.height
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.height:
            offset = x+y*self.width+z*self.width_height
            return self.tiles[offset]
        return self.default_tile

    def __setitem__(self, pos: tuple, tile: int) -> None:
        x = pos[0]
        y = pos[1]
        z = pos[2] if len(pos) > 2 else 0
        if self.wraps:
            x = (x + self.width) % self.width
            y = (z + self.height) % self.height
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.height:
            self.tiles[x+y*self.width+z*self.width_depth] = tile


class WorldMap(Map):
    def __init__(self) -> None:
        data = read_file("WORLD.MAP")
        tiles = [0] * (256*256)
        offset = 0
        for chunk in range(64):
            x = 32 * (chunk % 8)
            y = 32 * (chunk // 8)
            map_offset = x + 256 * y
            for _ in range(32):
                line = data[offset:offset+32]
                tiles[map_offset:map_offset+32] = line
                map_offset += 256
                offset += 32
        super().__init__(256, 256, 1, tiles, True, 0)

class TownMap(Map):
    def __init__(self, filename: str):
        temp = read_file(f"{filename}")
        super().__init__(32, 32, 1, temp[0:1024], False, TILE_GRASSLANDS)
        for n in range(32):
            self.mobiles[n] = Mobile()
            self.mobiles[n].tile = temp[0x400+n]
            self.mobiles[n].x = temp[0x420+n]
            self.mobiles[n].y = temp[0x440+n]
            self.mobiles[n].behaviour = temp[0x4C0+n]
            self.mobiles[n].convIndex = temp[0x4E0+n]
            if self.mobiles[n].tile == 0:
                 self.mobiles[n].tile = -1



