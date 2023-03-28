class Portal:
    location: int = 0
    x: int = 0
    y: int = 0
    z: int = 0
    dest: int = 0
    dest_x: int = 0
    dest_y: int = 0
    dest_z: int = 0

    def __init__(self, location: int=0, x: int=0, y: int=0, z: int=0, dest: int=0, dest_x: int=0, dest_y: int=0, dest_z: int=0):
        self.location = location
        self.x = x
        self.y = y
        self.z = z
        self.dest = dest
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.dest_z = dest_z

    def __str__(self) -> str:
        return f"{self.location} ({self.x},{self.y},{self.z}) -> {self.dest} ({self.dest_x},{self.dest_y},{self.dest_z})"
