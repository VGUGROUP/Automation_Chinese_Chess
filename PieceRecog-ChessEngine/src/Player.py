from src.Rule import Rule
from src.Evaluation import Evaluation
# Multi-threading
import concurrent.futures
# Regular expression
import re
# Csv data libs
import pandas as pd
import ast
# Time elapse
import datetime
Player_list = {
    "RED":1,
    "BLACK":-1
}
class Player():
    def __init__(self):
        self.currentPlayer = Player_list["RED"]
        self.pieceList = self.resetBoardState()
        self.gamerule = Rule()
        self.eval = Evaluation()

    # def __init__(State):
    def resetBoardState(self):
        # Load information into
        data_excel = pd.read_csv("src\\BoardData.csv")
        # print(data_excel)
        self.pieceList = []
        for i in range(len(data_excel)):
            # print(ast.literal_eval(data_excel["Pos"][i]))
            self.pieceList.append({
                'Name': data_excel["Name"][i],
                'Pos': ast.literal_eval(data_excel["Pos"][i]),
                'Symbol': data_excel["Symbol"][i],
                'Team': data_excel["Team"][i],
                'Score': data_excel["Score"][i],
                'Znumb': data_excel["Znumb"][i]
            })
        return self.pieceList
    def saveCurrentPieceList(self,pieceList):
        self.old_pieceList= pieceList

    def getCurrentPieceList(self):
        return self.pieceList

    def UpdatePieceList(self,pieceList):
        self.pieceList = pieceList
        # print(self.pieceList)

    def getPlayer(self):
        return self

    def getCurrentPlayer(self):
        return self.currentPlayer

    def changeCurrentPlayer(self):
        self.currentPlayer = - self.currentPlayer

    def possibleMoves(self, player_list):

        possibleMoves = []
        for i in range(search_range[0],search_range[1]):
            movelist = eval('self.gamerule.possibleMoveFor{}(self.pieceList[i],self.pieceList)'.
                format(re.findall('(?:Black|Red)(.*)', self.pieceList[i]['Name'])[0]))
            for item in movelist:
                possibleMoves.append((self.pieceList[i], item))

        return possibleMoves

    def getPlayerPieceList(self):
        player_list = []
        search_range = ((0,sum([self.pieceList[k]['Team'] == -1 for k in range(len(self.pieceList))])) if \
            self.currentPlayer == Player_list["BLACK"] else \
                (sum([self.pieceList[k]['Team'] == -1 for k in range(len(self.pieceList))]),len(self.pieceList)))

        for i in range(search_range[0],search_range[1]):
            player_list.append(self.pieceList[i])
        return player_list
    def getAllPossibleMoves(self):

        searchrange = ''
        possibleMoves = []
        # print("curr player: ", self.currentPlayer)
        search_range = ((0,sum([self.pieceList[k]['Team'] == -1 for k in range(len(self.pieceList))])) if \
            self.currentPlayer == Player_list["BLACK"] else \
                (sum([self.pieceList[k]['Team'] == -1 for k in range(len(self.pieceList))]),len(self.pieceList)))

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     t1 = executor.map(self.possibleMoves, player_list)
        #
        # t3.extend(t4)

        for i in range(search_range[0],search_range[1]):
            movelist = eval('self.gamerule.possibleMoveFor{}(self.pieceList[i],self.pieceList)'.
                format(re.findall('(?:Black|Red)(.*)', self.pieceList[i]['Name'])[0]))
            for item in movelist:
                possibleMoves.append((self.pieceList[i], item))

        # return t3
        return possibleMoves

    def checkCaptured(self, pieceList, pos):

        # index is reversed : curr player = black -> search red and vice versa
        searchrange = ((0,sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))])) if \
            self.currentPlayer == Player_list["RED"] else \
                (sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))]),len(pieceList)))

        for i in range(searchrange[0],searchrange[1]):
            if pieceList[i]['Pos'] == pos:
                # print("remove: ",pieceList[i])
                pieceList.pop(i)
                return True
        return False
    def isGeneralExist(self, pieceList):
        searchrange = ((0,sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))])) if \
            self.currentPlayer == Player_list["RED"] else \
                (sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))]),len(pieceList)))

        for i in range(searchrange[0],searchrange[1]):
            # print(pieceList[i]['Name'])
            if (pieceList[i]['Name'] == "RedGeneral" or pieceList[i]['Name'] == "BlackGeneral"):
                # print("Still exist")
                return True
            else:
                pass
        print("No general")
        return False

    def getPieceListScore(self, pieceList):

        RedScore = 0
        BlackScore = 0

        for i in range(2):
            searchrange = ((0, sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))])) if i == 0 else\
                (sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))]),len(pieceList)))

            for j in range(searchrange[0], searchrange[1]):
                if i == 0:
                    BlackScore += (pieceList[j]['Score'] + self.eval.posValue(pieceList[j]['Name'], pieceList[j]['Pos']))
                    # print("Black Score: {}".format(BlackScore))
                else:

                    RedScore += (pieceList[j]['Score'] + self.eval.posValue(pieceList[j]['Name'], pieceList[j]['Pos']))
                    # print("Red Score: {}".format(RedScore))



        # print("Red Score: {} - Black Score: {} = {}".format(RedScore, BlackScore, RedScore - BlackScore))

        return RedScore - BlackScore
    def movePiece_check(self, piece, pos):
        # Check if valid move:

            # Check if pos contain other team piece -> trigger capture
        # Return boolean
        return 0
    # def capturePiece(self, pos):
        # Delete opponent piece at pos

        # Check if opponent piece is deleted


