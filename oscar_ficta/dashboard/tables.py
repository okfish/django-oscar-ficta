from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

from django_tables2 import Column, LinkColumn, TemplateColumn, A

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
PersonGroup = get_model('oscar_ficta', 'PersonGroup')


class GroupTable(DashboardTable):
    name = LinkColumn('oscar_ficta_dashboard:group-update', args=[A('pk')])
    description = TemplateColumn(
        template_code='{{ record.description|default:""|striptags'
                      '|cut:"&nbsp;"|truncatewords:6 }}')
    # mark_safe is needed because of
    # https://github.com/bradleyayers/django-tables2/issues/187
    num_children = LinkColumn(
        'oscar_ficta_dashboard:group-detail-list', args=[A('pk')],
        verbose_name=mark_safe(_('Number of child categories')),
        accessor='get_num_children',
        orderable=False)
    actions = TemplateColumn(
        template_name='oscar_ficta/dashboard/group_row_actions.html',
        orderable=False)

    icon = "sitemap"
    caption = ungettext_lazy("%s Group", "%s Groups")

    class Meta(DashboardTable.Meta):
        model = PersonGroup
        fields = ('name', 'description')