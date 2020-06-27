import numpy as np
from src.Player import Player
from src.Rule import Rule

class GUI():
    def __init__(self):
        self.piece = ''
        self.player = Player()
    def drawBoard(self, player):
        self.player = player
        self.currentPlayer = self.player.getCurrentPlayer()
        self.pieceList= self.player.getCurrentPieceList()
        # print(self.pieceList)
        # print(self.pieceList)
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
        for row in range(2):
            for col in range (1,10):
                print("\t~~\t",end=('\n' if col == 9 else ''))

    def findPiece(self,row,col):
        # print(self.pieceList)
        self.piece=''
        # print(player.Pieces[0][:][0])
        pos=(row,col)
        for i in range(len(self.pieceList)):
            # print(type(self.pieceList['Pos'][i]))
            if self.pieceList[i]['Pos'] == pos:
                # print("curr :",self.current_BoardState['Symbol'][i])
                self.piece = self.pieceList[i]['Symbol']
            else:
                pass
        if self.piece == '':
            self.piece = "*"