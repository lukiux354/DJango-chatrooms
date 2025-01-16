from django import forms
from .models import Channel

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name']  # Add only the fields you want to expose to the user
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Channel Name'}),
        }
        labels = {
            'name': 'Channel Name',
        }
