from django.contrib import admin
#from treebeard.admin import TreeAdmin
#from treebeard.forms import movenodeform_factory

from oscar.core.loading import get_model

Invoice = get_model('invoice', 'Invoice')

class InvoiceAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('number', 'order', 'person', 'total_incl_tax')
    list_filter = ['person', 'user', 'status']
    #inlines = [AttributeInline, CategoryInline, ProductRecommendationInline]
 
    search_fields = ['number', 'order_number']

#     def get_queryset(self, request):
#         qs = super(ProductAdmin, self).get_queryset(request)
#         return (
#             qs
#             .select_related('product_class', 'parent')
#             .prefetch_related(
#                 'attribute_values',
#                 'attribute_values__attribute'))


admin.site.register(Invoice, InvoiceAdmin)