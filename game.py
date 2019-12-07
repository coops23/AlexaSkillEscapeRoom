from datetime import datetime


def get_level(level_number, bedroom, spaceship):
    if level_number == 0:
        return bedroom
    else:
        return spaceship


def save_game(handler_input, gameTimer, bedroom, spaceship, level_number):
    attributes_manager = handler_input.attributes_manager

    level = get_level(level_number, bedroom, spaceship)

    game_attributes = {
        "inventory": level.inventory,
        "elapsed": gameTimer.elapsed,
        "level": level_number,
        "wires_fixed": bedroom.wires_fixed,
        "power_on": bedroom.power_on,
        "bars_removed": bedroom.bars_removed,
        "helmet_powered": spaceship.helmet_powered
    }

    attributes_manager.persistent_attributes = game_attributes
    attributes_manager.save_persistent_attributes()


def load_game(handler_input, gameTimer, bedroom, spaceship):
    attr = handler_input.attributes_manager.persistent_attributes
    attributes_are_present = (
                "inventory" in attr and "elapsed" in attr and "level" in attr and "wires_fixed" in attr
                and "power_on" in attr and "bars_removed" in attr and "helmet_powered" in attr)

    if attributes_are_present:
        level_number = attr['level']
        level = get_level(level_number, bedroom, spaceship)

        level.inventory = attr['inventory']
        gameTimer.elapsed = attr['elapsed']  # month is a string, and we need to convert it to a month index later
        bedroom.wires_fixed = attr['wires_fixed']
        bedroom.power_on = attr['power_on']
        bedroom.bars_removed = attr['bars_removed']
        spaceship.helmet_powered = attr['helmet_powered']

        return level_number
    else:
        save_game(handler_input, gameTimer, bedroom, spaceship, 0)

        return 0


class GameTimer:
    def __init__(self):
        self.start_time = 0
        self.elapsed = 0

    def start_game_timer(self):
        self.start_time = datetime.now()

    def update_game_time(self):
        if self.elapsed != 0:
            self.elapsed += datetime.now() - self.start_time
        else:
            self.elapsed = datetime.now() - self.start_time

    def get_game_time(self):
        return round(self.elapsed.total_seconds(), 2)

    def clear(self):
        self.start_time = 0
        self.elapsed = 0


class BaseGame:
    INTRO_FIRST_TIME = "Hi there, welcome to Escape Room. Say start to begin or instructions to hear how to play"
    INTRO_WELCOME_BACK = "Welcome back! Say start to continue where you left off or instructions to hear how to play " \
                         "again"

    MENU_INSTRUCTION = "In this game you will attempt to escape the room by searching for clues, solving puzzles and " \
                       "using that clever brain of yours. You can perform four actions. Look. Inspect. Use. " \
                       "And instructions. You can look. Up. Down. Left. Right. And forward. You can inspect any " \
                       "object that is in the room. Use any item in your inventory on an object in the " \
                       "environment. To check what you have. Say inventory. For more time say wait. Say start to begin."
    ACTION_HELP = "Sorry, you can not do that. You can look in a direction, inspect an object, use an item on " \
                  "an object, check your inventory or say wait for more time."
    DIRECTION_HELP = "You can look. Up. Down. Left. Right. And forward."
    OBJECT_HELP = "Sorry, you do not see that object."
    HAS_ITEM_HELP = "Sorry, you do not have that item. Say inventory to check what you have."
    COMBO_HELP = "Sorry, you cannot do that. Please say cancel to go back or state four digits."
    MENU_HELP = "Sorry, you cannot do that. Please say start or say instructions to hear how to play."
    MENU_ASK = "Please say start or say instructions to hear how to play."
    GAME_ASK = "What would you like to do?" + ACTION_HELP
    COMBO_ASK = "Please say cancel to go back or state four digits."
    START_SOUND = "<audio src=\"soundbank://soundlibrary/bell/chimes/chimes_12\"/>"
    WAIT_SOUND = "<break time=\"10s\"/>" \
                 "<break time=\"10s\"/>" \
                 "<audio src='soundbank://soundlibrary/alarms/beeps_and_bloops/bell_02'/>" \
                 "What would you like to do?"

    def __init__(self):
        self.inventory = []
        self.game_victory = False
        self.game_playing = False
        self.looking_at_puzzle = False

    def intro(self, beginning=True):
        speak_output = "<speak>"
        speak_output += self.START_SOUND
        if not beginning:
            speak_output += self.INTRO_WELCOME_BACK
        else:
            speak_output += self.INTRO_FIRST_TIME
        speak_output += "</speak>"
        self.game_playing = False

        return speak_output

    def get_inventory(self):
        return self.inventory

    def add_inventory(self, item):
        if not self.has_item(item):
            self.inventory.append(item)

    def has_item(self, item):
        return item in self.inventory

    def reset(self):
        self.inventory = []
        self.game_victory = False
        self.game_playing = False
        self.looking_at_puzzle = False

    def room(self, action, direction, objects, items, cancel, combo):
        pass


class Bedroom(BaseGame):
    MENU_START_GAME = "You wake up in a daze. Unsure of where you are or how you got there. A quick glance reveals " \
                      "you are in a small bedroom. You slowly prop yourself up and peer through the window. You " \
                      "appear to be in the middle of a forest. Turning to the door. You realize you might be " \
                      "trapped! " \
                      "You turn the handle in a panic and scream " \
                      "for help! After a couple minutes you realize no one is coming. And begin to look around."
    SCENE_LEFT = "You see two exposed wires petruding from the wall, a switch and a guitar."
    SCENE_FRONT = "You see a window covered with metal bars. Like a prison. A chill goes down your spine."
    SCENE_DOWN = "You see an old rug covering most of the floor. It is an ugly rug. It displeases you."
    SCENE_UP = "You see the ceiling light. It appears to be off."
    SCENE_UP_POWER_ON = "You see the ceiling light. It appears to be on now."
    SCENE_RIGHT = "You see a bed and pillow and a cabinet that appears to have combination lock."

    INSPECT_CABINET = "You look at the cabinet. There appears to be four digit combination safe in one of the draws. " \
                      "What four digits would you like to try?"
    INSPECT_RUG = "You peer under the rug. There appears to be a knife. You take it for safe keeping."
    INSPECT_RUG_INSPECTED = "You look at the rug. It is ugly. It doesn't match the wall at all. " \
                            "You turn away in disgust."
    INSPECT_BED = "You peer under the bed. There appears to be a roll of electrical tape laying beneath the bed. " \
                  "You pick it up for safe keeping."
    INSPECT_BED_INSPECTED = "You look at the bed. You sit down on it. It is comfortable."
    INSPECT_PILLOW = "You pick up the pillow and give it a shake. It feels heavier than it should be."
    INSPECT_PILLOW_INSPECTED = "The pillow feels lighter than before. You put it back down."
    INSPECT_WINDOW = "You peer through the window. It appears to be pretty thick. " \
                     "You certainly couldn't break this yourself."
    INSPECT_BARS = "You inspect the bars. The bars are attached to the wall using a set of nuts and bolts."
    INSPECT_BARS_INSPECTED = "You look at the bars laying on the ground. Then continue on with your life."
    INSPECT_LIGHT_OFF = "You look up at the light. It appears to be off."
    INSPECT_LIGHT_ON = "You look up at the light. It is bright and hurts your eyes. You regret looking up."
    INSPECT_GUITAR = "The guitar looks to have two strings missing. It should have six. " \
                     "You notice string two and six are missing."
    INSPECT_SWITCH_NO_POWER = "You hit the switch. Nothing happens."
    INSPECT_SWITCH_POWER = "You hit the switch. You see the light on the ceiling turn on and hear a clicking " \
                           "sound come from the cabinet."
    INSPECT_SWITCH_POWER_INSPECTED = "You look at the switch. It is on."
    INSPECT_WIRES = "You see two wires sticking out the wall. You try to bend them together but they quickly fly apart."
    INSPECT_WIRES_CONNECTED = "You look at the two wires patched together with tape. You smile at your ingenuity."

    USE_KNIFE_PILLOW = "You use your knife to cut open the pillow. Revealing a wrench in the pillow. " \
                       "You pull it out wondering why someone would put a wrench in a pillow."
    USE_TAPE_WIRES = "You use the electrical tape to hold the two ends of the wires together. Looks like it holds!"
    USE_WRENCH_BARS = "You use the wrench to remove to loosen the nuts off the ends of the bars. " \
                      "The bars eventually comes off and fall to the floor."
    COMBO_SUCCESS = "You adjust the dials on the combination lock. And to your delight the safe swings open! " \
                    "Inside there is a brick. You pick it up for safe keeping."
    COMBO_FAILURE = "You adjust the dials on the combination lock. And pull at the door. The door is still locked."
    COMBO_NO_POWER = "You try the adjust the dials and they don't seem to move."
    COMBINATION = "1345"

    VICTORY = "You throw the brick at the window with all your might. And revel in delight as it smashes through. " \
              "You escape! "

    VICTORY_SOUND = "<audio src=\"soundbank://soundlibrary/glass/break_shatter_smash/break_shatter_smash_01\"/>"
    PILLOW_OPENING_SOUND = "<audio src=\"soundbank://soundlibrary/cloth_leather_paper/zippers/zippers_01\"/>"
    CABINET_OPENING_SOUND = "<audio src=\"soundbank://soundlibrary/doors/doors_squeaky/squeaky_11\"/>"
    CABINET_OPENING_FAILURE_SOUND = "<audio src=\"soundbank://soundlibrary/doors/doors_regular/regular_15\"/>"
    WIRES_ATTACHING_SOUND = "<audio src=\"soundbank://soundlibrary/electrical/arcs_sparks/arcs_sparks_13\"/>"
    BARS_REMOVED_SOUND = "<audio src=\"soundbank://soundlibrary/metal/metal_02\"/>"

    def __init__(self):
        BaseGame.__init__(self)
        self.wires_fixed = False
        self.power_on = False
        self.bars_removed = False
        self.tag = 0

    def reset(self):
        BaseGame.reset(self)
        self.wires_fixed = False
        self.power_on = False
        self.bars_removed = False

    def menu(self, menu_selection="", beginning=True):
        speak_output = "<speak>"
        if "start" in menu_selection:
            if beginning:
                speak_output += self.MENU_START_GAME

            self.game_playing = True

        elif "instructions" in menu_selection:
            speak_output += self.MENU_INSTRUCTION
        else:
            speak_output += self.MENU_HELP
        speak_output += "</speak>"

        return speak_output

    def room(self, action="", direction="", objects="", items="", cancel="", combo=""):
        speak_output = "<speak>"
        if not self.looking_at_puzzle:
            if "look" in action:
                if "left" in direction:
                    speak_output += self.SCENE_LEFT
                elif "right" in direction:
                    speak_output += self.SCENE_RIGHT
                elif "down" in direction:
                    speak_output += self.SCENE_DOWN
                elif "up" in direction:
                    if not self.power_on:
                        speak_output += self.SCENE_UP
                    else:
                        speak_output += self.SCENE_UP_POWER_ON
                elif "forward" in direction:
                    speak_output += self.SCENE_FRONT
                else:
                    speak_output += "Invalid direction. "
                    speak_output += self.DIRECTION_HELP
            elif "use" in action:
                valid_item = True
                valid_object = True
                if not self.has_item(items):
                    speak_output += self.HAS_ITEM_HELP
                    valid_item = False

                if objects not in ["cabinet", "bed", "pillow", "rug", "light", "bars", "window", "switch", "guitar",
                                   "wires"]:
                    speak_output += self.OBJECT_HELP
                    valid_object = False

                if valid_item and valid_object:
                    if "knife" in items and "pillow" in objects:
                        if not self.has_item("wrench"):
                            speak_output += self.PILLOW_OPENING_SOUND + "<break time=\"1s\"/>" + self.USE_KNIFE_PILLOW
                            self.add_inventory("wrench")
                        else:
                            speak_output += "You already destroyed that pillow."
                    elif "electrical tape" in items and "wires" in objects:
                        if not self.wires_fixed:
                            speak_output += self.WIRES_ATTACHING_SOUND + "<break time=\"1s\"/>" + self.USE_TAPE_WIRES
                            self.wires_fixed = True
                        else:
                            speak_output += "You admire your electrical handywork."
                    elif "wrench" in items and "bars" in objects:
                        speak_output += self.BARS_REMOVED_SOUND + "<break time=\"1s\"/>" + self.USE_WRENCH_BARS
                        self.bars_removed = True
                    elif "brick" in items and "window" in objects and self.bars_removed:
                        speak_output += self.VICTORY_SOUND + "<break time=\"1s\"/>" + self.VICTORY
                        self.game_victory = True

                        return speak_output
                    else:
                        speak_output += "You try to use the " + items + " on the " + objects + ". Nothing happens."

            elif "inspect" in action:
                if "cabinet" in objects:
                    if not self.has_item("brick"):
                        speak_output += self.INSPECT_CABINET
                        self.looking_at_puzzle = True
                    else:
                        speak_output += "You see a cabinet with a safe that is open."
                elif "bed" in objects:
                    if self.has_item("electrical tape"):
                        speak_output += self.INSPECT_BED_INSPECTED
                    else:
                        speak_output += self.INSPECT_BED
                        self.add_inventory("electrical tape")
                elif "pillow" in objects:
                    speak_output += self.INSPECT_PILLOW
                elif "rug" in objects:
                    if self.has_item("knife"):
                        speak_output += self.INSPECT_RUG_INSPECTED
                    else:
                        speak_output += self.INSPECT_RUG
                        self.add_inventory("knife")
                elif "light" in objects or "lights" in objects:
                    if not self.power_on:
                        speak_output += self.INSPECT_LIGHT_OFF
                    else:
                        speak_output += self.INSPECT_LIGHT_ON
                elif "bars" in objects:
                    speak_output += self.INSPECT_BARS
                elif "window" in objects:
                    speak_output += self.INSPECT_WINDOW
                elif "switch" in objects:
                    if self.wires_fixed:
                        if self.power_on:
                            speak_output += self.INSPECT_SWITCH_POWER_INSPECTED
                        else:
                            speak_output += self.INSPECT_SWITCH_POWER
                            self.power_on = True
                    else:
                        speak_output += self.INSPECT_SWITCH_NO_POWER
                elif "guitar" in objects:
                    speak_output += self.INSPECT_GUITAR
                elif "wires" in objects:
                    speak_output += self.INSPECT_WIRES
                else:
                    speak_output += self.OBJECT_HELP
            elif "inventory" in action:
                inventory = self.get_inventory()
                if len(inventory) > 0:
                    speak_output += "You have the following items."
                    for item in inventory:
                        speak_output += " " + item + ". "
                else:
                    speak_output += "You have no items in your inventory."
            elif "wait" in action:
                speak_output += self.WAIT_SOUND
            else:
                speak_output += self.ACTION_HELP
        else:
            if "cancel" in cancel:
                speak_output += "You leave the safe alone for now."
                self.looking_at_puzzle = False
            elif combo.isnumeric():
                if not self.power_on:
                    speak_output = self.COMBO_NO_POWER
                    self.looking_at_puzzle = False
                else:
                    if combo in self.COMBINATION:
                        if self.has_item("brick"):
                            speak_output += "The locker is already open."
                        else:
                            speak_output += self.CABINET_OPENING_SOUND + "<break time=\"1s\"/>" + self.COMBO_SUCCESS
                            self.add_inventory("brick")
                    else:
                        speak_output += self.CABINET_OPENING_FAILURE_SOUND + "<break time=\"1s\"/>" + self.COMBO_FAILURE
                    self.looking_at_puzzle = False
            elif "wait" in action:
                speak_output += self.WAIT_SOUND
            else:
                speak_output += self.COMBO_HELP

        speak_output += "</speak>"

        return speak_output


class SpaceShip(BaseGame):
    SPACESHIP_SOUND = "<audio src=\"soundbank://soundlibrary/scifi/amzn_sfx_scifi_spaceship_flyby_02\"/>"
    HELMET_POWERING_SOUND = "<audio src=\"soundbank://soundlibrary/electrical/buzz_hums/buzz_hums_07\"/>"
    DOOR_OPEN_SOUND = "<audio src=\"soundbank://soundlibrary/doors/doors_high_tech/high_tech_07\"/>"
    DOOR_OPEN_FAILURE_SOUND = "<audio src=\"soundbank://soundlibrary/scifi/amzn_sfx_scifi_door_open_01\"/>"

    MENU_START_GAME = "Making your way through the forest you hear a strange sound from above." + SPACESHIP_SOUND + \
                      "You are suddenly engulfed in a bright light. And begin to struggle to stay awake. Then. " \
                      "Darkness. <break time=\"1s\"/> You come to your senses once again and realize that once again " \
                      "you are stuck in a room. What a day. You start to look around."

    SCENE_LEFT = "You see a poster. A door and a console beside it. It must control the door."
    SCENE_FRONT = "You see a screen displaying information you cannot decipher. It looks like a different language."
    SCENE_FRONT_HELMET_ON = "You look at the screen but this time you can make out some of the information. " \
                            "A closer look would might reveal more information."
    SCENE_DOWN = "You simply see a metal floor with what appears to be a handle in the centre."
    SCENE_UP = "You look up and see a large window. To your amazement you can see into space. The stars appear so " \
               "clear as if it is a clear night."
    SCENE_RIGHT = "You see what looks to be a table."

    INSPECT_POSTER = "The poster looks to have a sigma symbol on it."
    INSPECT_DOOR = "The door looks like something from start trek. You give it a kick. Nothing happens."
    INSPECT_CONSOLE = "You look at the console. You cannot make sense of any of it."
    INSPECT_CONSOLE_HELMET_ON = "You look at the console. And notice you can understand the numbers. " \
                                "It requires a four digit number. What four digits would you like to use?"
    INSPECT_HANDLE = "You give the handle a pull. A small container comes out of the floor. Inside the container you " \
                     "see what looks like a coin. You pick it up for safe keeping."
    INSPECT_HANDLE_HAVE_COIN = "You give the handle a pull. Nothing is inside."
    INSPECT_TABLE = "The table appears to have an assortment of junk but one piece catches your attention. " \
                    "A strange looking helmet."
    INSPECT_HELMET = "You look at the helmet and notice a circular slot on the side."
    INSPECT_SCREEN = "The information on the screen looks like gibberish. You undestand nothing."
    INSPECT_SCREEN_HELMET_ON = "The information on the screen is now readable. It states that the temperature " \
                               "outside is 3 kelvin and that the distance to destination is 2000 light years."
    INSPECT_WINDOW = "You look up at the window and gaze in awe at vast number of constellations you can see. " \
                     "To your surprise, you recognize one of them. The zodiac Libra."

    USE_COIN_ON_HELMET = "You place the coin in the slot in the helmet. You then hear a humming noise and " \
                         "decide to put on the helmet. Not your colour but you think you are making it work."

    COMBO_SUCCESS = "You enter the four digits and to your surprise the door slides open."
    COMBO_FAILURE = "You enter the four digits and nothing happens."
    COMBINATION = "2013"

    VICTORY = "You exit the room through the door and are again met with a bright light. <break time=\"1s\"/>"

    OBJECTS = ["poster", "door", "console", "handle", "table", "helmet", "screen", "window"]

    def __init__(self):
        BaseGame.__init__(self)
        self.helmet_powered = False
        self.tag = 1

    def reset(self):
        BaseGame.reset(self)
        self.helmet_powered = False

    def menu(self, menu_selection="", beginning=True):
        speak_output = "<speak>"
        if "start" in menu_selection:
            if beginning:
                speak_output += self.MENU_START_GAME

            self.game_playing = True

        elif "instructions" in menu_selection:
            speak_output += self.MENU_INSTRUCTION
        else:
            speak_output += self.MENU_HELP
        speak_output += "</speak>"

        return speak_output

    def room(self, action="", direction="", objects="", items="", cancel="", combo=""):
        speak_output = "<speak>"
        if not self.looking_at_puzzle:
            if "look" in action:
                if "left" in direction:
                    speak_output += self.SCENE_LEFT
                elif "right" in direction:
                    speak_output += self.SCENE_RIGHT
                elif "down" in direction:
                    speak_output += self.SCENE_DOWN
                elif "up" in direction:
                    speak_output += self.SCENE_UP
                elif "forward" in direction:
                    if self.helmet_powered:
                        speak_output += self.SCENE_FRONT_HELMET_ON
                    else:
                        speak_output += self.SCENE_FRONT
                else:
                    speak_output += "Invalid direction. "
                    speak_output += self.DIRECTION_HELP
            elif "use" in action:
                valid_item = True
                valid_object = True
                if not self.has_item(items):
                    speak_output += self.HAS_ITEM_HELP
                    valid_item = False

                if objects not in self.OBJECTS:
                    speak_output += self.OBJECT_HELP
                    valid_object = False

                if valid_item and valid_object:
                    if "coin" in items and "helmet" in objects:
                        if not self.helmet_powered:
                            speak_output += self.HELMET_POWERING_SOUND + "<break time=\"1s\"/>" + self.USE_COIN_ON_HELMET
                            self.helmet_powered = True
                        else:
                            speak_output += "You already did that."
                    else:
                        speak_output += "You try to use the " + items + " on the " + objects + ". Nothing happens."
            elif "inspect" in action:
                if "poster" in objects:
                    speak_output += self.INSPECT_POSTER
                elif "door" in objects:
                    speak_output += self.INSPECT_DOOR
                elif "console" in objects:
                    if self.helmet_powered:
                        speak_output += self.INSPECT_CONSOLE_HELMET_ON
                        self.looking_at_puzzle = True
                    else:
                        speak_output += self.INSPECT_CONSOLE
                elif "handle" in objects:
                    if not self.has_item("coin"):
                        speak_output += self.INSPECT_HANDLE
                        self.add_inventory("coin")
                    else:
                        speak_output += self.INSPECT_HANDLE_HAVE_COIN
                elif "table" in objects:
                    speak_output += self.INSPECT_TABLE
                elif "helmet" in objects:
                    speak_output += self.INSPECT_HELMET
                elif "screen" in objects:
                    if not self.helmet_powered:
                        speak_output += self.INSPECT_SCREEN
                    else:
                        speak_output += self.INSPECT_SCREEN_HELMET_ON
                elif "window" in objects:
                    speak_output += self.INSPECT_WINDOW
                else:
                    speak_output += self.OBJECT_HELP
            elif "inventory" in action:
                inventory = self.get_inventory()
                if len(inventory) > 0:
                    speak_output += "You have the following items."
                    for item in inventory:
                        speak_output += " " + item + ". "
                else:
                    speak_output += "You have no items in your inventory."
            elif "wait" in action:
                speak_output += self.WAIT_SOUND
            else:
                speak_output += self.ACTION_HELP
        else:
            if "cancel" in cancel:
                speak_output += "You leave the console alone for now."
                self.looking_at_puzzle = False
            elif combo.isnumeric():
                if combo in self.COMBINATION:
                    speak_output += self.DOOR_OPEN_SOUND + "<break time=\"1s\"/>" + self.COMBO_SUCCESS + " " + self.VICTORY
                    self.game_victory = True

                    return speak_output
                else:
                    speak_output += self.DOOR_OPEN_FAILURE_SOUND + "<break time=\"1s\"/>" + self.COMBO_FAILURE
                self.looking_at_puzzle = False
            elif "wait" in action:
                speak_output += self.WAIT_SOUND
            else:
                speak_output += self.COMBO_HELP

        speak_output += "</speak>"

        return speak_output


def main():
    # action - direction - objects - items - cancel - combo
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

    bedroom = Bedroom()
    spaceship = SpaceShip()
    gameTimer = GameTimer()
    gameTimer.start_game_timer()
    level_number = 0

    if level_number == 0:
        for inputs in user_inputs_bedroom:
            action = inputs[0]
            direction = inputs[1]
            objects = inputs[2]
            items = inputs[3]
            cancel = inputs[4]
            combo = inputs[5]

            [finish, output] = bedroom.room(action=action, direction=direction, objects=objects, items=items,
                                            cancel=cancel, combo=combo)
            print(str(inputs) + "    " + str([finish, output]))
            if finish:
                level_number += 1
                gameTimer.update_game_time()
                print("You finished in %s" % str(gameTimer.get_game_time()))
                gameTimer.clear()

    if level_number == 1:
        print(spaceship.menu(menu_selection="start", beginning=True))
        for inputs in user_inputs_spaceship:
            action = inputs[0]
            direction = inputs[1]
            objects = inputs[2]
            items = inputs[3]
            cancel = inputs[4]
            combo = inputs[5]

            gameTimer.start_game_timer()
            [finish, output] = spaceship.room(action=action, direction=direction, objects=objects, items=items,
                                              cancel=cancel, combo=combo)
            print(str(inputs) + "    " + str([finish, output]))
            if finish:
                level_number += 1
                gameTimer.update_game_time()
                print("You finished in %s" % str(gameTimer.get_game_time()))


if __name__ == "__main__":
    main()


