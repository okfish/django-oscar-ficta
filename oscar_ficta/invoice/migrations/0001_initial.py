# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import oscar.core.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0002_auto_20150416_0202'),
        ('oscar_ficta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=64, unique=True, null=True)),
                ('order_number', models.CharField(max_length=128, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0437\u0430\u043a\u0430\u0437\u0430', db_index=True)),
                ('status', models.PositiveIntegerField(default=1, verbose_name='Invoice status', choices=[(1, '\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a'), (2, 'New'), (3, 'Invoice sent'), (4, 'Approved by buyer'), (5, 'Declined by buyer'), (6, 'Invoice paid partially'), (7, 'Invoice paid fully'), (8, 'Overpaid'), (9, 'Outdated for payment'), (10, 'Cancelled by manager'), (11, '\u0423\u0434\u0430\u043b\u0435\u043d\u043e.')])),
                ('merchant_reference', models.CharField(max_length=128, null=True, blank=True)),
                ('description', models.CharField(max_length=256, null=True, blank=True)),
                ('currency', models.CharField(default=oscar.core.utils.get_default_currency, max_length=12, verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430')),
                ('total_incl_tax', models.DecimalField(verbose_name='\u0412\u0441\u0435\u0433\u043e (\u0441 \u041d\u0414\u0421)', max_digits=12, decimal_places=2)),
                ('total_excl_tax', models.DecimalField(verbose_name='\u0412\u0441\u0435\u0433\u043e (\u0431\u0435\u0437 \u041d\u0414\u0421)', max_digits=12, decimal_places=2)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', db_index=True)),
                ('order', models.ForeignKey(related_name='assigned_invoices', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0417\u0430\u043a\u0430\u0437', blank=True, to='order.Order', null=True)),
                ('partner_person', models.ForeignKey(related_name='invoices', verbose_name='\u041f\u0430\u0440\u0442\u043d\u0435\u0440-\u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a', to='oscar_ficta.Person', null=True)),
                ('person', models.ForeignKey(related_name='person_invoices', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Juristic person', blank=True, to='oscar_ficta.Person', null=True)),
                ('user', models.ForeignKey(related_name='user_invoices', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
