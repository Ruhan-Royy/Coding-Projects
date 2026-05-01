#Stores board, applies move, undo moves, check legal, serializez board state

from __future__ import annotations

from typing import List, Optional, Tuple

from pieces import (
    Bishop,
    King,
    Knight,
    Move,
    Pawn,
    Piece,
    Queen,
    Rook,
    in_bounds,
    parse_square,
    piece_from_symbol,
    symbol_from_piece,
)

Square = Tuple[int, int]


class Board:
    def __init__(self, setup: bool = True):
        self.grid: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        #create grid
        self.turn: str = "w" #White moves first
        self.history: List[Move] = []#Stores moves for undo and logging
        if setup:
            self.setup_start() #Initialize board

    @staticmethod
    def opposite(color: str) -> str:
        #Returns opposite side
        return "b" if color == "w" else "w"

    def setup_start(self) -> None:
        #Place piece in position
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c, cls in enumerate(back_rank):
            self.grid[7][c] = cls("w")
            self.grid[0][c] = cls("b")
        for c in range(8):
            self.grid[6][c] = Pawn("w")
            self.grid[1][c] = Pawn("b")
        self.turn = "w"
        self.history.clear()

    def clone(self) -> "Board":
        #Creates a deep copy of the board so changes to the copy do not affect the original.
        b = Board(setup=False)
        b.turn = self.turn
        b.grid = [[p.copy() if p is not None else None for p in row] for row in self.grid]
        return b

    def piece_at(self, r: int, c: int) -> Optional[Piece]:
        #Returns piece at square
        if not in_bounds(r, c):
            return None
        return self.grid[r][c]

    def king_pos(self, color: str) -> Optional[Square]:
        #Finds king for color
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None and p.color == color and isinstance(p, King):
                    return (r, c)
        return None

    def square_attacked(self, r: int, c: int, by_color: str) -> bool:
        #Checkif square is attacked by color,
        #Loops through all pieces of color and checks whether any attached square matches
        for rr in range(8):
            for cc in range(8):
                p = self.grid[rr][cc]
                if p is None or p.color != by_color:
                    continue
                for ar, ac in p.attacks(self, rr, cc):
                    if (ar, ac) == (r, c):
                        return True
        return False

    def in_check(self, color: Optional[str] = None) -> bool:
        #Determine if color isin chechk
        if color is None:
            color = self.turn
        kpos = self.king_pos(color)
        if kpos is None:
            return False
        return self.square_attacked(kpos[0], kpos[1], self.opposite(color))

    def apply_move(self, move: Move) -> None:
        """
        Apply a move to the board.

        Parameters:
            move: a Move object containing start and end positions

        Output:
            None (the board is modified directly)

        Rules:
            - Move the piece from its start position to its end position
            - If a piece exists at the destination -> it is captured
            - The starting square must become empty
            - Update the board state correctly
            - Do not create a new board
            ● must store moved_piece, captured_piece, and previous turn in move
            ● must append move to history

        Hint:
            Access the piece using its starting position, then update both squares.
        """

        start_row, start_column = move.src #Get starting position and ending position of pieces
        end_row, end_column = move.dst
        piece = self.grid[start_row][start_column] #Getting the piece at the start square

        move.moved_piece = piece #Information for the undo function
        move.prev_turn = self.turn
        move.captured_piece = self.grid[end_row][end_column]

        self.grid[start_row][start_column] = None #Moving piece clearing the previous square and piece on new square
        self.grid[end_row][end_column] = piece

        if move.promotion is not None: #Handle pawn promotion to on board
            if move.promotion == 'q':
                self.grid[end_row][end_column] = Queen(piece.color)
            elif move.promotion == 'r':
                self.grid[end_row][end_column] = Rook(piece.color)
            elif move.promotion == 'b':
                self.grid[end_row][end_column] = Bishop(piece.color)
            elif move.promotion == 'n':
                self.grid[end_row][end_column] = Knight(piece.color)
        else:
            if isinstance(piece, Pawn) and (end_row == 0 or end_row == 7): #Defualt to queen if no promotion stated
                self.grid[end_row][end_column] = Queen(piece.color)

        if self.turn == "w": #This is for switching turns white then black
            self.turn = 'b'
        else:
            self.turn = 'w'

        self.history.append(move) #Adding move to history for undo function


    def undo_move(self, move: Move) -> None:
        #Restores moving piece to source, capture piece to dest, previous turn
        sr, sc = move.src
        dr, dc = move.dst
        if move.prev_turn is None:
            raise ValueError("Move does not contain undo information")
        self.turn = move.prev_turn
        self.grid[sr][sc] = move.moved_piece
        self.grid[dr][dc] = move.captured_piece
        if self.history and self.history[-1] == move:
            self.history.pop()

    def undo_last(self) -> Move:
        #Undo recent
        if not self.history:
            raise ValueError("No moves to undo")
        move = self.history[-1]
        self.undo_move(move)
        return move

    def generate_pseudo_legal_moves(self) -> List[Move]:
        """
        Generate all pseudo-legal moves for the current player.

        Parameters:
            None (uses the current board state)

        Output:
            A list of Move objects representing all possible moves.

        Rules:
            - Loop through all squares on the board
            - For each piece belonging to the current player:
                 Call its pseudo_legal_moves() function
            - Combine all moves into one list
            - Do not modify the board

        Hint:
            Check piece color before generating moves.
        """

        available_moves = [] #Makes a list to store all legal moves
        for row in range(8): #Loops every row 0-7
            for column in range(8): #Loops every column 0-7
                piece = self.piece_at(row,column) #Capture piece at square or nothing if empty

                if piece is not None and piece.color == self.turn: #Checks if piece is there and belongs to mover
                    move = piece.pseudo_legal_moves(self,row,column) #Gets legal move from position
                    available_moves.extend(move) #Adds move

        return available_moves #Return list of legal moves

    def generate_legal_moves(self) -> List[Move]:
        """
        Generate all legal moves for the current player.

        Parameters:
            None

        Output:
            A list of Move objects representing legal moves.

        Rules:
            - Start with pseudo-legal moves
            - For each move:
                 Apply the move temporarily
                 Check if the player is in check
                 If still in check → discard move
                 Otherwise → keep move
            - Undo the move after checking
            - Do not permanently modify the board

        Hint:
            Use apply_move() and undo functionality if available.
        """

        legal = []
        for move in self.generate_pseudo_legal_moves():
            # try the move, check if our king is now in check
            self.apply_move(move)
            still_in_check = self.in_check(self.opposite(self.turn))
            self.undo_move(move)
            if not still_in_check:
                legal.append(move)
        return legal

    def is_game_over(self) -> bool:
        """
        Determine whether the game has ended.

        Parameters:
            None

        Output:
            True if the game is over, False otherwise.

        Rules:
            - Game is over if:
                 The current player has no legal moves
                
            - Do not modify the board

        Hint:
            Check if there are no legal moves
        """

        return len(self.generate_legal_moves()) == 0

    def result(self) -> str:

        """
        Return the result of the game.

        Parameters:
            None

        Output:
            ● "ongoing"
            ● "<opposite side> wins by checkmate"
            ● "draw by stalemate"

        Rules:
            
        - If no legal moves exist:
            If in check → opponent wins
            Otherwise → draw (stalemate)

        Hint:
            Use is_game_over() and in_check() to decide.
        """

        if not self.is_game_over(): #If there is still legal moves
            return "ongoing"
        if self.in_check(self.turn): #If no legal moves and in check
            winner = "b" if self.turn == "w" else "w" #Opposite side win
            return f"{winner} wins by checkmate"
        return "draw by stalemate" #No legal move and not in check

    def position_key(self) -> str:
        #Builds a string representation of the board plus side to move.
        rows = []
        for r in range(8):
            rows.append("".join(symbol_from_piece(p) for p in self.grid[r]))
        return f"{self.turn}|" + "/".join(rows)

    def to_text(self) -> str:
        #Serialize board to plain text
        lines = [f"turn {self.turn}"]
        for r in range(8):
            lines.append("".join(symbol_from_piece(p) for p in self.grid[r]))
        return "\n".join(lines) + "\n"

    @classmethod
    def from_text(cls, text: str) -> "Board":
        #Loads board from text
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        if len(lines) < 9:
            raise ValueError("Position file must contain one turn line and 8 board lines")
        first = lines[0].split()
        if len(first) != 2 or first[0].lower() != "turn" or first[1] not in ("w", "b"):
            raise ValueError("First line must be 'turn w' or 'turn b'")
        board = cls(setup=False)
        board.turn = first[1]
        if len(lines[1:9]) != 8:
            raise ValueError("Board must have 8 rows")
        for r in range(8):
            row = lines[1 + r]
            if len(row) != 8:
                raise ValueError(f"Row {r+1} must have exactly 8 characters")
            for c, ch in enumerate(row):
                board.grid[r][c] = piece_from_symbol(ch)
        return board

    def __str__(self) -> str:
        #Create display
        out = []
        out.append("    a   b   c   d   e   f   g   h")
        out.append("  +---+---+---+---+---+---+---+---+")
        for r in range(8):
            rank = 8 - r
            cells = []
            for c in range(8):
                p = self.grid[r][c]
                cells.append(f" {symbol_from_piece(p)} ")
            out.append(f"{rank} |" + "|".join(cells) + f"| {rank}")
            out.append("  +---+---+---+---+---+---+---+---+")
        out.append("    a   b   c   d   e   f   g   h")
        out.append(f"Turn: {'White' if self.turn == 'w' else 'Black'}")
        if self.in_check(self.turn):
            out.append("Check!")
        return "\n".join(out)

    def try_parse_move(self, text: str) -> Move:
        """
        Convert a user input string into a Move object.

        Parameters:
            text: a string representing a move (e.g., "e2e4")

        Output:
            A Move object if valid, Raises an error if the input is invalid

        Rules:
            - Extract starting and ending positions from the string
            - Convert letters to columns (a=0, b=1, etc.)
            - Convert numbers to rows
            - Raise an error if input is invalid

        Hint:
            Carefully map chess notation to array indices.
        """

        #Converting files (a-h) to columns (0-7)
        letters_to_numbers = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5,'g':6,'h':7} #Dictionary

        move_input = text.strip().lower() #Stripping the unwanted spaces and making letters lowercase

        if len(move_input) !=4 and len(move_input) != 5: #Checking if move 4 characters or 5 if promotion
            raise ValueError("The input is invalid")

        start_square = move_input[0:2] #Splitting notation by first 2 char and last 2 char
        end_square = move_input[2:4]

        start_column = start_square[0] #Getting starting column (letter) and row (num)
        end_column = end_square[0]

        start_row = start_square[1] #Getting row numbers 1-8
        end_row = end_square[1]

        if start_column not in letters_to_numbers: #Confirm start column and ELSE converting to letter
            raise ValueError("The input is invalid, column must be a-h")
        else:
            start_column_num = letters_to_numbers[start_column]

        if start_row not in '12345678': #Confirm start row and convert to board row
            raise ValueError("The input is invalid, row must be 1-8")
        else: start_row_num = 8 - int(start_row)

        if end_column not in letters_to_numbers: #Confirming end column and converting to letter
            raise ValueError("The input is invalid, column must be a-h")
        else:
            end_column_num = letters_to_numbers[end_column]

        if end_row not in '12345678': #Confirming end row and converting to board row
            raise ValueError("The input is invalid, row must be 1-8")
        else:
            end_row_num = 8 - int(end_row)

        promotion = None #Does promotion piece only if 5 character move
        if len(move_input) == 5:
            promote = move_input[4] #Retrieve 5th letter for promotion
            if promote not in ['q', 'r', 'b', 'n']: #Throw error if not a piece to promote
                raise ValueError("The input is invalid, promotion must be queen, rook, bishop or knight.")
            promotion = promote

        legal_moves = self.generate_legal_moves() #Gets the legal moves from board position

        for move in legal_moves: #Search for move that matches coordinates
            if move.src[0] == start_row_num and move.src[1] == start_column_num and move.dst[0] == end_row_num and move.dst[1] == end_column_num:
                if promotion is not None: #If there is a promotion move, confirm it with promotion piece
                    if move.promotion == promotion:
                        return move
                else: #No promotion move
                    if move.promotion is None:
                        return move

        raise ValueError(f"This is an invalid move at {move_input}") #Shows error if move is illegal




    def play_move_text(self, text: str) -> Move:
        #Parse move, apply, return move
        move = self.try_parse_move(text)
        self.apply_move(move)
        return move
