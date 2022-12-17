from django.apps import AppConfig


class PsgPharmacyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'psg_pharmacy'
    
    def ready(self):
        from psg_pharmacy.jobs import updater
        updater.start()