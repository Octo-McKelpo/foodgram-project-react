import debug_toolbar
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path

handler404 = "foodgram.views.page_not_found"  # noqa
handler500 = "foodgram.views.server_error"  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("users.urls")),
    path("api/", include("api.urls"))
]

urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
]
