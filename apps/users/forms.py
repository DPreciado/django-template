from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
# from django.contrib.auth.models import User
from .models import User


class EditProfileForm(forms.ModelForm):

	password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password','id':'password', 'placeholder': 'Password'}))
	password2 = forms.CharField(required=False, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'id': 'verifyPassword'}))
	class Meta:
		model = User

        # Define the fields that will be displayed on the form with their DB column names
		fields = [
			"first_name", 
			"last_name", 
			"email", 
			"password",
			"password2",
			"image", 
			"city", 
			"state",
			'username',		
			"country",
			'address',
			'image',
		]


        # Modify any labels here if required
		labels = {
			# mark_safe to prevent XSS attacks
			'image': mark_safe(''), # Clean the image label
			'email': mark_safe('<b>Email Address*</b>'),
			'username': mark_safe('<b>Username</b>'),
			'first_name': mark_safe('<b>First Name*</b>'),
			'last_name': mark_safe('<b>Last Name*</b>'),
			'country': mark_safe('<b>Country*</b>'),
			'state': mark_safe('<b>State*</b>'),
			'city': mark_safe('<b>City</b>'),
			'address': mark_safe('<b>Address</b>'),
		}
		

        # Modify the input attributes
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name', 'placeholder': 'First Name', 'required': ''}),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name', 'placeholder': 'Last Name', 'required': ''}),
			'email': forms.TextInput(attrs={'class': 'form-control', 'name': 'email','id':'email', 'placeholder': 'Email Address', 'required': ''}),
			'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username', 'required': ''}),
			'country': forms.Select(attrs={'class': 'form-select countries order-alpha limit-pop-1000000 presel-MX group-continents group-order-na', 'name': 'country', 'required': '', 'id': 'countryId'}),
			'state': forms.Select(attrs={'class': 'form-select states order-alpha', 'name': 'state', 'required': '', 'id': 'stateId'}),
			'city': forms.TextInput(attrs={'class': 'form-control', 'name': 'city', 'placeholder': 'City', 'id': 'cityId'}),
			'address': forms.TextInput(attrs={'class': 'form-control', 'name': 'address', 'placeholder': 'Address'}),
		}
  
		help_texts = {
			"username": ""
		}
  
	def clean_email(self):
		email = self.cleaned_data.get('email')
		user = self.instance
		if User.objects.filter(email=email).exists() and user.email != email:
			raise ValidationError('This email is already taken')
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		user = self.instance
		if User.objects.filter(username=username).exists() and user.username != username:
			raise ValidationError('This username is already taken')
		return username
  
	def __ini__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
  
		self.fields['password'].required = False
		self.fields['password2'].required = False
  
		self.fields['username'].help_text = ''

  
	

	def save(self, commit=True):
		user = super(EditProfileForm, self).save(commit=False)
		password = self.cleaned_data["password"]
		if password != '':
			user.set_password(self.cleaned_data['password'])
		else:
			actual_user = User.objects.get(id=user.id)
			user.password = actual_user.password
		if commit:
			user.save()
		return user




class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'email', 'id':'email'}))

	username = forms.CharField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'username'}))

	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'type': 'password',
            'minlength': 8,
			'id':'password'}), required=True, label="Password")

	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'type': 'password',
            'minlength': 8,
			'id':'verifyPassword'}), required=True, label="Verify password")

	first_name = forms.CharField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'first name'}))

	last_name = forms.CharField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'last name'}))



	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "first_name", "last_name")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

	def clean_username(self):
		username  = self.cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			raise ValidationError('This username is already taken')
		return username

	def clean_email(self):
		email  = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise ValidationError('This email is already taken')
		return email
	
	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control form-control-user'


