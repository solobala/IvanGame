import pickle

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import MultiValueField, IntegerField
import json
from .models import Action, Feature, Owner, Person, PersonBar, Consumable
from ckeditor.widgets import CKEditorWidget
from django_json_widget.widgets import JSONEditorWidget
from . import slovar
from django.forms.models import inlineformset_factory


class NewUserForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    link = forms.URLField()
    owner_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# https://colinkingswood.github.io/Model-Form-Customisation/
class ActionUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActionUpdateForm, self).__init__(*args, **kwargs)

        self.fields['action_name'].widget = forms.TextInput()
        self.fields['action_alias'].widget = CKEditorWidget()

        self.fields['action_description'].widget = CKEditorWidget()
        self.fields['sp'].widget = forms.NumberInput()
        self.fields['mp'].widget = forms.NumberInput()
        self.fields['ip'].widget = forms.NumberInput()
        self.fields['pp'].widget = forms.NumberInput()
        self.fields['ap'].widget = forms.NumberInput()
        self.fields['fp'].widget = forms.NumberInput()
        self.fields['lp'].widget = forms.NumberInput()
        self.fields['cp'].widget = forms.NumberInput()
        self.fields['bp'].widget = forms.NumberInput()

        self.fields['fire_access'].widget = forms.NumberInput()
        self.fields['water_access'].widget = forms.NumberInput()
        self.fields['wind_access'].widget = forms.NumberInput()
        self.fields['dirt_access'].widget = forms.NumberInput()
        self.fields['lightning_access'].widget = forms.NumberInput()
        self.fields['holy_access'].widget = forms.NumberInput()
        self.fields['curse_access'].widget = forms.NumberInput()
        self.fields['bleed_access'].widget = forms.NumberInput()
        self.fields['nature_access'].widget = forms.NumberInput()
        self.fields['mental_access'].widget = forms.NumberInput()
        self.fields['twohanded_access'].widget = forms.NumberInput()
        self.fields['polearm_access'].widget = forms.NumberInput()
        self.fields['onehanded_access'].widget = forms.NumberInput()
        self.fields['stabbing_access'].widget = forms.NumberInput()
        self.fields['cutting_access'].widget = forms.NumberInput()
        self.fields['crushing_access'].widget = forms.NumberInput()
        self.fields['small_arms_access'].widget = forms.NumberInput()
        self.fields['shields_access'].widget = forms.NumberInput()

        self.fields['fire_res'].widget = forms.NumberInput()
        self.fields['water_res'].widget = forms.NumberInput()
        self.fields['wind_res'].widget = forms.NumberInput()
        self.fields['dirt_res'].widget = forms.NumberInput()
        self.fields['lightning_res'].widget = forms.NumberInput()
        self.fields['holy_res'].widget = forms.NumberInput()
        self.fields['curse_res'].widget = forms.NumberInput()
        self.fields['crush_res'].widget = forms.NumberInput()
        self.fields['cut_res'].widget = forms.NumberInput()
        self.fields['stab_res'].widget = forms.NumberInput()

        self.fields['helmet_status'].widget = forms.NumberInput()
        self.fields['chest_status'].widget = forms.NumberInput()
        self.fields['shoes_status'].widget = forms.NumberInput()
        self.fields['gloves_status'].widget = forms.NumberInput()
        self.fields['item_status'].widget = forms.NumberInput()

        self.fields['points'].widget = forms.HiddenInput()
        self.fields['permissions'].widget = forms.HiddenInput()
        self.fields['resistances'].widget = forms.HiddenInput()
        self.fields['equipment'].widget = forms.HiddenInput()
        self.fields['fov'].widget = forms.NumberInput()
        self.fields['rov'].widget = forms.NumberInput()

    class Meta:
        model = Action

        fields = ['action_name', 'action_alias', 'action_description']
        for key in slovar.dict_points.keys():
            fields.append(key)
        fields.append('points')

        for key in slovar.dict_resistances.keys():
            fields.append(key)
        fields.append('resistances')

        for key in slovar.dict_permissions.keys():
            fields.append(key)
        fields.append('permissions')

        for key in slovar.dict_equipment.keys():
            fields.append(key)
        fields.append('equipment')
        fields.append('fov')
        fields.append('rov')

    def clean(self):
        cleaned_data = super().clean()

        self.cleaned_data.update({'action_name': cleaned_data.get('action_name'),
                                  'action_alias': cleaned_data.get('action_alias'),
                                  'action_description': cleaned_data.get('action_description')})

        # Заполним JSON-поля из NumericField
        points = dict()
        for key in slovar.dict_points.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            points[key] = self.cleaned_data[key]

        self.cleaned_data.update({"points": json.dumps(points, indent=4)})

        permissions = dict()
        for key in slovar.dict_permissions.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            permissions[key] = self.cleaned_data[key]

        self.cleaned_data.update({"permissions": json.dumps(permissions, indent=4)})

        resistances = dict()
        for key in slovar.dict_resistances.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            resistances[key] = self.cleaned_data[key]

        self.cleaned_data.update({"resistances": json.dumps(resistances, indent=4)})

        equipment = dict()
        for key in slovar.dict_equipment.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            equipment[key] = self.cleaned_data[key]

        self.cleaned_data.update({"equipment": json.dumps(equipment, indent=4)})

        return self.cleaned_data


class FeatureUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeatureUpdateForm, self).__init__(*args, **kwargs)

        self.fields['feature_name'].widget = forms.TextInput()
        self.fields['feature_description'].widget = CKEditorWidget()
        self.fields['agg_points'].widget = forms.NumberInput()
        self.fields['sp'].widget = forms.NumberInput()
        self.fields['mp'].widget = forms.NumberInput()
        self.fields['ip'].widget = forms.NumberInput()
        self.fields['pp'].widget = forms.NumberInput()
        self.fields['ap'].widget = forms.NumberInput()
        self.fields['fp'].widget = forms.NumberInput()
        self.fields['lp'].widget = forms.NumberInput()
        self.fields['cp'].widget = forms.NumberInput()
        self.fields['bp'].widget = forms.NumberInput()

        self.fields['fire_access'].widget = forms.NumberInput()
        self.fields['water_access'].widget = forms.NumberInput()
        self.fields['wind_access'].widget = forms.NumberInput()
        self.fields['dirt_access'].widget = forms.NumberInput()
        self.fields['lightning_access'].widget = forms.NumberInput()
        self.fields['holy_access'].widget = forms.NumberInput()
        self.fields['curse_access'].widget = forms.NumberInput()
        self.fields['bleed_access'].widget = forms.NumberInput()
        self.fields['nature_access'].widget = forms.NumberInput()
        self.fields['mental_access'].widget = forms.NumberInput()
        self.fields['twohanded_access'].widget = forms.NumberInput()
        self.fields['polearm_access'].widget = forms.NumberInput()
        self.fields['onehanded_access'].widget = forms.NumberInput()
        self.fields['stabbing_access'].widget = forms.NumberInput()
        self.fields['cutting_access'].widget = forms.NumberInput()
        self.fields['crushing_access'].widget = forms.NumberInput()
        self.fields['small_arms_access'].widget = forms.NumberInput()
        self.fields['shields_access'].widget = forms.NumberInput()

        self.fields['fire_res'].widget = forms.NumberInput()
        self.fields['water_res'].widget = forms.NumberInput()
        self.fields['wind_res'].widget = forms.NumberInput()
        self.fields['dirt_res'].widget = forms.NumberInput()
        self.fields['lightning_res'].widget = forms.NumberInput()
        self.fields['holy_res'].widget = forms.NumberInput()
        self.fields['curse_res'].widget = forms.NumberInput()
        self.fields['crush_res'].widget = forms.NumberInput()
        self.fields['cut_res'].widget = forms.NumberInput()
        self.fields['stab_res'].widget = forms.NumberInput()

        self.fields['helmet_status'].widget = forms.NumberInput()
        self.fields['chest_status'].widget = forms.NumberInput()
        self.fields['shoes_status'].widget = forms.NumberInput()
        self.fields['gloves_status'].widget = forms.NumberInput()
        self.fields['item_status'].widget = forms.NumberInput()

        self.fields['points'].widget = forms.HiddenInput()
        self.fields['permissions'].widget = forms.HiddenInput()
        self.fields['resistances'].widget = forms.HiddenInput()
        self.fields['equipment'].widget = forms.HiddenInput()

    class Meta:
        model = Feature

        fields = ['feature_name', 'feature_description', 'agg_points']
        for key in slovar.dict_points.keys():
            fields.append(key)
        fields.append('points')

        for key in slovar.dict_resistances.keys():
            fields.append(key)
        fields.append('resistances')

        for key in slovar.dict_permissions.keys():
            fields.append(key)
        fields.append('permissions')

        for key in slovar.dict_equipment.keys():
            fields.append(key)
        fields.append('equipment')

    def clean(self):
        cleaned_data = super().clean()

        self.cleaned_data.update({'feature_name': cleaned_data.get('feature_name'),

                                  'feature_description': cleaned_data.get('feature_description')})
        # Заполним JSON-поля из NumericField
        points = dict()
        for key in slovar.dict_points.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            points[key] = self.cleaned_data[key]

        self.cleaned_data.update({"points": json.dumps(points, indent=4)})

        permissions = dict()
        for key in slovar.dict_permissions.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            permissions[key] = self.cleaned_data[key]

        self.cleaned_data.update({"permissions": json.dumps(permissions, indent=4)})

        resistances = dict()
        for key in slovar.dict_resistances.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            resistances[key] = self.cleaned_data[key]

        self.cleaned_data.update({"resistances": json.dumps(resistances, indent=4)})

        equipment = dict()
        for key in slovar.dict_equipment.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            equipment[key] = self.cleaned_data[key]

        self.cleaned_data.update({"equipment": json.dumps(equipment, indent=4)})

        return self.cleaned_data


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'
        widgets = {
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_description': forms.Textarea(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'owner_img': forms.FileInput(attrs={'class': 'form-control'})
        }


class PersonForm(forms.ModelForm):
    model = Person
    fields = '__all__'
    widgets = {
        'person_name': forms.TextInput(attrs={'class': 'form-control'}),
        'person_img': forms.FileInput(attrs={'class': 'form-control'}),
        'link': forms.URLInput(attrs={'class': 'form-control'}),
        'biography': forms.Textarea(attrs={'class': 'form-control'}),
        'character': forms.Textarea(attrs={'class': 'form-control'}),
        'interests': forms.Textarea(attrs={'class': 'form-control'}),
        'phobias': forms.Textarea(attrs={'class': 'form-control'}),
        'race': forms.Select(attrs={'class': 'form-control'}),
        'location_birth': forms.Select(attrs={'class': 'form-control'}),
        'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        'location_death': forms.Select(attrs={'class': 'form-control'}),
        'death_date': forms.DateInput(attrs={'class': 'form-control'}),
        'status': forms.Select(attrs={'class': 'form-control'}),
        'features': forms.SelectMultiple(attrs={'class': 'form-control'}),
    }


PersonFormSet = inlineformset_factory(
    Owner, Person, fields=('owner', 'person_name', 'person_img', 'link', 'biography', 'character', 'interests',
                           'phobias', 'race', 'location_birth', 'birth_date', 'location_death', 'death_date', 'status',
                           'features'),
    form=PersonForm, extra=1, can_delete=True, can_delete_extra=True)


class ConsumableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsumableForm, self).__init__(*args, **kwargs)

        self.fields['consumable_name'].widget = forms.TextInput()
        self.fields['consumable_description'].widget = CKEditorWidget()
        self.fields['sale_price'].widget = forms.NumberInput()
        self.fields['buy_price'].widget = forms.NumberInput()
        self.fields['weight'].widget = forms.NumberInput()
        self.fields['conditions'].widget = forms.HiddenInput
        for key in slovar.dict_conditions.keys():
            if key not in ["load_capacity", "avg_magic_resistance", "avg_physic_resistance"]:
                self.fields[key].widget = forms.NumberInput()
        self.fields['points_to_make'].widget = forms.HiddenInput
        for key in slovar.dict_points.keys():
            self.fields[key + '_to_make'].widget = forms.NumberInput()
        self.fields['points_from_use'].widget = forms.HiddenInput
        for key in slovar.dict_points.keys():
            self.fields[key + '_from_use'].widget = forms.NumberInput()
        self.fields['resistances_from_use'].widget = forms.HiddenInput
        for key in slovar.dict_resistances.keys():
            self.fields[key].widget = forms.NumberInput()
        self.fields['damage_from_use'].widget = forms.HiddenInput
        for key in slovar.dict_damage.keys():
            self.fields[key].widget = forms.NumberInput()

    class Meta:
        model = Consumable

        fields = ['consumable_name', 'consumable_description', 'sale_price', 'buy_price', 'weight',
                  'conditions']
        for key in slovar.dict_conditions.keys():
            if key not in ["load_capacity", "avg_magic_resistance", "avg_physic_resistance"]:
                fields.append(key)
        fields.append('points_to_make')
        for key in slovar.dict_points.keys():
            fields.append(key + '_to_make')
        fields.append('points_from_use')
        for key in slovar.dict_points.keys():
            fields.append(key + '_from_use')
        fields.append('resistances_from_use')
        for key in slovar.dict_resistances.keys():
            fields.append(key)
        fields.append('damage_from_use')
        for key in slovar.dict_damage.keys():
            fields.append(key)

    def clean(self):
        cleaned_data = super().clean()

        conditions = dict()
        points_to_make = dict()
        points_from_use = dict()

        for key in slovar.dict_conditions.keys():
            if key not in ["load_capacity", "avg_magic_resistance", "avg_physic_resistance"]:
                conditions[key] = self.cleaned_data[key]

        for key in slovar.dict_points.keys():
            points_to_make[key + '_to_make'] = self.cleaned_data[key]
            points_from_use[key + '_from_use'] = self.cleaned_data[key]

        resistances_from_use = dict()
        for key in slovar.dict_resistances.keys():
            resistances_from_use[key] = self.cleaned_data[key]

        damage_from_use = dict()
        for key in slovar.dict_damage.keys():
            damage_from_use[key] = self.cleaned_data[key]

        cleaned_data['conditions'] = json.dumps(conditions, indent=4)
        cleaned_data['points_to_make'] = json.dumps(points_to_make, indent=4)
        cleaned_data['points_from_use'] = json.dumps(points_from_use, indent=4)
        cleaned_data['resistances_from_use'] = json.dumps(resistances_from_use, indent=4)
        cleaned_data['damage_from_use'] = json.dumps(damage_from_use, indent=4)
     
        return self.cleaned_data

    def save(self, commit=True):
        consumable = super(ConsumableForm, self)
        consumable.consumable_name = self.cleaned_data['consumable_name']
        consumable.consumable_description = self.cleaned_data['consumable_description']
        consumable.sale_price = self.cleaned_data['sale_price']
        consumable.buy_price = self.cleaned_data['buy_price']
        consumable.weight = self.cleaned_data['weight']
        consumable.conditions = self.cleaned_data['conditions']
        consumable.points_to_make = self.cleaned_data['points_to_make']
        consumable.points_from_use = self.cleaned_data['points_from_use']
        consumable.resistances_from_use = self.cleaned_data['resistances_from_use']
        consumable.damage_from_use = self.cleaned_data['damage_from_use']

        return consumable
