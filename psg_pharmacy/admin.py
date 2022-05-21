from pyexpat.errors import messages
from django.contrib import admin
from .models import Messages
from .models import Mail
from .models import Orders

# Register your models here.
admin.site.register(Messages)
admin.site.register(Mail)
admin.site.register(Orders)