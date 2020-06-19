from datetime import datetime
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission
from django.contrib import admin
from django.db.models import Q

# IMPORT MODELS
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.models import User
from account_app.models import (
    Module,
    Role,
    Object,
    Operation,
    Permission,
    RoleAssignment,
    PermissionAssignment,
    RoleModule,
    ModuleObject
)


admin.site.register(Module)
admin.site.register(Role)
admin.site.register(Object)
admin.site.register(Operation)
admin.site.register(Permission)
admin.site.register(RoleAssignment)
admin.site.register(PermissionAssignment)
admin.site.register(RoleModule)
admin.site.register(ModuleObject)