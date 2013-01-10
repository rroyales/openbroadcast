from django.conf.urls.defaults import *

# app imports
from alibrary.models import Media
from alibrary.views import *

urlpatterns = patterns('',
    
    # url(r'^autocomplete/$', media_autocomplete, name='alibrary-media-edit'),
      
    url(r'^$', MediaListView.as_view(), name='alibrary-media-list'),
    url(r'^(?P<slug>[-\w]+)/$', MediaDetailView.as_view(), name='alibrary-media-detail'),
    #url(r'^(?P<pk>\d+)/edit/$', MediaEditView.as_view(), name='alibrary-media-edit'),

)