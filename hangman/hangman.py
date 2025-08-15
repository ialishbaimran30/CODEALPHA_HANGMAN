# -*- coding: utf-8 -*-
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        # Corrected geometry string: use 'x' instead of '×' and no trailing space
        self.root.geometry("1920x1080") 
        self.root.configure(bg="#2c3e50")
        
        # Predefined word list
        self.words = ["python", "hangman", "developer", "keyboard", "losangeles", "mirror", "football", "applejuice","vase","phone","nap","tumbler","sunglasses"]
        self.secret_word = random.choice(self.words).lower()
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.max_attempts = 6
        
        # Hangman images
        # IMPORTANT: Ensure these paths are correct and the images exist at these locations.
        # Use Image.open() to load existing images and then .resize()
        self.hangman_images = [
            ImageTk.PhotoImage(Image.open(r"C:\Users\User\Downloads\starting-removebg-preview.png").resize((380,280))), # State 0: Empty gallows
            ImageTk.PhotoImage(Image.open(r"C:\Users\User\Downloads\Untitled_design__2_-removebg-preview.png").resize((278, 280))), # State 1: Head
            ImageTk.PhotoImage(Image.open(r"C:\Users\User\Downloads\Untitled_design__3_-removebg-preview.png").resize((278, 280))), # State 2: Body
            ImageTk.PhotoImage(Image.open(r"C:\Users\User\Downloads\Untitled_design__4_-removebg-preview.png").resize((278, 280))), # State 3: One arm
            ImageTk.PhotoImage(Image.open(r"C:\Users\User\Downloads\Untitled_design__5_-removebg-preview.png").resize((278, 280))), # State 4: Both arms
            ImageTk.PhotoImage(Image.open(r"C:\Users\User\Downloads\Untitled_design__6_-removebg-preview.png").resize((278, 280))), # State 5: One leg
            ImageTk.PhotoImage(Image.open(r"C:\Users\User\Downloads\hangman6-removebg-preview.png").resize((278, 280)))  # State 6: Both legs (game over)
        ]
        
        # GUI Setup
        self.setup_gui()
    
    def setup_gui(self):
        self.main_frame = tk.Frame(self.root, bg="#2c3e50", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # New frame for the centered title across the entire top
        self.title_container_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.title_container_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 20)) # Pack at the top, fill horizontally

        title_label = tk.Label(self.title_container_frame, text="HANGMAN", font=("Helvetica", 36, "bold"), fg="#ecf0f1", bg="#2c3e50")
        # Center the title text within its new container frame
        title_label.pack(fill=tk.X, expand=True) # This will center the text within the expanded label
        
        # Frame to hold the control and hangman frames side-by-side below the title
        self.game_content_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.game_content_frame.pack(fill=tk.BOTH, expand=True)

        # Left side: Game controls (packed into game_content_frame)
        self.control_frame = tk.Frame(self.game_content_frame, bg="#2c3e50")
        self.control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 50))
        
        # New frame to contain all bottom-left elements: word display, guessed letters, input, and attempts
        self.game_info_and_input_frame = tk.Frame(self.control_frame, bg="#2c3e50")
        self.game_info_and_input_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True, pady=(20, 0))

        # Word display (blanks) - now left-aligned within its new container
        self.word_display = tk.Label(self.game_info_and_input_frame, text="_ " * len(self.secret_word), font=("Courier", 40, "bold"), fg="#f1c40f", bg="#2c3e50")
        self.word_display.pack(pady=20, anchor='w') 

        # Guessed letters label - now left-aligned and font bigger within its new container
        self.guessed_label = tk.Label(self.game_info_and_input_frame, text="Guessed letters:", font=("Arial", 20), fg="#ecf0f1", bg="#2c3e50")
        self.guessed_label.pack(pady=(0, 20), anchor='w') 
        
        # Input and attempts moved to this bottom frame
        input_frame = tk.Frame(self.game_info_and_input_frame, bg="#2c3e50")
        input_frame.pack(pady=20, anchor='w') # Anchor 'w' to left-align the input frame
        
        # Increased the width of the entry box from 3 to 10
        self.entry = tk.Entry(input_frame, font=("Arial", 20), width=10, justify="center", bd=2)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.entry.bind("<Return>", self.process_guess)
        
        self.submit_btn = tk.Button(input_frame, text="GUESS", command=self.process_guess, font=("Arial", 16, "bold"), bg="#3498db", fg="white", activebackground="#2980b9", bd=0, padx=10, pady=5)
        self.submit_btn.pack(side=tk.LEFT)
        
        self.attempts_label = tk.Label(self.game_info_and_input_frame, text=f"Attempts left: {self.max_attempts}", font=("Arial", 16), fg="#e74c3c", bg="#2c3e50")
        self.attempts_label.pack(pady=10, anchor='w') # Anchor 'w' to left-align attempts label
        
        # Right side: Hangman drawing (packed into game_content_frame)
        self.hangman_frame = tk.Frame(self.game_content_frame, bg="#2c3e50")
        # Ensure hangman_frame expands to allow centering of its contents
        self.hangman_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.hangman_canvas = tk.Canvas(self.hangman_frame, width=250, height=250, bg="#2c3e50", highlightthickness=0)
        # Center the hangman canvas within its frame
        self.hangman_canvas.pack(pady=50, anchor='center', expand=True)

        self.hangman_image = self.hangman_canvas.create_image(125, 125, image=self.hangman_images[0])
    
    def process_guess(self, event=None):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter (a-z).")
            return
        if guess in self.guessed_letters:
            messagebox.showwarning("Duplicate Guess", "You already guessed that letter.")
            return
        
        self.guessed_letters.append(guess)
        # Update the guessed letters display
        self.guessed_label.config(text=f"Guessed letters: {', '.join(self.guessed_letters)}")
        
        display_word = ""
        for letter in self.secret_word:
            display_word += letter + " " if letter in self.guessed_letters else "_ "
        self.word_display.config(text=display_word)
        
        if guess not in self.secret_word:
            self.incorrect_guesses += 1
            if self.incorrect_guesses <= self.max_attempts:
                self.hangman_canvas.itemconfig(self.hangman_image, image=self.hangman_images[self.incorrect_guesses])
            self.attempts_label.config(text=f"Attempts left: {self.max_attempts - self.incorrect_guesses}")
        
        # Cheerful message for winning
        if all(letter in self.guessed_letters for letter in self.secret_word):
            messagebox.showinfo("🥳 Congratulations! You Won! 🥳", f"Amazing! You guessed the word: '{self.secret_word.upper()}'! You're a true word wizard!")
            self.reset_game()
        # Sad message for losing
        elif self.incorrect_guesses >= self.max_attempts:
            messagebox.showinfo("😔 Game Over... Better Luck Next Time! 😔", f"Oh no! You ran out of attempts. The word was '{self.secret_word.upper()}'. Don't give up!")
            self.reset_game()
    
    def reset_game(self):
        self.secret_word = random.choice(self.words).lower()
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.word_display.config(text="_ " * len(self.secret_word))
        self.guessed_label.config(text="Guessed letters:")
        self.hangman_canvas.itemconfig(self.hangman_image, image=self.hangman_images[0])
        self.attempts_label.config(text=f"Attempts left: {self.max_attempts}")

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
