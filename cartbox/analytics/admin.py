from django.contrib import admin

from .models import SKUInOrderCounter, SKUPairInOrderCounter


admin.site.register(SKUInOrderCounter)
admin.site.register(SKUPairInOrderCounter)
