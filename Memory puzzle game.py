import os
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# Initialize sound system
try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("Sound disabled: Install pygame with 'pip install pygame'")

# File paths
HIGHSCORE_FILE = "highscore.json"
STATS_FILE = "stats.json"

THEMES = {
    "Emoji": ["🍎", "🚗", "🐶", "🌟", "🎵", "🏀", "🎲", "🍕", "📚", "✈️", "🎮", "👾", "💡", "🌈", "🎁", "⚽"],
    "Food": ["🍕", "🍔", "🍟", "🌮", "🍩", "🍓", "🍇", "🍉"],
    "Animal": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"],
    "Classic": ["A", "B", "C", "D", "E", "F", "G", "H"]
}

class MemoryGame:
    def __init__(self, root, theme, grid_size, time_limit, player_name):
        self.root = root
        self.theme = theme
        self.grid_size = grid_size
        self.time_limit = time_limit
        self.player_name = player_name
        self.score = 0
        self.high_score = self.load_high_score()
        self.stats = self.load_stats()
        self.timer_id = None

        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.flipped_cards = {}
        self.remaining_time = time_limit
        self.total_pairs = (grid_size * grid_size) // 2
        self.matched_pairs = 0

        self.style = ttk.Style()
        self.style.configure('Card.TButton', font=('Arial', 24), width=4, padding=20)

        self.setup_ui()
        self.create_board()
        self.start_timer()

    def load_high_score(self):
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, "r") as f:
                    scores = json.load(f)
                    return scores.get(self.player_name, 0)
        except:
            return 0
        return 0

    def load_stats(self):
        try:
            if os.path.exists(STATS_FILE):
                with open(STATS_FILE, "r") as f:
                    return json.load(f)
        except:
            pass
        return {"games_played": 0, "games_won": 0, "total_score": 0}

    def setup_ui(self):
        self.root.title(f"Memory Puzzle - {self.theme} Mode")
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(pady=10)

        ttk.Label(self.top_frame, text=f"Player: {self.player_name}").pack(side="left", padx=10)
        self.timer_label = ttk.Label(self.top_frame, text=f"Time Left: {self.remaining_time}")
        self.timer_label.pack(side="left", padx=10)
        self.score_label = ttk.Label(self.top_frame, text=f"Score: {self.score}")
        self.score_label.pack(side="left", padx=10)
        self.high_score_label = ttk.Label(self.top_frame, text=f"High Score: {self.high_score}")
        self.high_score_label.pack(side="left", padx=10)
        ttk.Button(self.top_frame, text="🔄 Restart", command=self.restart).pack(side="right", padx=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)
        self.progress["maximum"] = self.time_limit
        self.progress["value"] = self.time_limit

        # Create scrollable canvas
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def create_board(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        self.flipped_cards = {}
        self.first_card = None
        self.second_card = None
        self.score = 0
        self.matched_pairs = 0
        self.remaining_time = self.time_limit

        self.score_label.config(text=f"Score: {self.score}")
        self.progress["value"] = self.remaining_time
        self.timer_label.config(text=f"Time Left: {self.remaining_time}")

        symbols = THEMES.get(self.theme, THEMES["Emoji"])
        selected_symbols = random.sample(symbols, min(self.total_pairs, len(symbols)))
        pairs = selected_symbols * 2
        while len(pairs) < self.grid_size * self.grid_size:
            pairs += random.sample(selected_symbols, 1)
        pairs = pairs[:self.grid_size * self.grid_size]
        random.shuffle(pairs)

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                idx = i * self.grid_size + j
                btn = ttk.Button(
                    self.scrollable_frame,
                    text="",
                    style="Card.TButton",
                    command=lambda idx=idx: self.reveal_card(idx)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.flipped_cards[idx] = pairs[idx]
                row.append(btn)
            self.buttons.append(row)

    def reveal_card(self, idx):
        row = idx // self.grid_size
        col = idx % self.grid_size
        btn = self.buttons[row][col]
        if btn["text"] != "" or self.second_card:
            return
        btn.config(text=self.flipped_cards[idx])
        if not self.first_card:
            self.first_card = (idx, btn)
        else:
            self.second_card = (idx, btn)
            self.root.after(500, self.check_match)

    def check_match(self):
        idx1, btn1 = self.first_card
        idx2, btn2 = self.second_card

        if self.flipped_cards[idx1] == self.flipped_cards[idx2]:
            self.score += 10
            self.matched_pairs += 1
            btn1.config(state="disabled")
            btn2.config(state="disabled")
        else:
            btn1.config(text="")
            btn2.config(text="")

        self.score_label.config(text=f"Score: {self.score}")
        self.first_card = None
        self.second_card = None

        if self.matched_pairs == self.total_pairs:
            messagebox.showinfo("Congratulations!", "🎉 You Win! 🎉")
            self.root.destroy()

    def start_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.config(text=f"Time Left: {self.remaining_time}")
            self.progress["value"] = self.remaining_time
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            messagebox.showinfo("Time's up!", "⏱️ Time Over! Try Again.")
            self.root.destroy()

    def restart(self):
        self.create_board()
        self.start_timer()

def main():
    root = tk.Tk()
    root.geometry("900x700")  # Increased height for better space
    player_name = simpledialog.askstring("Player Name", "Enter your name:")
    if not player_name:
        root.destroy()
        return

    def start_game(theme, size, limit):
        for widget in root.winfo_children():
            widget.destroy()
        MemoryGame(root, theme, size, limit, player_name)

    menu_frame = ttk.Frame(root)
    menu_frame.pack(pady=20)

    ttk.Label(menu_frame, text="Choose Theme").pack()
    for theme in THEMES.keys():
        ttk.Button(menu_frame, text=theme, command=lambda t=theme: select_difficulty(t)).pack(pady=2)

    def select_difficulty(theme):
        for widget in root.winfo_children():
            widget.destroy()
        ttk.Label(root, text=f"{theme} - Select Difficulty").pack()
        difficulties = {
            "Very Easy": (2, 60),
            "Easy": (4, 90),
            "Medium": (6, 120),
            "Hard": (8, 150),
            "Insane": (10, 180)
        }
        for level, (size, time) in difficulties.items():
            ttk.Button(root, text=level, command=lambda s=size, t=time: start_game(theme, s, t)).pack(pady=2)

    root.mainloop()

if __name__ == "__main__":
    main()
