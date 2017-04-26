from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from geonode.urls import *

urlpatterns = patterns('',
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
 ) + urlpatterns

urlpatterns += patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^logout/$',
      'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'
    ),

)
    

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
