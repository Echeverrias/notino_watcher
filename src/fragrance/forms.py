from django import forms
from .models import URL


class URLForm(forms.ModelForm):

    error_messages = {
        'incorrect_url': ("The url is incorrect"),
        'existing_url': ("The url already exists"),
    }

    url = forms.URLField(
        label="Notino URL",
        error_messages={
            'invalid': ('Invalid url')
        }
    )
    class Meta:
        model=URL
        fields=['url']

    def clean_url(self):
        print(f'clean url')
        url = self.cleaned_data['url']
        if not 'notino' in url:
            raise forms.ValidationError(
                self.error_messages['incorrect_url'],
                code='incorrect_url'
            )
        elif URL.objects.filter(url=url):
            print(f'{url } exists')
            raise forms.ValidationError(
                self.error_messages['existing_url'],
                code='existing_url'
            )
        else:
            print(f'url ok')
            return url