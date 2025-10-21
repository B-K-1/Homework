import tkinter as tk
import random
import copy
class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = [[0.0 for _ in range(size)] for _ in range(size)]

    def train(self, patterns):
        for p in patterns:
            for i in range(self.size):
                for j in range(self.size):
                    if i != j:
                        self.weights[i][j] += p[i] * p[j]
        for i in range(self.size):
            for j in range(self.size):
                self.weights[i][j] /= len(patterns)

    def update(self, state, max_iter=100):
        state = state[:]
        for _ in range(max_iter):
            prev_state = state[:]
            for i in range(self.size):
                s = sum(self.weights[i][j] * state[j] for j in range(self.size))
                state[i] = 1 if s >= 0 else -1
            if state == prev_state:
                break
        return state

def pattern_to_grid(pattern):
    grid = []
    for i in range(5):
        row = []
        for j in range(5):
            row.append(pattern[i * 5 + j])
        grid.append(row)
    return grid

def grid_to_pattern(grid):
    pattern = []
    for row in grid:
        pattern.extend(row)
    return pattern

def add_noise(pattern, noise_level=0.2):
    noisy = pattern[:]
    for i in range(len(noisy)):
        if random.random() < noise_level:
            noisy[i] *= -1
    return noisy

PATTERNS = [
    # 'X'
    [1, -1, -1, -1, 1,
     -1, 1, -1, 1, -1,
     -1, -1, 1, -1, -1,
     -1, 1, -1, 1, -1,
     1, -1, -1, -1, 1],

    # 'O'
    [1, 1, 1, 1, 1,
     1, -1, -1, -1, 1,
     1, -1, -1, -1, 1,
     1, -1, -1, -1, 1,
     1, 1, 1, 1, 1],

    # '+'
    [-1, -1, 1, -1, -1,
     -1, -1, 1, -1, -1,
     1, 1, 1, 1, 1,
     -1, -1, 1, -1, -1,
     -1, -1, 1, -1, -1],
]
class HopfieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сеть Хопфилда (5x5)")
        self.size = 25
        self.grid_size = 5
        self.cell_size = 40

        self.network = HopfieldNetwork(self.size)
        self.network.train(PATTERNS)

        self.current_state = [1] * self.size

        self.canvas = tk.Canvas(root, width=self.grid_size * self.cell_size,
                                height=self.grid_size * self.cell_size, bg='white')
        self.canvas.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Образец X", command=lambda: self.set_pattern(PATTERNS[0])).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Образец O", command=lambda: self.set_pattern(PATTERNS[1])).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Образец +", command=lambda: self.set_pattern(PATTERNS[2])).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Добавить шум", command=self.add_noise_to_current).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Восстановить", command=self.restore).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=5)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        grid = pattern_to_grid(self.current_state)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = 'black' if grid[i][j] == 1 else 'white'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

    def set_pattern(self, pattern):
        self.current_state = pattern[:]
        self.draw_grid()

    def add_noise_to_current(self):
        self.current_state = add_noise(self.current_state, noise_level=0.3)
        self.draw_grid()

    def restore(self):
        restored = self.network.update(self.current_state)
        self.current_state = restored
        self.draw_grid()

    def clear(self):
        self.current_state = [-1] * self.size
        self.draw_grid()

    def on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        idx = row * self.grid_size + col
        if 0 <= idx < self.size:
            self.current_state[idx] *= -1
            self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = HopfieldApp(root)
    root.mainloop()
