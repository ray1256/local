from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text = "Enter a date between now and 4 weeks(defaults 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data >datetime.date.today()+datetime.timedelta(week = 4):
            raise ValidaitonError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

'''
放在model

from django.forms import ModelForm
from .models import BookInstance

# 如果有很多fields 要處理，可以使用這個節省時間
class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datatime.date.today():
            raise ValidationError(_('Invalid date - renewal in pass'))

        if data > datetime.date.today()+datetime.timedelta(weeks = 4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks'))

        return data

        class Meta:
            model = BookInstance
            fields = ['due_back']
            labels = {'due_back':_('Enter a date between now and 4 weeks (default 3).'),}


'''
