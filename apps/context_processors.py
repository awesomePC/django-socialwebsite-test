from django.conf import settings
# from .authentication.models import User

def cfg_assets_root(request):

    return { 'ASSETS_ROOT' : settings.ASSETS_ROOT }


