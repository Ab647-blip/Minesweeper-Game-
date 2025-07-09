# Minesweeper-Game-
# 🎯 Minesweeper Game

A classic **Minesweeper** implementation built using Python’s `tkinter` library.  
This game offers a smooth graphical interface with intuitive gameplay mechanics.

---

## 📌 Features

- 🧱 **10x10 Grid** with **25 Randomly Placed Mines**
- 🖱️ **Left Click** to Reveal Cells
- 🚩 **Right Click** to Flag/Unflag Suspected Mines
- 🔄 **Auto-Reveal** of Surrounding Empty Cells
- ✅ **Win Detection** when all safe cells are revealed
- ❌ **Loss Detection** on mine click
- 🔁 **"New Game"** Button to Restart Anytime
- 🎨 Visually Appealing UI with Color-Coded Numbers

---

## 🖼️ Screenshots

Photo attached to show the UI of Game

---

## ▶️ How to Run

### Prerequisites
- Python 3.x installed on your system

### Run the Game

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/YourRepoName.git
   cd YourRepoName

## 🧠 Game Rules

- Each cell may or may not contain a mine.
- Click (Left Click) on a cell to:
  - Reveal the number of adjacent mines (if any).
  - Auto-reveal nearby cells if the clicked cell has 0 surrounding mines.
  - Trigger a mine — 💣 *Game Over* — if the cell contains a mine.
- Right-click a cell to:
  - Place or remove a flag (🚩) to mark suspected mines.
- The game is won when all **non-mine** cells are revealed.

---

## 🚀 Future Improvements

- 🎯 Add difficulty levels (Easy, Medium, Hard) with adjustable grid/mine count.
- 🕒 Add a timer to track how fast the player finishes.
- 🏆 Add a high score board or best time tracking.
- 🎶 Include sound effects for actions and alerts.
- 📱 Make UI responsive for different screen sizes.
- 🌙 Add dark/light mode themes.
- 🔁 Implement undo/redo functionality.
- 📦 Package as an executable for easier sharing.
