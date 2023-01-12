from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import MultiValueField
import json
from .models import Action, Feature, Owner, Person, PersonBar
from ckeditor.widgets import CKEditorWidget
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


class PointsWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = {"sp": forms.NumberInput(attrs=attrs),
                   "mp": forms.NumberInput(attrs=attrs),
                   "ip": forms.NumberInput(attrs=attrs),
                   "pp": forms.NumberInput(attrs=attrs),
                   "ap": forms.NumberInput(attrs=attrs),
                   "fp": forms.NumberInput(attrs=attrs),
                   "lp": forms.NumberInput(attrs=attrs),
                   "bp": forms.NumberInput(attrs=attrs),
                   "cp": forms.NumberInput(attrs=attrs)

                   }
        super().__init__(self, widgets, attrs)

    def decompress(self, value):
        if isinstance(value, dict):
            value.sp = value['sp']
            value.mp = value['mp']
            value.ip = value['ip']
            value.pp = value['pp']
            value.ap = value['ap']
            value.fp = value['fp']
            value.lp = value['lp']
            value.bp = value['bp']
            value.cp = value['cp']
            return [value.sp, value.mp, value.ip, value.pp, value.ap, value.fp, value.lp, value.bp, value.cp]
        elif isinstance(value, str):
            a = json.loads(value)
            return [a.sp, a.mp, a.ip, a.pp, a.ap, a.fp, a.lp, a.bp, a.cp]
        return [None, None, None, None, None, None, None, None, None]

    def has_changed(self, initial, data):
        if initial is None:
            initial = {i: 0 for i in slovar.dict_points}
        else:
            if not isinstance(initial, dict):
                initial = self.widget.decompress(initial)
            for field, initial, data in zip(self.fields, initial, data):
                initial = field.to_python(initial)
                data = field.to_python(data)




# https://colinkingswood.github.io/Model-Form-Customisation/
class ActionUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActionUpdateForm, self).__init__(*args, **kwargs)

        self.fields['action_name'].widget = forms.TextInput()
        self.fields['action_alias'].widget = forms.TextInput()
        # self.fields['action_description'].widget = forms.Textarea(widget=CKEditorWidget())
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

        self.fields['points'].widget = forms.Textarea()
        self.fields['permissions'].widget = forms.Textarea()
        self.fields['resistances'].widget = forms.Textarea()
        self.fields['equipment'].widget = forms.Textarea()

    class Meta:
        model = Feature

        fields = ['feature_name', 'feature_description']
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


class PersonBarCharUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonBarCharUpdateForm, self).__init__(*args, **kwargs)
        self.fields['summary_points'].widget = forms.MultiWidget(widgets={'sp': forms.NumberInput(),
                                                                          'mp': forms.NumberInput(),
                                                                          'ip': forms.NumberInput(),
                                                                          'pp': forms.NumberInput(),
                                                                          'ap': forms.NumberInput(),
                                                                          'fp': forms.NumberInput(),
                                                                          'lp': forms.NumberInput(),
                                                                          'cp': forms.NumberInput(),
                                                                          'bp': forms.NumberInput(),
                                                                          })

    class Meta:
        model = PersonBar
        fields = ['summary_points']

    def clean(self):
        cleaned_data = super().clean()

        self.cleaned_data.update({'summary_points': cleaned_data.get('summary_points')})

        summary_points = dict()
        for key in slovar.dict_points.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            summary_points[key] = self.cleaned_data[key]
        self.cleaned_data.update({'summary_points': summary_points})
        return self.cleaned_data
