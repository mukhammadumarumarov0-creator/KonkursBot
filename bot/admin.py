from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,BroadcastMessage

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # List view
    list_display = ('display_full_name', 'display_phone', 'display_ball', 'is_staff', 'is_active')
    list_editable = ('is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('full_name', 'phone', 'username', 'telegram_id')

    # Edit view: faqat is_active va is_staff tahrir qilinadi
    fieldsets = (
        (None, {'fields': ('is_active', 'is_staff')}),
    )

    # Yangi user qo'shish
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff'),
        }),
    )

    ordering = ('id',)

    # --- Helper functions for list display ---
    def display_full_name(self, obj):
        return obj.full_name or obj.username
    display_full_name.short_description = "Ism Familiya"
    display_full_name.admin_order_field = 'full_name'

    def display_phone(self, obj):
        return obj.phone or "-"
    display_phone.short_description = "Telefon raqam"

    def display_ball(self, obj):
        return obj.referral_points or "--"
    display_ball.short_description = "Ball"



@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "short_text", "send_to_all", "is_sent", "created_at")
    list_filter = ("send_to_all", "is_sent")
    readonly_fields = ("is_sent", "created_at")

    def short_text(self, obj):
        return obj.text[:30]
