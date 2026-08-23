from django.conf import settings

def cbe_settings(request):
    boa_acc = getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775')
    boa_name = getattr(settings, 'BOA_ACCOUNT_NAME', 'Sol Merchant Account')
    boa_bank = getattr(settings, 'BOA_BANK_NAME', 'Bank of Abyssinia')
    return {
        'BOA_ACCOUNT_NUMBER': boa_acc,
        'BOA_ACCOUNT_NAME': boa_name,
        'BOA_BANK_NAME': boa_bank,
        'CBE_ACCOUNT_NUMBER': boa_acc,
        'CBE_ACCOUNT_NAME': boa_name,
        'CBE_BANK_NAME': boa_bank,
    }

