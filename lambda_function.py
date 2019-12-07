# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import game
import ask_sdk_core.utils as ask_utils
import os

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_s3.adapter import S3Adapter

s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

logger = logging.getLogger(__name__)

bedroom = game.Bedroom()
spaceship = game.SpaceShip()
gameTimer = game.GameTimer()

level_number = 0


class LaunchRequestHandler(AbstractRequestHandler):
    global bedroom
    global spaceship
    global gameTimer

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = ""
        if gameTimer.elapsed == 0:
            speak_output += bedroom.intro(beginning=True)
            gameTimer.start_game_timer()
        else:
            speak_output += bedroom.intro(beginning=False)
        ask_output = bedroom.MENU_ASK

        level_number = game.load_game(handler_input, gameTimer, bedroom, spaceship)

        return handler_input.response_builder.speak(speak_output).ask(ask_output).response


class MenuIntentHandler(AbstractRequestHandler):
    global bedroom
    global spaceship
    global level_number
    global gameTimer

    def can_handle(self, handler_input):
        level = game.get_level(level_number, bedroom, spaceship)
        if ask_utils.is_intent_name("MenuIntent")(handler_input) and not level.game_playing:
            return True
        else:
            return False

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        menu_selection = str(slots['menu'].value)

        speak_output = ""
        ask_output = ""
        level = game.get_level(level_number, bedroom, spaceship)

        if gameTimer.elapsed == 0:
            speak_output = level.menu(menu_selection=menu_selection, beginning=True)
        else:
            speak_output = level.menu(menu_selection=menu_selection, beginning=False)

        if not level.game_playing:
            ask_output = level.MENU_ASK
        else:
            ask_output = level.GAME_ASK

        return handler_input.response_builder.speak(speak_output).ask(ask_output).response


class GameIntentHandler(AbstractRequestHandler):
    global game
    global spaceship
    global level_number
    global gameTimer

    def can_handle(self, handler_input):
        level = game.get_level(level_number, bedroom, spaceship)
        if ask_utils.is_intent_name("GameIntent")(handler_input) and level.game_playing:
            return True
        else:
            return False

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        action = str(slots['action'].value)
        direction = str(slots['direction'].value)
        objects = str(slots['objects'].value)
        items = str(slots['items'].value)
        cancel = str(slots['cancel'].value)
        combo = str(slots['combo'].value)

        level = game.get_level(level_number, bedroom, spaceship)
        ask_output = ""
        speak_output = level.room(action=action, direction=direction, objects=objects, items=items, cancel=cancel,
                                  combo=combo)
        if not level.looking_at_puzzle:
            ask_output = level.GAME_ASK
        else:
            ask_output = level.COMBO_ASK
        gameTimer.update_game_time()
        if level.game_victory:
            if level.tag == 0:
                speak_output += "You finished in %s" % str(gameTimer.get_game_time())
                level.reset()
                level_number = 1
            elif level.tag == 1:
                return (handler_input.response_builder.speak(speak_output).response)

        return (handler_input.response_builder.speak(speak_output).ask(ask_output).response)


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    global bedroom
    global spaceship

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    global bedroom
    global spaceship

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."
        # speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MenuIntentHandler())
sb.add_request_handler(GameIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()