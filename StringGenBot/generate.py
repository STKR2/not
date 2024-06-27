import traceback
import ntplib
from time import ctime, time

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from asyncio.exceptions import TimeoutError

import config

from pyrogram1 import Client as Client1
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)

ask_ques = "- الان اختر ماتريد استخراجة ."
buttons_ques = [
    [
        InlineKeyboardButton("- بايروجرام .", callback_data="pyrogram1"),
    ],
    [
        InlineKeyboardButton("- ثليثون .", callback_data="telethon"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="- استخرج من جديد .", callback_data="generate")
    ]
]

ERROR_MESSAGE = "- لقد ارسلت الرقم او شي غير صحيح \n- اذا استمرت المشكلة تحدث مع المطور @RR8R9"


async def synchronize_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        system_time = time()
        ntp_time = response.tx_time
        if abs(system_time - ntp_time) > 1:
            print(f"System time: {ctime(system_time)}, NTP time: {ctime(ntp_time)}")
            print("Time difference is significant, consider synchronizing your system clock.")
    except Exception as e:
        print(f"Failed to synchronize time: {e}")


@Client.on_callback_query(filters.regex(pattern=r"^(generate|pyrogram|pyrogram1|pyrogram_bot|telethon_bot|telethon)$"))
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    query = callback_query.matches[0].group(1)
    if query == "generate":
        await callback_query.answer()
        await callback_query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))
    elif query.startswith("pyrogram") or query.startswith("telethon"):
        try:
            if query == "pyrogram":
                await callback_query.answer()
                await generate_session(bot, callback_query.message)
            elif query == "pyrogram1":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, old_pyro=True)
            elif query == "pyrogram_bot":
                await callback_query.answer("» ᴛʜᴇ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴡɪʟʟ ʙᴇ ᴏғ ᴩʏʀᴏɢʀᴀᴍ ᴠ2.", show_alert=True)
                await generate_session(bot, callback_query.message, is_bot=True)
            elif query == "telethon_bot":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True, is_bot=True)
            elif query == "telethon":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            await callback_query.message.reply(ERROR_MESSAGE.format(str(e)))


@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    await synchronize_time()  # Synchronize time before connecting the client
    if telethon:
        ty = "ثليثون"
    else:
        ty = "بايروجرام"
        if not old_pyro:
            ty += " ᴠ2"
    if is_bot:
        ty += " ʙᴏᴛ"
    await msg.reply(f"- انتظر قليلاً **{ty}** تحت أمرك .")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "- الان ارسل لي الايبي ايدي .\n\n- اذا مامستخرجهن اكتب سكب .", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "سكب":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("- تم خطواتك صحيحة استمر .", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "- الان ارسل لي الايبي هاش .", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "- الان ارسل لي رقمك \n- على سبيل المثال : +9640000000000"
    else:
        t = "ᴩʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ʙᴏᴛ_ᴛᴏᴋᴇɴ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴇxᴀᴍᴩʟᴇ : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("- يتم التحقق من الرقم .")
    else:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("- الايدي ايبي والايبي هاش غلط او انت داز وهميات .", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply("- الرقم غلط او ماكو حساب بهذا الرقم .", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "- تمام حب \n- هسه دزلي الكود بس شرط \n\n- يكون بأرقام مفصوله كمثال : 2 7 3 2 4 ", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("- انتهى وقت الاستخراج وين جنت .", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply("- الكود غلط .", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("- انتهت صلاحية الكود .", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await bot.ask(user_id,two_step_msg = await bot.ask(user_id, "- ارسل لي التحقق بخطوتين .", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("- انتهى وقت إرسال التحقق بخطوتين .", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply("- باسورد تحقق بخطوتين غلط حب .", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**- تم استخراج {ty} بنجاح .** \n\n`{string_session}` \n\n- المطور : @RR8R9 \n- قناة المطور : @xl444"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "- استخراج {} تم بنجاح .\n\n- دزيتلك الكود المستخرج ع الرسائل المحفوظة مال الرقم الي استخرجت بي . !".format("ثليثون" if telethon else "بايروجرام"))


async def cancelled(msg):
    if "مسح" in msg.text:
        await msg.reply("- انت في وضع الاستخراج .", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "ريستارت" in msg.text:
        await msg.reply("- تم اعادة تشغيل البوت بنحاح ", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "تخطي" في msg.text:
        return False
    elif msg.text.startswith(" "):  # Bot Commands
        await msg.reply("- تم الغاء الاستخراج .", quote=True)
        return True
    else:
        return False
