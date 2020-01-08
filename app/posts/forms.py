from django import forms


class PostCreateForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
            }
        )
    )
    text = forms.CharField(max_length=300)
