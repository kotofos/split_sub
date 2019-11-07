from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class SplitForm(forms.Form):
    sub_text = forms.CharField(
        widget=forms.Textarea(attrs={'cols':120, 'rows': 30}),
        label='Вставить сабы сюда',
        max_length=100000,
    )
