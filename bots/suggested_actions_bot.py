# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from config import DefaultConfig

class SuggestActionsBot(ActivityHandler):

    def __init__(self, config: DefaultConfig):
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id = "e99656af-e62c-41f2-92ee-40fb4ec05a84",
                endpoint_key = "8815dddf-20fb-4322-8780-69ae13ca554b",
                host = "https://universalrent.azurewebsites.net/qnamaker",
            )
        )

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext):
        
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Welcome to Universal Rental {member.name}."                        
                    )
                )
                await self._send_suggested_actions(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        # The actual call to the QnA Maker service.
        text = turn_context.activity.text.lower()
        rText = self._process_input(text)
        response = turn_context.activity.text
        if rText == "question" or response == "Question":
            await turn_context.send_activity("Ask away")
            response = turn_context.activity.text
            while response != "exit" or response != "Exit":
                response = await self.qna_maker.get_answers(turn_context)
                if response and len(response) > 0:
                    await turn_context.send_activity(MessageFactory.text(response[0].answer))
                else:
                    await turn_context.send_activity("No QnA Maker answers were found.")
                response = turn_context.activity.text
        if rText == "reg":
            await turn_context.send_activity("we lit")
            await turn_context.send_activity(MessageFactory.text("Yes baby"))


    def _process_input(self, text: str):
        if text == "Ask Question":
            return "Question"
        if text == "Registration":
            return "reg"
            

    async def _send_suggested_actions(self, turn_context: TurnContext):

        reply = MessageFactory.text("How May I assist.")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Ask Question",
                    type=ActionTypes.im_back,
                    value="Ask Question",     
                ),
                CardAction(
                    title="Registration",
                    type=ActionTypes.im_back,
                    value="Registration",
                ),
            ]
        )
        return await turn_context.send_activity(reply)

