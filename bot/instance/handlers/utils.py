import re
from asgiref.sync import sync_to_async
from aiogram.types import ChatMember
from decouple import config
from bot.models import User,LiveParticipant,LiveSession
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.instance.handlers.conf import BOT
from urllib.parse import urlparse
from django.core.exceptions import ObjectDoesNotExist



KANAL = config("KANAL")


def get_user_sync(telegram_id: int) -> User | None:
    return User.objects.filter(telegram_id=telegram_id).first()


async def is_registered(telegram_id: int) -> User | None:
    return await sync_to_async(get_user_sync)(telegram_id)


async def create_user(telegram_id: int, full_name: str, phone: str, inviter=None):
    
    user, created = await sync_to_async(User.objects.get_or_create)(
        telegram_id=telegram_id,
        defaults={
            "full_name": full_name,
            "phone": phone,
            "inviter": inviter
        }
    )

    if not created:
    
        user.full_name = full_name
        user.phone = phone
        if inviter:
            user.inviter = inviter
        await sync_to_async(user.save)()  # save ham sync-to-async qilamiz

    return user


async def check_channel_membership(user_id: int , bot=BOT) -> bool:
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
    FULL_NAME_REGEX = (
        r"^[A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]+(?:['’][A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]+)?"
        r"\s"
        r"[A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]+(?:['’][A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]+)?$"
    )

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

async def subscribe_keyboard(): 
    kb = InlineKeyboardBuilder()
    kb.button(
        text="📢 Kanalga a’zo bo‘ling",
        url=f"https://t.me/smmlessonsbyprof"
    )
    kb.button(text="✅ A’zo bo‘ldim", callback_data="added")
    kb.adjust(1)
    return kb.as_markup()


async def get_all_users():
    return await sync_to_async(list)(
        User.objects.filter(
            is_staff=False,
            telegram_id__isnull=False
        ).values_list('telegram_id', flat=True)
    )





@sync_to_async
def get_user_by_telegram_id(telegram_id: int) -> User | None:
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None


@sync_to_async
def get_all_user_ids() -> list[int]:
    return list(
        User.objects
        .exclude(telegram_id__isnull=True)
        .values_list("telegram_id", flat=True)
    )


@sync_to_async
def has_joined_live(user: User) -> bool:
    return LiveParticipant.objects.filter(user=user).exists()


@sync_to_async
def mark_live_joined(user: User):
    LiveParticipant.objects.create(user=user)



async def add_live_points(user: User, points: int = 5) -> bool:
    """
    Jonli efir uchun ball qo‘shish (faqat 1 marta)
    """
    if await has_joined_live(user):
        return False

    await user.add_referral_points_async(points)
    await mark_live_joined(user)
    return True


async def get_session(session_id: int):
    try:
        return await sync_to_async(LiveSession.objects.get)(id=session_id)
    except ObjectDoesNotExist:
        return None


async def parse_live_url(url: str) -> dict | None:
    parsed = urlparse(url)

    if parsed.netloc not in ("t.me", "www.t.me"):
        return None

    username = parsed.path.strip("/")
    if not username:
        return None


    return  f"@{username}"
        

