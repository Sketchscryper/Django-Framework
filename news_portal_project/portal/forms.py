from django import forms
from .models import Article, Comment, SiteSettings
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'article_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%; padding: 8px;'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'style': 'width: 100%;'}),
            'article_type': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'article_type': 'Тип материала',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'style': 'width: 100%; padding: 8px;'}),
        }
        labels = {
            'text': 'Ваш комментарий',
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['background_color', 'text_color', 'font_size']
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color', 'style': 'width: 50px;'}),
            'text_color': forms.TextInput(attrs={'type': 'color', 'style': 'width: 50px;'}),
            'font_size': forms.Select(attrs={'style': 'width: 100px;'}, choices=[
                ('12px', '12px'), ('14px', '14px'), ('16px', '16px'),
                ('18px', '18px'), ('20px', '20px'), ('24px', '24px'),
            ]),
        }


class BanUserForm(forms.Form):
    duration = forms.ChoiceField(
        choices=[('day', 'День'), ('week', 'Неделя'), ('month', 'Месяц'), ('forever', 'Навсегда')],
        label='Длительность бана'
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'style': 'width: 100%;'}),
        required=False,
        label='Причина'
    )


class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}),
            'email': forms.EmailInput(attrs={'style': 'width: 100%; padding: 8px;'}),
            'first_name': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}),
            'last_name': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data