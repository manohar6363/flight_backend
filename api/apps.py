from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.contrib.sites.models import Site
        try:
            if not Site.objects.exists():
                Site.objects.create(id=1, domain="localhost:8000", name="localhost")
            else:
                site = Site.objects.get_current()
                site.domain = "localhost:8000"
                site.name = "localhost"
                site.save()
        except Exception:
            # Ignore errors during migration phase
            pass