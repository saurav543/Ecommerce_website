from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms.widgets import Widget
from .models import Address, Customer


class UserAddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ('full_name','phone','postcode','address_line','address_line2','towncity',)
      
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['full_name'].widget.attrs.update(
            {
            'class':"form-control mb-2 account-form",
            'placeholder':"Enter your Full Name",
            }
        )
        self.fields['phone'].widget.attrs.update({
            'class':"form-control mb-2 account-form",
            'placeholder':"Enter your Phone number",
        })
        self.fields['address_line'].widget.attrs.update({
            'class':"form-control mb-2 account-form",
            'placeholder':"Address_line 1",
        })
        self.fields['address_line2'].widget.attrs.update({
            'class':"form-control mb-2 account-form",
            'placeholder':"Address Line 2",
        })
        self.fields['towncity'].widget.attrs.update({
            'class':"form-control mb-2 account-form",
            'placeholder':"Towncity",
        })  
        self.fields['postcode'].widget.attrs.update({
            'class':"form-control mb-2 account-form",
            'placeholder':"Postcode",
        })
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'username',
            'id': 'login-username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '**********',
            'id': 'login-pwd',
        }
    ))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label='Account email (can not be changed)', max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'email',
            'id': 'form-email',
            'readonly': 'readonly'
        }
    ))
    name = forms.CharField(label='Username', min_length=4, max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Username',
            'id': 'form-username',
            'readonly': 'readonly'
        }
    ))
    # first_name = forms.CharField(label='First Name', min_length=4, max_length=50, widget=forms.TextInput(
    #     attrs={
    #         'class': 'form-control mb-3',
    #         'placeholder': 'First Name',
    #         'id': 'form-firstname'
    #     }
    # ))
    # # phone_number = forms.CharField(label='Phone Number', max_length=15, widget=forms.TextInput(
    # #     attrs={
    # #         'class': 'form-control mb-3',
    # #         'placeholder': 'Phone Number',
    # #         'id': 'form-phone'
    # #     }
    # # ))
    # address_line_1 = forms.CharField(label='Address line 1', max_length=15, widget=forms.TextInput(
    #     attrs={
    #         'class': 'form-control mb-3',
    #         'placeholder': 'Address',
    #         'id': 'form-address_1'
    #     }
    # ))
    # address_line_2 = forms.CharField(label='Address line 2', max_length=15, widget=forms.TextInput(
    #     attrs={
    #         'class': 'form-control mb-3',
    #         'placeholder': 'Correspondence address',
    #         'id': 'form-address_2'
    #     }
    # ))
    

    class Meta:
        model = Customer
        fields = ('email', 'name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(
        label="Username", max_length=50, min_length=4, help_text='Required')
    email = forms.EmailField(
        label="Email", max_length=100, help_text='Required', error_messages={'required': 'You must have to enter email'})
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name', 'email',)

    # def clean_username(self):
    #     name = self.cleaned_data['name'].lower()
    #     r = Customer.objects.filter(name=name)
    #     if r.count():
    #         raise forms.ValidationError("Username already exists")
    #     return name

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password do not match')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email,that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter your Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter your E-mail', 'name': 'email', 'id': 'email'})
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': '**********'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': '**********'
        })


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(label='E-mail', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Email',
        'id': 'form-email'
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(' we can not find that email address ')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password', widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'New Password',
            'id': 'form-password'
        })
    )
    new_password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Confirm Password',
            'id': 'form-password2'
        })
    )
