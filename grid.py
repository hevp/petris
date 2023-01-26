from dataclasses import dataclass

@dataclass
class Grid:
    width: int
    height: int

    def __post_init__(self):
        self._data = [0] * self.width * self.height

    def get(self, x, y):
        return self._data[y * self.width + x]

    def set(self, x, y, c):
        self._data[y * self.width + x] = c

    def nonzero(self):
        for i, c in enumerate(self._data):
            if c > 0:
                yield (i % self.width, i // self.width, c)

    def full(self, i):
        return 0 not in self._data[i * self.width:(i + 1) * self.width]

    def intersects(self, x, y, coords):
        for i, j in coords:
            u, v = x + i, y + j
            if not (0 <= u < self.width) or not (0 <= v < self.height) or self.get(u, v) > 0:
                return True

        return False

    def burn(self, x, y, coords, c):
        for i, j in coords:
            self.set(x + i, y + j, c)

    def _move_lines(self, s, i):
        dy = (i - s)
        self._data[dy * self.width:i * self.width] = self._data[0:s * self.width]
        self._data[0:dy * self.width] = [0] * dy * self.width
        return dy

    def break_lines(self):
        s, lines = -1, 0
        for i in range(self.height):
            if self.full(i):
                s = i if s == -1 else s
            elif s >= 0:
                lines += self._move_lines(s, i)
                s = -1

        if s >= 0:
            self._move_lines(s, 20)

        return lines
