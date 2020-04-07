from django import forms


class PermissionForm(forms.Form):
    PERMISSION_CHOICES = [
        ('reader', 'Reader'),
        ('editor', 'Editor')
    ]

    username = forms.CharField(label="Username: ")
    permission= forms.ChoiceField(
        widget=forms.Select,
        choices=PERMISSION_CHOICES,
    )

class CreatePrivateForm(forms.Form):
    username = forms.CharField(label="Username: ")
    description = forms.CharField(label="Description", widget=forms.Textarea({}))
