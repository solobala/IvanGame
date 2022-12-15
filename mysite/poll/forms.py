from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Action, Feature
from ckeditor.widgets import CKEditorWidget
from . import slovar


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
        self.fields['action_alias'].widget = forms.TextInput()
        # self.fields['action_description'].widget = forms.Textarea(widget=CKEditorWidget())
        self.fields['action_description'].widget = CKEditorWidget()
        self.fields['SP'].widget = forms.NumberInput()
        self.fields['MP'].widget = forms.NumberInput()
        self.fields['IP'].widget = forms.NumberInput()
        self.fields['PP'].widget = forms.NumberInput()
        self.fields['AP'].widget = forms.NumberInput()
        self.fields['FP'].widget = forms.NumberInput()
        self.fields['LP'].widget = forms.NumberInput()
        self.fields['CP'].widget = forms.NumberInput()
        self.fields['BP'].widget = forms.NumberInput()

        self.fields['Fire_access'].widget = forms.NumberInput()
        self.fields['Water_access'].widget = forms.NumberInput()
        self.fields['Wind_access'].widget = forms.NumberInput()
        self.fields['Dirt_access'].widget = forms.NumberInput()
        self.fields['Lightning_access'].widget = forms.NumberInput()
        self.fields['Holy_access'].widget = forms.NumberInput()
        self.fields['Curse_access'].widget = forms.NumberInput()
        self.fields['Bleed_access'].widget = forms.NumberInput()
        self.fields['Nature_access'].widget = forms.NumberInput()
        self.fields['Mental_access'].widget = forms.NumberInput()
        self.fields['Twohanded_access'].widget = forms.NumberInput()
        self.fields['Polearm_access'].widget = forms.NumberInput()
        self.fields['Onehanded_access'].widget = forms.NumberInput()
        self.fields['Stabbing_access'].widget = forms.NumberInput()
        self.fields['Cutting_access'].widget = forms.NumberInput()
        self.fields['Crushing_access'].widget = forms.NumberInput()
        self.fields['Small_arms_access'].widget = forms.NumberInput()
        self.fields['Shields_access'].widget = forms.NumberInput()

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

        self.fields['points'].widget = forms.Textarea()
        self.fields['permissions'].widget = forms.Textarea()
        self.fields['resistances'].widget = forms.Textarea()
        self.fields['equipment'].widget = forms.Textarea()
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

        points = dict()
        for key in slovar.dict_points.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            points[key] = self.cleaned_data[key]
        self.cleaned_data.update({'points': points})
        permissions = dict()
        for key in slovar.dict_permissions.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            permissions[key] = self.cleaned_data[key]
        self.cleaned_data["permissions"] = permissions
        resistances = dict()
        for key in slovar.dict_resistances.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            resistances[key] = self.cleaned_data[key]
        self.cleaned_data["resistances"] = resistances
        equipment = dict()
        for key in slovar.dict_equipment.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            equipment[key] = self.cleaned_data[key]
        self.cleaned_data.update({"equipment": equipment})
        return self.cleaned_data


class FeatureUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeatureUpdateForm, self).__init__(*args, **kwargs)

        self.fields['feature_name'].widget = forms.TextInput()

        # self.fields['action_description'].widget = forms.Textarea(widget=CKEditorWidget())
        self.fields['feature_description'].widget = CKEditorWidget()
        self.fields['SP'].widget = forms.NumberInput()
        self.fields['MP'].widget = forms.NumberInput()
        self.fields['IP'].widget = forms.NumberInput()
        self.fields['PP'].widget = forms.NumberInput()
        self.fields['AP'].widget = forms.NumberInput()
        self.fields['FP'].widget = forms.NumberInput()
        self.fields['LP'].widget = forms.NumberInput()
        self.fields['CP'].widget = forms.NumberInput()
        self.fields['BP'].widget = forms.NumberInput()

        self.fields['Fire_access'].widget = forms.NumberInput()
        self.fields['Water_access'].widget = forms.NumberInput()
        self.fields['Wind_access'].widget = forms.NumberInput()
        self.fields['Dirt_access'].widget = forms.NumberInput()
        self.fields['Lightning_access'].widget = forms.NumberInput()
        self.fields['Holy_access'].widget = forms.NumberInput()
        self.fields['Curse_access'].widget = forms.NumberInput()
        self.fields['Bleed_access'].widget = forms.NumberInput()
        self.fields['Nature_access'].widget = forms.NumberInput()
        self.fields['Mental_access'].widget = forms.NumberInput()
        self.fields['Twohanded_access'].widget = forms.NumberInput()
        self.fields['Polearm_access'].widget = forms.NumberInput()
        self.fields['Onehanded_access'].widget = forms.NumberInput()
        self.fields['Stabbing_access'].widget = forms.NumberInput()
        self.fields['Cutting_access'].widget = forms.NumberInput()
        self.fields['Crushing_access'].widget = forms.NumberInput()
        self.fields['Small_arms_access'].widget = forms.NumberInput()
        self.fields['Shields_access'].widget = forms.NumberInput()

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

        self.fields['points'].widget = forms.Textarea()
        self.fields['permissions'].widget = forms.Textarea()
        self.fields['resistances'].widget = forms.Textarea()
        self.fields['equipment'].widget = forms.Textarea()

    class Meta:
        model = Feature

        fields = ['feature_name',  'feature_description']
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

        points = dict()
        for key in slovar.dict_points.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            points[key] = self.cleaned_data[key]
        self.cleaned_data.update({'points': points})
        permissions = dict()
        for key in slovar.dict_permissions.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            permissions[key] = self.cleaned_data[key]
        self.cleaned_data["permissions"] = permissions
        resistances = dict()
        for key in slovar.dict_resistances.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            resistances[key] = self.cleaned_data[key]
        self.cleaned_data["resistances"] = resistances
        equipment = dict()
        for key in slovar.dict_equipment.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            equipment[key] = self.cleaned_data[key]
        self.cleaned_data.update({"equipment": equipment})
        return self.cleaned_data
