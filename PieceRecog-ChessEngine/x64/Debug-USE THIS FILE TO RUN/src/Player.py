from src.Rule import Rule
from src.Evaluation import Evaluation
# Regular expression
import re
# Csv data libs
import pandas as pd
import ast
# Time elapse
import time

Player_list = {
    "RED": 1,
    "BLACK": -1
}
class Player():
    def __init__(self):
        self.currentPlayer = Player_list["RED"]
        # Reset BoardData update -> BoardData
        pd.read_csv("src\\BoardData.csv").to_csv("src\\BoardData_update.csv")
        self.pieceList = self.getChessPieceList("src\\BoardData.csv")
        self.gamerule = Rule()
        self.eval = Evaluation()



    def getChessPieceList(self, data):
        # Load information into
        data_excel = pd.read_csv(data)
        # print(data_excel)
        self.pieceList = []
        for i in range(len(data_excel)):
            # print(ast.literal_eval(data_excel["Pos"][i]))
            self.pieceList.append({
                'Name': data_excel["Name"][i],
                'Pos': ast.literal_eval(data_excel["Pos"][i]),
                'Symbol': data_excel["Symbol"][i],
                'Team': data_excel["Team"][i],
                'Score': data_excel["Score"][i]
            })
        return self.pieceList

    def updateData(self, current_data):

        chess_name = ['BlackGeneral', 'BlackCar', 'BlackCannon', 'BlackHorse',
                      'BlackSoldier', 'BlackElephant', 'BlackAdvisor']
        data_excel = pd.read_csv(current_data)
        print(len(data_excel))
        missing_piece = list()
        # Check if EndGame:
        opp_piece = pd.read_csv("GreenPiece.csv")
        # No Black General case -> return 0
        for i in chess_name:
            if len(opp_piece.loc[opp_piece['Name'] == i]) == 0:
                missing_piece.append(i)
                print("Missing piece: ", i)
                print(data_excel.loc[data_excel['Name'] == missing_piece[0]].index)
                if i == "BlackGeneral":
                    print("Game has ended")
                    return 0
        newdata = pd.concat([pd.read_csv("GreenPiece.csv"), pd.read_csv("RedPiece.csv")], ignore_index=True)
        # This list is for filter purposes
        newdata_used_piece = list()
        newdata_index = list()
        data_excel_index = list()
        # unused_data consist of newdata pos and index
        unused_data = list()
        delete_data = list()

        for i in range(len(newdata)):
            # print(newdata['Name'][i])
            if len(newdata_used_piece) > 0 and newdata['Name'][i] in newdata_used_piece:
                continue
            else:
                # Add newdata_name to newdata_used_piece list
                newdata_used_piece.append(newdata['Name'][i])
                # Add data_excel used index to list
                newdata_index.append(list(newdata.loc[newdata['Name'] == newdata['Name'][i]].index))
                # Case missing piece:
                data_excel_index.append(list(data_excel.loc[data_excel['Name'] == newdata['Name'][i]].index))

        print(newdata_index)
        print(data_excel_index)
        capture_flag = False
        # Loop through each index list of each piece in new data
        for i in range(len(newdata_index)):
            # Loop through each index of new data index list
            for j in newdata_index[i]:
                print("newdata: ", newdata['Name'][j], "new pos: ", newdata['Pos'][j])
                # 2 Cases: No piece missing or 1 piece is captured
                if len(newdata_index[i]) < len(data_excel_index[i]):
                    print("A piece is missing")
                    capture_flag = True
                # Loop through each index of data excel index list for each index of new data
                for k in data_excel_index[i]:
                    print(data_excel['Name'][k], ", ", data_excel['Pos'][k])
                    # If the 2 index share the same position -> remove that index from list of data excel index
                    if newdata['Pos'][j] == data_excel['Pos'][k]:
                        data_excel_index[i].pop(data_excel_index[i].index(k))
                        print("Remain index: ", data_excel_index[i])
                        break
                    # If 2 index has different position -> 2 Cases: captured or update
                    else:
                        print("Different position")
                        print("current index: ", data_excel_index[i].index(k))
                        # Update position case and all index of the index list in data excel has been loop through
                        if data_excel_index[i].index(k) == (len(data_excel_index[i]) - 1) and capture_flag is False:
                            # unused data store index of newdata index
                            print("Unused piece: ", newdata['Pos'][j])
                            unused_data.append(j)
                        else:
                            pass

                # Captured case -> delete that index from data excel
                if capture_flag is True:
                    print("Need to remove: ", data_excel_index[i])
                    delete_data.append(i)
                    # print("data excel:", data_excel)
                    capture_flag = False
                    # unused_data.clear()
            # Update case -> remaining data excel index replaced with unused data position
            if len(unused_data) > 0:
                print("unused data: {}, data_excel: {}, pos: {}".format(unused_data, data_excel['Name'][data_excel_index[i][0]], data_excel['Pos'][data_excel_index[i][0]]))
                data_excel = data_excel.replace(data_excel.iloc[data_excel_index[i][0]]['Pos'],
                                                newdata['Pos'][unused_data[0]])
                unused_data.clear()
        # delete data:
        if len(delete_data) > 0:
            # Remove the captured data:
            data_excel = data_excel.drop(index=data_excel_index[delete_data[0]][0])
            print("New data excel: ", data_excel)
            delete_data.clear()
        # missing piece in new data -> delete
        elif len(missing_piece) > 0 and len(data_excel.loc[data_excel['Name'] == missing_piece[0]]) > 0:
            data_excel = data_excel.drop(index=data_excel.loc[data_excel['Name'] == missing_piece[0]].index)
            missing_piece.clear()
        data_excel.to_csv(current_data, index=False)
        # Open BoardData update to check the new changes
        # self.xl.Workbooks.Open(Filename=self.update_file_pth)

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

    def getOpPlayerPieceList(self):
        player_list = []

        for i in range(len(self.pieceList)):
        # for i in range(search_range[0],search_range[1]):
            if self.pieceList[i]['Team'] != self.currentPlayer:
                player_list.append(self.pieceList[i])

        return player_list

    def getPlayerPieceList(self):
        player_list = []

        for i in range(len(self.pieceList)):
        # for i in range(search_range[0],search_range[1]):
            if self.pieceList[i]['Team'] == self.currentPlayer:
                player_list.append(self.pieceList[i])

        return player_list

    def getAllPossibleMoves(self):
        possibleMoves = []
        # print("curr player: ", self.currentPlayer)
        pieceList = self.getPlayerPieceList()

        for i in range(len(pieceList)):
            movelist = eval('self.gamerule.possibleMoveFor{}(pieceList[i],self.pieceList)'.
                            format(re.findall('(?:Black|Red)(.*)', pieceList[i]['Name'])[0]))
            # movelist = self.gamerule.possibleMoveForGeneral(pieceList[i], self.pieceList)
            for item in movelist:
                possibleMoves.append((pieceList[i], item))
        return possibleMoves

    def checkCaptured(self, pieceList, pos):
        # print("curr Player: ", self.currentPlayer)
        # index is reversed : curr player = black -> search red and vice versa
        searchrange = ((0, sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))])) if
            self.currentPlayer == Player_list["RED"] else
                (sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))]), len(pieceList)))

        for i in range(searchrange[0], searchrange[1]):
            if pieceList[i]['Pos'] == pos:
                pieceList.pop(i)
                return True
        return False

    def isGeneralExist(self):
        opp_pieceList = self.getOpPlayerPieceList()
        # print("opp piece: ", opp_pieceList)
        if (opp_pieceList[-1]['Name'] == "RedGeneral") or (opp_pieceList[-1]['Name'] == "BlackGeneral"):
            # print("Still exist")
            return True
        else:
            # print("No general")
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




