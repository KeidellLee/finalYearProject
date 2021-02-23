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
        response = await self.qna_maker.get_answers(turn_context)
        if response and len(response) > 0:
            await turn_context.send_activity(MessageFactory.text(response[0].answer))
        else:
            await turn_context.send_activity("No QnA Maker answers were found.")
        text = turn_context.activity.text.lower()
        response_text = self._process_input(text)

    async def _process_input(self, text: str):
        color_text = "is the best color, I agree."

        if text == "sure":
            return "Ask away"
            

    async def _send_suggested_actions(self, turn_context: TurnContext):

        reply = MessageFactory.text("How May I assist.")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Ask Question",
                    type=ActionTypes.im_back,
                    value="sure",     
                ),
            ]
        )
        return await turn_context.send_activity(reply)

