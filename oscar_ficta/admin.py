from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from oscar.core.loading import get_model

Person = get_model('oscar_ficta', 'Person')
PersonGroup = get_model('oscar_ficta', 'PersonGroup')
LegalAddress = get_model('oscar_ficta', 'LegalAddress')
Bank = get_model('oscar_ficta', 'Bank')
BankAccount = get_model('oscar_ficta', 'BankAccount')
LegalAddress = get_model('oscar_ficta', 'LegalAddress')

class LegalAddressInline(admin.TabularInline):
    model = LegalAddress
    extra = 1

class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1

class LegalAddressAdmin(admin.ModelAdmin):
    list_display = ('postcode', 'line4', 'line1', 'line2', 'line3')

class PersonGroupAdmin(TreeAdmin):
    form = movenodeform_factory(PersonGroup)

class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('vatin', 'name',)
    list_filter = ['group', 'is_active', 'status']
    inlines = [LegalAddressInline, BankAccountInline]
    search_fields = ['name', 'vatin']

#     def get_queryset(self, request):
#         qs = super(ProductAdmin, self).get_queryset(request)
#         return (
#             qs
#             .select_related('product_class', 'parent')
#             .prefetch_related(
#                 'attribute_values',
#                 'attribute_values__attribute'))

class BankAdmin(admin.ModelAdmin):
    list_display = ('bic', 'name',)
    #list_filter = ['group', 'is_active', 'status']
    #inlines = [AttributeInline, CategoryInline, ProductRecommendationInline]
    #prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'bic']


admin.site.register(Person, PersonAdmin)
admin.site.register(PersonGroup, PersonGroupAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(LegalAddress, LegalAddressAdmin)