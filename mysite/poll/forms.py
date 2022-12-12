from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Action
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
class ActionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        # user = kwargs.pop('user')
        # self.logged_user = user

        self.fields['action_name'].widget = forms.TextInput()
        self.fields['action_alias'].widget = forms.TextInput()
        self.fields['action_description'].widget = forms.TextInput()
        self.fields['action_points'].widget = forms.TextInput()
        self.fields['Стамина'].widget = forms.NumberInput()
        self.fields['Колдовство'].widget = forms.NumberInput()
        self.fields['Интеллект'].widget = forms.NumberInput()
        self.fields['Сила'].widget = forms.NumberInput()
        self.fields['Ловкость'].widget = forms.NumberInput()
        self.fields['Вера'].widget = forms.NumberInput()
        self.fields['Удача'].widget = forms.NumberInput()
        self.fields['Харизма'].widget = forms.NumberInput()
        self.fields['Рассудок'].widget = forms.NumberInput()

        self.fields['Пирокинектика'].widget = forms.TextInput()
        self.fields['Гидрософистика'].widget = forms.NumberInput()
        self.fields['Аэрософистика'].widget = forms.NumberInput()
        self.fields['Геомантия'].widget = forms.NumberInput()
        self.fields['Киловактика'].widget = forms.NumberInput()
        self.fields['Элафристика'].widget = forms.NumberInput()
        self.fields['Катифристика'].widget = forms.NumberInput()
        self.fields['Гематомантия'].widget = forms.NumberInput()
        self.fields['Ботаника'].widget = forms.NumberInput()
        self.fields['Псифистика'].widget = forms.NumberInput()
        self.fields['Владение навыками Древкового оружия'].widget = forms.NumberInput()
        self.fields['Владение навыками Одноручного оружия'].widget = forms.NumberInput()
        self.fields['Владение навыками Колющего оружия'].widget = forms.NumberInput()
        self.fields['Владение навыками Режущего оружия'].widget = forms.NumberInput()
        self.fields['Владение навыками Дробящего оружия'].widget = forms.NumberInput()
        self.fields['Владение навыками Стрелкового оружия'].widget = forms.NumberInput()
        self.fields['Владение навыками Щитов'].widget = forms.NumberInput()

        self.fields['action_resistanses'].widget = forms.TextInput()
        self.fields['Устойчивость к огню'].widget = forms.NumberInput()
        self.fields['Устойчивость к воде'].widget = forms.NumberInput()
        self.fields['Устойчивость к воздуху'].widget = forms.NumberInput()
        self.fields['Устойчивость к земле'].widget = forms.NumberInput()
        self.fields['Устойчивость к молниям'].widget = forms.NumberInput()
        self.fields['Устойчивость к свету'].widget = forms.NumberInput()
        self.fields['Устойчивость ко тьме'].widget = forms.NumberInput()
        self.fields['Устойчивость к дроблению'].widget = forms.NumberInput()
        self.fields['Устойчивость к порезам'].widget = forms.NumberInput()
        self.fields['Устойчивость к протыканию'].widget = forms.NumberInput()

        self.fields['action_equipment'].widget = forms.TextInput()
        self.fields['Шлем'].widget = forms.NumberInput()
        self.fields['Нагрудник'].widget = forms.NumberInput()
        self.fields['Сапоги'].widget = forms.NumberInput()
        self.fields['Наручи'].widget = forms.NumberInput()
        self.fields['Прочее'].widget = forms.NumberInput()

    class Meta:
        model = Action
        fields = ['action_name', 'action_alias', 'action_description', 'action_points', 'action_permissions',
                  'action_resistanses', 'action_equipment']

        for key, value in slovar.dict_points.items():
            fields.append(value)
        for key, value in slovar.dict_permissions.items():
            fields.append(value)
        for key, value in slovar.dict_resistances.items():
            fields.append(value)
        for key, value in slovar.dict_equipment.items():
            fields.append(value)

    # def get_form_kwargs(self):
    #     kwargs = {'user': self.request.user, }
    #     return kwargs

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data.update({'action_name': cleaned_data.get('action_name'),
                                  'action_alias': cleaned_data.get('action_alias'),
                                  'action_description': cleaned_data.get('action_description'),
                                  'action_points':  cleaned_data.get('action_points'),
                                  'action_permissions':  cleaned_data.get('action_permissions'),
                                  'action_resistanses': cleaned_data.get('action_resistanses'),
                                  'action_equipment': cleaned_data.get('action_equipment')})
