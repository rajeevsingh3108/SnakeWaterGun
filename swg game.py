import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from threading import Thread
import pygame

try:
    pygame.mixer.init()
    SOUND_ENABLED = True
except:
    SOUND_ENABLED = False
    print("Pygame not available - running without sound")

class SnakeWaterGunGame:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.init_game_state()
        self.create_widgets()
        self.animate_title()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🐍 Snake Water Gun - Epic Battle 🔫")
        self.root.geometry("800x700")
        self.root.configure(bg="#2C1810")
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
        
    def init_game_state(self):
        """Initialize game variables"""
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1
        self.game_history = []
        
        self.choices = {
            'snake': {'emoji': '🐍', 'beats': 'water', 'name': 'Snake', 'color': '#4ADE80'},
            'water': {'emoji': '💧', 'beats': 'gun', 'name': 'Water', 'color': '#3B82F6'},
            'gun': {'emoji': '🔫', 'beats': 'snake', 'name': 'Gun', 'color': '#EF4444'}
        }
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container with gradient-like effect
        main_frame = tk.Frame(self.root, bg="#1A1A2E", relief="raised", bd=2)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title with animation placeholder
        self.title_label = tk.Label(
            main_frame,
            text="🐍 SNAKE WATER GUN 🔫",
            font=("Arial", 28, "bold"),
            fg="#FFD700",
            bg="#1A1A2E",
            pady=20
        )
        self.title_label.pack()
        
        # Game rules
        rules_frame = tk.Frame(main_frame, bg="#16213E", relief="groove", bd=2)
        rules_frame.pack(fill="x", padx=20, pady=10)
        
        rules_label = tk.Label(
            rules_frame,
            text="🐍 Snake drinks Water 💧 | 💧 Water extinguishes Gun 🔫 | 🔫 Gun shoots Snake 🐍",
            font=("Arial", 12),
            fg="#E94560",
            bg="#16213E",
            pady=10
        )
        rules_label.pack()
        
        # Score and Round Display
        stats_frame = tk.Frame(main_frame, bg="#1A1A2E")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Round counter
        self.round_label = tk.Label(
            stats_frame,
            text="Round: 1",
            font=("Arial", 14, "bold"),
            fg="#FFD700",
            bg="#0F3460",
            relief="raised",
            bd=2,
            padx=20,
            pady=5
        )
        self.round_label.pack(pady=5)
        
        # Score display
        score_frame = tk.Frame(stats_frame, bg="#1A1A2E")
        score_frame.pack(fill="x")
        
        # Player score
        player_frame = tk.Frame(score_frame, bg="#16213E", relief="groove", bd=2)
        player_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Label(player_frame, text="YOU", font=("Arial", 12, "bold"), 
                fg="#4ADE80", bg="#16213E").pack(pady=5)
        self.player_score_label = tk.Label(
            player_frame, text="0", font=("Arial", 24, "bold"),
            fg="#4ADE80", bg="#16213E"
        )
        self.player_score_label.pack(pady=5)
        
        # Computer score
        computer_frame = tk.Frame(score_frame, bg="#16213E", relief="groove", bd=2)
        computer_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        tk.Label(computer_frame, text="COMPUTER", font=("Arial", 12, "bold"),
                fg="#EF4444", bg="#16213E").pack(pady=5)
        self.computer_score_label = tk.Label(
            computer_frame, text="0", font=("Arial", 24, "bold"),
            fg="#EF4444", bg="#16213E"
        )
        self.computer_score_label.pack(pady=5)
        
        # Battle Arena
        battle_frame = tk.Frame(main_frame, bg="#0F3460", relief="groove", bd=3)
        battle_frame.pack(fill="x", padx=20, pady=20)
        
        arena_label = tk.Label(
            battle_frame, text="⚔️ BATTLE ARENA ⚔️",
            font=("Arial", 16, "bold"), fg="#FFD700", bg="#0F3460", pady=10
        )
        arena_label.pack()
        
        choices_display_frame = tk.Frame(battle_frame, bg="#0F3460")
        choices_display_frame.pack(pady=10)
        
        # Player choice display
        self.player_choice_label = tk.Label(
            choices_display_frame, text="❓", font=("Arial", 48),
            fg="#4ADE80", bg="#0F3460", width=3
        )
        self.player_choice_label.pack(side="left", padx=20)
        
        # VS label
        tk.Label(choices_display_frame, text="VS", font=("Arial", 20, "bold"),
                fg="#FFD700", bg="#0F3460").pack(side="left", padx=20)
        
        # Computer choice display
        self.computer_choice_label = tk.Label(
            choices_display_frame, text="❓", font=("Arial", 48),
            fg="#EF4444", bg="#0F3460", width=3
        )
        self.computer_choice_label.pack(side="left", padx=20)
        
        # Result display
        self.result_label = tk.Label(
            battle_frame, text="Choose your weapon!",
            font=("Arial", 18, "bold"), fg="#FFD700", bg="#0F3460", pady=15
        )
        self.result_label.pack()
        
        # Choice buttons
        buttons_frame = tk.Frame(main_frame, bg="#1A1A2E")
        buttons_frame.pack(pady=20)
        
        # Create choice buttons with hover effects
        self.create_choice_button(buttons_frame, "snake", "🐍", "#4ADE80", 0, 0)
        self.create_choice_button(buttons_frame, "water", "💧", "#3B82F6", 0, 1)
        self.create_choice_button(buttons_frame, "gun", "🔫", "#EF4444", 0, 2)
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg="#1A1A2E")
        control_frame.pack(pady=20)
        
        # New Game button
        self.new_game_btn = tk.Button(
            control_frame, text="🔄 New Game", font=("Arial", 12, "bold"),
            bg="#E94560", fg="white", relief="raised", bd=3,
            padx=20, pady=10, command=self.new_game
        )
        self.new_game_btn.pack(side="left", padx=10)
        
        # Show History button
        self.history_btn = tk.Button(
            control_frame, text="📊 Game History", font=("Arial", 12, "bold"),
            bg="#0F4C75", fg="white", relief="raised", bd=3,
            padx=20, pady=10, command=self.show_history
        )
        self.history_btn.pack(side="left", padx=10)
        
        # Status bar
        self.status_label = tk.Label(
            main_frame, text="Ready to play! Use buttons or keyboard: S(Snake), W(Water), G(Gun)",
            font=("Arial", 10), fg="#BBB2B2", bg="#1A1A2E", pady=10
        )
        self.status_label.pack(side="bottom", fill="x")
        
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
    def create_choice_button(self, parent, choice, emoji, color, row, col):
        """Create an animated choice button"""
        btn = tk.Button(
            parent, text=f"{emoji}\n{choice.title()}", 
            font=("Arial", 16, "bold"), bg=color, fg="white",
            relief="raised", bd=4, width=10, height=3,
            command=lambda: self.play_round(choice)
        )
        btn.grid(row=row, column=col, padx=15, pady=10)
        
        # Add hover effects
        def on_enter(e):
            btn.config(relief="groove", bg=self.darken_color(color))
        
        def on_leave(e):
            btn.config(relief="raised", bg=color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            '#4ADE80': '#22C55E',
            '#3B82F6': '#2563EB', 
            '#EF4444': '#DC2626'
        }
        return color_map.get(color, color)
        
    def on_key_press(self, event):
        """Handle keyboard input"""
        key_map = {'s': 'snake', 'w': 'water', 'g': 'gun'}
        key = event.char.lower()
        
        if key in key_map:
            self.play_round(key_map[key])
        elif key == 'n':
            self.new_game()
            
    def play_round(self, player_choice):
        """Play a single round"""
        computer_choice = random.choice(['snake', 'water', 'gun'])
        
        # Update display with suspense
        self.status_label.config(text="Battle in progress...")
        self.animate_battle(player_choice, computer_choice)
        
    def animate_battle(self, player_choice, computer_choice):
        """Animate the battle sequence"""
        # Show spinning animation
        for i in range(6):
            self.player_choice_label.config(text="🔄")
            self.computer_choice_label.config(text="🔄")
            self.root.update()
            time.sleep(0.2)
            
        # Reveal choices
        self.player_choice_label.config(
            text=self.choices[player_choice]['emoji'],
            fg=self.choices[player_choice]['color']
        )
        self.computer_choice_label.config(
            text=self.choices[computer_choice]['emoji'],
            fg=self.choices[computer_choice]['color']
        )
        
        # Determine and show result
        result = self.determine_winner(player_choice, computer_choice)
        self.show_result(result, player_choice, computer_choice)
        
    def determine_winner(self, player_choice, computer_choice):
        """Determine the winner of the round"""
        if player_choice == computer_choice:
            return "draw"
        elif self.choices[player_choice]['beats'] == computer_choice:
            self.player_score += 1
            return "win"
        else:
            self.computer_score += 1
            return "lose"
            
    def show_result(self, result, player_choice, computer_choice):
        """Display the result with animation"""
        result_messages = {
            "win": ("🎉 YOU WIN! 🎉", "#4ADE80"),
            "lose": ("💀 YOU LOSE! 💀", "#EF4444"),
            "draw": ("🤝 IT'S A DRAW! 🤝", "#FFD700")
        }
        
        message, color = result_messages[result]
        
        # Animate result
        for _ in range(3):
            self.result_label.config(text="", bg="#0F3460")
            self.root.update()
            time.sleep(0.2)
            self.result_label.config(text=message, fg=color, bg="#0F3460")
            self.root.update()
            time.sleep(0.2)
            
        # Update scores and round
        self.update_display()
        
        # Add to history
        self.game_history.append({
            'round': self.round_number,
            'player': player_choice,
            'computer': computer_choice,
            'result': result
        })
        
        self.round_number += 1
        self.status_label.config(text=f"Round {self.round_number-1} complete! Ready for next round.")
        
        # Check for milestone scores
        if self.player_score == 5:
            messagebox.showinfo("Achievement!", "🏆 Congratulations! You've won 5 rounds!")
        elif self.computer_score == 5:
            messagebox.showinfo("Challenge!", "💪 Computer has won 5 rounds! Can you catch up?")
            
    def update_display(self):
        """Update score and round displays"""
        self.player_score_label.config(text=str(self.player_score))
        self.computer_score_label.config(text=str(self.computer_score))
        self.round_label.config(text=f"Round: {self.round_number}")
        
    def animate_title(self):
        """Animate the title with color changes"""
        colors = ["#FFD700", "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        current_color = 0
        
        def change_title_color():
            nonlocal current_color
            self.title_label.config(fg=colors[current_color])
            current_color = (current_color + 1) % len(colors)
            self.root.after(1000, change_title_color)
            
        change_title_color()
        
    def new_game(self):
        """Reset the game"""
        result = messagebox.askyesno("New Game", "Are you sure you want to start a new game?")
        if result:
            self.player_score = 0
            self.computer_score = 0
            self.round_number = 1
            self.game_history = []
            
            self.player_choice_label.config(text="❓", fg="#4ADE80")
            self.computer_choice_label.config(text="❓", fg="#EF4444")
            self.result_label.config(text="Choose your weapon!", fg="#FFD700")
            
            self.update_display()
            self.status_label.config(text="New game started! Good luck!")
            
    def show_history(self):
        """Show game history in a new window"""
        if not self.game_history:
            messagebox.showinfo("Game History", "No games played yet!")
            return
            
        history_window = tk.Toplevel(self.root)
        history_window.title("🎮 Game History")
        history_window.geometry("500x400")
        history_window.configure(bg="#1A1A2E")
        
        # Title
        tk.Label(history_window, text="📊 GAME HISTORY 📊", 
                font=("Arial", 16, "bold"), fg="#FFD700", bg="#1A1A2E").pack(pady=10)
        
        # Create scrollable text widget
        frame = tk.Frame(history_window, bg="#1A1A2E")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(frame, bg="#16213E", fg="#FFFFFF", font=("Courier", 10),
                             yscrollcommand=scrollbar.set, state="disabled")
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Populate history
        text_widget.config(state="normal")
        text_widget.insert("end", "Round | Your Choice | Computer | Result\n")
        text_widget.insert("end", "-" * 45 + "\n")
        
        for game in self.game_history:
            line = f"{game['round']:5} | {game['player']:11} | {game['computer']:8} | {game['result'].upper()}\n"
            text_widget.insert("end", line)
            
        # Add statistics
        wins = sum(1 for game in self.game_history if game['result'] == 'win')
        losses = sum(1 for game in self.game_history if game['result'] == 'lose')
        draws = sum(1 for game in self.game_history if game['result'] == 'draw')
        
        text_widget.insert("end", "\n" + "="*45 + "\n")
        text_widget.insert("end", f"STATISTICS:\n")
        text_widget.insert("end", f"Wins: {wins} | Losses: {losses} | Draws: {draws}\n")
        text_widget.insert("end", f"Win Rate: {(wins/len(self.game_history)*100):.1f}%\n")
        
        text_widget.config(state="disabled")

def main():
    """Main function to run the game"""
    root = tk.Tk()
    
    # Add some style improvements
    style = ttk.Style()
    style.theme_use('clam')
    
    game = SnakeWaterGunGame(root)
    
    # Welcome message
    messagebox.showinfo("Welcome!", 
        "🎮 Welcome to Snake Water Gun!\n\n" +
        "🎯 Use buttons or keyboard:\n" +
        "• S for Snake 🐍\n" +
        "• W for Water 💧\n" +
        "• G for Gun 🔫\n" +
        "• N for New Game\n\n" +
        "Good luck and have fun!")
    
    root.mainloop()

if __name__ == "__main__":
    main()