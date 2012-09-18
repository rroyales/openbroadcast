import re, datetime, os
from dateutil import relativedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django_countries import CountryField

import tagging
import arating

from lib.fields import extra

from django_extensions.db.fields import AutoSlugField, UUIDField

from phonenumber_field.modelfields import PhoneNumberField

def filename_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    path = "profiles/"
    
    # splitted
    filename = instance.uuid.replace('-', '/') + extension
    
    return os.path.join(path, filename)


class Profile(models.Model):
    """Profile model"""
    GENDER_CHOICES = (
        (0, _('Male')),
        (1, _('Female')),
        (2, _('Other')),
    )
    user = models.ForeignKey(User, unique=True)
    
    #
    uuid = UUIDField()
    
    #Personal
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    
    # Profile
    description = extra.MarkdownTextField(blank=True, null=True)
    image = models.ImageField(verbose_name=_('Profile Image'), upload_to=filename_by_uuid, null=True, blank=True)
    
    # hm...
    # mugshot = models.FileField(_('mugshot'), upload_to='mugshots', null=True, blank=True)
    
    # Contact
    mobile = PhoneNumberField(_('mobile'), blank=True, null=True)
    phone = PhoneNumberField(_('phone'), blank=True, null=True)
    fax = PhoneNumberField(_('fax'), blank=True, null=True)
    
    address1 = models.CharField(_('address'), null=True, blank=True, max_length=100)
    address2 = models.CharField(_('address (secondary)'), null=True, blank=True, max_length=100)
    # state = models.CharField(_('state'), null=True, blank=True, max_length=100)
    city = models.CharField(_('city'), null=True, blank=True, max_length=100)
    zip = models.CharField(_('zip'), null=True, blank=True, max_length=10)
    #country = models.CharField(_('country'), null=True, blank=True, max_length=100)
    country = CountryField(blank=True, null=True)
    
    
    iban = models.CharField(_('IBAN'), null=True, blank=True, max_length=100)
    paypal = models.EmailField(_('Paypal'), null=True, blank=True, max_length=200)
    
    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(verbose_name="Tags", blank=True, null=True)

    class Meta:
        app_label = 'profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        db_table = 'user_profiles'

    def __unicode__(self):
        return u"%s" % self.user.get_full_name()

    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.birth_date:
            return u"%s" % relativedelta.relativedelta(TODAY, self.birth_date).years
        else:
            return None

    @permalink
    def get_absolute_url(self):
        return ('profiles-profile-detail', None, { 'slug': self.user.username })

    @property
    def sms_address(self):
        if (self.mobile and self.mobile_provider):
            return u"%s@%s" % (re.sub('-', '', self.mobile), self.mobile_provider.domain)
        

    def save(self, *args, **kwargs):
        t_tags = ''
        """
        for tag in self.tags:
            t_tags += '%s, ' % tag    
        
        self.tags = t_tags;
        self.d_tags = t_tags;
        """
        super(Profile, self).save(*args, **kwargs)

try:
    tagging.register(Profile)
except:
    pass

arating.enable_voting_on(Profile)


def create_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = Profile.objects.get_or_create(user=instance)  

post_save.connect(create_profile, sender=User) 

class MobileProvider(models.Model):
    """MobileProvider model"""
    title = models.CharField(_('title'), max_length=25)
    domain = models.CharField(_('domain'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('mobile provider')
        verbose_name_plural = _('mobile providers')
        db_table = 'user_mobile_providers'

    def __unicode__(self):
        return u"%s" % self.title


class ServiceType(models.Model):
    """Service type model"""
    title = models.CharField(_('title'), blank=True, max_length=100)
    url = models.URLField(_('url'), blank=True, help_text='URL with a single \'{user}\' placeholder to turn a username into a service URL.', verify_exists=False)

    class Meta:
        verbose_name = _('service type')
        verbose_name_plural = _('service types')
        db_table = 'user_service_types'

    def __unicode__(self):
        return u"%s" % self.title


class Service(models.Model):
    """Service model"""
    service = models.ForeignKey(ServiceType)
    profile = models.ForeignKey(Profile)
    username = models.CharField(_('Userame / ID'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        db_table = 'user_services'

    def __unicode__(self):
        return u"%s" % self.username

    @property
    def service_url(self):
        return re.sub('{user}', self.username, self.service.url)

    @property
    def title(self):
        return u"%s" % self.service.title


class Link(models.Model):
    """Service type model"""
    profile = models.ForeignKey(Profile)
    title = models.CharField(_('title'), max_length=100, null=True, blank=True)
    url = models.URLField(_('url'), verify_exists=True)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        db_table = 'user_links'

    def __unicode__(self):
        return u"%s" % self.title