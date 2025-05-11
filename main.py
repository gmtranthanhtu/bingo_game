import random
import tkinter as tk
from tkinter import messagebox, Scrollbar
from bingo_game.card import BingoCard
import time
from . import config  # Use a relative import

class BingoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bingo Game")

        self.card1 = BingoCard()
        self.card2 = BingoCard()
        self.called_numbers = set()
        self.called_numbers_list = []  # List to track called numbers in order
        self.all_numbers = set(range(1, 76))
        self.winning_line1 = []
        self.winning_line2 = []
        self.winning_move = None # store the winning number
        self.winner = None
        self.bold_font = ("Arial", 10, "bold")
        self.normal_font = ("Arial", 10)

        self.create_widgets()
        #Mark the free space
        self.mark_free_space()
        # Bind space bar to call_number
        master.bind("<space>", lambda event: self.call_number())
    
    #def create_fireworks(self):
    #    # Function to create and animate the firework effect
    #    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    #    num_particles = 50
    #    
    #    canvas_width = self.canvas.winfo_width()
    #    canvas_height = self.canvas.winfo_height()
    #
    #    for _ in range(num_particles):
    #        x = random.randint(0, canvas_width)
    #        y = random.randint(0, canvas_height)
    #        size = random.randint(2, 5)
    #        color = random.choice(colors)
    #        
    #        particle = self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
    #        
    #        dx = random.uniform(-3, 3)
    #        dy = random.uniform(-3, 3)
    #        
    #        self.animate_particle(particle, dx, dy, 50)

    #def animate_particle(self, particle, dx, dy, life):
    #    if life <= 0:
    #        self.canvas.delete(particle)
    #        return
    #
    #    self.canvas.move(particle, dx, dy)
    #    self.master.after(10, lambda: self.animate_particle(particle, dx, dy, life - 1))
        
    def mark_free_space(self):
        self.card_buttons1[2][2].config(bg="yellow")
        self.card_buttons2[2][2].config(bg="yellow")

    def create_widgets(self):
        # Left Frame for Player 1
        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side="left", padx=10)
        # Label for Player 1
        self.player1_label = tk.Label(self.left_frame, text=config.PLAYER1_NAME, font=("Arial", 12, "bold"), fg="blue") #modified
        self.player1_label.pack()
        # Card Frame for Player 1
        self.card_frame1 = tk.Frame(self.left_frame)
        self.card_frame1.pack()
        self.card_buttons1 = []
        for row_index in range(5):
            row_buttons = []
            for col_index in range(5):
                value = self.card1.card[row_index][col_index]
                button = tk.Button(
                    self.card_frame1,
                    text=str(value),
                    width=4,
                    height=2,
                    font=("Arial", 10),
                    state="disabled",
                    disabledforeground="black" #modified
                )
                button.grid(row=row_index, column=col_index)
                row_buttons.append(button)
            self.card_buttons1.append(row_buttons)

        # Middle Frame for buttons and list
        self.middle_frame = tk.Frame(self.master)
        self.middle_frame.pack(side="left", padx=10)

        # Call Number Button
        self.call_button = tk.Button(
            self.middle_frame, text="Call Number", command=self.call_number
        )
        self.call_button.pack()

        # Called Number Label
        self.called_number_label = tk.Label(self.middle_frame, text="Called Number: ", width=15) #modified
        self.called_number_label.pack()

        # Called Numbers Listbox with Scrollbar
        self.listbox_frame = tk.Frame(self.middle_frame) # Create a frame for the listbox and scrollbar
        self.listbox_frame.pack()

        # Use a Text widget instead of Listbox
        self.called_numbers_text = tk.Text(self.listbox_frame, width=10, height=10, font=self.normal_font, wrap="none")
        self.called_numbers_text.pack(side="left")
        self.called_numbers_text.config(state="disabled")  # Make it read-only

        self.scrollbar = Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.called_numbers_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.called_numbers_text.yview)

        # Reset Button
        self.reset_button = tk.Button(
            self.middle_frame, text="Reset Game", command=self.reset_game
        )
        self.reset_button.pack()

        # Right Frame for Player 2
        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side="left", padx=10)
        # Label for Player 2
        self.player2_label = tk.Label(self.right_frame, text=config.PLAYER2_NAME, font=("Arial", 12, "bold"), fg="purple") #modified
        self.player2_label.pack()
        # Card Frame for Player 2
        self.card_frame2 = tk.Frame(self.right_frame)
        self.card_frame2.pack()
        self.card_buttons2 = []
        for row_index in range(5):
            row_buttons = []
            for col_index in range(5):
                value = self.card2.card[row_index][col_index]
                button = tk.Button(
                    self.card_frame2,
                    text=str(value),
                    width=4,
                    height=2,
                    font=("Arial", 10),
                    state="disabled",
                    disabledforeground="black" #modified
                )
                button.grid(row=row_index, column=col_index)
                row_buttons.append(button)
            self.card_buttons2.append(row_buttons)

    def mark_number(self, row, col, player):
        if player == 1:
            number = self.card1.card[row][col]
            if self.card1.mark_number(number):
                self.card_buttons1[row][col].config(bg="yellow")
        elif player == 2:
            number = self.card2.card[row][col]
            if self.card2.mark_number(number):
                self.card_buttons2[row][col].config(bg="yellow")

    def call_number(self):
        if len(self.called_numbers) == 75:
            messagebox.showinfo("Game Over", "All numbers have been called!")
            return

        number = random.choice(list(self.all_numbers - self.called_numbers))
        self.called_numbers.add(number)
        self.called_numbers_list.append(number)  # Add to the ordered list
        self.called_number_label.config(text=f"Called Number: {number}")

        # Add to Text widget with ordered number and bolding
        ordered_number = len(self.called_numbers_list)
        self.called_numbers_text.config(state="normal")  # Enable editing
        
        # Remove bold tag from the previous number
        if ordered_number > 1:
            self.called_numbers_text.tag_remove("bold", f"{ordered_number-1}.0", f"{ordered_number-1}.end")

        self.called_numbers_text.insert(tk.END, f"{ordered_number}. {number}\n")
        self.called_numbers_text.tag_add("bold", f"{ordered_number}.0", f"{ordered_number}.end")
        self.called_numbers_text.tag_config("bold", font=self.bold_font)
        self.called_numbers_text.see(tk.END)
        self.called_numbers_text.config(state="disabled")  # Disable editing again

        self.mark_number_on_cards(number)
        
        if self.card1.check_bingo():
            self.winner = 1
            self.winning_move = number
            self.find_winning_line(1)
            self.highlight_winning_line(1)
            self.show_winner_popup(config.PLAYER1_NAME) #modified
            self.call_button.config(state="disabled")
        elif self.card2.check_bingo():
            self.winner = 2
            self.winning_move = number
            self.find_winning_line(2)
            self.highlight_winning_line(2)
            self.show_winner_popup(config.PLAYER2_NAME) #modified
            self.call_button.config(state="disabled")
    
    def show_winner_popup(self, winner_name):
        # Get the position of the main window
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        width = self.master.winfo_width()
        height = self.master.winfo_height()

        # Calculate the position for the popup
        popup_x = x + width // 2 - 100  # Center horizontally
        popup_y = y + height + 10  # Below the main window

        # Show the message box
        messagebox.showinfo("Bingo!", f"{winner_name} won!", parent=self.master)

    def mark_number_on_cards(self, number):
        for row_index in range(5):
            for col_index in range(5):
                if self.card1.card[row_index][col_index] == number:
                    self.card_buttons1[row_index][col_index].config(bg="yellow")
                if self.card2.card[row_index][col_index] == number:
                    self.card_buttons2[row_index][col_index].config(bg="yellow")
        self.card1.mark_number(number)
        self.card2.mark_number(number)

    def highlight_winning_line(self, player):
        if player == 1:
            winning_line = self.winning_line1
            card = self.card1
            card_buttons = self.card_buttons1
        elif player == 2:
            winning_line = self.winning_line2
            card = self.card2
            card_buttons = self.card_buttons2
        #Highlight the winning line
        for row, col in winning_line:
          if card.card[row][col] == self.winning_move:
            card_buttons[row][col].config(bg="green", font=("Arial", 10, "bold"))
          else:
            card_buttons[row][col].config(bg="green")

    def find_winning_line(self, player):
        if player == 1:
            card = self.card1
        elif player == 2:
            card = self.card2
        # Check rows
        for i in range(5):
          if all(card.marked[i]):
            if player == 1:
                self.winning_line1 = [(i,j) for j in range(5)]
            elif player == 2:
                self.winning_line2 = [(i,j) for j in range(5)]
            return

        # Check columns
        for j in range(5):
          if all(card.marked[i][j] for i in range(5)):
            if player == 1:
                self.winning_line1 = [(i,j) for i in range(5)]
            elif player == 2:
                self.winning_line2 = [(i,j) for i in range(5)]
            return

        # Check diagonals
        if all(card.marked[i][i] for i in range(5)):
            if player == 1:
                self.winning_line1 = [(i,i) for i in range(5)]
            elif player == 2:
                self.winning_line2 = [(i,i) for i in range(5)]
            return

        if all(card.marked[i][4 - i] for i in range(5)):
            if player == 1:
                self.winning_line1 = [(i,4 - i) for i in range(5)]
            elif player == 2:
                self.winning_line2 = [(i,4 - i) for i in range(5)]
            return
    
    def reset_game(self):
        # Reset the game state
        self.card1 = BingoCard() #new card
        self.card2 = BingoCard() #new card
        self.called_numbers = set()
        self.called_numbers_list = []
        self.winning_line1 = []
        self.winning_line2 = []
        self.winning_move = None
        self.call_button.config(state="normal")
        self.winner = None

        # Clear the Text widget
        self.called_numbers_text.config(state="normal")
        self.called_numbers_text.delete("1.0", tk.END)
        self.called_numbers_text.config(state="disabled")

        # Reset button colors and text
        for row_index in range(5):
            for col_index in range(5):
                button = self.card_buttons1[row_index][col_index]
                button.config(bg="SystemButtonFace", font=("Arial", 10), text=str(self.card1.card[row_index][col_index]))
                button = self.card_buttons2[row_index][col_index]
                button.config(bg="SystemButtonFace", font=("Arial", 10), text=str(self.card2.card[row_index][col_index]))
        self.mark_free_space()

def main():
    root = tk.Tk()
    gui = BingoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
