from django import forms
from django.conf import settings

from django.forms import ModelForm, Form

from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.contrib.contenttypes.generic import BaseGenericInlineFormSet, generic_inlineformset_factory


from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import FormActions

from filer.models.imagemodels import Image

from django.contrib.admin import widgets as admin_widgets


from alibrary.models import Release, Media, Relation

from pagedown.widgets import PagedownWidget

import selectable.forms as selectable
from alibrary.lookups import *


import floppyforms as forms
from django_date_extensions.fields import ApproximateDateFormField

from ajax_select.fields import AutoCompleteSelectField
from ajax_select import make_ajax_field

    
from django.forms.widgets import FileInput, HiddenInput

#from floppyforms.widgets import DateInput
from tagging.forms import TagField
from ac_tagging.widgets import TagAutocompleteTagIt

from lib.widgets.widgets import ReadOnlyIconField



ACTION_LAYOUT =  action_layout = FormActions(
                HTML('<button type="submit" name="save" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-save icon-white"></i> Save</button>'),            
                HTML('<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-secondary pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'),
        )
ACTION_LAYOUT_EXTENDED =  action_layout = FormActions(
                Field('publish', css_class='input-hidden' ),
                HTML('<button type="submit" name="save" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-save icon-white"></i> Save</button>'),            
                HTML('<button type="submit" name="save-and-publish" value="save" class="btn pull-right ajax_submit save-and-publish" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-bullhorn icon-white"></i> Save & Publish</button>'),            
                HTML('<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-secondary pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'),
        )


class LabelActionForm(Form):
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', False)        
        super(LabelActionForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        
        
        self.helper.add_layout(ACTION_LAYOUT)
        """
        if self.instance and self.instance.publish_date:
            self.helper.add_layout(ACTION_LAYOUT)
        else:
            self.helper.add_layout(ACTION_LAYOUT_EXTENDED)
        """    
    publish = forms.BooleanField(required=False)


class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = ('name',
                  'type',
                  'labelcode',
                  'description',
                  'address',
                  'country',
                  'phone',
                  'fax',
                  'email',
                  'main_image',
                  'd_tags')
        

    def __init__(self, *args, **kwargs):

        self.user = kwargs['initial']['user']
        self.instance = kwargs['instance']
        
        print self.instance
        
        print self.user.has_perm("alibrary.edit_release")
        print self.user.has_perm("alibrary.admin_release", self.instance)

        
        self.label = kwargs.pop('label', None)
        

        super(LabelForm, self).__init__(*args, **kwargs)
        
        """
        Prototype function, set some fields to readonly depending on permissions
        """
        """
        if not self.user.has_perm("alibrary.admin_release", self.instance):
            self.fields['catalognumber'].widget.attrs['readonly'] = 'readonly'
        """

        self.helper = FormHelper()
        self.helper.form_id = "id_feedback_form_%s" % 'asd'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False
        
        
        base_layout = Fieldset(
                               
                _('General'),
                LookupField('name', css_class='input-xlarge'),
                LookupField('type', css_class='input-xlarge'),
                LookupField('labelcode', css_class='input-xlarge'),
        )
        
        contact_layout = Fieldset(
                _('Contact'),
                LookupField('address', css_class='input-xlarge'),
                LookupField('country', css_class='input-xlarge'),
                LookupField('phone', css_class='input-xlarge'),
                LookupField('fax', css_class='input-xlarge'),
                LookupField('email', css_class='input-xlarge'),
        )
        
        meta_layout = Fieldset(
                'Meta',
                LookupField('description', css_class='input-xxlarge'),
                'main_image',
        )
        
        tagging_layout = Fieldset(
                'Tags',
                'd_tags',
        )
            
        layout = Layout(
                        base_layout,
                        contact_layout,
                        meta_layout,
                        tagging_layout,
                        )

        self.helper.add_layout(layout)

        

    
    main_image = forms.Field(widget=FileInput(), required=False)
    d_tags = TagField(widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_('Tags'))
    description = forms.CharField(widget=PagedownWidget(), required=False, help_text="Markdown enabled text")   

    

    def clean(self, *args, **kwargs):
        
        cd = super(LabelForm, self).clean()

        print "*************************************"
        print cd
        print "*************************************"
        
            
        
        if 'main_image' in cd and cd['main_image'] != None:
            try:
                ui = cd['main_image']
                dj_file = DjangoFile(open(ui.temporary_file_path()), name='cover.jpg')
                cd['main_image'], created = Image.objects.get_or_create(
                                    original_filename='cover_%s.jpg' % self.instance.pk,
                                    file=dj_file,
                                    folder=self.instance.folder,
                                    is_public=True)
            except Exception, e:
                print e
                pass
            
        else:
            cd['main_image'] = self.instance.main_image


        return cd

    # TODO: take a look at save
    def save(self, *args, **kwargs):
        return super(LabelForm, self).save(*args, **kwargs)
   
    
    


  
class BaseLabelReleationFormSet(BaseGenericInlineFormSet):

        
        
    def __init__(self, *args, **kwargs):

        self.instance = kwargs['instance']
        super(BaseLabelReleationFormSet, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id_releasemediainline_form_%s" % 'asdfds'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False
        
        base_layout = Row(
                Column(
                       Field('url', css_class='input-xlarge'),
                       css_class='span5'
                       ),
                Column(
                       Field('service', css_class='input-small'),
                       css_class='span1'
                       ),
                Column(
                       Field('DELETE', css_class='input-mini'),
                       css_class='span1'
                       ),
                css_class='row relation-row',
        )
 
        self.helper.add_layout(base_layout)
        


class BaseLabelReleationForm(ModelForm):

    class Meta:
        model = Relation
        parent_model = Label
        formset = BaseLabelReleationFormSet
        fields = ('url','service',)
        
    def __init__(self, *args, **kwargs):
        super(BaseLabelReleationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['service'].widget.attrs['readonly'] = True
        
    def clean_service(self):
        return self.instance.service

    service = forms.CharField(label='', widget=ReadOnlyIconField(), required=False)
    url = forms.URLField(label=_('Website / URL'), required=False)



# Compose Formsets
LabelRelationFormSet = generic_inlineformset_factory(Relation, form=BaseLabelReleationForm, formset=BaseLabelReleationFormSet, extra=3, exclude=('action',), can_delete=True)






    