from django import forms
from apps.meme import img_flip_api


class Create(forms.Form):
    upper_text = forms.CharField(max_length=100)
    lower_text = forms.CharField(max_length=100)

    def __init__(self, template_id, *args, **kwargs):
        self.template_id = template_id
        return super().__init__(*args, **kwargs)

    def clean(self):
        clean_data = super().clean()

        try:
            clean_data['url'] = img_flip_api.create_meme(self.template_id,
                                                         clean_data['upper_text'],
                                                         clean_data['lower_text'])
        except img_flip_api.ImgFlipError as exc:
            raise forms.ValidationError(str(exc))

        return clean_data
