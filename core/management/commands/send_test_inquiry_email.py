from types import SimpleNamespace

from django.core.management.base import BaseCommand, CommandError

from core.views import send_contract_notification


class Command(BaseCommand):
    help = 'Send a test contact inquiry notification email using the current email settings.'

    def handle(self, *args, **options):
        contract = SimpleNamespace(
            id='test',
            contact_name='Test Buyer',
            phone='+1 555 000 0000',
            company_brand='PawNest SMTP Test',
            project_type='Pet supplies sourcing',
            estimated_quantity='500 pcs',
            delivery_city='Los Angeles',
            budget_range='$1,000 - $3,000',
            requirement='This is a test inquiry email from the Django management command.',
        )

        try:
            sent = send_contract_notification(contract)
        except Exception as exc:
            raise CommandError(f'Failed to send test inquiry email: {exc}') from exc

        if not sent:
            raise CommandError('Test email was not sent. Check CONTRACT_NOTIFICATION_EMAIL.')

        self.stdout.write(self.style.SUCCESS('Test inquiry email sent successfully.'))
