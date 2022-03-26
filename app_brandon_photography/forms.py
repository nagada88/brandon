from django import forms

# Create your forms here.

class ContactForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 50, label="név", label_suffix="")
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 150, label="email", label_suffix="")
	message = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), max_length = 2000, label="üzenet", label_suffix="")