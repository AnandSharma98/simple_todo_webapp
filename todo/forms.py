from django.forms import ModelForm
from .models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo  # this specifies that with which class we're working
        fields = ['title', 'memo', 'important']  # only  this feilds will show up from model Todo0 to use, vse b baki
        # k feilds edit layak ni h
