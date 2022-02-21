# from django.forms import ModelForm
import datetime
from django import forms
from django.forms import Select
from .models import Projects, Project_pics, ReportProj, Project_donations , ReportCom
from django.core.exceptions import ValidationError


def validate_end_date(value):
    if value < datetime.date.today():
        raise ValidationError(
            ('End Date can\'t be in the past...'),
            params={'value': value},
        )
    


class date_input(forms.DateInput):
    input_type = "date"

class NewProject(forms.ModelForm):
    title = forms.CharField(max_length=50)
    details = forms.CharField(max_length=100)
    total_target = forms.IntegerField(min_value=100)
    end_date = forms.DateField(widget=date_input(),validators=[validate_end_date])
    
    class Meta:
        model = Projects
        fields = ('title', 'details', 'category',
                  'total_target', 'end_date')


class Report1(forms.ModelForm):
    class Meta:
        model = ReportProj
        fields = ('report',)

class Report2(forms.ModelForm):
    class Meta:
        model = ReportCom
        fields = ('report',)


class Donate(forms.ModelForm):
    donation = forms.IntegerField(min_value=1)
    class Meta:
        model = Project_donations
        fields = ('donation',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Project_pics
        fields = ('image',)