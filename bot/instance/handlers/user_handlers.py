from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async
from aiogram.types import Message
from bot.models import User
from aiogram import Bot
from decouple import config

from bot.instance.handlers.messages import (
    welcome_message, meeting_message,admin_connect, ask_name_message,ask_phone_message,
    gift_caption,rules_caption,blocked_message,share_message_ref,message_text,obunaMatni)

from bot.instance.handlers.utils import (
    validate_full_name, FULLNAME_ERROR,PHONE_ERROR, normalize_phone,is_registered, check_channel_membership,
    KANAL, create_user,is_staff_async,is_user_active)

from bot.instance.handlers.bottens import (
   btn_admin, register_button,phone_button, face_button,face_button_for_admin,subscribe_keyboard)


BOT = Bot(token=config("BOT_TOKEN"))
user_router = Router()

class RegisterProcess(StatesGroup):
    full_name = State()
    phone = State()



@user_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    args = message.text.split()
    inviter_id = None

    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            ref_id = int(args[1].replace("ref_", ""))
            if ref_id != message.from_user.id:
                inviter_id = ref_id
        except ValueError:
            pass

    intro_message = (
    f"<b>👋 Assalomu Alaykum {message.from_user.full_name} ! Xush kelibsiz!</b><br>"
    "<i>Nurli Maskan</i> kanalida sizni <b>qiziqarli konkurslar</b> va <b>sovrinlar 🎁✨</b> kutmoqda!<br><br>"
    "<u>Kanalga obuna bo‘ling va ishtirok eting!</u>")


    if not await check_channel_membership(bot=BOT,user_id=message.chat.id):
        await state.update_data(inviter_id=inviter_id)
        await message.answer(text=intro_message,reply_markup=subscribe_keyboard(),parse_mode="HTML")
        return

    user = await is_registered(message.from_user.id)

    if user:
        await face_button(message, text=welcome_message)
        return

    await state.update_data(inviter_id=inviter_id)
    await register_button(message, meeting_message)


@user_router.callback_query(F.data == "added")
async def check_subscribed(callback: types.CallbackQuery, state: FSMContext):
    active = await is_user_active(callback.message.chat.id)
    if not active:
        await callback.message.answer(text=blocked_message,parse_mode="HTML")
        return
    if not await check_channel_membership(bot=BOT,user_id=callback.message.chat.id):
        await callback.answer("❌ Hali kanalga a’zo bo‘lmadingiz", show_alert=True)
        return

    await callback.answer("✅ Obuna tasdiqlandi.",show_alert=True)
    await register_button(callback.message, meeting_message)




# ================= REGISTER START =================
@user_router.message(F.text == "📃 Ro'yhatdan o'tish")
async def start_register(message: Message, state: FSMContext):
    await state.set_state(RegisterProcess.full_name)
    await message.answer(ask_name_message, parse_mode="HTML")


# ================= FULL NAME =================
@user_router.message(RegisterProcess.full_name)
async def fullname_register(message: Message, state: FSMContext):
    if not message.text or not await validate_full_name(message.text):
        await message.answer(FULLNAME_ERROR, parse_mode="HTML")
        return

    await state.update_data(full_name=message.text)
    await state.set_state(RegisterProcess.phone)
    await phone_button(message, ask_phone_message)



@user_router.message(RegisterProcess.phone)
async def phone_register(message: types.Message, state: FSMContext):
     phone = message.contact.phone_number if message.contact else message.text
     if not phone:
        await message.answer(PHONE_ERROR)
        return

     normalized = await normalize_phone(phone)
     if not normalized:
        await message.answer(PHONE_ERROR)
        return

    # FSM dan ma’lumotlarni olish
     data = await state.get_data()
     inviter_id = data.get("inviter_id")

     inviter = None
     if inviter_id:
        inviter = await sync_to_async(User.objects.filter(telegram_id=inviter_id).first)()

    # 👤 YANGI USER YARATISH
     user = await create_user(
        full_name=data["full_name"],
        phone=normalized,
        telegram_id=message.from_user.id,
        inviter=inviter)

    # 🔗 REFERRAL BONUS → INVITERGA +5
     if inviter:     # agar hamma hirganga bermoqchi bolsam ballni shu erni ozgartiraman
        inviter.add_referral_points(5)
        await sync_to_async(inviter.save)()


    # 📢 KANAL BONUS → USERGA +5 (FAQAT SHU YERDA, 1 MARTA)
     if await check_channel_membership(bot=BOT, user_id=message.chat.id):
        user.add_referral_points(10)
        await sync_to_async(user.save)()


     await state.clear()

     # Agar kanalga obuna bo‘lmagan bo‘lsa (xavfsizlik uchun)
     if not await check_channel_membership(bot=BOT,user_id=message.chat.id):
        await message.answer(text=obunaMatni,reply_markup=subscribe_keyboard(),parse_mode="HTML")
        return


     done_message = (
    f"🎉Tabriklaymiz <b>{message.from_user.first_name}</b> ! \n"
    "<b>✅ Ro‘yxatdan muvaffaqiyatli o‘tdingiz!</b>\n"
    "Endi siz botimizning barcha qulayliklaridan to‘liq foydalanishingiz mumkin.\n\n")

     await message.answer(done_message, parse_mode="HTML")
     await face_button(message, text=message_text)









# ================= KONKURS =================
@user_router.message(F.text == "Konkursda qatnashish 🔴")
async def contest_handler(message: Message):  
    user = await is_registered(message.from_user.id)

    if not user:
      await message.answer("❌ Siz hali ro‘yxatdan o‘tmagansiz.\nIltimos, tizimdan to‘liq foydalanish uchun ro‘yxatdan o‘ting. 💛")
      return
    
    link_message = (
    "<b>🏠 <b>Bepul</b> sovg‘alar – <b>Nurli Maskan</b> Konkursi!</b>\n\n"
    "Salom! 🎉\n"
    "<b>Nurli Maskan turar joy kompleks</b> sizni konkursga taklif qilmoqda.\n\n"
    "Shartlar oddiy va qatnashish juda oson:\n"
    "<b>🧊 Muzlatkich</b>\n"
    "<b>🧹 Changyutgich</b>\n"
    "<b>📺 Televizor</b>\n"
    "<b>🧺 Kir yuvish mashinasi</b>\n"
    "…va boshqa sovg‘alar sizni kutmoqda!\n\n"
    "⚡ Sovg‘alar haqiqiy, qatnashish esa juda oson – sinab ko‘ring! 😄\n"
    "<b> 👇 Konkursga qatnashish uchun havola:</b>\n\n"
   f"  {user.get_invite_link()}\n\n\n")

    try:
        await message.answer_photo(photo="https://t.me/smmlessonsbyprof/10",caption=link_message,parse_mode="HTML")
        await message.answer(text=share_message_ref,parse_mode="HTML")
    except Exception as e:
        print("Media yuborishda xatlik:", e)
      

@user_router.message(F.text == "👤 Ballarim")
async def points_handler(message: Message): 
    user = await is_registered(message.from_user.id)
    score_message = f"""
    💡 <b>Siz to'plagan ball:</b> {user.referral_points}

    ✨ Zo'r ish! Harakatni to'xtatmang,  
    har bir yangi do‘st sizni g‘oliblik sari yaqinlashtiradi! ⚡️

    🌟 Harakatni davom ettiring —  
    har bir qadam sizni sovg‘aga yaqinlashtiradi! 💫
    """
    await message.answer(text=score_message,parse_mode="HTML")


@user_router.message(F.text == "🎁 Sovg'alar")
async def gifts_handler(message: Message):
    try:
        await message.answer_photo(photo="https://t.me/smmlessonsbyprof/10",caption=gift_caption,parse_mode="HTML")
    except Exception as e:
        print("Media yuborishda xatlik (gifts handler):", e)


@user_router.message(F.text == "💡Shartlar")
async def rules_handler(message: Message):
    try:
        await message.answer_photo(photo="https://t.me/smmlessonsbyprof/10",caption=rules_caption,parse_mode="HTML")
    except Exception as e:
        print("Media yuborishda xatlik (rules_handler):", e)


@user_router.message(F.text == "👤 Admin")
async def admin_btn_handler(message: types.Message):
    await message.answer(admin_connect,parse_mode="HTML",disable_web_page_preview=True)

