from datetime import datetime
from uuid import uuid4

from uagents import Context, Protocol
from uagents.experimental.chat_agent.protocol import build_llm_message_history
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

from http_client import ask_asi1

SYSTEM_PROMPT = (
    "You are Negotiator AI, a friendly shopping assistant for laptops and smartphones. "
    "Your job is to help users get better prices: compare offers, judge whether a price is "
    "fair for the specs, and recommend the best deal. "
    "When a user shares one or more offers (product, price, storage, RAM, chip, condition, "
    "seller or link), analyze them: note key spec differences, estimate fair value, rank the "
    "offers, and clearly recommend one with reasons. "
    "Also give short, practical negotiation tips such as politely asking for a discount, "
    "price matching, bundle deals, and buying during sales events. "
    "Never invent prices, stock levels or promotions you cannot verify - ask the user to "
    "share offer details instead. "
    "You only help with laptops and smartphones; for any other topic, politely say that you "
    "specialize in laptops and smartphones. "
    "Reply in the user's language, be concise, and use plain text."
)

negotiator_protocol = Protocol(spec=chat_protocol_spec)


@negotiator_protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    text = msg.text()
    if not text:
        return

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *build_llm_message_history(ctx),
    ]

    try:
        reply = ask_asi1(messages)
    except Exception:
        ctx.logger.exception("Error querying model")
        reply = "Sorry, something went wrong while analyzing your request. Please try again in a moment."

    content = [TextContent(type="text", text=reply)]
    await ctx.send(
        sender,
        ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content),
    )


@negotiator_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass
