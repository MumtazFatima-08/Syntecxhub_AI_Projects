import tkinter as tk
from tkinter import messagebox
import random

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def astar(maze, start, end):
    start_node = Node(None, start)
    end_node = Node(None, end)
    open_list = []
    closed_list = []
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = manhattan_distance(child.position, end_node.position)
            child.f = child.g + child.h

            if any(open_node for open_node in open_list if child == open_node and child.g > open_node.g):
                continue

            open_list.append(child)
    return None

# --- MODERN STYLED UI ---
class MazeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Pathfinding Visualizer")
        
        # Sleek Pastel Palette
        self.BG_COLOR = "#F8F9FA"       # Clean off-white background
        self.WALL_COLOR = "#2D3748"     # Elegant dark charcoal
        self.START_COLOR = "#4FD1C5"    # Minty pastel teal
        self.GOAL_COLOR = "#F687B3"     # Soft pastel rose
        self.PATH_COLOR = "#F6E05E"     # Warm pastel sunny yellow
        self.EMPTY_COLOR = "#FFFFFF"    # Crisp white grid cells
        self.BORDER_COLOR = "#E2E8F0"   # Subtle light border lines
        
        self.root.configure(bg=self.BG_COLOR)
        self.grid_size = 6
        self.cell_size = 55
        self.start = (0, 0)
        self.goal = (5, 5)
        
        # Title Header Label
        # Title Header Label (Fixed - removed letterspacing)
        title_lbl = tk.Label(
            root, 
            text="MAZE SOLVER", 
            font=("Helvetica", 14, "bold"), 
            bg=self.BG_COLOR, 
            fg="#1A202C"
        )
        title_lbl.pack(pady=(20, 5))
        
        # Interactive Canvas with custom border styling
        canvas_width = self.grid_size * self.cell_size
        canvas_height = self.grid_size * self.cell_size
        self.canvas = tk.Canvas(
            root, 
            width=canvas_width, 
            height=canvas_height, 
            bg=self.BG_COLOR, 
            highlightthickness=0
        )
        self.canvas.pack(pady=15)
        
        # Elegant Button Container
        btn_frame = tk.Frame(root, bg=self.BG_COLOR)
        btn_frame.pack(pady=(5, 25))
        
        # Modern Styled Action Buttons
        self.solve_btn = tk.Button(
            btn_frame, 
            text="Solve Path", 
            font=("Helvetica", 11, "bold"), 
            command=self.draw_path, 
            bg="#319795", 
            fg="white", 
            activebackground="#2C7A7B",
            activeforeground="white",
            bd=0, 
            padx=15, 
            pady=8,
            cursor="hand2"
        )
        self.solve_btn.pack(side="left", padx=10)
        
        self.reset_btn = tk.Button(
            btn_frame, 
            text="New Maze", 
            font=("Helvetica", 11), 
            command=self.generate_new_maze, 
            bg="#EDF2F7", 
            fg="#4A5568", 
            activebackground="#E2E8F0",
            bd=0, 
            padx=15, 
            pady=8,
            cursor="hand2"
        )
        self.reset_btn.pack(side="left", padx=10)
        
        self.generate_new_maze()

    def generate_new_maze(self):
        self.maze = []
        for r in range(self.grid_size):
            row = []
            for c in range(self.grid_size):
                if (r, c) != self.start and (r, c) != self.goal and random.random() < 0.25:
                    row.append(1)
                else:
                    row.append(0)
            self.maze.append(row)
        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Assigning refined color schemes
                if (r, c) == self.start:
                    color = self.START_COLOR
                    text = "START"
                elif (r, c) == self.goal:
                    color = self.GOAL_COLOR
                    text = "GOAL"
                elif self.maze[r][c] == 1:
                    color = self.WALL_COLOR
                    text = ""
                else:
                    color = self.EMPTY_COLOR
                    text = ""
                
                # Drawing cleaner squares with premium soft borders
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.BORDER_COLOR, width=1.5)
                
                if text:
                    self.canvas.create_text(
                        x1 + (self.cell_size/2), 
                        y1 + (self.cell_size/2), 
                        text=text, 
                        fill="white", 
                        font=("Helvetica", 8, "bold")
                    )

    def draw_path(self):
        path = astar(self.maze, self.start, self.goal)
        
        if path:
            for (r, c) in path:
                if (r, c) != self.start and (r, c) != self.goal:
                    x1 = c * self.cell_size
                    y1 = r * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    # Highlight paths with soft rounded dots inside clean boxes
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.PATH_COLOR, outline=self.BORDER_COLOR, width=1.5)
                    self.canvas.create_oval(
                        x1 + 20, y1 + 20, x2 - 20, y2 - 20, 
                        fill="#D69E2E", outline=""
                    )
            messagebox.showinfo("Success", "Shortest path successfully calculated!")
        else:
            messagebox.showerror("No Route", "This random generation leaves the goal unreachable.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeUI(root)
    root.mainloop()