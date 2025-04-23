from django import forms

# Create your forms here.
class ContactForm(forms.Form):
	name = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		label='Név',
		max_length=100,
		error_messages={
			'required': 'Kérlek, add meg a neved!',
		}
	)
	email_address = forms.EmailField(
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		label='Email-cím',
		error_messages={
			'required': 'Kérlek, add meg az email címed!',
			'invalid': 'Kérlek, érvényes email címet adj meg!',
		}
	)
	message = forms.CharField(
		widget = forms.Textarea(attrs={'class': 'form-control'}),
		label='Üzenet',
		max_length = 2000, 
		error_messages={
			'required': 'Kérlek, írd meg az üzeneted!',
		}
	)