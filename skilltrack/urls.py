from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from app.views import SkillsTest, Auth, IdentifyUser

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'auth/$', Auth.as_view()),
    url(r'auth/identify/$', IdentifyUser.as_view()),
    url(r'skills/$', login_required(SkillsTest.as_view()))
]
