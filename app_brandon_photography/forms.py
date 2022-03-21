from django import forms

# Create your forms here.

class ContactForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 50, label="keresztnév")
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 50, label="vezetéknév")
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 150, label="email")
	message = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), max_length = 2000, label="üzenet")