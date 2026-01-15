from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    # Admin listida ko'rinadigan ustunlar
    list_display = (
        'id', 'full_name_link', 'telegram_id', 'phone',
        'inviter', 'referral_points_display', 'is_staff', 'is_active_display',
    )
    list_editable = ["is_staff",]

    # Sortlash mumkin bo‘lgan ustunlar
    ordering = ('-referral_points',)

    # Qidiruv uchun maydonlar
    search_fields = ('username', 'full_name', 'telegram_id', 'phone')

    # Filterlar
    list_filter = ('is_staff', 'is_active', 'inviter')

    # Fieldsets (expandable)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Shaxsiy ma’lumotlar'), {'fields': ('full_name', 'telegram_id', 'phone')}),
        (_('Referral'), {'fields': ('inviter', 'referral_points')}),
        (_('Ruxsatlar'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Muhim sanalar'), {'fields': ('last_login', 'date_joined')}),
    )

    # Readonly fields
    readonly_fields = ('referral_points', 'last_login', 'date_joined')

    # --- Qo‘shimcha funksiyalar ---

    # full_name ustuni orqali link
    def full_name_link(self, obj):
        return format_html('<a href="{}">{}</a>', f'/admin/app_name/user/{obj.id}/change/', obj.full_name)
    full_name_link.short_description = _("Foydalanuvchi ismi")
    full_name_link.admin_order_field = 'full_name'

    # referral_points ustuni labelini o‘zbekcha
    def referral_points_display(self, obj):
        return obj.referral_points
    referral_points_display.short_description = _("Ball")
    referral_points_display.admin_order_field = 'referral_points'

    # is_staff ustuni o‘zbekcha
    def is_staff_display(self, obj):
        return "Ha" if obj.is_staff else "Yo'q"
    is_staff_display.short_description = _("Xodim statusi")
    is_staff_display.admin_order_field = 'is_staff'

    # is_active ustuni o‘zbekcha
    def is_active_display(self, obj):
        return "Ha" if obj.is_active else "Yo'q"
    is_active_display.short_description = _("Faol")
    is_active_display.admin_order_field = 'is_active'

    # Delete action qo‘shish
    actions = ['delete_selected_users']

    def delete_selected_users(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, _("Tanlangan foydalanuvchilar o‘chirildi"))
    delete_selected_users.short_description = _("Tanlangan foydalanuvchilarni o‘chirish")
