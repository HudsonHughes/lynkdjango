# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import (UserAdmin as BaseUserAdmin, User as BaseUser)
from .models import User
from .forms import UserCreationForm

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name', 'email', 'date_of_birth',)}),
        (_('Contact info'), {'fields': ('home_phone', 'cell_phone', 'address',)}),
        (_('Academic info'), {'fields': ('year',)}),
        (_('Other'), {'fields': ('avatar_thumbnail',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('last_name', 'first_name', 'middle_name', 'email')
    ordering = ('last_name', 'first_name', 'middle_name', 'id')
    add_form = UserCreationForm


admin.site.register(User, UserAdmin)