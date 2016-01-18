# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='partner_person',
            field=models.ForeignKey(related_name='invoices', verbose_name='\u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a', to='oscar_ficta.Person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='person',
            field=models.ForeignKey(related_name='person_invoices', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e', blank=True, to='oscar_ficta.Person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.PositiveIntegerField(default=1, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0441\u0447\u0435\u0442\u0430', choices=[(1, '\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a'), (2, '\u041d\u043e\u0432\u044b\u0439'), (3, '\u0412\u044b\u0441\u043b\u0430\u043d'), (4, '\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u0435\u043c'), (5, '\u041e\u0442\u043a\u043b\u043e\u043d\u0435\u043d \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u0435\u043c'), (6, '\u041e\u043f\u043b\u0430\u0447\u0435\u043d \u0447\u0430\u0441\u0442\u0438\u0447\u043d\u043e'), (7, '\u041e\u043f\u043b\u0430\u0447\u0435\u043d \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e'), (8, '\u041f\u0435\u0440\u0435\u043f\u043b\u0430\u0447\u0435\u043d'), (9, '\u041f\u0440\u043e\u0441\u0440\u043e\u0447\u0435\u043d'), (10, '\u041e\u0442\u043c\u0435\u043d\u0435\u043d \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u043e\u043c'), (11, '\u0423\u0434\u0430\u043b\u0435\u043d')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_excl_tax',
            field=models.DecimalField(verbose_name='\u0418\u0442\u043e\u0433\u043e (\u0431\u0435\u0437 \u043d\u0430\u043b\u043e\u0433\u043e\u0432)', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_incl_tax',
            field=models.DecimalField(verbose_name='\u0418\u0442\u043e\u0433\u043e (\u0432\u043a\u043b. \u043d\u0430\u043b\u043e\u0433\u0438)', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
