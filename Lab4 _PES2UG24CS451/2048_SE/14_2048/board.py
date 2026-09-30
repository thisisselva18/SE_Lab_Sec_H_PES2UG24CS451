import random

SIZE = 4
WIN_TILE = 2048


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def slide_line(line):
        """Compress a line towards index 0, merging equal neighbours.

        Each original tile takes part in at most one merge, so a tile
        created by a merge cannot merge again in the same move.
        Returns (new_line, points) where points is the sum of merged tiles.
        """
        values = [x for x in line if x]
        result = []
        points = 0
        i = 0
        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                result.append(values[i] * 2)
                points += values[i] * 2
                i += 2  # both original tiles are consumed by this merge
            else:
                result.append(values[i])
                i += 1
        return result + [0] * (SIZE - len(result)), points

    def move_left(self):
        changed = False
        for r in range(SIZE):
            old = self.grid[r][:]
            self.grid[r], points = self.slide_line(old)
            self.score += points
            changed |= old != self.grid[r]
        return changed

    def move_right(self):
        changed = False
        for r in range(SIZE):
            old = self.grid[r][:]
            new, points = self.slide_line(list(reversed(old)))
            self.grid[r] = list(reversed(new))
            self.score += points
            changed |= old != self.grid[r]
        return changed

    def move_up(self):
        changed = False
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, points = self.slide_line(old)
            self.score += points
            for r in range(SIZE):
                self.grid[r][c] = new[r]
            changed |= old != new
        return changed

    def move_down(self):
        changed = False
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, points = self.slide_line(list(reversed(old)))
            new = list(reversed(new))
            self.score += points
            for r in range(SIZE):
                self.grid[r][c] = new[r]
            changed |= old != new
        return changed

    def has_won(self):
        return any(x >= WIN_TILE for row in self.grid for x in row)

    def can_move(self):
        """Read-only check: is there an empty cell or an adjacent equal pair?"""
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False
