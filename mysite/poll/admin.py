from django.contrib import admin
from django.db.models.fields.json import JSONField
from jsoneditor.admin import JSONFieldModelAdmin
from jsoneditor.forms import JSONEditor
from .models import *


class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


class PersonInline(admin.TabularInline):
    model = Person


class OwnerAdmin(admin.ModelAdmin):
    inlines = [
        PersonInline,
    ]
    list_display = ("owner_name",)


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Race, JSONFieldModelAdmin)
admin.site.register(Clan)
admin.site.register(Fraction)
admin.site.register(Location)
admin.site.register(Action, JSONFieldModelAdmin)
admin.site.register(FractionFraction)
admin.site.register(PersonFraction)
admin.site.register(PersonLocation)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Zone)
admin.site.register(ActionType)
admin.site.register(Thing, JSONFieldModelAdmin)
admin.site.register(Safe)
admin.site.register(Inventory)
admin.site.register(Consumable, JSONFieldModelAdmin)
admin.site.register(Spell, JSONFieldModelAdmin)
admin.site.register(Money)
admin.site.register(Feature, JSONFieldModelAdmin)
