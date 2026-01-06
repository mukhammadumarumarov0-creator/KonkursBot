from django.db import models
from django.contrib.auth.models import AbstractUser
from decouple import config
import random
import string

BOT_FULL_PATH = config("BOT_FULL_PATH")

class User(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True)
    invited_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="invited_users")
    referral_points = models.IntegerField(default=0) 


    def get_invite_link(self):
        return f"{BOT_FULL_PATH}_{self.telegram_id}"


    def generate_username(self) -> str:
        base = f"user_{self.telegram_id}"
        if not User.objects.filter(username=base).exists():
            return base
        rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return f"{base}_{rand_str}"


    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        super().save(*args, **kwargs)


    def add_referral_points(self, points: int = 5):
        self.referral_points += points
        self.save()


    def __str__(self):
        return self.full_name or self.username



class BroadcastMessage(models.Model):
    text = models.TextField("Xabar matni")
    image_url = models.URLField( "Rasm URL (ixtiyoriy)",blank=True,null=True)
    users = models.ManyToManyField(User,blank=True,verbose_name="Qabul qiluvchilar")
    send_to_all = models.BooleanField(default=False,verbose_name="Barchaga yuborish")

    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "📢 Xabar yuborish"
        verbose_name_plural = "📢 Xabar yuborishlar"

    def __str__(self):
        return self.text[:40]
