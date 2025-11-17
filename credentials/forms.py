from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UpdateCredentialsForm(forms.Form):
    """
    Secure form for updating user credentials (email, username, password)
    with comprehensive validation
    """
    
    # Email field
    email = forms.EmailField(
        label='Email Address',
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new email address'
        }),
        help_text='Enter a valid email address'
    )
    
    # Username field
    username = forms.CharField(
        label='Username',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new username'
        }),
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    
    # Current password (for verification) - only required if not using token
    current_password = forms.CharField(
        label='Current Password',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        }),
        help_text='Enter your current password to verify it\'s you'
    )
    
    # New password fields
    new_password = forms.CharField(
        label='New Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        help_text='Create a strong password for your account'
    )
    
    confirm_password = forms.CharField(
        label='Confirm New Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        help_text='Re-enter the new password'
    )
    
    def __init__(self, user, *args, via_token=False, **kwargs):
        """Initialize form with current user data"""
        self.user = user
        self.via_token = via_token
        super().__init__(*args, **kwargs)
        
        # Pre-fill with current data
        if not self.is_bound:
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
        
        # If accessing via token, remove current password requirement
        if via_token:
            del self.fields['current_password']
    
    def clean_current_password(self):
        """Verify the current password is correct (only if not via token)"""
        if self.via_token:
            return None
            
        current_password = self.cleaned_data.get('current_password')
        
        if not current_password:
            raise ValidationError('Current password is required.')
        
        if not self.user.check_password(current_password):
            raise ValidationError('Current password is incorrect. Please try again.')
        
        return current_password
    
    def clean_email(self):
        """Validate email is unique (except for current user)"""
        email = self.cleaned_data.get('email')
        
        # Check if email is already taken by another user
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError('This email address is already in use.')
        
        return email
    
    def clean_username(self):
        """Validate username is unique (except for current user)"""
        username = self.cleaned_data.get('username')
        
        # Check if username is already taken by another user
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('This username is already taken.')
        
        # Validate username format
        if not username.replace('_', '').replace('-', '').replace('.', '').replace('@', '').replace('+', '').isalnum():
            raise ValidationError('Username can only contain letters, numbers and @/./+/-/_ characters.')
        
        return username
    
    def clean(self):
        """Validate password fields match and meet requirements"""
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # If new password is provided, validate it
        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError({
                    'confirm_password': 'The two password fields didn\'t match.'
                })
            
            # Validate password strength using Django's validators
            if new_password:
                try:
                    validate_password(new_password, self.user)
                except ValidationError as e:
                    raise ValidationError({'new_password': e})
        
        return cleaned_data
    
    def save(self):
        """Update user credentials securely"""
        # Update email and username
        self.user.email = self.cleaned_data['email']
        self.user.username = self.cleaned_data['username']
        
        # Update password if provided
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            self.user.set_password(new_password)  # Automatically hashes the password
        
        self.user.save()
        return self.user
