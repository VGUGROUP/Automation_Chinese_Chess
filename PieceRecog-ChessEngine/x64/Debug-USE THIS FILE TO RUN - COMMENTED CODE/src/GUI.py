import numpy as np
from src.Player import Player
class GUI:
    """
    This class handle the simulation interface of the system
    """
    def __init__(self):
        self.piece = ''
        self.player = Player()

    def drawBoard(self, player):
        """
        This function draws the board of the game which includes adding the river and chess pieces
        
        :param player: This object is used to get the current chess piece list to draw the pieces on the board
        """
        self.player = player
        self.currentPlayer = self.player.getCurrentPlayer()
        self.pieceList= self.player.getCurrentPieceList()

        print("-----------------------------------------------------------------------")
        for col in range(1,10):
            print("\t{}\t".format(col), end=('\n' if col == 9 else ''))

        for row in range(1,11):
            print("\n{}".format(row), end='')
            for col in range (1,10):
                self.findPiece(row,col)
                print("\t{}\t".format(self.piece),end=('\n' if col == 9 else ''))
            if row == 5:
                self.drawRiver()
        print("-----------------------------------------------------------------------")

    def drawRiver(self):
        """
        This function draw the river on the board with symbol (~~)
        """
        for row in range(2):
            for col in range (1,10):
                print("\t~~\t",end=('\n' if col == 9 else ''))

    def findPiece(self, row, col):
        """
        This function draw the chess piece using symbol in the chess piece list
        or draw (*) if the position is empty.
        This function will be called for each location on the chess board.

        :param row, col: Board position variable which will be compared with
        the position of the chess piece in the chess piece list.
        """

        self.piece=''

        pos =(row, col)
        for i in range(len(self.pieceList)):

            if self.pieceList[i]['Pos'] == pos:
                self.piece = self.pieceList[i]['Symbol']

            else:
                pass

        if self.piece == '':
            self.piece = "*"