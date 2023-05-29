from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""-  بوت استخراج كود بايروجرام .
- البوت يشتغل على كل السورسات .

- المطور الوحيد : [by developer](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="- استخرج الان .", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("- قناة المطور .", url="https://t.me/xl444"),
                    InlineKeyboardButton("- مالك البوت .", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
