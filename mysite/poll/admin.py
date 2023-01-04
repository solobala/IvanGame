from django.contrib import admin

from .models import Owner, Person, Group, Membership, Race, Clan, Fraction, Location, Action, Region, District, Zone
from .models import FractionFraction,  PersonFraction, PersonLocation, ActionType


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
admin.site.register(Race)
admin.site.register(Clan)
admin.site.register(Fraction)
admin.site.register(Location)
admin.site.register(Action)
admin.site.register(FractionFraction)
admin.site.register(PersonFraction)
admin.site.register(PersonLocation)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Zone)
admin.site.register(ActionType)

