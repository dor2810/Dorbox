from django import forms
from groups.models import Group
from folders.models import Folder


class UpdateForm(forms.ModelForm):
    name = forms.CharField(label="Name: ")
    # folders = forms.ModelMultipleChoiceField(queryset=None,
    #                                 label="Folder: ",
    #                                 widget=forms.Select,
    #                                 required=False
    #                                 )

    description = forms.CharField(label="Description", widget=forms.Textarea({}))

    # def __init__(self, *args, **kwargs):
    #         group_slug = kwargs.pop('slug', None)
    #         super(UpdateForm, self).__init__(*args, **kwargs)
    #
    #         group = Group.objects.get(slug = group_slug)
    #         self.fields['folders'].queryset = Folder.objects.filter(group = group)
    #         self.fields['folders'].empty_label = group.name
    class Meta:
        model = Folder
        fields = []
