import settings, sys, random, ctypes
from tkinter import Button, Label


class Cell:
    all = list()
    cell_count_label_object = None
    cell_count = settings.CELL_COUNT

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.is_opened = False
        self.is_marked = False
        self.x = x
        self.y = y
        
        # Append object to the Cell.all list
        Cell.all.append(self)
    
    def __repr__(self):
        return f'Cell ({self.x}, {self.y})'

    @staticmethod
    def create_cell_button_label(location):
        lbl = Label(location,
                    bg='black',
                    fg='white',
                    text=f'Cells left: {Cell.cell_count}',
                    font=('', 24))
        Cell.cell_count_label_object = lbl
        
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for cell in picked_cells:
            cell.is_mine = True
    
    @property
    def surrounding_cells(self):
        cells = [self.get_cell_by_axis(self.x - 1, self.y - 1),
                self.get_cell_by_axis(self.x, self.y - 1),
                self.get_cell_by_axis(self.x + 1, self.y - 1),
                self.get_cell_by_axis(self.x - 1, self.y),
                self.get_cell_by_axis(self.x + 1, self.y),
                self.get_cell_by_axis(self.x - 1, self.y + 1),
                self.get_cell_by_axis(self.x, self.y + 1),
                self.get_cell_by_axis(self.x + 1, self.y + 1)]
        cells = [cell for cell in cells if cell is not None]
        return cells
    
    @property
    def adjacent_mine_count(self):
        total = 0
        for cell in self.surrounding_cells:
            if cell.is_mine == True:
                total += 1
        return total

    def create_btn_object(self, location):
        btn = Button(location, width=12, height=4)
        btn.bind('<Button-1>', self.left_click_actions) # Left click
        btn.bind('<Button-3>', self.right_click_actions) # Right click
        self.cell_btn_object = btn
    
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()
            if self.adjacent_mine_count == 0:
                for cell in self.surrounding_cells:
                    cell.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'You won', 'Game over', 0)
                sys.exit()
        
        # Cancel left and right click events if cell is opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def right_click_actions(self, event):
        if not self.is_marked:
            self.cell_btn_object.configure(bg='blue')
            self.is_marked = True
        else:
            self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_marked = False
    
    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game over', 0)
        sys.exit()

    def show_cell(self):
        # Show number of adjacent mines
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.adjacent_mine_count)
            # Replace the text of Cell count label with new count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f'Cells left: {Cell.cell_count}')
            self.cell_btn_object.configure(bg='SystemButtonFace')
            # Mark cell as opened
            self.is_opened = True
    
    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the values of x, y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell