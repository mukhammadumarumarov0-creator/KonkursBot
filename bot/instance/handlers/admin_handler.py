# from aiogram import Router, types, F
# from aiogram.filters import CommandStart
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from asgiref.sync import sync_to_async
# from aiogram.types.input_media_photo import InputMediaPhoto
# from aiogram.types import FSInputFile
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from bot.models import User
# from .conf import BOT

# from bot.instance.handlers.messages import (
#     welcome_message, meeting_message,
#     admin_connect, ask_name_message,
#     ask_phone_message,
#     gift_message,
#     rules_message
# )

# from bot.instance.handlers.utils import (
#     validate_full_name, FULLNAME_ERROR,
#     PHONE_ERROR, normalize_phone,
#     is_registered, check_channel_membership,
#     KANAL, create_user,is_staff_async
# )

# from bot.instance.handlers.bottens import (
#     btn_admin, register_button,
#     phone_button, face_button
# )








# # ================= FSM =================
# class RegisterProcess(StatesGroup):
#     full_name = State()
#     phone = State()

# admin_router = Router()



# # @admin_router.message(CommandStart())
# # async def start_handler(message: Message, state: FSMContext):
# # pass