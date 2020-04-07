from django import forms
from groups.models import Group
from folders.models import Folder
from files.models import File


class UpdateForm(forms.ModelForm):
    name = forms.CharField(label="Name: ")
    folder = forms.ModelChoiceField(queryset=None,
                                    label="Folder: ",
                                    widget=forms.Select,
                                    required=False
                                    )

    description = forms.CharField(label="Description", widget=forms.Textarea({}))

    def __init__(self, *args, **kwargs):
            group_slug = kwargs.pop('slug', None)
            super(UpdateForm, self).__init__(*args, **kwargs)

            group = Group.objects.get(slug = group_slug)
            self.fields['folder'].queryset = Folder.objects.filter(group = group)
            self.fields['folder'].empty_label = group.name
    class Meta:
        model = File
        fields = []
