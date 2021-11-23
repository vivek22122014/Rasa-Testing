# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []




class ActionTalkToHuman(Action):
    """
	human in the loop action
	"""

    def name(self):
        return "action_talk_to_human"

    def run(self, dispatcher, tracker, domain):
        response = "Reaching out to a human agent [{}]...".format(tracker.sender_id)
        dispatcher.utter_message(response)

        """
		seems like rasa will stop listening once conversation
		is paused, which means no actions are attempted, therefore
		preventing triggering ConversationResumed() in a straightforward way.
		"""
        tracker.update(ConversationPaused())
        message = ""
        while message != "/unpause":
            url = "http://127.0.0.1:5000/handoff/{}".format(tracker.sender_id)
            req = requests.get(url)
            resp = json.loads(req.text)
            if "error" in resp:
                raise Exception("Error fetching message: " + repr(resp["error"]))
            message = resp["message"]
            if message != "/unpause":
                dispatcher.utter_message("Human agent: {}".format(message))

        tracker.update(ConversationResumed())

