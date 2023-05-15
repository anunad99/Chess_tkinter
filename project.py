import tkinter
from tkinter import ttk
import chess


class Board(tkinter.Tk):

    def __init__(self):
        super().__init__()

        # Configuring the main window
        self.title('CHESS')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width}x{screen_height}')
        self.resizable(False, False)

        # Making a main_frame canvas on which all the widgets will be placed
        self.main_frame = tkinter.Canvas(self)
        self.main_frame.grid(row=0, padx=350, pady=20)

        self.result_label = tkinter.Label(self.main_frame, width=20, height=5, background='gold', compound='center')
        self.result_label.grid(row=4, column=9, columnspan=4, padx=180)

        # Creating dictionaries for files and ranks
        self.file_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

        self.rank_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}

        # Create a dictionary for the pieces and their images
        self.white_pieces = {'P': tkinter.PhotoImage(file='Images/P.png'),
                             'R': tkinter.PhotoImage(file='Images/R.png'),
                             'N': tkinter.PhotoImage(file='Images/N.png'),
                             'B': tkinter.PhotoImage(file='Images/B.png'),
                             'Q': tkinter.PhotoImage(file='Images/Q.png'),
                             'K': tkinter.PhotoImage(file='Images/K.png'),
                             }

        self.black_pieces = {'p': tkinter.PhotoImage(file='Images/p.png'),
                             'r': tkinter.PhotoImage(file='Images/r.png'),
                             'n': tkinter.PhotoImage(file='Images/n.png'),
                             'b': tkinter.PhotoImage(file='Images/b.png'),
                             'q': tkinter.PhotoImage(file='Images/q.png'),
                             'k': tkinter.PhotoImage(file='Images/k.png'),
                             }

        # Create a dictionary for all the pieces together
        # Dictionary is initialised with a square_key as '0' with value of null image
        # so that the square buttons do not behave weirdly. This key also helps to fill
        # the empty squares and to remove a piece from the square
        null_image = tkinter.PhotoImage('')
        self.all_pieces = {'0': null_image}

        for key, value in self.white_pieces.items():
            self.all_pieces[key] = value
        for key, value in self.black_pieces.items():
            self.all_pieces[key] = value

        self.promoted_piece = 'q'

        # Create a dictionary for the current/starting postion
        self.position_on_board = {
            'a8': 'r', 'b8': 'n', 'c8': 'b', 'd8': 'q', 'e8': 'k', 'f8': 'b', 'g8': 'n', 'h8': 'r',
            'a7': 'p', 'b7': 'p', 'c7': 'p', 'd7': 'p', 'e7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p',
            'a6': '0', 'b6': '0', 'c6': '0', 'd6': '0', 'e6': '0', 'f6': '0', 'g6': '0', 'h6': '0',
            'a5': '0', 'b5': '0', 'c5': '0', 'd5': '0', 'e5': '0', 'f5': '0', 'g5': '0', 'h5': '0',
            'a4': '0', 'b4': '0', 'c4': '0', 'd4': '0', 'e4': '0', 'f4': '0', 'g4': '0', 'h4': '0',
            'a3': '0', 'b3': '0', 'c3': '0', 'd3': '0', 'e3': '0', 'f3': '0', 'g3': '0', 'h3': '0',
            'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',
            'a1': 'R', 'b1': 'N', 'c1': 'B', 'd1': 'Q', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': 'R',
        }

        # Make a list for the squares on the board
        self.squares_list = [j + i for i in '12345678' for j in 'abcdefgh']

        # Creating the theme of the board
        self.board_themes = {'fritz': ('#E8EBEF', '#7D8796'),
                             'marine': ('#9DACFF', '#6F73D2'),
                             'emerald': ('#ADBD8F', '#6F8F72'),
                             'sandcastle': ('#E3C16F', '#B88B4A'),
                             }

        # Making two attributes: from_square(from which the piece moves)
        #                        to_square(to which the piece moves)
        self.from_square = ''
        self.to_square = ''

        # Assigning the right colour to the squares
        # Make a dictionary for squares
        self.squares_board = {}
        for file in self.file_dict:
            for rank in self.rank_dict:
                light, dark = self.board_themes['fritz']  # 'fritz' theme for the chess board
                if (self.file_dict[file] + self.rank_dict[rank]) % 2 == 0:
                    color = dark
                else:
                    color = light

                square_name = file + rank

                square = tkinter.Button(self.main_frame, width=70, height=70,
                                        highlightthickness=0, relief='solid',
                                        image=self.all_pieces['0'], bg=color)

                square.grid(row=8 - self.rank_dict[rank], column=self.file_dict[file])

                # Add the square to the dictionary of squares
                self.squares_board[square_name] = square

        # Assigning commands to the square buttons
        for square_ in self.squares_board:
            button = self.squares_board[square_]
            button.configure(command=lambda var=square_: self.button_click(var))

        # Creating labels for files and ranks
        for file in self.file_dict:
            file_label = ttk.Label(self.main_frame, text=file,)
            file_label.grid(row=9, column=self.file_dict[file], pady=5)
        for rank in self.rank_dict:
            rank_label = ttk.Label(self.main_frame, text=rank)
            rank_label.grid(row=8 - self.rank_dict[rank], column=0, padx=5)

        # Creating a board which works on chess module,
        # aiding the GUI with piece movement, legal moves, result of the game
        self.comparison_board = chess.Board()

    def add_piece_to_square(self, piece: str, square: str) -> None:
        """
        Puts the image of the piece on the square
        :param piece: The piece that has to be put up on
        :param square: The square on which the image will be put up
        :return: None
        """
        self.squares_board[square].configure(image=self.all_pieces[piece])

    def set_board(self) -> None:
        """
        Sets up the board to the initial position and also helps in making the current move.
        :return: None
        """
        for square, piece in self.position_on_board.items():
            self.add_piece_to_square(piece, square)

    def button_click(self, square: str) -> None:
        """
        The function to make moves on the board
        :return: None
        """
        if self.from_square == '' and self.to_square == '':
            self.from_square = square
        elif self.to_square == '':
            self.to_square = square

            # If both from_square and to_square hold the same square
            # then it is treated as a null move in the chess module,
            # so we remove this case
            if self.from_square != self.to_square:
                # 'requested_move' variable holds the move in uci
                requested_move = self.from_square + self.to_square

                if chess.Move.from_uci(requested_move) in self.comparison_board.legal_moves:

                    # Check if the move is en passant and configure the GUI accordingly
                    if self.comparison_board.is_en_passant(chess.Move.from_uci(requested_move)):
                        # Making the pawn capture, for e.g. e5 takes d6
                        # Putting the e5 pawn on d6(which sets the e5 square to '0')
                        # After that making the d5 pawn disappear(putting '0' on d5)
                        self.make_move(self.from_square, self.to_square)
                        removing_square = self.to_square[0] + self.from_square[1]
                        self.make_move(removing_square, removing_square)

                    # Check if the move is castling and configure the GUI accordingly
                    elif self.comparison_board.is_castling(chess.Move.from_uci(requested_move)):
                        # Configure the GUI for the 4 possible ways of castling
                        if requested_move == 'e1g1' or requested_move == 'e1h1':
                            self.make_move('e1', 'g1')
                            self.make_move('h1', 'f1')
                        elif requested_move == 'e1c1' or requested_move == 'e1a1':
                            self.make_move('e1', 'c1')
                            self.make_move('a1', 'd1')
                        elif requested_move == 'e8g8' or requested_move == 'e8h8':
                            self.make_move('e8', 'g8')
                            self.make_move('h8', 'f8')
                        else:
                            self.make_move('e8', 'c8')
                            self.make_move('a8', 'd8')

                    else:
                        self.make_move(self.from_square, self.to_square)

                    # Make the move on the comparison board and reset the from_square and to_square
                    self.comparison_board.push_uci(requested_move)
                    self.from_square, self.to_square = ('', '')

                # Check if the move is promotion and configure the GUI accordingly
                elif chess.Move.from_uci(requested_move + 'q') in self.comparison_board.legal_moves:
                    promoted_piece_strvar = tkinter.StringVar()

                    def on_option_selected():
                        promoted_piece_strvar.set(promoted_piece_strvar.get())

                    promotion_window = tkinter.Toplevel(self.main_frame)
                    promotion_window.title('Promote:')
                    promotion_window.geometry('150x75-200+315')
                    promotion_window.resizable(False, False)
                    promotion_window.grid()

                    radio_queen = tkinter.Radiobutton(promotion_window, text='Queen', variable=promoted_piece_strvar,
                                                      value='q', command=on_option_selected)
                    radio_rook = tkinter.Radiobutton(promotion_window, text='Rook', variable=promoted_piece_strvar,
                                                     value='r', command=on_option_selected)
                    radio_knight = tkinter.Radiobutton(promotion_window, text='Knight', variable=promoted_piece_strvar,
                                                       value='n', command=on_option_selected)
                    radio_bishop = tkinter.Radiobutton(promotion_window, text='Bishop', variable=promoted_piece_strvar,
                                                       value='b', command=on_option_selected)

                    radio_queen.grid(row=0, column=0, sticky=tkinter.W)
                    radio_rook.grid(row=1, column=0, sticky=tkinter.W)
                    radio_knight.grid(row=2, column=0, sticky=tkinter.W)
                    radio_bishop.grid(row=3, column=0, sticky=tkinter.W)

                    promotion_window.wait_window()

                    promoted_piece = promoted_piece_strvar.get()
                    # if user closes the toplevel window, without choosing any option
                    if promoted_piece == '':
                        promoted_piece = 'q'

                    # If white pawn is getting promoted
                    if self.to_square[1] == '8':
                        self.make_move(self.from_square, self.from_square)  # Vacating the from_square
                        self.add_piece_to_square(promoted_piece.upper(), self.to_square)
                        # Updating the dictionary of position_on_board
                        self.position_on_board[self.to_square] = promoted_piece.upper()

                    else:
                        self.make_move(self.from_square, self.from_square)  # Vacating the from_square
                        self.add_piece_to_square(promoted_piece, self.to_square)
                        # Updating the dictionary of position_on_board
                        self.position_on_board[self.to_square] = promoted_piece

                    # Making the move on comparison board and reset from_square and to_square
                    self.comparison_board.push_uci(requested_move + promoted_piece)
                    self.from_square, self.to_square = ('', '')

                else:
                    self.from_square, self.to_square = ('', '')
            else:
                self.from_square, self.to_square = ('', '')

        # Based on the move played, display the result of the game on result label
        if self.comparison_board.result() == '*':
            self.result_label.configure(text='Game in Progress')
        elif self.comparison_board.result() == '1-0':
            self.result_label.configure(text='White Wins')
        elif self.comparison_board.result() == '0-1':
            self.result_label.configure(text='Black Wins')
        else:
            self.result_label.configure(text='Game Drawn')

    def make_move(self, square1: str, square2: str) -> None:
        """
        Makes move using uci(universal chess interface notation)
        :param square1: The initial square from which the piece moves
        :param square2: The final square to which the piece moves
        :return: None
        """
        piece_to_move = self.position_on_board[square1]
        self.add_piece_to_square(piece_to_move, square2)
        self.add_piece_to_square('0', square1)

        # After making the changes on the board, update the current position dictionary
        self.position_on_board[square2] = self.position_on_board[square1]
        self.position_on_board[square1] = '0'

    @staticmethod
    def print_square(square: str) -> None:
        """Prints the algebraic notation of a square"""
        print(square)


if __name__ == '__main__':
    board = Board()
    board.set_board()
    board.mainloop()
