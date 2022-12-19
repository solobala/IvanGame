from rest_framework import serializers
from .models import Owner, Person, Group, Membership, Race, Fraction, Location, Zone, Region, Action, Feature


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"


class FractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fraction
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"
