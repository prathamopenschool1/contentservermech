from django.contrib import admin
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import CustomUserAdminCreationForm, CustomUserAdminChangeForm
# from .models import CrlUserModel


# class CustomUserAdmin(BaseUserAdmin):
#     form = CustomUserAdminChangeForm
#     add_form = CustomUserAdminCreationForm

#     list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('username',)}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email', 'username')
#     ordering = ('email',)
#     filter_horizontal = ()
#     readonly_fields = ('date_joined', 'last_login')


# admin.site.register(CrlUserModel, CustomUserAdmin)
# # admin.site.unregister(Group)


