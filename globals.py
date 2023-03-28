from file_io import DosFile

class AvatarExe:
    ult_filenames: list[str]
    stone_colors: list[str]
    dng_filenames: list[str]
    location_names: list[str]
    locations_x: list[int]
    locations_y: list[int]
    walkable_tiles: list[int]

    def __init__(self) -> None:
        bin = DosFile("AVATAR.EXE")
        print(bin.get_sha256())
        self.ult_filenames = bin.read_n_asciiz(16, 0x0f97f)
        self.stone_colors = bin.read_n_asciiz(16, 0x0fa2a)
        self.dng_filenames = bin.read_n_asciiz(16, 0x0fa5a)
        self.location_names = bin.read_n_asciiz(32, 0x1101e)
        self.locations_x = bin.read_n_bytes(32, 0x0fb01)
        self.locations_y = bin.read_n_bytes(32, 0x0fb21)
        self.walkable_tiles = bin.read_n_bytes(37, 0x0fbc1)

avatar_exe: AvatarExe = None

def load_avatar_exe():
    global avatar_exe

    avatar_exe = AvatarExe()
