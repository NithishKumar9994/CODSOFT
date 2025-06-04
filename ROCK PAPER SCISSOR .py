import tkinter as tk
from tkinter import font, messagebox
import random
from PIL import Image, ImageTk

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Rock-Paper-Scissors")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")
        
        # Game variables
        self.user_score = 0
        self.computer_score = 0
        self.round = 1
        
        # Color scheme
        self.colors = {
            "bg": "#2b2b2b",
            "primary": "#6b8cff",
            "secondary": "#ff6b6b",
            "accent": "#a5d6a7",
            "text": "#ffffff",
            "button": "#4e5254"
        }
        
        # Load images (placeholder - replace with actual images if available)
        self.load_images()
        
        # Create UI
        self.create_widgets()
        
    def load_images(self):
        # Create colored circles as placeholders for game choices
        self.choice_images = {
            "rock": self.create_circle_image("#3498db"),
            "paper": self.create_circle_image("#e74c3c"),
            "scissors": self.create_circle_image("#2ecc71")
        }
        
        # Result emojis
        self.result_emojis = {
            "win": "🎉",
            "lose": "😢",
            "tie": "🤝"
        }
        
    def create_circle_image(self, color, size=150):
        """Create a circular placeholder image with the given color"""
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        return ImageTk.PhotoImage(img)
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["bg"])
        header_frame.pack(pady=20)
        
        tk.Label(
            header_frame,
            text="Rock-Paper-Scissors",
            font=("Arial", 32, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["primary"]
        ).pack()
        
        # Score display
        score_frame = tk.Frame(self.root, bg=self.colors["bg"])
        score_frame.pack(pady=10)
        
        self.user_score_label = tk.Label(
            score_frame,
            text=f"You: {self.user_score}",
            font=("Arial", 18),
            bg=self.colors["bg"],
            fg=self.colors["accent"]
        )
        self.user_score_label.pack(side=tk.LEFT, padx=20)
        
        self.round_label = tk.Label(
            score_frame,
            text=f"Round: {self.round}",
            font=("Arial", 18),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        self.round_label.pack(side=tk.LEFT, padx=20)
        
        self.computer_score_label = tk.Label(
            score_frame,
            text=f"Computer: {self.computer_score}",
            font=("Arial", 18),
            bg=self.colors["bg"],
            fg=self.colors["secondary"]
        )
        self.computer_score_label.pack(side=tk.LEFT, padx=20)
        
        # Game area
        game_frame = tk.Frame(self.root, bg=self.colors["bg"])
        game_frame.pack(pady=30)
        
        # User choice frame
        user_frame = tk.Frame(game_frame, bg=self.colors["bg"])
        user_frame.grid(row=0, column=0, padx=20)
        
        tk.Label(
            user_frame,
            text="Your Choice",
            font=("Arial", 16),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(pady=10)
        
        self.user_choice_label = tk.Label(
            user_frame,
            image=self.choice_images["rock"],
            bg=self.colors["bg"]
        )
        self.user_choice_label.pack()
        
        # VS label
        tk.Label(
            game_frame,
            text="VS",
            font=("Arial", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).grid(row=0, column=1, padx=20)
        
        # Computer choice frame
        computer_frame = tk.Frame(game_frame, bg=self.colors["bg"])
        computer_frame.grid(row=0, column=2, padx=20)
        
        tk.Label(
            computer_frame,
            text="Computer",
            font=("Arial", 16),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(pady=10)
        
        self.computer_choice_label = tk.Label(
            computer_frame,
            image=self.choice_images["rock"],
            bg=self.colors["bg"]
        )
        self.computer_choice_label.pack()
        
        # Result display
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 24),
            bg=self.colors["bg"],
            fg=self.colors["primary"]
        )
        self.result_label.pack(pady=20)
        
        # Choice buttons
        button_frame = tk.Frame(self.root, bg=self.colors["bg"])
        button_frame.pack(pady=20)
        
        choices = ["rock", "paper", "scissors"]
        for choice in choices:
            btn = tk.Button(
                button_frame,
                text=choice.capitalize(),
                font=("Arial", 14, "bold"),
                bg=self.colors["button"],
                fg=self.colors["text"],
                padx=20,
                pady=10,
                bd=0,
                command=lambda c=choice: self.play_round(c)
            )
            btn.pack(side=tk.LEFT, padx=10)
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["primary"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["button"]))
        
        # Play again button (initially hidden)
        self.play_again_button = tk.Button(
            self.root,
            text="Play Again?",
            font=("Arial", 14, "bold"),
            bg=self.colors["accent"],
            fg="#000000",
            padx=20,
            pady=10,
            bd=0,
            command=self.reset_game
        )
        self.play_again_button.pack(pady=10)
        self.play_again_button.pack_forget()
        
        # Instructions
        tk.Label(
            self.root,
            text="Choose rock, paper, or scissors to play!",
            font=("Arial", 12),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(pady=20)
        
    def play_round(self, user_choice):
        # Update user choice display
        self.user_choice_label.config(image=self.choice_images[user_choice])
        
        # Computer makes random choice
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)
        self.computer_choice_label.config(image=self.choice_images[computer_choice])
        
        # Determine winner
        if user_choice == computer_choice:
            result = "tie"
            message = "It's a tie!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            result = "win"
            self.user_score += 1
            message = "You win!"
        else:
            result = "lose"
            self.computer_score += 1
            message = "Computer wins!"
        
        # Update UI
        self.round += 1
        self.update_scores()
        
        # Show result with emoji
        self.result_label.config(
            text=f"{message} {self.result_emojis[result]}",
            fg=self.colors["accent"] if result == "win" else 
               self.colors["secondary"] if result == "lose" else 
               self.colors["primary"]
        )
        
        # Show play again button
        self.play_again_button.pack()
        
    def update_scores(self):
        self.user_score_label.config(text=f"You: {self.user_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        self.round_label.config(text=f"Round: {self.round}")
        
    def reset_game(self):
        self.user_choice_label.config(image=self.choice_images["rock"])
        self.computer_choice_label.config(image=self.choice_images["rock"])
        self.result_label.config(text="")
        self.play_again_button.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissors(root)
    root.mainloop()