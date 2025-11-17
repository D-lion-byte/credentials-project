from django import forms


class PublicCredentialSubmissionForm(forms.Form):
    """
    Public form for anyone to submit their credentials
    """
    
    current_password = forms.CharField(
        label='Current Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        })
    )
    
    new_password = forms.CharField(
        label='New Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password'
        })
    )
    
    confirm_password = forms.CharField(
        label='Confirm New Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('Passwords do not match.')
        
        return cleaned_data

