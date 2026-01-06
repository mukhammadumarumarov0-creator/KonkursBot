import re
from asgiref.sync import sync_to_async
from bot.models import User
from aiogram.types import ChatMember
from decouple import config

KANAL = config("KANAL")


def get_user_sync(telegram_id: int) -> User | None:
    return User.objects.filter(telegram_id=telegram_id).first()

async def is_registered(telegram_id: int) -> User | None:
    return await sync_to_async(get_user_sync)(telegram_id)

async def create_user(full_name: str, phone: str, telegram_id: int, inviter: User | None = None) -> User:
    user = User(
        telegram_id=telegram_id,
        full_name=full_name,
        phone=phone,
        invited_by=inviter
    )
    await sync_to_async(user.save)()
    return user


async def check_channel_membership(user_id: int , bot) -> bool:
    try:
        member: ChatMember = await bot.get_chat_member(chat_id=KANAL, user_id=user_id)
        # Status "left" yoki "kicked" bo‘lsa → user obuna emas
        if member.status in ["left", "kicked"]:
            return False
        return True
    except Exception as e:
        # Xatolik log qilish tavsiya qilinadi
        print(f"[check_channel_membership] Xato user_id={user_id}: {e}")
        return False


FULLNAME_ERROR = (
    "❌ Ism va familiyani to‘g‘ri kiriting.\n"
    "Masalan: Muhammad Umarov"
)

PHONE_ERROR = (
    "❌ Telefon raqam noto‘g‘ri.\n"
    "Namuna: +998901234567\n"
    "Yoki 📞 tugmani bosing"
)


async def validate_full_name(full_name: str) -> bool:
    """
    Format: 'Ism Familiya' (2-30 harf, Lotin va Kirill)
    """
    FULL_NAME_REGEX = r"^[A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]{2,30}\s[A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]{2,30}$"
    return bool(re.fullmatch(FULL_NAME_REGEX, full_name.strip()))


async def normalize_phone(phone: str) -> str | None:
    """
    Normalize: +998901234567 formatiga keltirish
    """
    PHONE_REGEX = r"^\+998(90|91|93|94|95|97|98|99|33|88)\d{7}$"
    digits = re.sub(r"\D", "", phone)

    if digits.startswith("998") and len(digits) == 12:
        digits = "+" + digits
    elif digits.startswith("9") and len(digits) == 9:
        digits = "+998" + digits
    else:
        return None

    return digits if re.fullmatch(PHONE_REGEX, digits) else None



def is_staff_sync(telegram_id: int) -> User | None:
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user and (user.is_staff or user.is_superuser):
        return user
    return None

async def is_staff_async(telegram_id: int) -> User | None:
    return await sync_to_async(is_staff_sync)(telegram_id)



async def is_user_active(telegram_id: int) -> bool:
    user = await sync_to_async(User.objects.filter(telegram_id=telegram_id).first)()
    if user and user.is_active:
        return True
    return False
