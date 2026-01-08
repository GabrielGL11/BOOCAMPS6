from django.apps import AppConfig
import os

class PaginaUsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagina_usuario'

    def ready(self):
        if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
            try:
                from django.contrib.auth.models import User

                if not User.objects.filter(username="GabrielGL").exists():
                    User.objects.create_superuser(
                        username="GabrielGL",
                        email="gabrielguaman1105@gmail.com",
                        password="aGGl1105."
                    )
                    print("Superusuario creado automáticamente en Render")
            except Exception as e:
                print("Error creando superusuario:", e)
