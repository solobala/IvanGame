from django.contrib import admin

from .models import Owner, Person, Group, Membership, Race, Clan, Fraction, Location, Action
from .models import FractionFraction,  PersonFraction, PersonLocation


admin.site.register(Owner)
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


