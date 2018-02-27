from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.documentation import include_docs_urls
from app.views import Skills, TimeEntries, Auth, IdentifyUser
import debug_toolbar

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='Skills API')),
    url(r'auth/$', Auth.as_view()),
    url(r'auth/identify/$', IdentifyUser.as_view()),
    path(r'entries/', login_required(TimeEntries.as_view())),
    path(r'skills/', login_required(Skills.as_view())),    
    path(r'skills/<int:skill_id>', login_required(Skills.as_view())),
    url(r'^__debug__/', include(debug_toolbar.urls))
]
