from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



async def register_button(message: Message, text: str):
    """Ro'yhatdan o'tish tugmasini yuboradi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📃 Ro'yhatdan o'tish")]],
        resize_keyboard=True
    )
    await message.answer(text=text, reply_markup=keyboard, parse_mode='HTML')


async def phone_button(message: Message, text: str):
    """Telefon raqam yuborish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📲 Raqam jo'natish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(text=text, reply_markup=keyboard, parse_mode='HTML')


btn_admin = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="👤 Admin bilan bog‘lanish")]],
    resize_keyboard=True
)


async def face_button(message: Message, text: str):
  keyboard = ReplyKeyboardMarkup(
        keyboard=[
           [KeyboardButton(text="Konkursda qatnashish 🔴")],
           [KeyboardButton(text="🎁 Sovg'alar"),KeyboardButton(text="👤 Ballarim")],
           [KeyboardButton(text="💡Shartlar"),KeyboardButton(text="👤 Admin")],
            ],
        resize_keyboard=True
    )
  await message.answer(text=text, reply_markup=keyboard, parse_mode='HTML')


async def face_button_for_admin(message: Message, text: str):
  keyboard = ReplyKeyboardMarkup(
        keyboard=[
           [KeyboardButton(text="Xabar Yuborish 📝"),KeyboardButton(text="Jonli Efirni Bo'shlash 📺")]
            ],
        resize_keyboard=True
    )
  await message.answer(text=text, reply_markup=keyboard, parse_mode='HTML')


def subscribe_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📢 Kanalga a’zo bo‘ling", url="https://t.me/testchennelforbotkonkur")
    kb.button(text="✅ A’zo bo‘ldim", callback_data="added")
    kb.adjust(1)
    return kb.as_markup()