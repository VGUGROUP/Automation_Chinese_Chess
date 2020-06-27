from src.GUI import GUI
from src.GUI import Player
from src.Zobrist import Zobrist
import datetime
import copy
import os
class State():
    def __init__(self):
        self.player = Player().getPlayer()
        # self.player.getCurrentPlayer()
        self.pieceList = self.player.getCurrentPieceList()
        self.Zobrist = Zobrist()
        self.HashTable = self.Zobrist.getHashTable()

    def initGameState(self):
        print("Setting game state: ")
        self.playGUI = GUI()
        self.playGUI.drawBoard(self.player)

    # Test Functions:

    def playGame(self):

        print("\nPlay Game")
        if self.EndGame(self.player.getCurrentPieceList()) == True :
            print("The End")
            return True
        else:
            # Get pieceList from thong
            # Running the code 
            os.system("g++ -g -std=c++11 -I/usr/local/include/opencv4/opencv -I/usr/local/include/opencv4 -L/usr/local/lib main.cpp Piece.cpp -o a.exe -lopencv_dnn -lopencv_gapi -lopencv_highgui -lopencv_ml -lopencv_objdetect -lopencv_photo -lopencv_stitching -lopencv_video -lopencv_calib3d -lopencv_features2d -lopencv_flann -lopencv_videoio -lopencv_imgcodecs -lopencv_imgproc -lopencv_xfeatures2d -lopencv_core --debug <")

            #input Move
            input_result =self.inputMove()
            print("Chess piece: {}, pos: {}".format(input_result['Piece'], input_result['Pos']))
            self.movePiece(self.pieceList, input_result['Piece'], input_result['Pos'])
            self.player.UpdatePieceList(self.pieceList)
            self.playGUI.drawBoard(self.player)
            # print("End game: ",self.EndGame(self.player.getCurrentPieceList()))
            # Activate Game bot
            AB_result = self.setNextMove_AB()
            if  AB_result == 0: # Endgame condition
                return True
            else:
                self.player.changeCurrentPlayer()
                return AB_result

    def find(self, list, key, value):
        for i, dic in enumerate(list):
            if dic[key] == value:
                return i
        return -1

    def inputMove(self):

        chesspiece = input("Input chess piece: ")
        if chesspiece == 'end' :
            return 0
        else:
            print("input position:")
            row = int(input("row: "))
            col = int(input("\ncol: "))
            pos = (row, col)

            # Input from csv
            #--------------------------------------------------------------------
            input_result = {
                "Piece" : chesspiece,
                "Pos": (row,col)
            }
        return input_result

    def setNextMove_AB(self):
        print ("1====================================")
        # Set timer start here:
        start = datetime.datetime.now()
        # Call Alpha Beta algorithm. Result is a dict: (score, piece, pos)
        result = self.alphabeta(2, False, -9999, 9999)
        # Set timer stop here:
        end = datetime.datetime.now()
        elapse = end - start
        print("elapse: ",elapse)
        # movePiece using result piece and position:
        print("Result: ",result)
        old_pos = self.pieceList[self.find(self.pieceList,'Symbol', result['Piece'])]['Pos']
        check_capture = self.movePiece(self.pieceList,result['Piece'],result['Pos'])
        self.player.UpdatePieceList(self.pieceList)
        self.playGUI.drawBoard(self.player)
        check_endgame = self.EndGame(self.player.getCurrentPieceList())
        if check_endgame == True:
            return 0
        else:
            print ("Information to pass: Old pos: {}, New pos: {}, check capture: {}, check Endgame: {}".
                   format(old_pos,
                          result['Pos'],
                          check_capture,
                          check_endgame))
            AB_result = (old_pos, result['Pos'], check_capture)
            return AB_result

    def movePiece(self, pieceList, piece, pos):

        # check captured:
        check = self.player.checkCaptured(pieceList, pos)

        for i in range(len(pieceList)):
            # print("I{} = ".format(i),self.pieceList['Symbol'][i])
            if piece == pieceList[i]['Symbol']:
                # print('Old: {} to {}'.format( pieceList[i]['Pos'], pos))
                self.pieceList[i]['Pos'] = pos
            else:
                pass
        return check

    def EndGame(self, pieceList):
        check_endgame = not self.player.isGeneralExist(pieceList)
        # print("check end game: ",check_endgame)
        return check_endgame

    def nextState(self, piece, pos):
        # Copy current pieceList to new state obj
        nextState = copy.deepcopy(self)

        nextState.movePiece(nextState.player.getCurrentPieceList(), piece, pos)

        return nextState



    def alphabeta(self, depth, isMax, alpha, beta):

        # Check for endgame condition:
        if self.EndGame(self.player.getCurrentPieceList()) == True:
            result = {
                "Score": '',
                "Piece": '',
                "Pos": ''
            }
            pass
            # Get score of pieceList
            result['Score'] = (99999999)*self.player.getCurrentPlayer()
            # print("Score in depth 0 = ", result['Score'])
            return result

        # Check for depth = 0
        if depth == 0:
            # print("Depth 0")
            result = {
                "Score": '',
                "Piece": '',
                "Pos": ''
            }
            pass

            # Get score of pieceList
            result['Score'] = self.player.getPieceListScore(self.pieceList)
            # print("Score in depth 0 = ", result['Score'])
            return result
        # Get Zobrist key of this State:
        # key = self.Zobrist.ZobristKeyGen(self.player.getCurrentPieceList())
        # print("Key: ", key)
        #Check Hash table:

        # Change current player
        self.player.changeCurrentPlayer()
        # Get possible move of the current player

        possibleMoves = self.player.getAllPossibleMoves()

        # print(possibleMoves)
        eval_result = list()

        # Loop through possible move and create new piecelist with each move
        for i in range(len(possibleMoves)):
            # Collect inputs (piece and piece's position)
            piece = possibleMoves[i][0]['Symbol']
            to_pos = possibleMoves[i][1]
            # Create new pieceList
            nextState = self.nextState( piece, to_pos)
            # Recall alpha beta to collect score from lower depth
            alpha_beta_result = nextState.alphabeta( depth - 1, not isMax, alpha, beta)

            try:
                score = alpha_beta_result['Score']
                # print("Score type: ",type(score))
            except :
                print("\nWrong\n")
            # print("alpha_beta_result score_{}: ".format(depth),score)
            result = {
                "Score": score,
                "Piece": piece,
                "Pos": to_pos
            }

            eval_result.append(result)
            # print("eval result: ", eval_result)
            # if score >= beta: # LOWER BOUND CASE
            #     self.HashEntry = {
            #         'Zobrist_Key': key,
            #         'Depth': depth,
            #         'Entry_Type': 'LOWER',  # EXACT ( Alpha < eval < Beta), LOWER ( >= Beta) OR UPPER (<= Alpha)
            #         'Eval': result  # Score
            #         # 'Ancient': '',
            #     }
            #     self.HashTable.insert(self.Zobrist.findIndex(key),self.HashEntry)
            #     return result
            # else:
            if isMax:
                alpha = max(alpha, score)
                if beta <= alpha:
                    # print("EQUAL")
                    return eval_result[-1]
            else:
                beta = min(beta, score)
                if beta <= alpha:
                    # print("EQUAL")
                    return eval_result[-1]
        # Get score from eval result
        score_list = list()
        index = ''
        for j in range(len(eval_result)):
            score_list.append(eval_result[j]['Score'])

        if isMax:
            index = score_list.index(max(score_list))
        else:
            index = score_list.index(min(score_list))

        return eval_result[index]

