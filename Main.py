"""
Minesweeper Game
A classic Minesweeper implementation using Python's tkinter library.

Features:
- 10x10 grid with 25 mines
- Left click to reveal cells
- Right click to flag/unflag cells
- Auto-reveal for empty areas
- Win/Loss detectiona
- New Game functionality """

import tkinter as tk
import random
import tkinter.messagebox as msgbox


class MinesweeperGame:
    """Main game class"""
    GRID_SIZE = 10
    MINE_COUNT = 25
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 500
    TOP_FRAME_HEIGHT = 100
    
    def __init__(self):
        self.setup_window()
        self.setup_frames()
        self.setup_ui_components()
        self.create_game_grid()
        self.start_new_game()
    
    def setup_window(self):
        self.root = tk.Tk()
        self.root.configure(bg="black")  # Changed: No background visible
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.title("Minesweeper Game")
        self.root.resizable(False, False)
    
    def setup_frames(self):
        self.top_frame = tk.Frame(
            self.root,
            bg="black",
            width=self.WINDOW_WIDTH,
            height=self.TOP_FRAME_HEIGHT,
        )
        self.top_frame.place(x=0, y=0)
        self.top_frame.pack_propagate(False)  

        self.center_frame = tk.Frame(
            self.root,
            bg="black",
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT - self.TOP_FRAME_HEIGHT,
        )
        self.center_frame.place(x=0, y=self.TOP_FRAME_HEIGHT)
        self.center_frame.pack_propagate(False) 
    
    def setup_ui_components(self):

        self.title_label = tk.Label(
            self.top_frame,
            text="🎯 MINESWEEPER",
            font=("Arial", 18, "bold"),
            bg="black",
            fg="white"
        )
        self.title_label.pack(pady=(10, 5))
        
        stats_frame = tk.Frame(self.top_frame, bg="black")
        stats_frame.pack(pady=5)
        
        self.mines_label = tk.Label(
            stats_frame,
            text=f"Mines: {self.MINE_COUNT}",
            font=("Arial", 12),
            bg="black",
            fg="yellow"
        )
        self.mines_label.pack(side=tk.LEFT, padx=10)
        
        self.restart_btn = tk.Button(
            stats_frame,
            text="🔄 New Game",
            command=self.start_new_game,
            bg="lightgreen",
            fg="black",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.restart_btn.pack(side=tk.RIGHT, padx=10)
        
        self.info_label = tk.Label(
            self.top_frame,
            
        )
        self.info_label.pack()
    
    def create_game_grid(self):
        Cell.all.clear()
        
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                cell = Cell(x, y, self)
                cell.create_btn_object(self.center_frame)
                cell.cell_btn_object.grid(
                    column=y, 
                    row=x, 
                    padx=1, 
                    pady=1,
                    sticky="nsew"  
                )
        
        
        for i in range(self.GRID_SIZE):
            self.center_frame.grid_rowconfigure(i, weight=1)
            self.center_frame.grid_columnconfigure(i, weight=1)
    
    def start_new_game(self):
       
        Cell.game_over = False
        for cell in Cell.all:
            cell.reset()
        
        Cell.randomize_mines(self.MINE_COUNT)
        
        self.update_game_status("Game Started!")
    
    def update_game_status(self, message):
        
        self.info_label.configure(text=message)
        self.root.after(2000, lambda: self.info_label.configure(
            text="Left Click: Reveal | Right Click: Flag"
        ))
    
    def game_over(self, won=False):
        
        Cell.game_over = True
        
        if won:
            msgbox.showinfo("🎉 Victory!", "Congratulations! You found all mines!")
            self.update_game_status("You Won! 🎉")
        else:
            msgbox.showinfo("💥 Game Over", "You hit a mine! Better luck next time!")
            self.update_game_status("Game Over 💥")
    
    def check_win_condition(self):
        
        if Cell.game_over:
            return
       
        safe_cells = [cell for cell in Cell.all if not cell.is_mine]
        revealed_safe_cells = [cell for cell in safe_cells if cell.is_clicked]
        
        if len(revealed_safe_cells) == len(safe_cells):
            self.game_over(won=True)
    
    def run(self):
        self.root.mainloop()


class Cell:
    
    all = []
    game_over = False
    NUMBER_COLORS = {
        1: "#0000FF",  # Blue
        2: "#008000",  # Green  
        3: "#FF0000",  # Red
        4: "#800080",  # Purple
        5: "#800000",  # Maroon
        6: "#008080",  # Teal
        7: "#000000",  # Black
        8: "#808080",  # Gray
    }
    
    def __init__(self, x, y, game):
        """Initialize a cell with coordinates and game reference."""
        self.x = x
        self.y = y
        self.game = game
        self.is_mine = False
        self.is_clicked = False
        self.is_flagged = False
        self.cell_btn_object = None
        
        # Add to class list
        Cell.all.append(self)
    
    def create_btn_object(self, parent):
        
        self.cell_btn_object = tk.Button(
            parent,
            bg="darkgray",
            width=3,
            height=1,
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        
        # Bind mouse events
        self.cell_btn_object.bind('<Button-1>', self.left_click_action)
        self.cell_btn_object.bind('<Button-3>', self.right_click_action)
    
    def left_click_action(self, event):
       
        # Prevent actions if game is over or cell is flagged/clicked
        if Cell.game_over or self.is_flagged or self.is_clicked:
            return
        
        self.is_clicked = True
        
        if self.is_mine:
            self.reveal_mine()
            self.reveal_all_mines()  # CHANGED: Show all mines on game over
            self.game.game_over(won=False)
        else:
            self.reveal_cell()
            self.game.check_win_condition()
    
    def right_click_action(self, event):
        
        if Cell.game_over or self.is_clicked:
            return
        
        if self.is_flagged:
            # Remove flag
            self.cell_btn_object.configure(text="", bg="darkgray")
            self.is_flagged = False
        else:
            # Add flag
            self.cell_btn_object.configure(text="🚩", bg="orange")
            self.is_flagged = True
    
    def reveal_mine(self):
        
        self.cell_btn_object.configure(
            bg="red", 
            text="💣", 
            relief=tk.SUNKEN
        )
    
    def reveal_all_mines(self):
        
        for cell in Cell.all:
            if cell.is_mine and cell != self:
                cell.cell_btn_object.configure(
                    bg="lightcoral", 
                    text="💣",
                    relief=tk.SUNKEN
                )
    
    def reveal_cell(self):
        
        mine_count = self.count_surrounding_mines()
        
        if mine_count == 0:
            
            self.cell_btn_object.configure(
                text="", 
                bg="lightgray", 
                relief=tk.SUNKEN
            )
            self.auto_reveal_surrounding()
        else:
            
            color = self.NUMBER_COLORS.get(mine_count, "black")
            self.cell_btn_object.configure(
                text=str(mine_count),
                bg="lightgray",
                fg=color,
                relief=tk.SUNKEN
            )
    
    def count_surrounding_mines(self):
        
        count = 0
        for cell in self.get_surrounding_cells():
            if cell and cell.is_mine:
                count += 1
        return count
    
    def get_surrounding_cells(self):
        
        surrounding = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip self
                surrounding.append(self.get_cell_by_coordinates(self.x + dx, self.y + dy))
        return surrounding
    
    def auto_reveal_surrounding(self):
        
        for cell in self.get_surrounding_cells():
            if (cell and not cell.is_clicked and 
                not cell.is_flagged and not cell.is_mine):
                cell.left_click_action(None)
    
    def get_cell_by_coordinates(self, x, y):
        
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        return None
    
    def reset(self):
        
        self.is_mine = False
        self.is_clicked = False
        self.is_flagged = False
        self.cell_btn_object.configure(
            text="", 
            bg="darkgray",
            relief=tk.RAISED
        )
    
    @staticmethod
    def randomize_mines(mine_count):
        
        for cell in Cell.all:
            cell.is_mine = False
        
        # Place mines randomly
        mine_cells = random.sample(Cell.all, mine_count)
        for cell in mine_cells:
            cell.is_mine = True
    
    def __repr__(self):
        
        return f"Cell({self.x}, {self.y})"


def main():
    game = MinesweeperGame()
    game.run()


if __name__ == "__main__":
    main()