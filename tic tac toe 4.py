from tkinter import *
from tkinter import messagebox
import tkinter.font as font

window = Tk()
window.geometry("320x320")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
table = Canvas(window, bg='black')
table.grid(sticky='nesw')
width, heigth = table.winfo_width(), table.winfo_height()
my_font = font.Font(family='Arial')
my_font['size'] = 70

line = table.create_line(width / 20, heigth / 3, width / 20 * 19, heigth / 3, width=3, fill='white')
line2 = table.create_line(width / 20, heigth / 3 * 2, width / 20 * 19, heigth / 3 * 2, width=3, fill='white')
line3 = table.create_line(width / 3, heigth / 20, width / 3, heigth / 20 * 19, width=3, fill='white')
line4 = table.create_line(width / 3 * 2, heigth / 20, width / 3 * 2, heigth / 20 * 19, width=3, fill='white')


class Field:
    def __init__(self, row, col, name):
        self.row = row
        self.col = col
        self.name = name
        self.txt = None

    def get_name(self):
        return self.name

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def set_txt(self, txt):
        self.txt = txt

    def get_txt(self):
        return self.txt


class Board:
    def __init__(self):
        self.board = [[], [], []]
        for row in range(3):
            for col in range(3):
                f = Field(row, col, ' ')
                self.board[row].append(f)


class Player:
    def __init__(self, name, winner, score):
        self.name = name
        self.winner = winner
        self.score = score

    def play(self, event):
        width, heigth = table.winfo_width(), table.winfo_height()
        if event.x+10 > width or event.y+10 > heigth:  # avoid play on window resizing
            pass
        else:
            global switch
            self.winner = check_score()
            if self.winner is None:
                if event.x < width/3:
                    col = 0
                elif width/3 < event.x < width/3*2:
                    col = 1
                else:
                    col = 2
                if event.y < heigth/3:
                    row = 0
                elif heigth/3 < event.y < heigth/3*2:
                    row = 1
                else:
                    row = 2

                # create X O on click
                if b.board[row][col].name == ' ':  # if empty field
                    b.board[row][col].name = str(self.name)
                    x = locate(row, col, self.name)[0]
                    y = locate(row, col, self.name)[1]
                    txt = table.create_text(x, y, tag='text', font=my_font, fill='white', text=str(self.name))
                    b.board[row][col].set_txt(txt)
                else:
                    print('Not available, choose again: ')
                    switch -= 1
                    pass

                switch += 1
                return row, col, self.name

            else:
                message()


def switch_player(event):
    global game
    if switch % 2 == 0:
        p_x.play(event)
        if check_score():
            p_x.score += 1
            game = False
    else:
        p_o.play(event)
        if check_score():
            p_o.score += 1
            game = False
    return game


def check_score():
    col = 0
    winner = None
    # row check
    for row in range(3):
        if ' ' not in b.board[row][0].name and \
                b.board[row][0].name == b.board[row][1].name == b.board[row][2].name:
            winner = b.board[row][0].name
            x = locate(row, 0, winner)[0] - 40
            y = locate(row, 0, winner)[1]
            x1 = locate(row, 2, winner)[0] + 40
            draw_line(x, y, x1, y)

    # column check
    for i in range(3):
        if b.board[0][col].name != ' ' and \
                b.board[0][col].name == b.board[1][col].name == b.board[2][col].name:
            winner = b.board[0][col].name
            x = locate(0, col, winner)[0]
            y = locate(0, col, winner)[1] - 40
            y1 = locate(2, col, winner)[1] + 40
            draw_line(x, y, x, y1)
        col += 1
    # diagonal check
    if b.board[1][1].name != ' ' and \
            b.board[0][0].name == b.board[1][1].name == b.board[2][2].name:
        winner = b.board[1][1].name
        x = locate(0, 0, winner)[0] - 40
        y = locate(0, 0, winner)[1] - 40
        x1 = locate(2, 2, winner)[0] + 40
        y1 = locate(2, 2, winner)[1] + 40
        draw_line(x, y, x1, y1)
    elif b.board[1][1].name != ' ' and \
            b.board[0][2].name == b.board[1][1].name == b.board[2][0].name:
        winner = b.board[0][2].name
        x = locate(0, 2, winner)[0] + 40
        y = locate(0, 2, winner)[1] - 40
        x1 = locate(2, 0, winner)[0] - 40
        y1 = locate(2, 0, winner)[1] + 40
        draw_line(x, y, x1, y1)
    count = 0
    for row in range(3):
        for col in range(3):
            if b.board[row][col].name != ' ':
                count += 1
    if count == 9 and winner is None:
        winner = None
        message_tie()

    if winner is None:
        return None
    else:
        return winner


def resize(event):
    width, heigth = table.winfo_width(), table.winfo_height()
    table.coords(line, width / 20, heigth / 3, width / 20 * 19, heigth / 3)
    table.coords(line2, width / 20, heigth / 3 * 2, width / 20 * 19, heigth / 3 * 2)
    table.coords(line3, width / 3, heigth / 20, width / 3, heigth / 20 * 19)
    table.coords(line4, width / 3 * 2, heigth / 20, width / 3 * 2, heigth / 20 * 19)

    for row in range(3):
        for col in range(3):
            x_pos, y_pos = locate(row, col, b.board[row][col].get_name())
            txt = b.board[row][col].get_txt()
            if txt is not None:
                table.coords(txt, x_pos, y_pos)
    if width < heigth:
        my_font['size'] = int(width/5)
    else:
        my_font['size'] = int(heigth/5)



def locate(row, col, player):
    width, heigth = table.winfo_width(), table.winfo_height()

    if row == 0:
        y_pos = heigth / 5
    elif row == 1:
        y_pos = heigth / 2
    else:
        y_pos = heigth / 5 * 4
    if col == 0:
        x_pos = width / 5
    elif col == 1:
        x_pos = width / 2
    else:
        x_pos = width / 5 * 4

    return x_pos, y_pos


def draw_line(x, y, x1, y1):
    table.create_line(x, y, x1, y1, width=12, fill='white', tags='finish')


def message():
    messagebox.geometry = ('320X100')
    q = messagebox.askquestion(f'X score:{p_x.score}   O score:{p_o.score}', f'Player {check_score()} wins! Another one?')
    if q == 'yes':
        reset()
    else:
        exit()


def message_tie():
    messagebox.geometry = ('320X100')
    q = messagebox.askquestion("It's a tie!", "Another one?")
    if q == 'yes':
        reset()
    else:
        exit()


def reset():
    global switch, game
    switch = 0
    game = True
    table.delete('text')
    table.delete('finish')
    reset_board()
    p_x.winner = None
    p_o.winner = None


def reset_board():
    for row in range(3):
        for col in range(3):
            b.board[row][col].name = ' '
            b.board[row][col].set_txt(None)


game = True
switch = 0

b = Board()
p_x = Player('X', None, 0)
p_o = Player('O', None, 0)

window.bind("<Button-1>", switch_player)  # hook mouse click to field
window.bind('<Configure>', resize)  # hook window size changes

window.mainloop()