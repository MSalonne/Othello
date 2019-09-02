# Marissa Salcido 86569875
import tkinter
import othello_logic
FONT = 'Helvetica', 15
SETUP_FONT = 'Helvetica', 10
class OthelloGameGui:
    def __init__(self):
        self._color = 'black'
        self.state = othello_logic.GameState()
        self._root_window = tkinter.Tk()
        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.rowconfigure(2, weight = 0)
        self._root_window.columnconfigure(0, weight = 1)
        self._canvas = tkinter.Canvas(master = self._root_window, width = 400,
                                      height = 400, background = 'green')
        self._canvas.grid(row = 1, column = 0,
                          sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._top_frame = tkinter.Frame(master = self._root_window)
        self._top_frame.grid(row = 0, column = 0,
                             sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._turn_display = tkinter.Label(master = self._top_frame, text = '',
                                           font = FONT)
        self._turn_display.grid(row = 0, column = 0, sticky = tkinter.W)
        self._score_display = tkinter.Label(master = self._top_frame, font = (FONT),
                                            text = '')
        self._score_display.grid(row = 0, column = 1, sticky = tkinter.E)
        self._top_frame.rowconfigure(0, weight = 0)
        self._top_frame.columnconfigure(0, weight = 1)
        self._top_frame.columnconfigure(1, weight = 1)
        self._frame = tkinter.Frame(master = self._root_window)
        self._frame.grid(row = 2, column = 0,
                         sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        full_txt = tkinter.Label(master = self._frame, text = 'Full Othello',
                                   font = FONT)
        full_txt.grid(row = 0, column = 2, sticky = tkinter.E)
        self._frame.rowconfigure(0, weight = 0)
        self._frame.columnconfigure(0, weight = 1)
        self._frame.columnconfigure(2, weight = 1)
        
    def _display_turn(self):
        '''displays the turn in the gui'''
        turn = self.state.display_turn()
        self._turn_display['text'] = f'TURN: {turn}'
        
    def _display_score(self):
        '''displayes the score to the gui'''
        b_score, w_score = self.state.count_discs()
        self._score_display['text'] = f' BLACK SCORE: {b_score}  WHITE SCORE: {w_score} '
       
    def setup_complete(self):
        '''allows the player to choose the parameters of the game'''
        self._row = setup._rows
        self._col = setup._cols
        self.state.winning_value(setup._win_cond)
        self.state.turn(setup._player_turn)
        self.state.init_board(self._row, self._col)
        self.draw_board()
        self._setup_board()
        self._display_turn()
        self._display_score()
        
    def _start_game(self):
        '''sets up the pieces, first move, and score to begin the game'''
        self._start.grid_remove()
        self._choose_color.grid_remove()
        self._display_score()
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self.check_next_move()
                
    def _setup_board(self):
        '''adds buttons to change the disc color and allows the player to place the initial discs'''
        self._start = tkinter.Button(master = self._frame, text = 'Start',
                                     font = (FONT),
                                     command = self._start_game)
        self._start.grid(row = 1, column = 2, sticky = tkinter.E, padx = 10, pady = 10)
        self._choose_color = tkinter.Button(master = self._frame,
                                            text = 'Click to place white discs',
                                            font = FONT,
                                            command = self._change_disc_color)
        self._choose_color.grid(row = 1, column = 0, sticky = tkinter.W, padx = 10, pady = 10)
        self._canvas.bind('<Button-1>', self._init_discs)
        
    def _init_discs(self, event: tkinter.Event):
        '''places the starting discs on the board based on the button click event
            within the area of a rectangle on the board'''
        width = self._canvas.winfo_width() / self._col
        height = self._canvas.winfo_height() / self._row
        for row in range(self._row):
            for col in range(self._col):
                x_zero = width * (col)
                y_zero = height * (row)
                x_one = width * (col+1)
                y_one = height * (row+1)
                if event.x > x_zero and event.x < x_one and event.y > y_zero and event.y < y_one:
                    if self.state.board[row][col] == '.':
                        self._canvas.create_oval(x_zero, y_zero, x_one, y_one, fill = self._color)
                        if self._color == 'black':
                            self.state.board[row][col] = 'B'
                        else:
                            self.state.board[row][col] = 'W'

    def _change_disc_color(self):
        '''changes the color attribute'''
        if self._color == 'black':
            self._color = 'white'
            self._choose_color['text'] = 'Click to place black discs'
        else:
            self._color = 'black'
            self._choose_color['text'] = 'Click to place white discs'
                                            
    def _on_canvas_clicked(self, event):
        '''checks within which rectangle the click event occurred and checks if the move is valid
            in that rectangle'''
        width = self._canvas.winfo_width() / self._col
        height = self._canvas.winfo_height() / self._row
        for row in range(self._row):
            for col in range(self._col):
                x_zero = width * (col)
                y_zero = height * (row)
                x_one = width * (col+1)
                y_one = height * (row+1)
                if event.x > x_zero and event.x < x_one and event.y > y_zero and event.y < y_one:
                    if self.state.player_move(row, col):
                        self._handle_click(row, col)
                    
    def _handle_click(self, row: int, col: int):
        '''translates the player's move to the board and checks if the game is over after a turn'''
        self.draw_board()
        self.state.turn(self.state.change_player_turn(self.state.display_turn()))
        self.check_next_move()
    
    def check_next_move(self):
        '''ends the game and displays the win results, else display the current board'''
        if self.state.check_player_passes() == 'NONE':
            self._display_score()
            self._winner()
            
        else:
            self._display_turn()
            self._display_score()
  
    def _on_canvas_resized(self, event):
        '''redraws the board when the canvas is resized'''
        try:
            self.draw_board()
        except:
            pass
        
    def draw_board(self):
        '''draws the board depending on the current board stored in self.state.board'''
        self._canvas.delete(tkinter.ALL)
        width = self._canvas.winfo_width() / self._col
        height = self._canvas.winfo_height() / self._row
        for row in range(self._row):
            for col in range(self._col):
                x_zero = width * (col)
                y_zero = height * (row)
                x_one = width * (col+1)
                y_one = height * (row+1)
                self._canvas.create_rectangle(x_zero, y_zero, x_one, y_one)
                if self.state.board[row][col] == '.':
                    continue
                elif self.state.board[row][col] == 'W':
                    self._canvas.create_oval(x_zero, y_zero, x_one, y_one, fill = 'white')
                else:
                    self._canvas.create_oval(x_zero, y_zero, x_one, y_one, fill = 'black')
                    
    def run(self) -> None:
        '''maintains game on infinite loop until destroyed'''
        self._root_window.mainloop()
  
    def _winner(self):
        '''displays the winner or a tie'''
        winner = self.state.check_winner()
        if winner == 'NONE':
            self._turn_display['text'] = 'It is a tie!'
        elif winner == 'B':
            self._turn_display['text'] = 'Black wins!'
        else:
            self._turn_display['text'] = 'White wins!'

class OthelloSetup:
    def __init__(self):
        self._window = tkinter.Tk()
        for i in range(0,6):
            self._window.rowconfigure(i, weight = 1)
            
        self._window.columnconfigure(0, weight = 1)
        self._window.columnconfigure(1, weight = 1)
        self._othello_text = tkinter.Label(master = self._window,
                                           text = 'Othello Setup',
                                           font = (SETUP_FONT),
                                           justify = tkinter.LEFT)
        
        self._othello_text.grid(row = 0, column = 0, padx = 10, pady = 10,
                                sticky = tkinter.W)
        
        row_col_text = tkinter.Label(master = self._window,
                                           text = 'Choose the number of rows',
                                           font = (SETUP_FONT),
                                           justify = tkinter.LEFT)
        row_col_text.grid(row = 1,column = 0,padx = 10,sticky = tkinter.W)
        self._choose_row = tkinter.Listbox(master = self._window,
                                           selectmode = tkinter.SINGLE,
                                           justify = tkinter.LEFT,
                                           exportselection = 0)
        self._choose_row.bind('<<ListboxSelect>>', self.set_row)
        for i in range(2,17,2):
            self._choose_row.insert(i, "{}".format(i))
            
        self._choose_row.grid(row = 2, column = 0, padx = 10,
                              sticky = tkinter.W)
        
        choose_col_text = tkinter.Label(master = self._window,
                                              text = 'Choose the number of columns',
                                              font = (SETUP_FONT),
                                              justify = tkinter.LEFT)

        choose_col_text.grid(row = 3, column = 0, padx = 10,
                                   sticky = tkinter.W)

        self._choose_col = tkinter.Listbox(master = self._window,
                                           selectmode = tkinter.SINGLE,
                                           justify = tkinter.LEFT,
                                           exportselection = 0)
        self._choose_col.bind('<<ListboxSelect>>', self.set_col)
        for i in range(2,17,2):
            self._choose_col.insert(i, "{}".format(i))
        self._choose_col.grid(row = 4, column = 0, padx = 10,
                              sticky = tkinter.W)

        player_turn_text = tkinter.Label(master = self._window,
                                              text = 'Choose which player goes first',
                                              font = (SETUP_FONT),
                                              justify = tkinter.LEFT)
        
        player_turn_text.grid(row = 1, column = 1, padx = 10,
                                   sticky = tkinter.W)
        self._player_turn = tkinter.Listbox(master = self._window,
                                            selectmode = tkinter.SINGLE,
                                            justify = tkinter.LEFT,
                                            exportselection = 0)
        self._player_turn.bind('<<ListboxSelect>>', self.set_first_turn)
        self._player_turn.insert(1, 'B')
        self._player_turn.insert(2, 'W')
        self._player_turn.grid(row = 2, column = 1, padx = 10,
                               sticky = tkinter.W)
        win_value_text = tkinter.Label(master = self._window,
                                              text = 'Choose if a player wins by fewer (<) or more (>) discs',
                                              font = (SETUP_FONT),
                                              justify = tkinter.LEFT)
        
        win_value_text.grid(row = 3, column = 1, padx = 10,
                                   sticky = tkinter.W)
        self._win_value = tkinter.Listbox(master = self._window,
                                          selectmode = tkinter.SINGLE,
                                          justify = tkinter.LEFT,
                                          exportselection = 0)
        self._win_value.bind('<<ListboxSelect>>', self.set_win_var)
        self._win_value.insert(1, '<')
        self._win_value.insert(2, '>')
        self._win_value.grid(row = 4, column = 1, padx = 10,
                             sticky = tkinter.W)
        self._start = tkinter.Button(master = self._window,
                                     text = 'Start Disc Placement',
                                     font = (SETUP_FONT),
                                     command = self._start_game_clicked)
        self._start.grid(row = 5, column = 0, padx = 10, pady = 10,
                         sticky = tkinter.W)
        self._rows = None
        self._cols = None
        self._player_turn = None
        self._win_cond = None
    def set_first_turn(self, event):
        '''sets the initial turn'''
        self._player_turn = self.set_variable(event)
    def set_win_var(self, event):
        '''sets the winning value'''
        self._win_cond = self.set_variable(event)
    def set_row(self, event):
        '''sets the attribute for rows'''
        self._rows = int(self.set_variable(event))
    def set_col(self, event):
        '''sets the attribute for columns'''
        self._cols = int(self.set_variable(event))
    def set_variable(self, event):
        '''returns the result based on what the player chose in the setup window'''
        event_feedback = event.widget
        result = event_feedback.curselection()
        return event_feedback.get(result[0])
    def _start_game_clicked(self):
        '''exits the setup window once all choices have been made'''
        if self._rows == None or self._cols == None or self._player_turn == None or self._win_cond == None:
            return 
        else:
            game = OthelloGameGui()
            game.setup_complete()
            self._window.destroy()
            
        

if __name__ == '__main__':
    setup = OthelloSetup()
    
