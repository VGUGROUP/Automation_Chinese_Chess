class Rule():
    def __init__(self):
        # Define board dimension
        self.minCol = 1
        self.maxCol = 9
        self.minRow = 1
        self.maxRow = 10
        #-----------------------
        pass
    def isValidMove(self,piece,pos, pieceList):

        pass
    #-------------------------------------------------#
    #      CHECK ALL ROW IN COL OR ALL COL IN ROW     #
    #-------------------------------------------------#
    def findPieceOnCol(self, initial_pos, pieceList, increase):
        row = initial_pos[0]
        col = initial_pos[1]
        # print("Row: ",row)
        # print("Row type: ",type(row))
        while (row >= self.minRow) and (row <= self.maxRow):
            if increase:
                row += 1
            else:
                row -= 1
            # print("row in fpoc: ",row)
            for i in range(len(pieceList)):
                pos = (row, col)
                if pieceList[i]['Pos'] == pos:
                    # print('Piece on col: ',pieceList[i])
                    return pieceList[i]
                else:
                    continue
        return None

    def findPieceOnRow(self, initial_pos, pieceList, increase):
        row = initial_pos[0]
        col = initial_pos[1]
        while (col >= self.minCol) and (col <= self.maxCol):
            if increase:
                col += 1
            else:
                col -= 1
            for i in range(len(pieceList)):
                if pieceList[i]['Pos'] == (row, col):
                    # print('Piece on row: ',pieceList[i])
                    return pieceList[i]
                else:
                    continue
        return None
    #-------------------------------------------------#
    #           POSSIBLE MOVE FOR CANNON              #
    #-------------------------------------------------#
    def possibleMoveForCannon(self, piece, pieceList):
        legalMove = list()
        initial_pos = piece['Pos']
        row = piece['Pos'][0]
        col = piece['Pos'][1]
        for i in range(2):  # i= 0(bool(i)= False) and i= 1(bool(i) = True)

            # find row:
            result = self.findPieceOnCol(initial_pos, pieceList, bool(i))

            if result is not None:

                # get pos of piece found in result
                found_piece_row = result['Pos'][0]

                # Get pos from initial pos to piece found pos, +1: Lower row ; -1: Upper row
                for j in range(row - 1, found_piece_row, -1) if i == 0 else \
                        range(row + 1, found_piece_row, 1):

                    legalMove.append((j, col))

                result = self.findPieceOnCol(result['Pos'], pieceList, bool(i))

                if result is not None and result['Team'] != piece['Team']:

                    legalMove.append(result['Pos'])

            else:
                for j in range(row-1, self.minRow, -1) if i == 0 else range(row+1, self.maxRow+1, 1):

                    legalMove.append((j, col))

           # find col:
            result = self.findPieceOnRow(initial_pos, pieceList, bool(i))

            if result is not None:

                # get pos of piece found in result
                found_piece_col = result['Pos'][1]

                # Get pos from initial pos to piece found pos , +1: To the right col ; -1: To the left col
                for j in range(col-1, found_piece_col, -1) if i == 0 else range(col+1, found_piece_col, 1):

                    legalMove.append((row,j))

                result = self.findPieceOnRow(result['Pos'], pieceList, bool(i))

                if result is not None and result['Team'] != piece['Team']:

                    legalMove.append(result['Pos']) #int form

            else:
                for j in range(col-1, self.minCol-1, -1) if i == 0 else range(col+1, self.maxCol+1, 1):

                    legalMove.append((row,j))

        return legalMove
    #-------------------------------------------------#
    #              POSSIBLE MOVE FOR CAR              #
    #-------------------------------------------------#
    def possibleMoveForCar(self, piece, pieceList):
        legalMove = list()
        initial_pos = piece['Pos']
        row = piece['Pos'][0]
        col = piece['Pos'][1]
        for i in range(2):  # i= 0(bool(i)= False) and i= 1(bool(i) = True)

            # Find Row:
            result = self.findPieceOnCol(initial_pos, pieceList, bool(i))

            if result is not None:

                # Get pos of piece found in result
                found_piece_row = result['Pos'][0]

                # Get pos from initial pos to piece found pos, +1: Lower row ; -1: Upper row
                for j in range(row-1, found_piece_row, -1) if i == 0 \
                        else range(row+1, found_piece_row, 1):

                    legalMove.append((j, col))

                if result['Team'] != piece['Team']:
                    legalMove.append(result['Pos'])
            else:

                for j in range(row-1, self.minRow - 1, -1) if i == 0 else \
                        range(row+1, self.maxRow + 1, 1):

                    legalMove.append((j, col))

           # find col:
            result = self.findPieceOnRow(initial_pos, pieceList, bool(i))
            if result is not None:

                # get pos of piece found in result
                found_piece_col = result['Pos'][1]

                # Get pos from initial pos to piece found pos , +1: To the right col ; -1: To the left col
                for j in range(col-1, found_piece_col, -1) if i == 0 \
                        else range(col+1, found_piece_col, 1):

                    legalMove.append((row, j))

                if result['Team'] != piece['Team']:

                    legalMove.append(result['Pos'])  #int form

            else:
                for j in range(col-1, self.minCol - 1, -1) if i == 0 else \
                        range(col+1, self.maxCol + 1, 1):

                    legalMove.append((row,j))
        return legalMove
    #-------------------------------------------------#
    #            POSSIBLE MOVE FOR HORSE              #
    #-------------------------------------------------#
    def possibleMoveForHorse(self, piece, pieceList):
        legalMove = list()
        row = piece['Pos'][0]
        col = piece['Pos'][1]
        for i in range(2):
            # Check for Row boundaries:
            if ((row - 2 >= self.minRow) if i == 0 else (row + 2 <= self.maxRow)):


                result = ((row - 1) if i == 0 else (row + 1), col)

                if all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True:

                    # Check upper right and lower right ( +1 col) -> || ; ||_
                    result = (((row - 2) if i == 0 else (row + 2)), col + 1)

                    if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                        range(len(pieceList))]) == True:

                            legalMove.append(result)

                    elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True \
                        and col +1 <= self.maxCol:

                        legalMove.append(result)
                    #                                             _
                    # Check upper left and lower left ( -1 col) -> || ; _||
                    result = (((row - 2) if i == 0 else (row + 2)),col - 1)

                    if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                        range(len(pieceList))]) == True:

                            legalMove.append(result)

                    elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))])\
                        and col - 1 >= self.minCol:

                        legalMove.append(result)

            # Check for Col boundaries:
            if ((col - 2 >= self.minCol) if i == 0 else (col + 2 <= self.maxCol)):

                result = (row, ((col - 1) if i == 0 else (col + 1)))

                if all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True:

                    # Check upper right and lower right ( +1 row) -> |__ ; __|
                    result = (row + 1, ((col - 2) if i == 0 else (col + 2)))

                    if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                        range(len(pieceList))]) == True:

                        legalMove.append(result)

                    elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True \
                        and row +1 <= self.maxRow:

                        legalMove.append(result)
                    #                                                 __      __
                    # Check upper left and lower left ( -1 row) ->   |    ;     |
                    result = (row - 1, ((col - 2) if i == 0 else (col + 2)))

                    if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                                range(len(pieceList))]) == True:

                        legalMove.append(result)

                    elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True \
                        and row - 1 >= self.minRow:

                        legalMove.append(result)

        return legalMove
    #-------------------------------------------------#
    #           POSSIBLE MOVE FOR ELEPHANT            #
    #-------------------------------------------------#
    def possibleMoveForElephant(self, piece, pieceList):
        legalMove = list()
        row = piece['Pos'][0]
        col = piece['Pos'][1]
        for i in range(2):  # i = 0 : Down ; i = 1 : Up
            for j in range(2):  # j = 0 : Left ; j = 1 : Right

                if (((((row <= self.maxRow - 2) and (row >= self.maxRow - 3)) if i == 0 else \
                       ((row >= self.minRow + 2) and (row <= self.minRow + 3))) and \
                       ((col >= self.minCol + 2) if j == 0 else (col <= self.maxCol - 2))) or \
                    (((row <= self.minRow + 2) if i == 0 else (row >= self.maxRow - 2)) and \
                     ((col >= self.minCol + 2) if j == 0 else (col <= self.maxCol - 2)))):

                    result = (((row + 1) if i == 0 else (row - 1)), ((col - 1) if j == 0 else (col + 1)))

                    # print("i = {}, j = {}, result: {}".format(i,j,result))

                    if all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True:

                        result = (((row + 2) if i == 0 else (row - 2)), ((col - 2) if j == 0 else (col + 2)))

                        if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                                range(len(pieceList))]) == True:

                            legalMove.append(result)

                        elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True:

                            legalMove.append(result)

        return legalMove
    #-------------------------------------------------#
    #            POSSIBLE MOVE FOR ADVISOR            #
    #-------------------------------------------------#
    def possibleMoveForAdvisor(self, piece, pieceList):
        legalMove = list()
        row = piece['Pos'][0]
        col = piece['Pos'][1]
        for i in range(2):  # i = 0 : Down ; i = 1 : Up
            for j in range(2):  # j = 0 : Left ; j = 1 : Right

                if (((row <= self.minRow + 1) if i == 0 else (row >= self.minRow + 1)) and \
                    ((col >= self.minCol + 4) if j == 0 else (col <= self.maxCol - 4))) or \
                    (((row <= self.maxRow - 1) if i == 0 else (row >= self.maxRow - 1)) and \
                     ((col >= self.minCol +4) if j == 0 else (col <= self.maxCol - 4))):

                    result = ((row + 1) if i == 0 else (row - 1),\
                              (col - 1) if j == 0 else (col + 1))
                    # print("I: {}, result: {}".format(i, result))

                    if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                            range(len(pieceList))]):

                        legalMove.append(result)

                    elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]):

                        legalMove.append(result)

        return legalMove
    #-------------------------------------------------#
    #            POSSIBLE MOVE FOR GENERAL            #
    #-------------------------------------------------#
    def possibleMoveForGeneral(self, piece, pieceList):
        legalMove = list()
        initial_pos = piece['Pos']
        row = piece['Pos'][0]
        col = piece['Pos'][1]
        for i in range(4):  # i = 0 : Down ; i = 1 : Up ; i = 2 : Left ; i = 3 Right
            # i= 0(bool(i)= False) and i= 1(bool(i) = True)
            if i <= 1:
                # Find in Col:
                result = self.findPieceOnCol(initial_pos, pieceList, bool(i))
                # Chess Piece detected:
                if result is not None and (result['Name'] == "BlackGeneral" or result['Name'] == 'RedGeneral'):
                    legalMove.append(result['Pos'])

            if (((row <= self.minRow + 1) or (row <= self.maxRow - 1 and (row >= self.maxRow - 2))) if i == 0 else \
                (((row >= self.minRow + 1) and (row <= self.minRow + 2)) or (row >= self.maxRow - 1)) if i == 1 else \
                (col >= self.minCol + 4) if i == 2 else (col <= self.maxCol - 4)):

                result = (((row + 1) if i == 0 else (row - 1) if i == 1 else row),
                          ((col - 1) if i == 2 else (col + 1) if i == 3 else col))
                # print("I: {}, result: {}".format(i, result))
                if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                        range(len(pieceList))]):

                    legalMove.append(result)

                elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]):

                    legalMove.append(result)

        return legalMove
    #-------------------------------------------------#
    #            POSSIBLE MOVE FOR SOLDIER            #
    #-------------------------------------------------#
    def possibleMoveForSoldier(self, piece, pieceList):
        legalMove = list()
        row = piece['Pos'][0]
        col = piece['Pos'][1]
        initial_team = piece['Team']
        for i in range(3):  # i = 0 : Down or Up ; i = 1 : Left ; i = 2 : Right
            for j in range(2):  # j = 0 : Black ; j = 1 : Red
                if (((row <= self.maxRow - 1) and (initial_team == -1)) if j == 0 else \
                    ((row >= self.minRow + 1) and (initial_team == 1))) if i == 0 else \
                    ((col >= self.minCol + 1) and ((row >= self.maxRow - 4 and initial_team == -1)\
                    if j == 0 else (row <= self.minRow + 4 and initial_team == 1))) if i == 1 else \
                    ((col <= self.maxCol - 1) and ((row >= self.maxRow - 4 and initial_team == -1)\
                    if j == 0 else (row <= self.minRow + 4 and initial_team == 1))):

                    result = (((row + 1) if j == 0 else (row - 1)), col) if i == 0 \
                        else (row, col - 1) if i == 1 else (row, col + 1)

                    if any([result == pieceList[k]['Pos'] and pieceList[k]['Team'] != piece['Team'] for k in
                            range(len(pieceList))]) == True:
                        legalMove.append(result)

                    elif all([result != pieceList[k]['Pos'] for k in range(len(pieceList))]) == True:
                        legalMove.append(result)

        return legalMove

