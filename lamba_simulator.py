import game

escape_room = game.EscapeRoom()

class Start:
    global escape_room

    def start(self):

class Menu:
    global escape_room

    def menu(self):

class Game:
    global escape_room

    def game(self):

class Exit:
    global escape_room

    def exit(self):

def main():
    user_inputs_bedroom = [["look", "left", "", "", "", ""],
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
                           ["use", "", "window", "brick", "", ""]
                           ]

    user_inputs_spaceship = [["look", "left", "", "", "", ""],
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
                             ["", "", "", "", "", "2013"],
                             ]

if __name__ == "__main__":
    main()