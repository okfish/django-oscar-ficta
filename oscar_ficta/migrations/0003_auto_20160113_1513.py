# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oscar_ficta.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oscar_ficta', '0002_auto_20150924_0027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank',
            options={'verbose_name': '\u0411\u0430\u043d\u043a', 'verbose_name_plural': '\u0411\u0430\u043d\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='bankaccount',
            options={'verbose_name': '\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u0441\u0447\u0435\u0442', 'verbose_name_plural': '\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0438\u0435 \u0441\u0447\u0435\u0442\u0430'},
        ),
        migrations.AlterModelOptions(
            name='legaladdress',
            options={'verbose_name': '\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u0434\u0440\u0435\u0441', 'verbose_name_plural': '\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0430\u0434\u0440\u0435\u0441\u0430'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': '\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e', 'verbose_name_plural': '\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043b\u0438\u0446\u0430'},
        ),
        migrations.AlterModelOptions(
            name='persongroup',
            options={'ordering': ['path'], 'verbose_name': '\u0413\u0440\u0443\u043f\u043f\u0430', 'verbose_name_plural': '\u0413\u0440\u0443\u043f\u043f\u044b'},
        ),
        migrations.AlterField(
            model_name='bank',
            name='bic',
            field=oscar_ficta.fields.BICField(help_text='\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u043a\u043e\u0434', unique=True, verbose_name='\u0411\u0418\u041a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bank',
            name='correspondent_account',
            field=models.CharField(max_length=20, verbose_name='\u041a\u043e\u0440\u0440\u0435\u0441\u043f\u043e\u043d\u0434\u0435\u043d\u0442\u0441\u043a\u0438\u0439 \u0441\u0447\u0435\u0442'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bank',
            name='location',
            field=models.CharField(help_text='\u041a\u043e\u0440\u043e\u0442\u043a\u043e\u0435 \u043d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u0431\u0430\u043d\u043a\u0430 (\u043e\u0431\u044b\u0447\u043d\u043e \u0433\u043e\u0440\u043e\u0434),\u043a\u0430\u043a \u043f\u0440\u0430\u0432\u0438\u043b\u043e, \u043f\u043e\u043b\u0443\u0447\u0430\u0435\u043c\u043e\u0435 \u0447\u0435\u0440\u0435\u0437 \u0431\u0430\u043d\u043a-\u043a\u043b\u0438\u0435\u043d\u0442', max_length=200, null=True, verbose_name='\u041c\u0435\u0441\u0442\u043e', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bank',
            name='person',
            field=models.OneToOneField(related_name='banks', null=True, blank=True, to='oscar_ficta.Person', verbose_name='\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bank',
            name='swift',
            field=models.CharField(max_length=11, unique=True, null=True, verbose_name='\u043a\u043e\u0434 SWIFT', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='bank',
            field=models.ForeignKey(related_name='person_accounts', verbose_name='\u0411\u0430\u043d\u043a', to='oscar_ficta.Bank'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u043e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='is_default',
            field=models.BooleanField(default=True, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u043f\u043e-\u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='person',
            field=models.ForeignKey(related_name='bank_accounts', verbose_name='\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u0438\u043a\u0430 \u0441\u0447\u0435\u0442\u0430', to='oscar_ficta.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='settlement_account',
            field=models.CharField(max_length=20, verbose_name='\u0420\u0430\u0441\u0441\u0447\u0435\u0442\u043d\u044b\u0439 \u0441\u0447\u0435\u0442'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='legaladdress',
            name='person',
            field=models.OneToOneField(related_name='legal_address', verbose_name='\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e', to='oscar_ficta.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='accountant_name',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0413\u043b\u0430\u0432\u043d\u044b\u0439 \u0431\u0443\u0445\u0433\u0430\u043b\u0442\u0435\u0440', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='chief_name',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0414\u0438\u0440\u0435\u043a\u0442\u043e\u0440 \u0438\u043b\u0438 \u0433\u0435\u043d\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='chief_title',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0422\u0438\u0442\u0443\u043b \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0430 \u0438\u043b\u0438 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u0430', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='date_liquidation',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043b\u0438\u043a\u0432\u0438\u0434\u0430\u0446\u0438\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='date_registration',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='full_name',
            field=models.CharField(max_length=254, null=True, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u043e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='logo',
            field=models.ImageField(max_length=255, upload_to=b'juristic/logos', null=True, verbose_name='\u041b\u043e\u0433\u043e\u0442\u0438\u043f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='manager_name',
            field=models.CharField(max_length=200, null=True, verbose_name='\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='partner',
            field=models.ForeignKey(related_name='juristic_persons', verbose_name='\u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a', blank=True, to='partner.Partner', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='reason_code',
            field=models.CharField(max_length=9, null=True, verbose_name='\u041a\u041f\u041f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='reference',
            field=models.CharField(null=True, max_length=32, blank=True, help_text='\u041d\u043e\u043c\u0435\u0440-\u0441\u0441\u044b\u043b\u043a\u0430, \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0434\u043b\u044f \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u044e\u0440.\u043b\u0438\u0446\u0430', unique=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.PositiveIntegerField(default=1, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u044e\u0440.\u043b\u0438\u0446\u0430', choices=[(1, '\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0435'), (2, '\u041d\u0430\u0447\u0430\u0442 \u043f\u0440\u043e\u0446\u0435\u0441\u0441 \u043b\u0438\u043a\u0432\u0438\u0434\u0430\u0446\u0438\u0438'), (3, '\u041b\u0438\u043a\u0432\u0438\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u043e')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='vatin',
            field=oscar_ficta.fields.VATNumberField(help_text='\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440 \u043d\u0430\u043b\u043e\u0433\u043e\u043f\u043b\u0430\u0442\u0435\u043b\u044c\u0449\u0438\u043a\u0430', verbose_name='\u0418\u041d\u041d', countries=[b'RU', b'UA']),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='website',
            field=models.URLField(null=True, verbose_name='\u0412\u0435\u0431-\u0441\u0430\u0439\u0442', blank=True),
            preserve_default=True,
        ),
    ]
