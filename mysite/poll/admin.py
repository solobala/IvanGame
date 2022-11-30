from django.contrib import admin

from .models import Owner, Person, Group, Membership, Race


admin.site.register(Owner)
admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Race)

