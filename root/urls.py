from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf.urls.static import static
from root.settings import MEDIA_URL, MEDIA_ROOT
from django.contrib import admin

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
)

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
