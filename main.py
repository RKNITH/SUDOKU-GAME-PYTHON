
import numpy as np
import os
import random
import turtle
import time
import sys
try:
    from tkinter import *
except:
    from Tkinter import *


class Game:

    def __init__(self):
        
        self._screen = turtle.Screen()  # init turtle screen
        self._screen.title("LET'S PLAY SUDOKU")  # screen title
        self._screen.bgcolor("royal blue")  # background color
        self._screen.setup(width=600, height=600)  # screen dimensions
        self._screen.tracer(0)  # frame delay
        self._screen._root.resizable(False, False)  # not resizable window
        self._found_solved = False  # flag to generate solveable board
        self._original_grid = None  # store original grid
        self._copy_original_grid = None  # keep a clean copy of the original grid
        self._solved_grid = None  # store grid solution
        self._done = False  # flag to close gui
        self._clicked = None  # store clicked location position in grid array
        self._box = None  # store box turtle marker
        self._input = None  # store input from user
        self._position_to_draw = None  # store gui position to draw input number
        self._input_marker = None  # store turtle input marker
        self._wrong_marker = None  # store turtle marker for wrong or missing answers
        self._wrong_answers_drawn = False  # flag to clear wrong or missing answers visual
        self._found = False  # flag to clear wrong or missing answers visual
        self._position_highlighted = None  # store gui position of clicked box
        self._correct = True  # flag to see if user solution is correct
        self._inputs = []  # keep track of inputs if reset or delete is initialized
        self.find_board()  # generate board
        self.create_grid()  # create grid
        self.draw_numbers()  # draw numbers
        self.create_highlight_box_turtle()  # create marker
        self.create_wrong_marker()  # create marker
        self.listen()  # bind keyboard and mouse inputs

    def find_board(self):
        """
        Checks if a given board is solveable
        :return None
        """
        self._found_solved = False
        while not self._found_solved:
            s = Sudoku(self.create_random_board())
            if s.solve():
                self._original_grid = s._original_grid
                self._copy_original_grid = s._original_grid.copy()
                self._solved_grid = s.solve(ret=True)
                self._found_solved = True

    def create_random_board(self):
        """
        Removes numbers from a solveable sudoku board to create a new one
        :return 9x9 sudoku board
        """
        board_1 = [[3, 1, 6, 5, 7, 8, 4, 9, 2],
                   [5, 2, 9, 1, 3, 4, 7, 6, 8],
                   [4, 8, 7, 6, 2, 9, 5, 3, 1],
                   [2, 6, 3, 4, 1, 5, 9, 8, 7],
                   [9, 7, 4, 8, 6, 3, 1, 2, 5],
                   [8, 5, 1, 7, 9, 2, 6, 4, 3],
                   [1, 3, 8, 9, 4, 7, 2, 5, 6],
                   [6, 9, 2, 3, 5, 1, 8, 7, 4],
                   [7, 4, 5, 2, 8, 6, 3, 1, 9]]

        board_2 = [[4, 3, 5, 2, 6, 9, 7, 8, 1],
                   [6, 8, 2, 5, 7, 1, 4, 9, 3],
                   [1, 9, 7, 8, 3, 4, 5, 6, 2],
                   [8, 2, 6, 1, 9, 5, 3, 4, 7],
                   [3, 7, 4, 6, 8, 2, 9, 1, 5],
                   [9, 5, 1, 7, 4, 3, 6, 2, 8],
                   [5, 1, 9, 3, 2, 6, 8, 7, 4],
                   [2, 4, 8, 9, 5, 7, 1, 3, 6],
                   [7, 6, 3, 4, 1, 8, 2, 5, 9]]

        board_3 = [[1, 5, 2, 4, 8, 9, 3, 7, 6],
                   [7, 3, 9, 2, 5, 6, 8, 4, 1],
                   [4, 6, 8, 3, 7, 1, 2, 9, 5],
                   [3, 8, 7, 1, 2, 4, 6, 5, 9],
                   [5, 9, 1, 7, 6, 3, 4, 2, 8],
                   [2, 4, 6, 8, 9, 5, 7, 1, 3],
                   [9, 1, 4, 6, 3, 7, 5, 8, 2],
                   [6, 2, 5, 9, 4, 8, 1, 3, 7],
                   [8, 7, 3, 5, 1, 2, 9, 6, 4]]

        board_4 = [[5, 8, 1, 6, 7, 2, 4, 3, 9],
                   [7, 9, 2, 8, 4, 3, 6, 5, 1],
                   [3, 6, 4, 5, 9, 1, 7, 8, 2],
                   [4, 3, 8, 9, 5, 7, 2, 1, 6],
                   [2, 5, 6, 1, 8, 4, 9, 7, 3],
                   [1, 7, 9, 3, 2, 6, 8, 4, 5],
                   [8, 4, 5, 2, 1, 9, 3, 6, 7],
                   [9, 1, 3, 7, 6, 8, 5, 2, 4],
                   [6, 2, 7, 4, 3, 5, 1, 9, 8]]

        board = random.choice([board_1, board_2, board_3, board_4])
        count = 0
        while count <= len(board)*len(board[0]) - 30:
            location = [random.randint(0, 8), random.randint(0, 8)]
            if board[location[0]][location[1]] != 0:
                board[location[0]][location[1]] = 0
                count += 1
        return board

    def create_grid(self):
        """
        Creates the grid lines
        :return: None
        """
        pen = turtle.Turtle()
        pen.speed(0)
        pen.pensize(10)
        pen.hideturtle()
        # create column box grid
        pen.penup()
        pen.setpos(self._screen.window_width()/6, self._screen.window_height())
        pen.pendown()
        pen.setpos(self._screen.window_width()/6, -self._screen.window_height())
        pen.penup()
        pen.setpos(-self._screen.window_width()/6, self._screen.window_height())
        pen.pendown()
        pen.setpos(-self._screen.window_width()/6, -self._screen.window_height())
        # create row box grid
        pen.penup()
        pen.setpos(self._screen.window_width(), self._screen.window_height()/6)
        pen.pendown()
        pen.setpos(-self._screen.window_width(), self._screen.window_height()/6)
        pen.penup()
        pen.setpos(self._screen.window_width(), -self._screen.window_height()/6)
        pen.pendown()
        pen.setpos(-self._screen.window_width(), -self._screen.window_height()/6)
        # resize pen
        pen.pensize(2)
        # create column grid
        for i in range(8):
            if i == 1 or i == 5 or i == 7:
                pen.penup()
                pen.setpos(i*self._screen.window_width()/18, self._screen.window_height())
                pen.pendown()
                pen.setpos(i*self._screen.window_width()/18, -self._screen.window_height())
                pen.penup()
                pen.setpos(-i*self._screen.window_width()/18, self._screen.window_height())
                pen.pendown()
                pen.setpos(-i*self._screen.window_width()/18, -self._screen.window_height())
        # create row grid
        for i in range(8):
            if i == 1 or i == 5 or i == 7:
                pen.penup()
                pen.setpos(self._screen.window_width(), i*self._screen.window_height()/18)
                pen.pendown()
                pen.setpos(-self._screen.window_width(), i*self._screen.window_height()/18)
                pen.penup()
                pen.setpos(self._screen.window_width(), -i*self._screen.window_height()/18)
                pen.pendown()
                pen.setpos(-self._screen.window_width(), -i*self._screen.window_height()/18)

    def draw_original_grid(self):
        """
        Deletes everything and redraws original grid
        :return None
        """
        self._input_marker = turtle.Turtle()
        self._input_marker.speed(0)
        self._input_marker.color('black')
        self._input_marker.penup()
        self._input_marker.hideturtle()
        for i in range(len(self._copy_original_grid)):
            for j in range(len(self._copy_original_grid[0])):
                self._input_marker.setpos(-(8 - j*2)*self._screen.window_width()/18, (8 - i*2)*self._screen.window_height()/18 - self._screen.window_height()/18/2)
                if self._copy_original_grid[i][j] != 0:
                    self._input_marker.write("{}".format(self._copy_original_grid[i][j]), align="center", font=("Arial", 26, "normal"))

    def draw_input_numbers(self):
        """
        Draws user input numbers
        :return None
        """
        self._input_marker.color('yellow')
        for start_x, start_y, input, i, j in self._inputs:
            self._input_marker.setpos(start_x, start_y)
            self._input_marker.write("{}".format(input), align="center", font=("Arial", 26, "normal"))

    def draw_numbers(self):
        """
        Draws numbers from generated Sudoku board
        :return None
        """
        self._input_marker = turtle.Turtle()
        self._input_marker.speed(0)
        self._input_marker.color('black')
        self._input_marker.penup()
        self._input_marker.hideturtle()
        for i in range(len(self._original_grid)):
            for j in range(len(self._original_grid[0])):
                self._input_marker.setpos(-(8 - j*2)*self._screen.window_width()/18, (8 - i*2)*self._screen.window_height()/18 - self._screen.window_height()/18/2)
                if self._original_grid[i][j] != 0:
                    self._input_marker.write("{}".format(self._original_grid[i][j]), align="center", font=("Arial", 26, "normal"))

    def find_position_on_grid(self, x, y):
        """
        Finds the corresponding position of the clicked box inside the sudoku grid array, and the appropriate position to draw number
        :return None
        """
        for i in range(len(self._original_grid)):
            for j in range(len(self._original_grid[0])):
                if -(7 - j * 2)*self._screen.window_width()/18 >= x >= -(9 - j * 2)*self._screen.window_width()/18 and (9 - i * 2) * self._screen.window_height()/18 >= y >= (7 - i * 2) * self._screen.window_height()/18:
                    self.make_clicked_visible(-(9 - j * 2)*self._screen.window_width()/18, (7 - i * 2) * self._screen.window_height()/18)
                    self._clicked = [i, j]
                    self._position_to_draw = [-(8 - j*2)*self._screen.window_width()/18, (8 - i*2)*self._screen.window_height()/18 - self._screen.window_height()/18/2]
                    self._position_highlighted = [-(9 - j * 2)*self._screen.window_width()/18, (7 - i * 2) * self._screen.window_height()/18]

    def make_clicked_visible(self, start_x, start_y):
        """
        Creates a green box around the clicked box
        :param start_x: Starting x position to draw square
        :param start_y: Starting y position to draw square
        :return: None
        """
        self._box.clear()
        self._box.penup()
        self._box.setpos(start_x, start_y)
        self._box.pendown()
        self._box.setpos(start_x, start_y + 2*self._screen.window_height()/18)
        self._box.setpos(start_x + 2*self._screen.window_width()/18, start_y + 2*self._screen.window_height()/18)
        self._box.setpos(start_x + 2*self._screen.window_width()/18, start_y)
        self._box.setpos(start_x, start_y)
        self._box.penup()

    def create_highlight_box_turtle(self):
        """
        Creates the marker for the green highlight box around the clicked box
        :return None
        """
        self._box = turtle.Turtle()
        self._box.speed(0)
        self._box.pensize(9)
        self._box.color('green')
        self._box.hideturtle()

    def create_wrong_marker(self):
        """
        Creates the marker for the wrong or missing answers
        :return None
        """
        self._wrong_marker = turtle.Turtle()
        self._wrong_marker.speed(0)
        self._wrong_marker.pensize(9)
        self._wrong_marker.color('red')
        self._wrong_marker.hideturtle()

    def delete_number(self):
        """
        Deletes the input corresponding to the highlighted marker
        :return None
        """
        if self._clicked is not None:
            if self._copy_original_grid[self._clicked[0]][self._clicked[1]] == 0:
                self._input_marker.clear()
                self._original_grid[self._clicked[0]][self._clicked[1]] = 0
                for i, inputs in enumerate(self._inputs):
                    if inputs[3] == self._clicked[0] and inputs[4] == self._clicked[1]:
                        del self._inputs[i]
                self.draw_original_grid()
                self.draw_input_numbers()

    def draw_input_number(self, input):
        """
        Draws the user input number
        :param input: Input number to draw
        :return None
        """
        if self._clicked is not None:
            if self._original_grid[self._clicked[0]][self._clicked[1]] == 0:
                self._input_marker.color('yellow')
                self._input_marker.setpos(self._position_to_draw[0], self._position_to_draw[1])
                self._input_marker.write("{}".format(input), align="center", font=("Arial", 26, "normal"))
                self._original_grid[self._clicked[0]][self._clicked[1]] = input
                self._inputs.append([self._position_to_draw[0], self._position_to_draw[1], input, self._clicked[0], self._clicked[1]])

    def draw_wrong_answers(self, start_x, start_y):
        """
        Draw red box for wrong or missing answers
        :param start_x: Starting x position to draw square
        :param start_y: Starting y position to draw square
        :return None
        """
        if not self._wrong_answers_drawn:
            self._wrong_marker.penup()
            self._wrong_marker.setpos(start_x, start_y)
            self._wrong_marker.pendown()
            self._wrong_marker.setpos(start_x, start_y + 2 * self._screen.window_height() / 18)
            self._wrong_marker.setpos(start_x + 2 * self._screen.window_width() / 18, start_y + 2 * self._screen.window_height() / 18)
            self._wrong_marker.setpos(start_x + 2 * self._screen.window_width() / 18, start_y)
            self._wrong_marker.setpos(start_x, start_y)
            self._wrong_marker.penup()
        else:
            self._wrong_marker.clear()

    def finished(self):
        """
        Checks if board is finished or if there are
        wrong or missing answers and highlights them
        :return None
        """
        self._correct = True
        for i in range(len(self._original_grid)):
            for j in range(len(self._original_grid[0])):
                if not self._original_grid[i][j] == self._solved_grid[i][j]:
                    self._correct = False
                    break
            if not self._correct:
                break
        if self._correct:
            self.win()
        else:
            not_finished = False
            for i in range(len(self._original_grid)):
                for j in range(len(self._original_grid[0])):
                    if self._original_grid[i][j] == 0:
                        not_finished = True
            if not_finished:
                if not self._found:
                    for i in range(len(self._original_grid)):
                        for j in range(len(self._original_grid[0])):
                            if self._original_grid[i][j] == 0:
                                self._wrong_answers_drawn = False
                                self.draw_wrong_answers(-(9 - j * 2)*self._screen.window_width()/18, (7 - i * 2) * self._screen.window_height()/18)
                                self._found = True
                else:
                    self._wrong_answers_drawn = True
                    self._found = False
                    self.draw_wrong_answers(0, 0)
            else:
                if not self._found:
                    for i in range(len(self._original_grid)):
                        for j in range(len(self._original_grid[0])):
                            if not self._original_grid[i][j] == self._solved_grid[i][j]:
                                self._wrong_answers_drawn = False
                                self.draw_wrong_answers(-(9 - j * 2) * self._screen.window_width() / 18, (7 - i * 2) * self._screen.window_height() / 18)
                                self._found = True
                else:
                    self._wrong_answers_drawn = True
                    self._found = False
                    self.draw_wrong_answers(0, 0)

    def draw_answer(self):
        """
        Draws the solution using the backtrack algorithm
        :return None
        """
        self._input_marker.clear()
        self.draw_original_grid()
        self._input_marker.color('purple')
        for i in range(len(self._original_grid)):
            for j in range(len(self._original_grid[0])):
                if self._copy_original_grid[i][j] == 0:
                    self._input_marker.setpos(-(8 - j*2)*self._screen.window_width()/18, (8 - i*2)*self._screen.window_height()/18 - self._screen.window_height()/18/2)
                    self._input_marker.write("{}".format(self._solved_grid[i][j]), align="center", font=("Arial", 26, "normal"))
                    time.sleep(.1)

    def number_one(self):
        """
        Handles the callback from the keyboard input 1
        :return None
        """
        self.draw_input_number(1)

    def number_two(self):
        """
        Handles the callback from the keyboard input 2
        :return None
        """
        self.draw_input_number(2)

    def number_three(self):
        """
        Handles the callback from the keyboard input 3
        :return None
        """
        self.draw_input_number(3)

    def number_four(self):
        """
        Handles the callback from the keyboard input 4
        :return None
        """
        self.draw_input_number(4)

    def number_five(self):
        """
        Handles the callback from the keyboard input 5
        :return None
        """
        self.draw_input_number(5)

    def number_six(self):
        """
        Handles the callback from the keyboard input 6
        :return None
        """
        self.draw_input_number(6)

    def number_seven(self):
        """
        Handles the callback from the keyboard input 7
        :return None
        """
        self.draw_input_number(7)

    def number_eight(self):
        """
        Handles the callback from the keyboard input 8
        :return None
        """
        self.draw_input_number(8)

    def number_nine(self):
        """
        Handles the callback from the keyboard input 9
        :return None
        """
        self.draw_input_number(9)

    def move_highlight_up(self):
        """
        Handles the callback from the keyboard input pressing Arrow Key Up
        :return: None
        """
        if self._position_highlighted is not None:
            if self._position_highlighted[1] < self._screen.window_height()/2 - 2*self._screen.window_height()/18:
                self._position_highlighted[1] += 2*self._screen.window_height()/18
                self.make_clicked_visible(self._position_highlighted[0], self._position_highlighted[1])
                self._clicked[0] -= 1
                self._position_to_draw[1] += 2 * self._screen.window_height() / 18

    def move_highlight_down(self):
        """
        Handles the callback from the keyboard input pressing Arrow Key Down
        :return: None
        """
        if self._position_highlighted is not None:
            if self._position_highlighted[1] > - self._screen.window_height()/2:
                self._position_highlighted[1] -= 2*self._screen.window_height()/18
                self.make_clicked_visible(self._position_highlighted[0], self._position_highlighted[1])
                self._clicked[0] += 1
                self._position_to_draw[1] -= 2 * self._screen.window_height() / 18

    def move_highlight_left(self):
        """
        Handles the callback from the keyboard input pressing Arrow Key Left
        :return: None
        """
        if self._position_highlighted is not None:
            if self._position_highlighted[0] > - self._screen.window_width() / 2:
                self._position_highlighted[0] -= 2 * self._screen.window_height() / 18
                self.make_clicked_visible(self._position_highlighted[0], self._position_highlighted[1])
                self._clicked[1] -= 1
                self._position_to_draw[0] -= 2 * self._screen.window_height() / 18

    def move_highlight_right(self):
        """
        Handles the callback from the keyboard input pressing Arrow Key Right
        :return: None
        """
        if self._position_highlighted is not None:
            if self._position_highlighted[0] < self._screen.window_width() / 2 - 2*self._screen.window_width()/18:
                self._position_highlighted[0] += 2 * self._screen.window_height() / 18
                self.make_clicked_visible(self._position_highlighted[0], self._position_highlighted[1])
                self._clicked[1] += 1
                self._position_to_draw[0] += 2 * self._screen.window_height() / 18

    def listen(self):
        """
        Binds the keyboard and mouse inputs
        :return None
        """
        self._screen.listen()
        # for python 2 and python 3
        if sys.version_info[0] < 3:
            self._screen.onscreenclick(self.find_position_on_grid)
            self._screen.onkey(self.quit, 'Escape')
            self._screen.onkey(self.delete_number, 'Delete')
            self._screen.onkey(self.finished, 'Return')
            self._screen.onkey(self.draw_answer, 'space')
            self._screen.onkey(self.move_highlight_up, 'Up')
            self._screen.onkey(self.move_highlight_down, 'Down')
            self._screen.onkey(self.move_highlight_left, 'Left')
            self._screen.onkey(self.move_highlight_right, 'Right')
            self._screen.onkey(self.reset, 'r')
            self._screen.onkey(self.reset, 'R')
            self._screen.onkey(self.number_one, '1')
            self._screen.onkey(self.number_two, '2')
            self._screen.onkey(self.number_three, '3')
            self._screen.onkey(self.number_four, '4')
            self._screen.onkey(self.number_five, '5')
            self._screen.onkey(self.number_six, '6')
            self._screen.onkey(self.number_seven, '7')
            self._screen.onkey(self.number_eight, '8')
            self._screen.onkey(self.number_nine, '9')
        else:
            self._screen.onclick(self.find_position_on_grid)
            self._screen.onkeypress(self.quit, 'Escape')
            self._screen.onkeypress(self.delete_number, 'Delete')
            self._screen.onkeypress(self.finished, 'Return')
            self._screen.onkeypress(self.draw_answer, 'space')
            self._screen.onkeypress(self.move_highlight_up, 'Up')
            self._screen.onkeypress(self.move_highlight_down, 'Down')
            self._screen.onkeypress(self.move_highlight_left, 'Left')
            self._screen.onkeypress(self.move_highlight_right, 'Right')
            self._screen.onkeypress(self.reset, 'r')
            self._screen.onkeypress(self.reset, 'R')
            self._screen.onkeypress(self.number_one, '1')
            self._screen.onkeypress(self.number_two, '2')
            self._screen.onkeypress(self.number_three, '3')
            self._screen.onkeypress(self.number_four, '4')
            self._screen.onkeypress(self.number_five, '5')
            self._screen.onkeypress(self.number_six, '6')
            self._screen.onkeypress(self.number_seven, '7')
            self._screen.onkeypress(self.number_eight, '8')
            self._screen.onkeypress(self.number_nine, '9')

    def run(self):
        """
        Main run loop
        :return None
        """
        while not self._done:
            self._screen.update()

    def reset(self):
        """
        Resets the board and draws the original generated board
        :return None
        """
        self._input_marker.clear()
        for inputs in self._inputs:
            self._original_grid[inputs[3]][inputs[4]] = 0
            self._copy_original_grid[inputs[3]][inputs[4]] = 0
        self._inputs = []
        self.draw_numbers()

    def quit(self):
        """
        Quits game
        :return None
        """
        self._done = True

    def win(self):
        """
        Draws the winning green boxes if the user solves the grid
        :return: None
        """
        win = turtle.Turtle()
        win.speed(0)
        win.pensize(10)
        win.color('green')
        win.hideturtle()
        for i in range(len(self._original_grid)):
            for j in range(len(self._original_grid[0])):
                self.make_clicked_visible(-(9 - j * 2) * self._screen.window_width() / 18, (7 - i * 2) * self._screen.window_height() / 18)
                win.penup()
                win.setpos(-(9 - j * 2) * self._screen.window_width() / 18, (7 - i * 2) * self._screen.window_height() / 18)
                win.pendown()
                win.setpos(-(9 - j * 2) * self._screen.window_width() / 18, (7 - i * 2) * self._screen.window_height() / 18 + 2 * self._screen.window_height() / 18)
                win.setpos(-(9 - j * 2) * self._screen.window_width() / 18 + 2 * self._screen.window_width() / 18, (7 - i * 2) * self._screen.window_height() / 18 + 2 * self._screen.window_height() / 18)
                win.setpos(-(9 - j * 2) * self._screen.window_width() / 18 + 2 * self._screen.window_width() / 18, (7 - i * 2) * self._screen.window_height() / 18)
                win.setpos(-(9 - j * 2) * self._screen.window_width() / 18, (7 - i * 2) * self._screen.window_height() / 18)
                win.penup()


class Sudoku:

    def __init__(self, grid):
        """
        Sudoku Class that solves a 9x9 grid using backtrack
        :return None
        """
        self._original_grid = np.asarray(grid)  # store original grid
        self._grid = np.asarray(grid)  # store grid that will be modified
        self._indexes = [0, 0]  # store indexes last input inserted
        self._solved = False  # flag to check if board is solved

    def __str__(self):
        """
        Handles the print calls
        :return: string containg the represantion of the class
        """
        if self._solved:
            full = 'Solving for:\n'
            full += 'ORIGINAL\n'
            full += "-" * 13 + '\n'
            full += '|'
            for i in range(len(self._original_grid)):
                for j in range(len(self._original_grid[0])):
                    if j % 3 == 0 and j != 0:
                        full += "|"
                    full += str(self._original_grid[i][j])
                full += '|\n'
                if i != 0 and (i + 1) % 3 == 0:
                    full += "-" * 13
                    full += '\n'
                if i != 8:
                    full += '|'
            full += "SOLVED\n"
            full += "-" * 13 + '\n'
            full += '|'
            for i in range(len(self._grid)):
                for j in range(len(self._grid[0])):
                    if j % 3 == 0 and j != 0:
                        full += "|"
                    full += str(self._grid[i][j])
                full += '|\n'
                if i != 0 and (i + 1) % 3 == 0:
                    full += "-" * 13
                    full += '\n'
                if i != 8:
                    full += '|'
        else:
            full = 'No solution for:\n'
            full += "-" * 13 + '\n'
            full += '|'
            for i in range(len(self._original_grid)):
                for j in range(len(self._original_grid[0])):
                    if j % 3 == 0 and j != 0:
                        full += "|"
                    full += str(self._original_grid[i][j])
                full += '|\n'
                if i != 0 and (i + 1) % 3 == 0:
                    full += "-" * 13
                    full += '\n'
                if i != 8:
                    full += '|'
        return full

    def solve(self, ret=False):
        """
        main function to solve the grid
        :param ret: Flag to return the solved grid
        :return: Boolean if solved
        """
        if self.backtrack():
            self._solved = True
            if ret:
                return self._grid
            return True
        else:
            if ret:
                return self._grid
            self._solved = False
            return False

    def move_to_next_cell(self, indexes):
        """
        Finds the next empty cell
        :return Boolean
        """
        for i in range(9):
            for j in range(9):
                if self._grid[i][j] == 0:
                    indexes[0] = i
                    indexes[1] = j
                    return True
        return False

    def check_location(self, indexes, number):
        """
        Checks if input number follows sudoku rules for row, grid, box
        :param indexes: Position of inserted number
        :param number:  inserted number
        :return: Boolean
        """
        for i in range(9):
            if self._grid[indexes[0]][i] == number:
                return False

        for i in range(9):
            if self._grid[i][indexes[1]] == number:
                return False

        for i in range(3):
            for j in range(3):
                if self._grid[i + (indexes[0] // 3) * 3][j + (indexes[1] // 3) * 3] == number:
                    return False

        return True

    def backtrack(self):
        """
        Backtrack algorithm with regression to solve the 9x9 board
        :return: boolean if solution is correct or not
        """
        indexes = [0, 0]

        if not self.move_to_next_cell(indexes):
            return True

        for number in range(1, 10):

            if self.check_location(indexes, number):

                self._grid[indexes[0]][indexes[1]] = number

                if self.backtrack():
                    return True

                self._grid[indexes[0]][indexes[1]] = 0

        return False


if __name__ == "__main__":

    a = Game()
    a.run()