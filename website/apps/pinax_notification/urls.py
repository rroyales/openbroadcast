from django.conf.urls.defaults import patterns, url

from notification.views import notice_settings


urlpatterns = patterns("",
    url(r"^settings/$", notice_settings, name="notification_notice_settings"),
)
