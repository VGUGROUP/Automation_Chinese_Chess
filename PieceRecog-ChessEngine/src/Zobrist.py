import random
from functools import reduce
import pandas as pd
import ast


# from src.Player import Player
class Zobrist():
    def __init__(self):
        #Zorbrist[15][9][10]
        self.ZArray = [[[None]*15 for _ in range(9)] for _ in range(10)]
        self.TranspositionTable = list()
        self.HashEntry = {
            'Zobrist_Key': '',
            'Depth': '',
            'Entry_Type': '', # EXACT ( Alpha < eval < Beta), LOWER ( >= Beta) OR UPPER (<= Alpha)
            'Eval': '', # Score
            # 'Ancient': '',
            'Move': ''
        }
        print(self.ZArray)
        print(len(self.ZArray[1][0]))
        self.ZobristFillArray()
        # pd.DataFrame(self.ZArray).to_csv('ZArray.csv', index=False)
        # create csv

    # def resetBoardState(self, csv):
    #     # Load information into
    #     data_excel = pd.read_csv(csv)
    #     # print(data_excel)
    #     self.pieceList = []
    #     for i in range(len(data_excel)):
    #         # print(ast.literal_eval(data_excel["Pos"][i]))
    #         self.pieceList.append({
    #             'Name': data_excel["Name"][i],
    #             'Pos': ast.literal_eval(data_excel["Pos"][i]),
    #             'Symbol': data_excel["Symbol"][i],
    #             'Team': data_excel["Team"][i],
    #             'Score': data_excel["Score"][i],
    #             'Znumb': data_excel["Znumb"][i]
    #         })
    #     return self.pieceList

    def findIndex(self, key):

        index = key % len(self.TranspositionTable)
        return index

    def ZobristFillArray(self):
        for row in range(10):
            for col in range(9):
                for piece in range(15):
                    # print("row: ",row," col: ",col, " piece: ", piece, "Zarray: ",self.ZArray[row][col][piece])
                    self.ZArray[row][col][piece] = random.getrandbits(64)

    def getHashTable(self):
        return self.TranspositionTable

    def ZobristKeyGen(self, pieceList):
        ZobristKey = 0
        for row in range(1, 11):
            for col in range(1, 10):
                for piece in range(len(pieceList)):
                    # print("row: ",row," col: ",col, " piece: ", piece)
                    # print(pieceList[piece]['Pos'])
                    if pieceList[piece]['Pos'] == (row, col):
                        # print("Match", "row: ",row-1," col: ",col-1, " piece: ", piece, "Zarray: ",self.ZArray[row-1][col-1][pieceList[piece]['Znumb']])
                        ZobristKey ^= self.ZArray[row-1][col-1][pieceList[piece]['Znumb']]
                    else:
                        ZobristKey ^= self.ZArray[row-1][col-1][0]
        return ZobristKey

# if __name__ == "__main__":
#     a = Zobrist()
#     while 1:
#         pieceList_csv = input("Input csv file: ")
#         if pieceList_csv != 'end':
#             a.pieceList = a.resetBoardState(pieceList_csv)
#             print(a.pieceList)
#             a.ZobristKey = a.ZobristKeyGen(a.pieceList)
#             print(a.ZobristKey)
#             a.HashEntry = {
#                 'Zobrist_Key': a.ZobristKey,
#                 'Depth': '',
#                 'Flag': '',
#                 'Eval': '',
#                 'Ancient': '',
#                 'Move': ''
#             }
#             a.TranspositionTable.append(a.HashEntry)
#         else:
#             break
#     while(1):
#         key = input("Enter Zobrist Key: ")
#         if key != 'end':
#             index = a.findIndex(key)
#             print(a.TranspositionTable[index])