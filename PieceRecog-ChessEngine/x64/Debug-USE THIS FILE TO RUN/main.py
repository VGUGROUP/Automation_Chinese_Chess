# import Local Libs
from src.State import State
from src.ArmControl import ArmControl
if __name__ == "__main__":
    SCARA = ArmControl()
    Game = State()
    Game.initGameState()
    while 1:
        while 1:
            button_check = SCARA.ReadButton()
            print("button: ", button_check)
            if button_check == 'Done playing\r\n':
                break
        result = Game.playGame()
        print("result: ", result)
        # Result variable returns 2 forms: True if EndGame State satisfied ; tuple if False
        if result is True:
            break
        else:
            SCARA.RunSCARA(result[0], result[1], result[2])

