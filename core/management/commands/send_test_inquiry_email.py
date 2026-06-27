from types import SimpleNamespace

from django.core.management.base import BaseCommand, CommandError

from core.views import send_contract_notification


class Command(BaseCommand):
    help = 'Send a test contact inquiry notification email using the current email settings.'

    def handle(self, *args, **options):
        contract = SimpleNamespace(
            id='test',
            name='Test Buyer',
            email='buyer@example.com',
            country='United States',
            interested_products='Pino Feeder Set',
            message='This is a test inquiry email from the Django management command.',
            contact_name='Test Buyer',
            company_brand='PawNest SMTP Test',
            project_type='Website inquiry',
            estimated_quantity='1 sample',
            delivery_city='Los Angeles',
            budget_range='$100 - $300',
            requirement='This is a test inquiry email from the Django management command.',
            phone='+1 555 000 0000',
        )

        try:
            sent = send_contract_notification(contract)
        except Exception as exc:
            raise CommandError(f'Failed to send test inquiry email: {exc}') from exc

        if not sent:
            raise CommandError('Test email was not sent. Check CONTRACT_NOTIFICATION_EMAIL.')

        self.stdout.write(self.style.SUCCESS('Test inquiry email sent successfully.'))
