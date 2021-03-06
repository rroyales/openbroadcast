from selectable.base import ModelLookup
from selectable.registry import registry
from django.utils.safestring import mark_safe
from alibrary.models import *


class ReleaseNameLookup(ModelLookup):
    model = Release
    search_fields = ['name__icontains',]
    
    def get_item_label(self, item):
        return u"%s, %s" % (item.name, item.catalognumber)
    
registry.register(ReleaseNameLookup)

""""""
class ReleaseLabelLookup(ModelLookup):
    model = Label
    search_fields = ['name__icontains',]

    #def get_item_value(self, item):
        # Display for currently selected item
        #return item.name

    def get_item_label(self, item):
        # Display for choice listings
        return u"%s (%s)" % (item.name, item.pk)

    #def get_item_id(self, item):
        #return u"%s" % item.name
    
    
    
registry.register(ReleaseLabelLookup)

""""""
class ArtistLookup(ModelLookup):
    model = Artist
    search_fields = ['name__icontains',]

    #def get_item_value(self, item):
        # Display for currently selected item
        #return item.name

    def get_item_label(self, item):
        # Display for choice listings
        return u"%s (%s)" % (item.name, item.pk)

    #def get_item_id(self, item):
        #return u"%s" % item.name
    
    
    
registry.register(ArtistLookup)


class LabelLookup(ModelLookup):
    model = Label
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        return u"%s (%s)" % (item.name, item.pk)    
    
registry.register(LabelLookup)


class LicenseLookup(ModelLookup):
    model = License
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        return mark_safe(u'%s (%s) <span class="%s">%s</span>' % (item.name, item.restricted, item.key, item.key))
    
    
registry.register(LicenseLookup)
