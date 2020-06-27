# import os
# import re
# import re
# import pandas as pd
# import csv
# import json
# # import threading
# import concurrent.futures
# import datetime
# import time
# # Player_list = {
# #     "RED":1,
# #     "BLACK":-1
# # }
# # data ={
# #         ((1,1), Player_list["BLACK"],"BC1"),
# #        ((1,2), Player_list["BLACK"],"BH1"),
# #        ((1,3), Player_list["BLACK"],"BE1"),
# #        ((1,4), Player_list["BLACK"],"BA1"),
# #        ((1,5), Player_list["BLACK"],"BG1"),
# #        ((1,6), Player_list["BLACK"],"BA1"),
# #        ((1,7), Player_list["BLACK"],"BE2"),
# #        ((1,8), Player_list["BLACK"],"BH2"),
# #        ((1,9), Player_list["BLACK"],"BC2"),
# #        ((3,2), Player_list["BLACK"],"BO1"),
# #        ((3,8), Player_list["BLACK"],"BO2"),
# #        ((4,1), Player_list["BLACK"],"BS1"),
# #        ((4,3), Player_list["BLACK"],"BS2"),
# #        ((4,5), Player_list["BLACK"],"BS3"),
# #        ((4,7), Player_list["BLACK"],"BS4"),
# #        ((4,9), Player_list["BLACK"],"BS5"),
# #     # Red Pieces
# #        ((10, 1), Player_list["RED"], "RC1"),
# #        ((10, 2), Player_list["RED"], "RH1"),
# #        ((10, 3), Player_list["RED"], "RE1"),
# #        ((10, 4), Player_list["RED"], "RA1"),
# #        ((10, 5), Player_list["RED"], "RG1"),
# #        ((10, 6), Player_list["RED"], "RA1"),
# #        ((10, 7), Player_list["RED"], "RE2"),
# #        ((10, 8), Player_list["RED"], "RH2"),
# #        ((10, 9), Player_list["RED"], "RC2"),
# #        ((8, 2), Player_list["RED"], "RO1"),
# #        ((8, 8), Player_list["RED"], "RO2"),
# #        ((7, 1), Player_list["RED"], "RS1"),
# #        ((7, 3), Player_list["RED"], "RS2"),
# #        ((7, 5), Player_list["RED"], "RS3"),
# #        ((7, 7), Player_list["RED"], "RS4"),
# #        ((7, 9), Player_list["RED"], "RS5")}
# # # data_csv = pd.DataFrame(data).to_csv('Data.csv',index=False)
# # data_csv = pd.read_csv('BoardData.csv')
# # # print(data_csv)
# # pieceList =[]
# # for i in range(len(data_csv)):
# #     # print(data_csv["Name"][i],data_csv["Pos"][i],data_csv["Symbol"][i],data_csv["Team"][i])
# #     pieceList.append({
# #         'Name': data_csv["Name"][i],
# #         'Pos': data_csv["Pos"][i],
# #         'Symbol': data_csv["Symbol"][i],
# #         'Team': data_csv["Team"][i]
# #     })
#
# # print(sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))]))
# # pieceList.pop(3)
# # print(sum([pieceList[k]['Team'] == -1 for k in range(len(pieceList))]))
#
# # print(pieceList.count(all([pieceList[k]['Team'] == -1 for k in pieceList])))
#
# # print(data_total[0])
# # df = pd.DataFrame(data_total).to_csv('OldBoardData.csv', index=False)
# # dict_new = pd.read_csv('OldBoardData.csv').to_dict()
# # print(dict_new)
# # with open('Data.csv','wb') as out:
# #     csv_out=csv.writer(out)
# #     csv_out.writerow()
# #     for row in data:
# #         csv_out.writerow(row)
# # ChessType = pd.DataFrame(data, columns= ['Black', 'Red'])
# # Black_Pos = []
# # Red_Pos = []
# # Red_Symbol=[]
# # Black_Symbol=[]
# # Black_Team=[]
# # Red_Team=[]
# # for i in range(len(data)):
# #     for j in range(len(data[i])):
# #         if data[i][j][1] == 1:# Red
# #             Red_Pos.append(data[i][j][0])
# #             Red_Symbol.append(data[i][j][2])
# #             Red_Team.append(data[i][j][1])
# #         else:
# #             Black_Pos.append(data[i][j][0])
# #             Black_Symbol.append(data[i][j][2])
# #             Black_Team.append(data[i][j][1])
# #
# # # Black_data = pd.DataFrame(Black,columns=["Pos","Team","Name"])
# # # Red_data = pd.DataFrame(Red,columns=["Pos","Team","Name"])
# # main_dict = {
# #     "Black":
# #         {
# #             "Symbol": Black_Symbol,
# #             "Pos": Black_Pos,
# #             "Team": Black_Team
# #         },
# #     "Red":
# #         {
# #             "Symbol":Red_Symbol,
# #             "Pos": Red_Pos,
# #             "Team": Red_Team
# #         }
# # }
# # df1 = pd.DataFrame(main_dict["Black"],columns=["Symbol", "Pos", "Team"])
# # df2 = pd.DataFrame(main_dict["Red"],columns=["Symbol", "Pos", "Team"])
# #
# # # print(df1)
# # # print(df2)
# #
# # frames = [df1,df2]
# # df_keys = pd.concat(frames, keys=['Black', 'Red'])
# # # print(df_keys)
# # # main_df = pd.DataFrame(frames,columns=['Black','Red'])
# # df_keys.to_csv('OldBoardData.csv', index=False)
# # df_keys.to_csv('NewBoardData.csv', index=False)
# #
# # #
# # current_BoardState = pd.read_csv('OldBoardData.csv').to_dict()
# # print(len(current_BoardState['Pos']))
# # a = ''
# # pos = '(10, 1)'
# # for i in range(len(current_BoardState['Pos'])):
# #     # print(type(current_BoardState['Pos'][i]))
# #     if current_BoardState['Pos'][i] == pos:
# #         # print("curr :",current_BoardState['Symbol'][i])
# #         a = current_BoardState['Symbol'][i]
# #     else:
# #         pass
# # if a == '':
# #     a = "*"
# # print(a)
#
# possibleMove = []
#
#
# def thread_task(lock, search_range):
#     for i in range(search_range[0], search_range[1]):
#         if i % 2 == 0 or i % 2 != 0: # Chan
#             print(i)
#             lock.acquire()
#             if i == 0:
#                 movelist = getList0()
#                 print("0: ", movelist)
#                 for j in range(len(movelist)):
#                     possibleMove.append((0, movelist[j]))
#             elif i == 1:
#                 movelist = getList1()
#                 print("1: ", movelist)
#                 for j in range(len(movelist)):
#                     possibleMove.append((1, movelist[j]))
#             if i == 2:
#                 movelist = getList2()
#                 print("2: ", movelist)
#                 for j in range(len(movelist)):
#                     possibleMove.append((2,movelist[j]))
#             if i == 3:
#                 movelist = getList3()
#                 print("3: ", movelist)
#                 for j in range(len(movelist)):
#                     possibleMove.append((3, movelist[j]))
#             lock.release()
#     return possibleMove
# def task1(possibleMove, search_range):
#     for i in range(search_range[0], search_range[1]):
#         vars()['movelist_{}'.format(i)] = eval('getList{}()'.format(i))
#         # print("HAHA: ", vars()['movelist_{}'.format(i)])
#         for j in range(len(vars()['movelist_{}'.format(i)])):
#             possibleMove.append((i, vars()['movelist_{}'.format(i)][j]))
#     return possibleMove
#
# def getList0():
#     movelist=[]
#     for i in range(1):
#         movelist.append((0,i))
#     return movelist
#
# def getList1():
#     movelist=[]
#     for i in range(1):
#         movelist.append((1,i))
#     return movelist
#
# def getList2():
#     movelist=[]
#     for i in range(1):
#         movelist.append((2,i))
#     return movelist
#
# def getList3():
#     movelist=[]
#     for i in range(2):
#         movelist.append((3,i))
#     return movelist
# if __name__ == "__main__":
#     possibleMove=[]
#
#     search_range = (0, 4)
#     # start_pos = datetime.datetime.now()
#     start_pos = time.time()
#     # multithread way:
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future = executor.submit(task1, possibleMove, (search_range[0], (search_range[0]+search_range[1])//2))
#         future = executor.submit(task1, future.result(), (((search_range[0]+search_range[1])//2), search_range[1]))
#         possibleMove = future.result()
#     # time.sleep(1)
#     end_pos = time.time()
#     # end_pos = datetime.datetime.now()
#     elapse = end_pos - start_pos
#     print("possi time: ", elapse)
#     print(possibleMove)
#     # print("t2: ",t2)
#     d = "BlackCannon"
#     print(re.findall('(?:Black|Red)(.*)', d))
#     print("possibleMoveFor{}(self.pieceList[i],self.pieceList)".format(re.findall('(?:Black|Red)(.*)', d)[0]))
#
#
#
#     # multithread way:
#     # with concurrent.futures.ThreadPoolExecutor() as executor:
#     #     future = executor.submit(task1, possibleMove, (search_range[0], (search_range[0]+search_range[1])//2))
#     #     future = executor.submit(task1, future.result(), (((search_range[0]+search_range[1])//2), search_range[1]))
#     #     possibleMove = future.result()
#
#     normal: 0.001020193099975586
#     0.01562047004699707

# import random
# a = random.getrandbits(64)
# print(a)
import serial
import serial.tools.list_ports


ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
    if 'Arduino' in p.description:
        print(p[0])