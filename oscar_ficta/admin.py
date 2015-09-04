from django.contrib import admin
#from treebeard.admin import TreeAdmin
#from treebeard.forms import movenodeform_factory

from oscar.core.loading import get_model

Person = get_model('oscar_ficta', 'Person')
PersonGroup = get_model('oscar_ficta', 'PersonGroup')
LegalAddress = get_model('oscar_ficta', 'LegalAddress')


#class AttributeInline(admin.TabularInline):
#    model = ProductAttributeValue


#class ProductRecommendationInline(admin.TabularInline):
#    model = ProductRecommendation
#    fk_name = 'primary'


#class CategoryInline(admin.TabularInline):
#    model = ProductCategory
#    extra = 1



class LegalAddressAdmin(admin.ModelAdmin):
    list_display = ('postcode', 'line4', 'line1', 'line2', 'line3')
    #inlines = [ProductAttributeInline]


class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('vatin', 'name',)
    list_filter = ['group', 'is_active', 'status']
    #inlines = [AttributeInline, CategoryInline, ProductRecommendationInline]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'vatin']

#     def get_queryset(self, request):
#         qs = super(ProductAdmin, self).get_queryset(request)
#         return (
#             qs
#             .select_related('product_class', 'parent')
#             .prefetch_related(
#                 'attribute_values',
#                 'attribute_values__attribute'))


admin.site.register(Person, PersonAdmin)
admin.site.register(LegalAddress, LegalAddressAdmin)