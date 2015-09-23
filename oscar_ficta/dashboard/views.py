import datetime
import logging
from decimal import Decimal as D

from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django import http
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum, Q
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict
from django.conf import settings

from django_tables2 import SingleTableMixin

from extra_views import (CreateWithInlinesView, UpdateWithInlinesView,
                         InlineFormSet)

from oscar.core.loading import get_classes, get_model, get_class
from oscar.templatetags.currency_filters import currency
from oscar.core.utils import format_datetime, datetime_combine
from oscar.core.compat import UnicodeCSVWriter
from oscar.views import sort_queryset
from oscar.views.generic import BulkEditMixin



# from accounts.dashboard import forms, reports
# from accounts import facade, names, exceptions

PersonGroup = get_model('oscar_ficta', 'PersonGroup')
Person = get_model('oscar_ficta', 'Person')
LegalAddress = get_model('oscar_ficta', 'LegalAddress')
BankAccount = get_model('oscar_ficta', 'BankAccount')
Bank = get_model('oscar_ficta', 'Bank')

Invoice = get_model('invoice', 'Invoice')
Partner = get_model('partner', 'Partner')

PersonSearchForm = get_class('oscar_ficta.dashboard.forms', 'PersonSearchForm')
NewPersonForm = get_class('oscar_ficta.dashboard.forms', 'NewPersonForm')
UpdatePersonForm = get_class('oscar_ficta.dashboard.forms', 'UpdatePersonForm')
FreezePersonForm = get_class('oscar_ficta.dashboard.forms', 'FreezePersonForm')
EnablePersonForm = get_class('oscar_ficta.dashboard.forms', 'EnablePersonForm')
InvoiceSearchForm = get_class('oscar_ficta.dashboard.forms', 'InvoiceSearchForm')
BankAccountFormSet = get_class('oscar_ficta.dashboard.forms', 'BankAccountFormSet')
BankAccountForm = get_class('oscar_ficta.dashboard.forms', 'BankAccountForm')
BankForm = get_class('oscar_ficta.dashboard.forms', 'BankForm')
LegalAddressFormSet = get_class('oscar_ficta.dashboard.forms', 'LegalAddressFormSet')

GroupForm = get_class('oscar_ficta.dashboard.forms', 'GroupForm')
GroupTable = get_class('oscar_ficta.dashboard.tables', 'GroupTable')
#Transfer = get_model('accounts', 'Transfer')
#Transaction = get_model('accounts', 'Transaction')

logger = logging.getLogger('oscar_ficta.invoice')

def queryset_invoices_for_user(user):
    """
    Returns a queryset of all invoices that a user is allowed to access.
    A staff user may access all orders.
    To allow access to an invoice for a non-staff user, invoice's
    partner_person has to have the user in the user's list.
    """
    queryset = Invoice._default_manager.select_related(
        'partner_person__partner', 'person', 'user', 'order')
    if user.is_staff:
        return queryset
    else:
        partners = Partner._default_manager.filter(users=user)
        return queryset.filter(partner_person__partner__in=partners).distinct()

def get_invoice_for_user_or_404(user, number):
    try:
        return queryset_invoices_for_user(user).get(number=number)
    except ObjectDoesNotExist:
        raise Http404()

class PersonListView(generic.ListView):
    model = Person
    context_object_name = 'persons'
    template_name = 'oscar_ficta/dashboard/persons_list.html'
    form_class = PersonSearchForm
    description = _("All juristic persons")

    def get_context_data(self, **kwargs):
        ctx = super(PersonListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['title'] = _("Juristic persons")
        ctx['queryset_description'] = self.description
        return ctx

    def get_queryset(self):
        queryset = Person.objects.all()

        if 'vatin' not in self.request.GET:
            # Form not submitted
            self.form = self.form_class()
            return queryset

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            # Form submitted but invalid
            return queryset

        # Form valid - build queryset and description
        data = self.form.cleaned_data
        desc_template = _(
            "%(status)s %(vatin_filter)s %(name_filter)s")
        desc_ctx = {
            'status': "All",
            'vatin_filter': "",
            'name_filter': "",
        }
        if data['name']:
            queryset = queryset.filter(name__icontains=data['name'])
            desc_ctx['name_filter'] = _(
                " with name matching '%s'") % data['name']
        if data['vatin']:
            queryset = queryset.filter(vatin=data['vatin'])
            desc_ctx['vatin_filter'] = _(
                " with VATIN '%s'") % data['code']
        if data['status']:
            queryset = queryset.filter(status=data['status'])
            desc_ctx['status'] = data['status']

        self.description = desc_template % desc_ctx

        return queryset
    

class PersonCreateView(generic.CreateView):
    model = Person
    context_object_name = 'person'
    template_name = 'oscar_ficta/dashboard/person_form.html'
    form_class = NewPersonForm

    def get_context_data(self, **kwargs):
        ctx = super(PersonCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Create a new Juristic Person") 
        return ctx
    
    def get_success_url(self):
        messages.success(self.request,
                         _("Juristic person '%s' was created successfully.") %
                         self.object.name)
        return reverse('oscar_ficta_dashboard:persons-detail', kwargs={'pk':self.object.id})

# class LegalAddressInline(InlineFormSet):
#     extra = 1
#     max_num = 1
#     can_delete = False
#     model = LegalAddress
#     form_class = LegalAddressForm
# 
# class BankAccountInline(InlineFormSet):
#     extra = 1
#     max_num = 1
#     can_delete = False
#     model = BankAccount
#     form_class = BankAccountForm
# 
# class BankInline(InlineFormSet):
#     extra = 1
#     max_num = 1
#     can_delete = False
#     model = Bank
#     form_class = BankForm

    
class PersonUpdateView(generic.UpdateView):
    model = Person
    context_object_name = 'person'
    template_name = 'oscar_ficta/dashboard/person_update_form.html'
    form_class = UpdatePersonForm
    
    success_url = reverse_lazy('oscar_ficta_dashboard:persons-list')
        
    bank_form = BankForm
    account_formset = BankAccountFormSet
    address_formset = LegalAddressFormSet
    
    # next some methods stolen from oscar.apps.dashboard.catalogue.views
    # thanks for good ideas :)
   
    def __init__(self, *args, **kwargs):
        super(PersonUpdateView, self).__init__(*args, **kwargs)
        self.formsets = {'bank_form': self.bank_form,
                         'account_formset': self.account_formset,
                         'address_formset': self.address_formset}

    
    def get_context_data(self, **kwargs):
        accounts = address = None
        ctx = super(PersonUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Update '%s'") % self.object.name
        if self.object.bank_accounts.all().count() > 0:
            accounts = ctx['accounts'] = self.object.bank_accounts.all()
        if self.object.users.all().count() > 0:
            ctx['users'] = self.object.users.all()
        if self.object.person_invoices.all().count() > 0:
            ctx['invoices'] = self.object.person_invoices.all()
        
        for ctx_name, formset_class in self.formsets.items():
            form_kwargs = {}
            if ctx_name not in ctx:
                form_kwargs['prefix'] = ctx_name
                # workaround to pass instance args for bank form
                if ctx_name != 'bank_form':
                    form_kwargs['instance']=self.object
                ctx[ctx_name] = formset_class(**form_kwargs)

        return ctx
    

    
    
    def process_all_forms(self, form):
        """
        Short-circuits the regular logic to have one place to have our
        logic to check all forms
        """
        # Need to create the person here because the inline forms need it
        # can't use commit=False because UpdatePersonForm does not support it
        if form.is_valid():
            self.object = form.save()

        formsets = {}
        is_valid = []
        for ctx_name, formset_class in self.formsets.items():
            form_kwargs = {'prefix':ctx_name}
            if ctx_name != 'bank_form':
                    form_kwargs['instance']=self.object
            formsets[ctx_name] = formset_class(self.request.POST,
                                               **form_kwargs)

        # here we need to do some tricks as forms 
        # for address and account can be empty
        
        is_valid.append(form.is_valid())
        
        if not formsets['address_formset'].is_valid():
            is_valid.append(False)
        
        # trying to create or get bank instance anyway
        new_bank = None
        if formsets['bank_form'].has_changed() and formsets['bank_form'].is_valid():
            is_valid.append(True)
            new_bank_kwargs = formsets['bank_form'].cleaned_data
            new_bic = new_bank_kwargs.pop('bic')
            logger.debug("Found valid bank form")
            try:
                new_bank, created = Bank.objects.get_or_create(bic=new_bic, 
                                                           defaults=new_bank_kwargs)
            except Bank.MultipleObjectsReturned:
                msg = _('Strange! Too many banks for this BIC %(bic)s') % {'bic' : new_bic}
                logger.error(msg)
                messages.error(self.request, msg)
                
            if created:
                msg = _('New bank %(bank)s for person %(person)s saved') % {'bank' : new_bank,
                                                                   'person': self.object}
                messages.success(self.request, msg)
                logger.info(msg)
            elif getattr(new_bank, 'pk', None) is None:
                msg = _('Cant create new bank record for %(person)s') % {'person': self.object}
                messages.success(self.request, msg)
                logger.error(msg)
                is_valid.append(False)
        bank_id = getattr(new_bank, 'pk', None) 
    
        # if user added only the settlement account number and has not bank selected 
        # (or no bank in the db saved yet, e.g. dropdown list is empty)
        # assumes new bank should be created from the bank form
        for acc_form in formsets['account_formset'].forms:
            # check for the empty bank field and assign new one if available
            if getattr(acc_form.instance, 'bank', None) is None and bank_id:
                acc_form.set_bank(bank_id)
            if not acc_form.is_valid():
                is_valid.append(False)
    
        cross_form_validation_result = self.clean(form, formsets)
        if all(is_valid) and cross_form_validation_result:
            return self.forms_valid(form, formsets)
        else:
            return self.forms_invalid(form, formsets)

    # form_valid and form_invalid are called depending on the validation result
    # of just the person form and redisplay the form respectively return a
    # redirect to the success URL. In both cases we need to check our formsets
    # as well, so both methods do the same. process_all_forms then calls
    # forms_valid or forms_invalid respectively, which do the redisplay or
    # redirect.
    form_valid = form_invalid = process_all_forms

    def clean(self, form, formsets):
        """
        Perform any cross-form/formset validation. If there are errors, attach
        errors to a form or a form field so that they are displayed to the user
        and return False. If everything is valid, return True. This method will
        be called regardless of whether the individual forms are valid.
        """
        return True

    def forms_valid(self, form, formsets):
        """
        Save all changes and display a success url.
        Excluding bank form as it was saved on the previous step
        """
        self.object = form.save()

        # Save formsets except bank_form
        for ctx_name, formset in formsets.items():
            if ctx_name != 'bank_form':
                formset.save()

        return http.HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formsets):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        ctx = self.get_context_data(form=form, **formsets)
        return self.render_to_response(ctx)


class PersonFreezeView(generic.UpdateView):
    model = Person
    template_name = 'oscar_ficta/dashboard/person_freeze.html'
    form_class = FreezePersonForm

    def get_success_url(self):
        messages.success(self.request, _("Juristic Person frozen"))
        return reverse('oscar_ficta_dashboard:persons-list')


class PersonEnableView(generic.UpdateView):
    model = Person
    template_name = 'oscar_ficta/dashboard/person_enable.html'
    form_class = EnablePersonForm

    def get_success_url(self):
        messages.success(self.request, _("Juristic Person now active"))
        return reverse('oscar_ficta_dashboard:persons-list')

class PersonDetailView(generic.DetailView):
    model=Person
    context_object_name = 'person'
    template_name = 'oscar_ficta/dashboard/person_detail.html'
    
    
class GroupListView(SingleTableMixin, generic.TemplateView):
    template_name = 'oscar_ficta/dashboard/group_list.html'
    table_class = GroupTable
    context_table_name = 'groups'

    def get_queryset(self):
        return PersonGroup.get_root_nodes()

    def get_context_data(self, *args, **kwargs):
        ctx = super(GroupListView, self).get_context_data(*args, **kwargs)
        ctx['child_groups'] = PersonGroup.get_root_nodes()
        return ctx


class GroupDetailListView(SingleTableMixin, generic.DetailView):
    template_name = 'oscar_ficta/dashboard/group_list.html'
    model = PersonGroup
    context_object_name = 'group'
    table_class = GroupTable
    context_table_name = 'groups'

    def get_table_data(self):
        return self.object.get_children()

    def get_context_data(self, *args, **kwargs):
        ctx = super(GroupDetailListView, self).get_context_data(*args,
                                                                   **kwargs)
        ctx['child_groups'] = self.object.get_children()
        ctx['ancestors'] = self.object.get_ancestors_and_self()
        return ctx


class GroupListMixin(object):

    def get_success_url(self):
        parent = self.object.get_parent()
        if parent is None:
            return reverse("oscar_ficta_dashboard:group-list")
        else:
            return reverse("oscar_ficta_dashboard:group-detail-list",
                           args=(parent.pk,))


class GroupCreateView(GroupListMixin, generic.CreateView):
    template_name = 'oscar_ficta/dashboard/group_form.html'
    model = PersonGroup
    form_class = GroupForm

    def get_context_data(self, **kwargs):
        ctx = super(GroupCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new group")
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Group created successfully"))
        return super(GroupCreateView, self).get_success_url()

    def get_initial(self):
        # set child group if set in the URL kwargs
        initial = super(GroupCreateView, self).get_initial()
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class GroupUpdateView(GroupListMixin, generic.UpdateView):
    template_name = 'oscar_ficta/dashboard/group_form.html'
    model = PersonGroup
    form_class = GroupForm

    def get_context_data(self, **kwargs):
        ctx = super(GroupUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Update group '%s'") % self.object.name
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Group updated successfully"))
        return super(GroupUpdateView, self).get_success_url()


class GroupDeleteView(GroupListMixin, generic.DeleteView):
    template_name = 'oscar_ficta/dashboard/group_delete.html'
    model = PersonGroup

    def get_context_data(self, *args, **kwargs):
        ctx = super(GroupDeleteView, self).get_context_data(*args, **kwargs)
        ctx['parent'] = self.object.get_parent()
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Group deleted successfully"))
        return super(GroupDeleteView, self).get_success_url()
    
class InvoiceListView(BulkEditMixin, generic.ListView):
    """
    Dashboard view for a list of orders.
    Supports the permission-based dashboard.
    """
    model = Invoice
    context_object_name = 'invoices'
    template_name = 'oscar_ficta/dashboard/invoice_list.html'
    form_class = InvoiceSearchForm
    paginate_by = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
    actions = ('download_selected_invoices', 'change_invoice_statuses')

    def dispatch(self, request, *args, **kwargs):
        # base_queryset is equal to all orders the user is allowed to access
        self.base_queryset = queryset_invoices_for_user(
            request.user).order_by('-date_created')
        return super(InvoiceListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'invoice_number' in request.GET and request.GET.get(
                'response_format', 'html') == 'html':
            # Redirect to Invoice detail page if valid order number is given
            try:
                invoice = self.base_queryset.get(
                    number=request.GET['invoice_number'])
            except Invoice.DoesNotExist:
                pass
            else:
                return redirect(
                    'oscar_ficta_dashboard:invoice-detail', number=invoice.number)
        return super(InvoiceListView, self).get(request, *args, **kwargs)

    def get_queryset(self):  # noqa (too complex (19))
        """
        Build the queryset for this list.
        """
        queryset = sort_queryset(self.base_queryset, self.request,
                                 ['number', 'total_incl_tax'])

        # Look for shortcut query filters
        if 'invoice_status' in self.request.GET:
            self.form = self.form_class()
            status = self.request.GET['invoice_status']
            if status.lower() == 'none':
                status = None
            return self.base_queryset.filter(status=status)

        if 'invoice_number' not in self.request.GET:
            self.form = self.form_class()
            return queryset

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data

        if data['invoice_number']:
            queryset = self.base_queryset.filter(
                number__istartswith=data['invoice_number'])

        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()

            if len(parts) == 1:
                parts = [data['name'], data['name']]
            else:
                parts = [parts[0], parts[1:]]

            filter = Q(user__first_name__istartswith=parts[0])
            filter |= Q(user__last_name__istartswith=parts[1])

            queryset = queryset.filter(filter).distinct()
        
        if data['person_name']:
            queryset = queryset.filter(person__name__istartswith=data['person_name']).distinct()
            
        if data['date_from'] and data['date_to']:
            date_to = datetime_combine(data['date_to'], datetime.time.max)
            date_from = datetime_combine(data['date_from'], datetime.time.min)
            queryset = queryset.filter(
                date_created__gte=date_from, date_created__lt=date_to)
        elif data['date_from']:
            date_from = datetime_combine(data['date_from'], datetime.time.min)
            queryset = queryset.filter(date_created__gte=date_from)
        elif data['date_to']:
            date_to = datetime_combine(data['date_to'], datetime.time.max)
            queryset = queryset.filter(date_created__lt=date_to)

        if data['vatin']:
            queryset = queryset.filter(
                person__vatin=data['vatin']).distinct()

        if data['status']:
            queryset = queryset.filter(status=data['status'])

        return queryset

    def get_search_filter_descriptions(self):  # noqa (too complex (19))
        """Describe the filters used in the search.

        These are user-facing messages describing what filters
        were used to filter invoices in the search query.

        Returns:
            list of unicode messages

        """
        descriptions = []

        # Attempt to retrieve data from the submitted form
        # If the form hasn't been submitted, then `cleaned_data`
        # won't be set, so default to None.
        data = getattr(self.form, 'cleaned_data', None)

        if data is None:
            return descriptions

        if data.get('invoice_number'):
            descriptions.append(
                _('Invoice number starts with "{invoice_number}"').format(
                    invoice_number=data['invoice_number']
                )
            )

        if data.get('name'):
            descriptions.append(
                _('Customer name matches "{customer_name}"').format(
                    customer_name=data['name']
                )
            )
        if data.get('person_name'):
            descriptions.append(
                _('Juristic person matches "{person_name}"').format(
                    customer_name=data['person_name']
                )
            )
        if data.get('date_from') and data.get('date_to'):
            descriptions.append(
                # Translators: This string refers to orders in an online
                # store that were made within a particular date range.
                _('Placed between {start_date} and {end_date}').format(
                    start_date=data['date_from'],
                    end_date=data['date_to']
                )
            )

        elif data.get('date_from'):
            descriptions.append(
                # Translators: This string refers to orders in an online store
                # that were made after a particular date.
                _('Placed after {start_date}').format(
                    start_date=data['date_from'])
            )

        elif data.get('date_to'):
            end_date = data['date_to'] + datetime.timedelta(days=1)
            descriptions.append(
                # Translators: This string refers to orders in an online store
                # that were made before a particular date.
                _('Placed before {end_date}').format(end_date=end_date)
            )

        if data.get('vatin'):
            descriptions.append(
                _('Juristic person VAT number matches "{vatin}"').format(
                    vatin=data['vatin']
                )
            )

        if data.get('status'):
            descriptions.append(
                # Translators: This string refers to an order in an
                # online store.  Some examples of order status are
                # "purchased", "cancelled", or "refunded".
                _('Invoice status is {invoice_status}').format(
                    invoice_status=data['status'])
            )

        return descriptions

    def get_context_data(self, **kwargs):
        ctx = super(InvoiceListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['invoice_statuses'] = Invoice.status_choices
        ctx['search_filters'] = self.get_search_filter_descriptions()
        return ctx

    def is_csv_download(self):
        return self.request.GET.get('response_format', None) == 'csv'

    def get_paginate_by(self, queryset):
        return None if self.is_csv_download() else self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        if self.is_csv_download():
            return self.download_selected_invoices(
                self.request,
                context['object_list'])
        return super(InvoiceListView, self).render_to_response(
            context, **response_kwargs)

    def get_download_filename(self, request):
        return 'invoices.csv'

    def download_selected_invoices(self, request, invoices):
        response = http.HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' \
            % self.get_download_filename(request)
        writer = UnicodeCSVWriter(open_file=response)

        meta_data = (('number', _('Invoice number')),
                     ('value', _('Invoice value')),
                     ('date', _('Date of purchase')),
                     ('order_number', _('Order number')),
                     ('num_items', _('Number of items')),
                     ('status', _('Invoice status')),
                     ('customer', _('Customer email address')),
                     ('person_name', _('Pay as juristic person')),
                     ('person_vatin', _('Juristic person VAT number')),
                     ('person_code', _('Juristic person code (e.g. KPP in Russia)')),
                     )
        columns = SortedDict()
        for k, v in meta_data:
            columns[k] = v

        writer.writerow(columns.values())
        for invoice in invoices:
            row = columns.copy()
            row['number'] = invoice.number
            row['value'] = invoice.total_incl_tax
            row['date'] = format_datetime(invoice.date_created, 'DATETIME_FORMAT')
            row['order_number'] = invoice.order_number
            row['num_items'] = invoice.order.num_items
            row['status'] = invoice.status
            row['customer'] = invoice.order.email
            if invoice.person:
                row['person_name'] = invoice.person.name
                row['person_vatin'] = invoice.person.vatin
                row['person_code'] = invoice.person.reason_code
            else:
                row['person_name'] = '<none>'
                row['person_vatin'] = '<none>'
                row['person_code'] = '<none>'
            writer.writerow(row.values())
        return response

    def change_invoice_statuses(self, request, invoices):
        for invoice in invoices:
            self.change_invoice_status(request, invoice)
        return redirect('oscar_ficta_dashboard:invoice-list')

    def change_invoice_status(self, request, invoice):
        # This method is pretty similar to what
        # OrderDetailView.change_order_status does. Ripe for refactoring.
        new_status = int(request.POST['new_status'].strip())
        if not new_status:
            messages.error(request, _("The new status '%s' is not valid")
                           % new_status)
        elif new_status not in invoice.INVOICE_STATUSES.keys():
            logger.error("Invoice #%s new status %s INVALID", invoice.number, new_status)
            messages.error(request, _("The new status '%s' is not valid for"
                                      " this invoice") % new_status)
        else:
            #handler = EventHandler(request.user)
            old_status = invoice.status
            # here we need to mimic oscar's order status pipes but for the moment
            # just try to set 'linear' status and log it
            invoice.status = new_status
            invoice.save()
            msg = _("Invoice %(number)s status changed from '%(old_status)s' to"
                         " '%(new_status)s'") % {'number'   : invoice.number,
                                                 'old_status': Invoice.INVOICE_STATUSES[old_status],
                                                 'new_status': Invoice.INVOICE_STATUSES[new_status]}
            messages.info(request, msg)
            logger.info(msg)
#             try:
#                 handler.handle_order_status_change(order, new_status)
#             except PaymentError as e:
#                 messages.error(request, _("Unable to change order status due"
#                                           " to payment error: %s") % e)
#             else:
#                 msg = _("Order status changed from '%(old_status)s' to"
#                         " '%(new_status)s'") % {'old_status': old_status,
#                                                 'new_status': new_status}
#                 messages.info(request, msg)
#                 order.notes.create(
#                     user=request.user, message=msg, note_type=OrderNote.SYSTEM)    