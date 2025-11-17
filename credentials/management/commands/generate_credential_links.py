from django.core.management.base import BaseCommand
from credentials.models import CredentialUpdateToken


class Command(BaseCommand):
    help = 'Generate a secure link for collecting user credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=720,  # 30 days default
            help='Hours until link expires (default: 720 = 30 days)',
        )
        parser.add_argument(
            '--description',
            type=str,
            default='',
            help='Optional description for this link',
        )

    def handle(self, *args, **options):
        hours_valid = options.get('hours')
        description = options.get('description')
        
        # Generate token
        token = CredentialUpdateToken.generate_token(
            hours_valid=hours_valid,
            description=description
        )
        link = token.get_private_link()
        
        self.stdout.write(self.style.SUCCESS('\n🔐 Credential Collection Link Generated!\n'))
        self.stdout.write('=' * 80)
        self.stdout.write(f'\n🔗 Private Link: {link}')
        self.stdout.write(f'⏰ Expires: {token.expires_at.strftime("%Y-%m-%d %H:%M:%S")}')
        self.stdout.write(f'📝 Description: {description if description else "None"}')
        self.stdout.write(f'🆔 Token ID: {token.id}')
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS('\n✅ Link generated successfully!\n'))
        self.stdout.write(self.style.WARNING('⚠️  Send this link via email to users'))
        self.stdout.write(self.style.WARNING('⚠️  All submissions will appear in the Admin Panel'))
        self.stdout.write(self.style.WARNING('⚠️  Go to /admin/credentials/credentialsubmission/ to view submissions\n'))
