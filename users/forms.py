from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.contrib.auth import authenticate

class RegistraionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
   
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email' ,'password', 'phone','photo')
       

    def clean(self):
        cleaned_data = super(RegistraionForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )



# class RegistraionForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ('email','first_name','last_name','phone','photo','password1','password2')



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('email','password')





# class DateInput(forms.DateInput):
#     input_type = 'date'


class UpdateUserForm(forms.ModelForm):

    date_birth = forms.DateField(required=False,widget=forms.DateInput())
    photo = forms.ImageField(required=False,widget=forms.FileInput)
    facebook_link = forms.URLField(required=False)
    country = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('first_name','last_name','phone','photo','date_birth','facebook_link','country')

    def clean_country(self):
        if self.is_valid():
            country = self.cleaned_data['country']
            if country:
                return country
            else : 
                return None


    def clean_facebook_link(self):
        if self.is_valid():
            facebook_link = self.cleaned_data['facebook_link']
            if facebook_link:
                return facebook_link
            else : 
                return None
    

    def clean_date_birth(self):
        if self.is_valid():
            date_birth = self.cleaned_data['date_birth']
            if date_birth:
                return date_birth
            else : 
                return None