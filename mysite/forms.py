from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    HQDog, TpsMoshiDog, DodomaDog, IringaDog,
    HQHorse, TpsMoshiHorse, DodomaHorse, IringaHorse,
    MedicalRecord, Picture, User
)

from django import forms
# from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, initial='user', widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ChoiceField(choices=User.LOCATION_CHOICES, initial='HQ', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'location']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.location = self.cleaned_data['location']
        if commit:
            user.save()
        return user

class HQDogForm(forms.ModelForm):
    class Meta:
        model = HQDog
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class TpsMoshiDogForm(forms.ModelForm):
    class Meta:
        model = TpsMoshiDog
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class DodomaDogForm(forms.ModelForm):
    class Meta:
        model = DodomaDog
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class IringaDogForm(forms.ModelForm):
    class Meta:
        model = IringaDog
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class HQHorseForm(forms.ModelForm):
    class Meta:
        model = HQHorse
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class TpsMoshiHorseForm(forms.ModelForm):
    class Meta:
        model = TpsMoshiHorse
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class DodomaHorseForm(forms.ModelForm):
    class Meta:
        model = DodomaHorse
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class IringaHorseForm(forms.ModelForm):
    class Meta:
        model = IringaHorse
        fields = ['name', 'breed', 'microchip_id', 'behavioral_notes', 'origin', 'date_of_birth', 'gender', 'work', 'training_details', 'weight', 'treatment_details', 'transfer_details']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['dog', 'horse', 'date', 'description', 'doctor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the dog and horse choices to only show instances from HQ
        self.fields['dog'].queryset = HQDog.objects.all()
        self.fields['horse'].queryset = HQHorse.objects.all()

class UserForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, initial='user', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Optional title for this image'}),
            'age_description': forms.TextInput(attrs={'placeholder': 'e.g., Recent, 2 years old, etc.'}),
            'related_object_name': forms.TextInput(attrs={'placeholder': 'Name of the dog, horse, or other entity'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'animal_type': forms.RadioSelect(),
            'medical_records': forms.Textarea(attrs={'rows': 3}),
            'training_details': forms.Textarea(attrs={'rows': 3}),
            'work': forms.Textarea(attrs={'rows': 3}),
            'vaccination_record': forms.Textarea(attrs={'rows': 3}),
            'treatment_record': forms.Textarea(attrs={'rows': 3}),
            'deworming_record': forms.Textarea(attrs={'rows': 3}),
            'transfer_detail': forms.Textarea(attrs={'rows': 3}),
        }

