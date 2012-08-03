#
import django_filters

from alibrary.models import Release

from django.utils.datastructures import SortedDict
ORDER_BY_FIELD = 'o'

from django.db import models

class CharListFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        if isinstance(value, (list, tuple)):
            lookup = str(value[1])
            if not lookup:
                lookup = 'exact'
            value = value[0]
        else:
            values = value.split(',')
            lookup = self.lookup_type
            
        if value and values:
            
            if len(values) > 1:
                lookup = 'in'
                return qs.filter(**{'%s__%s' % (self.name, lookup): values})
                
            else:
                return qs.filter(**{'%s__%s' % (self.name, lookup): value})
        
        return qs


class ReleaseFilter(django_filters.FilterSet):

    # releasedate = django_filters.DateFilter()
    releasetype = CharListFilter(label="Release type")
    release_country = CharListFilter(label="Country")
    media_release__license__name = CharListFilter(label="License")
    main_format__name = CharListFilter(label="Release Format")
    class Meta:
        model = Release
        fields = ['releasetype', 'release_country', 'main_format__name', 'media_release__license__name',]
    
    @property
    def filterlist(self):

        flist = []
        
        if not hasattr(self, '_filterlist'):
            
            """
            fields = SortedDict([(name, filter_.label) for name, filter_ in self.filters.iteritems()])
            fields[ORDER_BY_FIELD] = self.ordering_field
            """
            
            print "QS"
            print self.queryset
            
            for name, filter_ in self.filters.iteritems():

                    
                #ds = Release.objects.values_list(name, flat=True).distinct()
                ds = self.queryset.values_list(name, flat=False).annotate(n=models.Count("pk")).distinct()
                
                print ds
                
                filter_.ds = ds
                
                if ds not in flist:
                    
                    flist.append(filter_)

            
            self._filterlist = flist
        
        return self._filterlist
    