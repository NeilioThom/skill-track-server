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
    path(r'admin/', admin.site.urls),
    path(r'docs/', include_docs_urls(title='Skills API')),
    path(r'auth/', Auth.as_view()),
    path(r'auth/identify/', IdentifyUser.as_view()),
    path(r'entries/', login_required(TimeEntries.as_view())),
    path(r'skills/', login_required(Skills.as_view())),    
    path(r'skills/<uuid:skill_id>/', login_required(Skills.as_view())),
    path(r'__debug__/', include(debug_toolbar.urls))
]
