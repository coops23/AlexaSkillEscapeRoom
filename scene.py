INTRO_FIRST_TIME    = "Hi there, welcome to Escape Room. Say start to begin or instructions to hear how to play"
INTRO_WELCOME_BACK  = "Welcome back! Say start to continue where you left off or instructions to hear how to play again"

MENU_INSTRUCTION    = "In this game you will attempt to escape by searching for clues, solving puzzles and using that clever brain of yours. You are placed in a room where you have the option of looking forward, left, right, backwards, up and down. Each direction will paint a picture of your environment. You can interact with your environment by using four action words. Inspect, look, use, inventory . Simply say inspect object like inspect table to hear more information about that object. Say look with a direction word like look forward to describe the scene in front of you. Saying use item requires that you state the object being used and the object being acted on, for example use hammer on window. Saying inventory, I will list all the objects you currently have. You generally will pick up objects by using the inspect action word on parts of the scene. If you are done playing before escaping simply say exit and I will save your state in the game. Would you like to start the game? Start game to continue."
MENU_START_GAME     = "You wake up in a daze. Unsure of where you are or how you got there. A quick glance reveals you are in a small bedroom. You slowly prop yourself up and peer through the window. The outside surrounding are unrecognizable as you appear to be in the middle of a forest. You turn to the door realizing you might be trapped and scream in the heat of frustration and panic as you grasp and turn at the handle. As you slowly calm down you stop and begin to survey your surroundings. What would you like to do?"
MENU_INVALID_SELECTION = "Invalid choice. Please say start or instructions to hear how to play."

SCENE_LEFT      = "You see two exposed wires petruding from the wall, a switch and a guitar."
SCENE_FRONT     = "You see a window covered with metal bars. Like a prison. A chill goes down your spine."
SCENE_DOWN      = "You see an old rug covering most of the floor. It is an ugly rug. It displeases you."
SCENE_UP        = "You see the ceiling light. It appears to be off."
SCENE_RIGHT     = "You see a bed and pillow and a cabinet that appears to have combination lock."

INSPECT_CABINET = "You look at the cabinet. There appears to be four digit combination safe in one of the draws. What four digits would you like to try?"
INSPECT_RUG     = "You peer under the rug. There appears to be a knife. You take it for safe keeping."
INSPECT_RUG_INSPECTED = "You look at the rug. It is ugly. It doesn't match the wall at all. You turn away in disgust."
INSPECT_BED     = "You peer under the bed. There appears to be a roll of electrical tape laying beneath the bed. You pick it up for safe keeping."
INSPECT_BED_INSPECTED = "You look at the bed. You sit down on it. It is comfortable."
INSPECT_PILLOW  = "You pick up the pillow and give it a shake. It feels heavier than it should be."
INSPECT_PILLOW_INSPECTED = "The pillow feels ligher than before. You put it back down."
INSPECT_WINDOW  = "You peer through the window. It appears to be pretty thick. You certainly couldn't break this yourself."
INSPECT_BARS    = "You inspect the bars. The bars are attached to the wall using a set of nuts and bolts."
INSPECT_BARS_INSPECTED = "You look at the bars laying on the ground. Then continue on with your life."
INSPECT_LIGHT_OFF   = "You look up at the light. It appears to be off."
INSPECT_LIGHT_ON   = "You look up at the light. It is bright and hurts your eyes. You regret looking up."
INSPECT_GUITAR  = "The guitar looks to have two strings missing. It should have six. You notice string two and six are missing."
INSPECT_SWITCH_NO_POWER  = "You hit the switch. Nothing happens."
INSPECT_SWITCH_POWER  = "You hit the switch. You see the light on the ceiling turn on and hear a click sound come from the cabinet."
INSPECT_SWITCH_POWER_INSPECTED = "You look at the switch. It is on."
INSPECT_WIRES   = "You see two wires sticking out the wall. You try to bend them together but they quickly fly apart."
INSPECT_WIRES_CONNECTED = "You look at the two wires patched together with tape. You smile at your ingenuity."

USE_KNIFE_PILLOW = "You use your knife to cut open the pillow. Revealing a wrench in the pillow. You pull it out wondering why someone would put a wrench in a pillow."
USE_TAPE_WIRES = "You use the electrical tape to hold the two ends of the wires together. Looks like it holds!"
USE_WRENCH_BARS = "You use the wrench to remove to loosen the nuts off the ends of the bars. The bars eventually comes off and fall to the fall."
COMBO_SUCCESS = "You adjust the dials on the combination lock. And to your delight the safe swings open! Inside there is a brick. You pick it up for safe keeping."
COMBO_FAILURE = "You adjust the dials on the combination lock. And pull at the door. The door is still locked."
COMBO_NO_POWER = "You try the adjust the dials and they don't seem to move."
COMBINATION = "1345"

VICTORY = "You throw the brick at the window with all your might. And revel in delight as it smashes through. You crawl through to freedom. Congratulations!"

VICTORY_SOUND = "<audio src=\"soundbank://soundlibrary/glass/break_shatter_smash/break_shatter_smash_01\"/>"
PILLOW_OPENING_SOUND = "<audio src=\"soundbank://soundlibrary/cloth_leather_paper/zippers/zippers_01\"/>"
CABINET_OPENING_SOUND = "<audio src=\"soundbank://soundlibrary/doors/doors_squeaky/squeaky_11\"/>"
CABINET_OPENING_FAILURE_SOUND = "<audio src=\"soundbank://soundlibrary/doors/doors_regular/regular_15\"/>"
WIRES_ATTACHING_SOUND = "<audio src=\"soundbank://soundlibrary/electrical/arcs_sparks/arcs_sparks_13\"/>"
BARS_REMOVED_SOUND = "<audio src=\"soundbank://soundlibrary/metal/metal_02\"/>"
SCENE_START_SOUND = "<audio src=\"soundbank://soundlibrary/bell/chimes/chimes_12\"/>"

#--- State variables ---# 
INVENTORY = []
GAME_PLAYING = False
WIRES_FIXED = False
POWER_ON = False
LOOKING_AT_SAFE = False
BARS_REMOVED = False
START_TIME = 0
ELAPSED = 0