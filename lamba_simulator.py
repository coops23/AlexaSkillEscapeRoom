import game, time

escape_room = None

class Start:
    def start(self):
        global escape_room

        escape_room = game.EscapeRoomGame(None)
        return escape_room.intro()

class Menu:
    def can_handle(self):
        global escape_room

        return not escape_room.game_playing

    def menu(self, user_input):
        global escape_room

        if self.can_handle():
            return escape_room.menu(user_input)
        return ""

class Game:
    def can_handle(self):
        global escape_room

        return escape_room.game_playing

    def game(self, action, direction, objects, items, cancel, combo):
        global escape_room

        if self.can_handle():
            return escape_room.room(action, direction, objects, items, cancel, combo)
        return ""

class Exit:
    def exit(self):
        global escape_room

        return escape_room.exit(None)

def main():
    # action - direction - objects - items - cancel - combo
    user_inputs = [["look", "left", "", "", "", ""],
                   ["look", "right", "", "", "", ""],
                   ["look", "up", "", "", "", ""],
                   ["look", "down", "", "", "", ""],
                   ["look", "forward", "", "", "", ""],
                   ["inspect", "", "rug", "", "", ""],
                   ["inventory", "", "", "", "", ""],
                   ["use", "", "pillow", "knife", "", ""],
                   ["inventory", "", "", "", "", ""],
                   ["inspect", "", "bed", "", "", ""],
                   ["use", "", "wires", "electrical tape", "", ""],
                   ["inspect", "", "switch", "", "", ""],
                   ["look", "up", "", "", "", ""],
                   ["inspect", "", "cabinet", "", "", ""],
                   ["", "", "", "", "", "1345"],
                   ["inventory", "", "", "", "", ""],
                   ["use", "", "bars", "wrench", "", ""],
                   ["use", "", "window", "brick", "", ""],
                   ["look", "left", "", "", "", ""],
                   ["look", "right", "", "", "", ""],
                   ["look", "up", "", "", "", ""],
                   ["look", "down", "", "", "", ""],
                   ["look", "forward", "", "", "", ""],
                   ["inspect", "", "poster", "", "", ""],
                   ["inspect", "", "door", "", "", ""],
                   ["inspect", "", "handle", "", "", ""],
                   ["inspect", "", "table", "", "", ""],
                   ["inspect", "", "helmet", "", "", ""],
                   ["inspect", "", "screen", "", "", ""],
                   ["inspect", "", "window", "", "", ""],
                   ["inventory", "", "", "", "", ""],
                   ["use", "", "helmet", "coin", "", ""],
                   ["inspect", "", "console", "", "", ""],
                   ["", "", "", "", "cancel", ""],
                   ["look", "forward", "", "", "", ""],
                   ["inspect", "", "screen", "", "", ""],
                   ["inspect", "", "console", "", "", ""],
                   ["", "", "", "", "", "2013"]
                   ]

    start_handler = Start()
    menu_handler = Menu()
    game_handler = Game()
    exit_handler = Exit()

    print(start_handler.start())
    print(menu_handler.menu("start"))
    for inputs in user_inputs:
        action = inputs[0]
        direction = inputs[1]
        objects = inputs[2]
        items = inputs[3]
        cancel = inputs[4]
        combo = inputs[5]

        speak_output = game_handler.game(action=action, direction=direction, objects=objects, items=items, cancel=cancel, combo=combo)
        print(str(inputs) + "\t\t\t\t\t" + str(speak_output))
        if escape_room.game_victory:
            escape_room.exit(None)
            print("You finished in %s" % escape_room.get_game_time())
        time.sleep(0.1)
    exit_handler.exit()

if __name__ == "__main__":
    main()