from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Адміністративна панель"
    site_title = "Адмін Groups та Users"
    index_title = "Управління даними"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Сортуємо так, щоб Groups були першими
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'] != 'Groups')  # Groups у пріоритеті
        return app_list

custom_admin_site = CustomAdminSite(name='custom_admin')
