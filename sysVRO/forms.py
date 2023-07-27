from django.contrib.auth.models import User
from django import forms
from .models import Profile, Institution, Detachment, Mark, Event


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('patronymic', 'institution', 'photo', 'link_vk', 'about', 'telephone')
        widgets = {'about': forms.Textarea(attrs={'rows': 3}), }


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', help_text='Минимум 8 символов, не простой '
                                                                                     'и не распространенный')
    repeat_password = forms.CharField(widget=forms.PasswordInput, label='Повтор пароля')
    username = forms.CharField(label='Логин', help_text='Только буквы, цифры и символы @/./+/-/_.')
    # Ниже добавляем дополнительные поля из других моделей
    telephone = forms.CharField(label='Телефон')

    # institution = forms.ModelChoiceField(required=False, queryset=Institution.objects)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',

            'email',
            'telephone',
            'username',
            'password',
        ]


class DetachmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Detachment
        fields = (
            'flag',
            'emblem',
            'link_vk',
            'about',
        )


class PartCreateForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('event', 'profile')


class PartUpdateForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('deleted',)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'title', 'scale', 'form', 'kind', 'beginning_date', 'beginning_time', 'ending_date',
                  'photo', 'content', 'place', 'organizer', 'contact', 'admin')
        widgets = {'title': forms.Textarea(attrs={'rows': 4}),
                   'kind': forms.SelectMultiple(attrs={'style': 'height:100px'}),
                   'admin': forms.SelectMultiple(attrs={'style': 'height:200px'}),
                   }
