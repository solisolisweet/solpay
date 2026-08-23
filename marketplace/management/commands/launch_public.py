import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Launches a 100% free instant public URL tunnel for your Django monetization store'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Launching instant free public URL for your store...'))
        self.stdout.write(self.style.WARNING('Share the generated link with buyers on Telegram/WhatsApp! Payments clear to Bank of Abyssinia Account 96072775.'))
        self.stdout.write(self.style.WARNING('Host header forwarding enabled: USE_X_FORWARDED_HOST = True'))
        try:
            subprocess.run(['npx', 'localtunnel', '--port', '8000'], check=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Could not launch localtunnel automatically. Run command manually: npx localtunnel --port 8000'))

