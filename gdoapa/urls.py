from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'gdoapa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^accounts/login/$', auth_views.login, name='login'),
	url(r'^accounts/logout/$', auth_views.logout_then_login, name='logout_then_login'),
	url(r'^accounts/pwchange/$', auth_views.password_change, {'post_change_redirect': '/gestione_ordini/'}, name='pwchange'),
    url(r'^gestione_ordini/', include('gestione_ordini.urls', namespace="gestione_ordini")),
    url(r'^admin/', include(admin.site.urls)),
		
	# ex: /media/filename.ext (serve a user uploaded file)
	url(r'^media/(?P<path>.*)$', login_required(serve), 
		{'document_root': settings.MEDIA_ROOT,}, name='servefile'),
]
