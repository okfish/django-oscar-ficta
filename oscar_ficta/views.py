from django.contrib import messages
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.views import generic

from oscar.core.loading import get_classes, get_class, get_model
from oscar.core.compat import get_user_model
from oscar.views import sort_queryset
from oscar.views.generic import ObjectLookupView

User = get_user_model()
Person = get_model('oscar_ficta', 'Person')

(
    PersonForm, PersonSelectForm, LegalAddressForm
) = get_classes(
    'oscar_ficta.forms',
    ['PersonForm', 'PersonSelectForm', 'LegalAddressForm',])

CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')

class PersonSelectView(generic.View):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'oscar_ficta/partials/person_select.html'
    context_object_name = 'persons'
    create_form_class = PersonForm
    select_form_class = PersonSelectForm
    success_url = reverse_lazy('checkout:shipping-address')
    
    def get_default_person(self):
        # Get previously saved person data
        # smth via CheckoutSessionData
        return False
    
        
    def get_queryset(self):
        qs = self.model.browsable().filter(users__contains=self.user)
        qs = sort_queryset(qs, self.request, ['name'])

        self.description = _("Available persons")

#         # We track whether the queryset is filtered to determine whether we
#         # show the search form 'reset' button.
#         self.is_filtered = False
#         self.form = self.form_class(self.request.GET)
#         if not self.form.is_valid():
#             return qs
# 
#         data = self.form.cleaned_data
# 
#         if data['name']:
#             qs = qs.filter(name__icontains=data['name'])
#             self.description = _("Partners matching '%s'") % data['name']
#             self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        #ctx = super(PersonSelectView, self).get_context_data(**kwargs)
        ctx = {}
        default_person = self.get_default_person()
        ctx['default_person'] = default_person
        ctx['select_form'] = self.select_form_class(for_user=self.user, 
                                               default_person=default_person)
        ctx['create_form'] = self.create_form_class()
        return ctx

#     def form_valid(self, form):
#         messages.success(
#             self.request, _("Juristic person '%s' was updated successfully.") %
#             self.person.name)
#         self.person.name = form.cleaned_data['name']
#         self.person.save()
#         return super(PersonSelectView, self).form_valid(form)
    
    def get(self, request, **kwargs):

        self.request = request
        self.user = request.user
        ctx = self.get_context_data(**kwargs)
#         ctx['basket'] = request.basket

        return render(request, 
                      self.template_name, 
                      ctx, content_type="text/html" )
         
class PersonLookupView(ObjectLookupView):
    model = Person

    def get_queryset(self):
        return self.model.browsable.all()

    def lookup_filter(self, qs, term):
        return qs.filter(Q(title__icontains=term)
                         | Q(parent__title__icontains=term))

class PersonDetailView(generic.DetailView):
     pass

class PersonGroupView(generic.TemplateView):
     pass