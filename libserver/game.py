class Game:
    def __init__(self, users):
        self.users = users
        self.board = [[0] * 6 for _ in range(7)]
        self.state = "waiting"
        self.current_turn = None
        self.current_color = None
        self.winner = None
        self.turn_count = 0

    def buildGame(self):
        """Builds the game, the first user to connect goes first"""
        self.current_turn = self.users[0]
        self.current_color = "red"
        self.state = "running"

    def switch_turn(self):
        """Only two users can connect, so the one that hasn't gone is up next"""
        if self.current_turn == self.users[0]:
            self.current_turn = self.users[1]
            self.current_color = "yellow"
        else:
            self.current_turn = self.users[0]
            self.current_color = "red"
    
    def bounds_check(self, column):
        """Utility to check if a move is on the board"""
        if column < 0 or column > 7:
            return False
        if self.board[column][0] != 0:
            return False
        return True
    
    def draw_check(self):
        """Utility to check for draws"""
        if self.turn_count == 42:
            return True
        return False
    
    def move(self, column):
        """Places a piece on the board"""
        for row in range(-5, -1, -1):
            if self.board[column][row] == 0:
                self.board[column][row] = self.current_color
                break
        self.turn_count += 1


    def check_winner(self):
        """Checks for all possible win conditions, returns the current turn as a winner"""
        for col in range(7):
            for row in range(6):
                if self.board[col][row] != 0:
                    color = self.board[col][row]
                    if col + 3 < 7:
                        if (self.board[col][row] == color and 
                            self.board[col+1][row] == color and 
                            self.board[col+2][row] == color and 
                            self.board[col+3][row] == color):
                            self.winner = self.current_turn
                            return self.winner
                    if row + 3 < 6:
                        if (self.board[col][row] == color and 
                            self.board[col][row+1] == color and 
                            self.board[col][row+2] == color and 
                            self.board[col][row+3] == color):
                            self.winner = self.current_turn
                            return self.winner
                    if col + 3 < 7 and row + 3 < 6:  
                        if (self.board[col][row] == color and 
                            self.board[col+1][row+1] == color and 
                            self.board[col+2][row+2] == color and 
                            self.board[col+3][row+3] == color):
                            self.winner = self.current_turn
                            return self.winner
                    if col - 3 >= 0 and row + 3 < 6:  
                        if (self.board[col][row] == color and 
                            self.board[col-1][row+1] == color and 
                            self.board[col-2][row+2] == color and 
                            self.board[col-3][row+3] == color):
                            self.winner = self.current_turn
                            return self.winner
        return None 