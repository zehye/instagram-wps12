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


class CommentCreateForm(forms.Form):
    content = forms.CharField(
        max_length=10,
        widget=forms.Textarea()
    )

    def save(self, post, author):
        return post.postcomment_set.create(
            author=author,
            content=self.cleaned_data['content'],
        )