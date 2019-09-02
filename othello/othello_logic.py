# Marissa Salcido 86569875 salcidom

class GameState():
    
    def winning_value(self, winning_choice: str) -> None:
        '''sets the winning rule attribute'''
        self._win_choice = winning_choice
        
    def check_winner(self) -> str:
        '''compares the player's scores and checks if there is a winner'''
        b_count, w_count = self.count_discs()
        if self._win_choice == '>':
            if b_count > w_count:
                return 'B'
            elif w_count > b_count:
                return 'W'
            else:
                return 'NONE'
        elif self._win_choice == '<':
            if b_count < w_count:
                return 'B'
            elif w_count < b_count:
                return 'W'
            else:
                return 'NONE'
            
    def check_player_passes(self) -> str:
        '''checks if each player can make a move and returns NONE if no more available moves'''
        if not self._check_available_moves():
            self._turn = self.change_player_turn(self._turn)
            if not self._check_available_moves():
                return 'NONE' 
            
    def _check_available_moves(self) -> bool:
        '''checks if there are any more available moves after each player makes their turn'''
        available_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == '.':
                    if self._check_valid_moves(row, col):
                        available_moves.append('TRUE')
        if 'TRUE' in available_moves:
            return True

    def turn(self, player_turn: str) -> None:
        '''sets the player's turn to the attribute self._turn'''
        self._turn = player_turn
        
    def display_turn(self) -> str:
        '''returns the value 'turn' to be displayed to the players'''
        return self._turn
    
    def change_player_turn(self, turn: str) -> str:
        '''returns the opposite color depending on the current player's turn'''
        if turn == 'B':
            return 'W'
        else:
            return 'B'

    def init_board(self, rows: int, cols: int) -> None:
        '''initializes the board dimensions and defines the board value'''
        board = []
        self._temp_board = []
        for row in range(rows):
            single_row = []
            for col in range(cols):
                single_row.append('.')
            board.append(single_row)
        self.board = board   

    def count_discs(self) -> int:
        '''counts the number of 'W's and 'B's on the board that represent each player's total points'''
        B_count = 0
        W_count = 0
        for row in self.board:
            for element in row:
                if element == 'B':
                    B_count += 1
                elif element == 'W':
                    W_count += 1
        return B_count, W_count

    def _check_row_col(self, row: int, col: int) -> bool:
        '''checks if the player's input is a valid row and column on the board'''
        if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
            return True
        
    
    def _change_col_row(self, row: int, col: int, rowdelta: int, coldelta: int) -> int:
        '''if the player move is a valid point on the board, the function adds rowdelta, coldelta
            to the point to be used to recursively check each point in a  direction'''
        row = row + rowdelta
        col = col + coldelta
        if self._check_row_col(row, col):
            current_position = self.board[row][col]
            return current_position
        else:
            return '.'
        
    def _check_valid_moves(self, row: int, col: int) -> bool:
        '''checks if a move can be made in any direction'''
        directions = [[row, col, 0, 1], [row, col, 1, 0], [row, col, 0, -1], [row, col, -1, 0],
                      [row, col, 1, 1], [row, col, -1, -1], [row, col, -1, 1], [row, col, 1, -1]]
        filtered_lst = []
        for direction in directions:
            row, col, rowdelta, coldelta = direction[0], direction[1], direction[2], direction[3]
            if self._check_trail(direction[0], direction[1], direction[2], direction[3]):
                filtered_lst.append('TRUE')
            elif not self._check_trail(direction[0], direction[1], direction[2], direction[3]):
                continue
        if 'TRUE' in filtered_lst:
            return True

    def _check_trail(self, row: int, col: int, rowdelta: int, coldelta: int) -> bool:
        '''checks if the points surrounding the player's move has a valid direction to execute
            the player's move'''
        current_pos = self._change_col_row(row, col, rowdelta, coldelta)
        opp_pos = self.change_player_turn(self._turn)
        if current_pos == opp_pos:
            next_row, next_col = self._recursive_row_col(row, col, rowdelta, coldelta)
            valid_trail = self._trail(next_row, next_col, rowdelta, coldelta)
            return valid_trail
      
    def _trail(self, row: int, col: int, rowdelta: int, coldelta: int) -> bool:
        '''recursively checks each point in a direction to see if any discs in the direction can be
            changed'''
        if self._change_col_row(row, col, rowdelta, coldelta) == self.change_player_turn(self._turn):
            next_row, next_col = self._recursive_row_col(row, col, rowdelta, coldelta)
            return self._trail(next_row, next_col, rowdelta, coldelta)
        elif self._change_col_row(row, col, rowdelta, coldelta) == self._turn:
            return True

    def _check_move(self, row: int, col: int) -> bool:
        '''checks if the player's row and col input is valid'''
        if self._check_row_col(row, col):
            if self.board[row][col] == '.':
                if self._check_valid_moves(row, col):
                    return True
        
        
    def player_move(self, row: int, col: int) -> bool:
        '''executes the player's move'''
        if self._check_move(row, col):
            self.board[row][col] = self._turn
            self._change_discs_in_dir(row, col)
            return True
        
    def _change_discs_in_dir(self, row: int, col: int) -> None:
        '''checks if each direction can be changed to the player's color and continues with
            recursive function that changes the color on the board if the direction is True'''
        directions = [[row, col, 0, 1], [row, col, 1, 0], [row, col, 0, -1], [row, col, -1, 0],
                      [row, col, 1, 1], [row, col, -1, -1], [row, col, -1, 1], [row, col, 1, -1]]
        for direction_set in directions:
            row, col, rowdelta, coldelta = direction_set[0], direction_set[1], direction_set[2], direction_set[3]
            if self._check_trail(direction_set[0], direction_set[1], direction_set[2], direction_set[3]):
                next_row, next_col = self._recursive_row_col(row, col, rowdelta, coldelta)
                self._change_disc_color(next_row, next_col, rowdelta, coldelta)
            elif not self._check_trail(direction_set[0], direction_set[1], direction_set[2], direction_set[3]):
                continue
            
    def _change_disc_color(self, row: int, col: int, rowdelta: int, coldelta: int) -> None:
        '''recursively checks each point in any a direction on the board and turns each
            opposite color, either 'W' or 'B', depending on the player's turn'''
        if self.board[row][col] == self.change_player_turn(self._turn):
            self.board[row][col] = self._turn
            next_row, next_col = self._recursive_row_col(row, col, rowdelta, coldelta)
            self._change_disc_color(next_row, next_col, rowdelta, coldelta)
            
    def _recursive_row_col(self, row: int, col: int, rowdelta: int, coldelta: int) -> int:
        '''returns the next row and column that defines the next point on the board for a recursive
            search of each point in any direction'''
        next_row = row + rowdelta
        next_col = col + coldelta
        return next_row, next_col

