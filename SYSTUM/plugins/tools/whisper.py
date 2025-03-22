from SYSTUM import app as app
from config import BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Start A Love latter", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []
    
    if len(data.split()) < 2:
        mm = [
            InlineQueryResultArticle(
                title="💒 love latter",
                description=f"@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]",
                input_message_content=InputTextMessageContent(f"💒 Usage:\n\n@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]"),
                thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                reply_markup=switch_btn
            )
        ]
    else:
        try:
            user_id = data.split()[0]
            msg = data.split(None, 1)[1]
        except IndexError as e:
            pass
        
        try:
            user = await _.get_users(user_id)
        except:
            mm = [
                InlineQueryResultArticle(
                    title="💒 Love latter",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("Invalid username or ID!"),
                    thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                    reply_markup=switch_btn
                )
            ]
        
        try:
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔩 One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="💒 love latter",
                    description=f"Send a Love latter to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"💒 You are sending a love letter to {user.first_name}.\n\nType your message/sentence."),
                    thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="🔩 One-Time love latter",
                    description=f"Send a one-time whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"🔩 You are sending a one-time whisper to {user.first_name}.\n\nType your message/sentence."),
                    thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
        except:
            pass
        
        try:
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except:
            pass
    
    results.append(mm)
    return results


@app.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id
    
    if user_id not in [from_user, to_user, 7582601826]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} is trying to open your love latter.")
        except Unauthorized:
            pass
        
        return await query.answer("This whisper is not for you 🚧", show_alert=True)
    
    search_msg = f"{from_user}_{to_user}"
    
    try:
        msg = whisper_db[search_msg]
    except:
        msg = "🚫 Error!\n\nWhisper has been deleted from the database!"
    
    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline 🪝", switch_inline_query_current_chat="")]])
    
    await query.answer(msg, show_alert=True)
    
    if len(data) > 3 and data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text("📬 a love letter has been read!\n\nPress the button below to send a love latter!", reply_markup=SWITCH)


async def in_help():
    answers = [
        InlineQueryResultArticle(
            title="💒 love latter",
            description=f"@asxqueen_bot [USERNAME | ID] [TEXT]",
            input_message_content=InputTextMessageContent(f"**📍Usage:**\n\nnaveem (Target Username or ID) (Your Message).\n\n**Example:**\n@naveen_720 miss quee kai acount delete kala kire"),
            thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
            reply_markup=switch_btn
        )
    ]
    return answers


@app.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()
    
    if string.strip() == "":
        answers = await in_help()
        await inline_query.answer(answers)
    else:
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)
                                               
