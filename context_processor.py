import os, json
from django.conf import settings

menu_file_path = os.path.join(settings.BASE_DIR, 'menu/menu.json')


def default_context_data(request):
    menu_file = open(menu_file_path)
    data = json.load(menu_file)
    menu_file.close()
    return {
        "menu": data
    }

