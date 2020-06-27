from src.GUI import GUI
from src.GUI import Player
import win32com.client as win32
import time
import copy
import pandas as pd
from operator import itemgetter
import os

class State:
    """
    This class is a bridge to all other classes and contain the Minimax algorithm with Alpha-Beta pruning
    """
    def __init__(self):
        self.current_dir = os.getcwd()
        self.checkOpenStatus()
        self.player = Player().getPlayer()
        self.player.getCurrentPlayer()
        self.pieceList = self.player.getCurrentPieceList()
        self.red_count = 0
        self.black_count = 0
        self.logdata = list()
        self.timetable_red = list()
        self.timetable_black = list()
        self.infi_loop = list()

    def initGameState(self):
        """
        This function creates a GUI obj and draw the simulation board
        """
        print("Setting game state: ")
        self.playGUI = GUI()
        self.playGUI.drawBoard(self.player)

    def genDataFiles(self, pieceList):
        """
        This function creates 2 csv files (m_GreenPiece.csv and m_RedPiece.csv) based on the chess piece list data

        :param pieceList: The current chess piece list
        """
        b_list, r_list = list(), list()
        for i in range(len(pieceList)):
            eval("{}.append((pieceList[i]['Name'], pieceList[i]['Pos']))".format('b_list' if pieceList[i]['Team'] == -1
                                                                                            else 'r_list'))
        print("red: ", r_list)
        print("Black: ", b_list)
        pd.DataFrame(b_list, columns=['Name', 'Pos']).to_csv("m_GreenPiece.csv", index=False)
        pd.DataFrame(r_list, columns=['Name', 'Pos']).to_csv("m_RedPiece.csv", index=False)

    def playGame(self):
        """
        This function calls the inputMove() function

        :return: True if the Game has ended, else the result to pass to the SCARA arm
        """
        print("\nPlay Game")
        if (self.EndGame()):
            print("EndGame stt: ", self.EndGame())

            print("The End")
            return True
        else:
            # Get pieceList from thong
            input_result = self.inputMove() 
            # input move return 2 forms: True and input result
            if input_result is not True:
                return input_result
            else:
                # Export time table to csv
                black_timetable = pd.DataFrame(self.timetable_black, columns=['Iteration', 'Time']).to_csv(
                    "Time_black.csv", index=False)
                return True


    def checkOpenStatus(self):
        """
        This function checks whether the BoardData_update.csv is still open to avoid problem when writing to that file
        """
        xl = win32.gencache.EnsureDispatch('Excel.Application')
        update_file = "BoardData_update.csv"
        update_file_pth = os.path.join(self.current_dir, 'src', update_file)

        if xl.Workbooks.Count > 0:
            print("opened: ", xl.Workbooks.Count)

            # if none of opened workbooks matches the name, openes my_workbook
            if any(i.Name == update_file for i in xl.Workbooks):
                print("It is opended")
                xl.Workbooks.Open(Filename=update_file_pth).Close(True)

            else:
                print("It is not opended")

    def find(self, list, key, value):
        """
        This function give the index of a key in the dictionary in a list that match the input value

        :param list: The collection of dictionaries
        :param key: the key of a dictionary
        :param value: the input key that needs to be found
        :return: The index of the dictionary containing the key that match the input key
        """
        for i, dic in enumerate(list):
            if dic[key] == value:
                return i
        return -1

    def inputMove(self):
        """
        This function handles the inputs from the recognition system and call the Alpha-Beta function

        :return: True if the game has ended, else return the result to pass to the SCARA arm
        """
        # Check if BoardData_update is still opended
        self.checkOpenStatus()

        self.genDataFiles(self.player.getCurrentPieceList())
        print("PieceRecog.exe", len(self.player.getCurrentPieceList()))

        # Call the recognition function
        os.system("PieceRecog.exe " + str(len(self.player.getCurrentPieceList())))

        # Check if BoardData_update is still opended
        self.checkOpenStatus()
        self.player.updateData('src\\BoardData_update.csv')
        self.player.getChessPieceList('src\\BoardData_update.csv')
        self.pieceList = self.player.getCurrentPieceList()
        # Update the simulation board
        self.playGUI.drawBoard(self.player)

        check = self.setNextMove_AB()

        if check == 0:
            return True

        else:
            pd.DataFrame(self.player.getCurrentPieceList()).to_csv('src\\BoardData_update.csv', index=False)
            print("Piecelist after Alpha beta: ", self.pieceList)
            return check

    def autochess(self):
        """
        Simulation chess engine which will replace the player role. The depth in this chess engine is fixed to 2
        :return: 0 if the game has ended, else does not return
        """
        print("Player {}: depth = 2".format(self.player.getCurrentPlayer()))
        self.player.changeCurrentPlayer()

        red_start = time.time()
        result = self.alphabeta(2, True, -9999, 9999, 2)
        red_end = time.time()
        red_elapse = red_end - red_start
        print("red elapse: ", red_elapse)
        self.red_count += 1
        self.timetable_red.append((self.red_count, red_elapse))

        # movePiece using result piece and position:
        print("Result: ", result)
        self.movePiece(self.pieceList, result['Piece'], result['Pos'])
        self.player.UpdatePieceList(self.pieceList)
        self.playGUI.drawBoard(self.player)

        check = self.setNextMove_AB()

        if (self.EndGame()) or (check == 0):
            print(self.timetable_black)
            return 0
        else:
            pass

    def setNextMove_AB(self):
        """
        This function calls the Minimax algorithm with Alpha-Beta pruning and update the Board data with its result
        and pass that result to the SCARA arm

        :return: result containing (old_pos, new_pos, check_capture) to the SCARA arm
        """
        print("Player {} depth = 2".format(self.player.getCurrentPlayer()))

        # Set timer start here:
        black_start = time.time()
        # Call Alpha Beta algorithm. Result is a dict: (score, piece, pos)
        result = self.alphabeta(2, False, -9999, 9999, 2)
        # Set timer stop here:
        black_end = time.time()
        black_elapse = black_end - black_start
        print("black elapse: ", black_elapse)
        self.black_count += 1
        self.timetable_black.append((self.black_count, black_elapse))

        # movePiece using result piece and position:
        print("Result: ", result)
        old_pos = self.pieceList[self.find(self.pieceList, 'Symbol', result['Piece'])]['Pos']
        check_capture = self.movePiece(self.pieceList, result['Piece'], result['Pos'])

        # Update the chess piece list and the simulation board
        self.player.UpdatePieceList(self.pieceList)
        self.playGUI.drawBoard(self.player)

        # Update BoardData_update.csv
        df = pd.DataFrame(self.pieceList)
        df.set_index('Name', inplace=True)
        print("df: \n", df)
        df.to_csv("src\\BoardData_Update.csv")

        # Check if the opponent player still has the General
        check_endgame = self.EndGame()
        if (check_endgame is True):
            print(self.timetable_black)
            # pd.DataFrame(self.logdata, columns=["Piece", "Pos", "Score", "Depth", "isMax", "Alpha", "Beta"]).to_csv("LogData.csv")
            return 0

        # Passing result to the SCARA arm
        else:
            self.player.changeCurrentPlayer()
            print("Information to pass: Old pos: {}, New pos: {}, check capture: {}, check Endgame: {}".
                  format(old_pos,
                         result['Pos'],
                         check_capture,
                         check_endgame))
            AB_result = (old_pos, result['Pos'], check_capture)
            return AB_result

    def movePiece(self, pieceList, piece, pos):
        """
        This function update the current position of the chess piece in the chess piece list

        :param pieceList: The current chess piece list
        :param piece: The chess piece
        :param pos: The position to update
        :return: The captured status
        """
        # check captured:
        check = self.player.checkCaptured(self.pieceList, pos)

        for i in range(len(pieceList)):
            # print("I{} = ".format(i),self.pieceList['Symbol'][i])
            if piece == pieceList[i]['Symbol']:
                # print('Old: {} to {}'.format( pieceList[i]['Pos'], pos))
                self.pieceList[i]['Pos'] = pos
                break
            else:
                pass
        return check

    def EndGame(self):
        """
        This function calls the isGeneralExist() function to check if the game has ended

        :return: the Boolean deciding whether the game has ended
        """
        check_endgame = not self.player.getPlayer().isGeneralExist()

        return check_endgame

    def nextState(self, piece, pos):
        """
        This function clone the current State to not affect the current chess piece list

        :param piece: The chess piece to change position
        :param pos: The position to change
        :return: The State with the changed position
        """
        # Copy current pieceList to new state obj
        nextState = copy.deepcopy(self)

        nextState.movePiece(nextState.player.getCurrentPieceList(), piece, pos)

        return nextState

    def alphabeta(self, depth, isMax, alpha, beta, depth_flag):
        """
        Minimax algorithm with Alpha-Beta pruning. This algorithm is upgraded
        to fix the pruning problem at the highest depth

        :param depth: The times a player is changed.
        :param isMax: A Boolean to decide whether a Node is a Maximizer or a Minimizer
        :param alpha: Initial value is -9999. This variable is updated at every Max node
        :param beta: Initial value is 9999. This variable is updated at every Min node
        :param depth_flag: The flag to inform and compared with the current depth
        :return: The result containing (score, piece, position)
        """
        # Check for endgame condition:
        if self.EndGame() == True:
            # print(self.player.getCurrentPieceList())
            result = {
                "Score": '',
                "Piece": '',
                "Pos": ''
            }
            pass
            # Get score of pieceList
            result['Score'] = ((99999999) * self.player.getCurrentPlayer(), depth + 1)
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
            result['Score'] = (self.player.getPieceListScore(self.pieceList), depth + 1)
            return result

        # Change current player
        self.player.changeCurrentPlayer()

        # Get possible move of the current player
        possibleMoves = self.player.getAllPossibleMoves()
        eval_result = list()

        # Loop through possible move and create new piecelist with each move
        for i in range(len(possibleMoves)):
            # Collect inputs (piece and piece's position)
            piece = possibleMoves[i][0]['Symbol']
            to_pos = possibleMoves[i][1]

            # Create new pieceList
            nextState = self.nextState(piece, to_pos)

            # Recall alpha beta to collect score from lower depth
            alpha_beta_result = nextState.alphabeta(depth - 1, not isMax, alpha, beta, depth_flag)

            try:
                score = alpha_beta_result['Score']

            except:
                print("\nWrong\n")

            result = {
                "Score": score,
                "Piece": piece,
                "Pos": to_pos
            }

            eval_result.append(result)
            if isMax:
                alpha = max(alpha, score[0])

            else:
                beta = min(beta, score[0])
            # Check if depth is at top depth. Don't check beta <= alpha to avoid wrong pruning
            if depth == depth_flag and (score[0] != 99999999 or score[0] != -99999999):
                pass

            else:
                if beta <= alpha:
                    # print("Prun")
                    return eval_result[-1]

        # Get score from eval result
        score_list = list()
        id = ''
        for j in range(len(eval_result)):
            score_list.append(eval_result[j]['Score'])

        # Find index, check max depth , base on max or min value of tuple score
        if isMax:
            id = score_list.index(max(filter(lambda t: t[0] == max(score_list,
                                                                   key=itemgetter(0))[0], score_list),
                                      key=itemgetter(1)))
        else:
            id = score_list.index(max(filter(lambda t: t[0] == min(score_list,
                                                                   key=itemgetter(0))[0], score_list),
                                      key=itemgetter(1)))

        return eval_result[id]

