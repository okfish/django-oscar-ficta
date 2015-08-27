# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oscar.models.fields.autoslugfield
import internationalflavor.iban.models
import oscar.models.fields
from django.conf import settings
import internationalflavor.vat_number.models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0004_auto_20150828_0054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0418\u043c\u044f')),
                ('bic', internationalflavor.iban.models.BICField(verbose_name='BIC')),
                ('swift', models.CharField(max_length=11, null=True, verbose_name='SWIFT code', blank=True)),
                ('correspondent_account', models.CharField(max_length=20, verbose_name='Correspondent account number')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iban', internationalflavor.iban.models.IBANField(countries='IBAN', null=True, blank=True)),
                ('settlement_account', models.CharField(max_length=20, verbose_name='Settlement account number')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_default', models.BooleanField(default=True, verbose_name='Use it by default?')),
                ('bank', models.ForeignKey(related_name='person_accounts', verbose_name='Bank', to='oscar_ficta.Bank')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Bank account',
                'verbose_name_plural': 'Bank accounts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LegalAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=64, verbose_name='Title', choices=[(b'Mr', 'Mr'), (b'Miss', 'Miss'), (b'Mrs', 'Mrs'), (b'Ms', 'Ms'), (b'Dr', 'Dr')])),
                ('first_name', models.CharField(max_length=255, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name', blank=True)),
                ('line1', models.CharField(max_length=255, verbose_name='First line of address')),
                ('line2', models.CharField(max_length=255, verbose_name='Second line of address', blank=True)),
                ('line3', models.CharField(max_length=255, verbose_name='Third line of address', blank=True)),
                ('line4', models.CharField(max_length=255, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=255, verbose_name='State/County', blank=True)),
                ('postcode', oscar.models.fields.UppercaseCharField(max_length=64, verbose_name='Post/Zip-code', blank=True)),
                ('search_text', models.TextField(verbose_name='Search text - used only for searching addresses', editable=False)),
                ('country', models.ForeignKey(verbose_name='Country', to='address.Country')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Legal address',
                'verbose_name_plural': 'Legal addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vatin', internationalflavor.vat_number.models.VATNumberField(help_text='VAT or tax payer ID', countries=[b'RU'])),
                ('reason_code', models.CharField(max_length=9, null=True, verbose_name='Code for Reason of registration, e.g. KPP in Russia', blank=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0418\u043c\u044f')),
                ('slug', oscar.models.fields.autoslugfield.AutoSlugField(populate_from=b'name', editable=False, max_length=200, blank=True, unique=True, verbose_name='\u041a\u043e\u0434')),
                ('manager_name', models.CharField(max_length=200, null=True, verbose_name='Manager name', blank=True)),
                ('chief_name', models.CharField(max_length=200, null=True, verbose_name='GM or Director name', blank=True)),
                ('chief_title', models.CharField(max_length=200, null=True, verbose_name='Title for GM or Director', blank=True)),
                ('accountant_name', models.CharField(max_length=200, null=True, verbose_name='Main Accountant name', blank=True)),
                ('phone', models.CharField(max_length=64, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441 \u044d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u043e\u0439 \u043f\u043e\u0447\u0442\u044b', blank=True)),
                ('reference', models.CharField(null=True, max_length=32, blank=True, help_text='A reference number that uniquely identifies this person', unique=True, verbose_name='\u0417\u0430\u043c\u0435\u0442\u043a\u0438')),
                ('description', models.TextField(max_length=2000, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('status', models.PositiveIntegerField(verbose_name='State status', choices=[(1, '\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435'), (2, 'Liquidating process started'), (3, 'Liquidated')])),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', db_index=True)),
                ('date_registration', models.DateTimeField(null=True, verbose_name='Date of registration', blank=True)),
                ('date_liquidation', models.DateTimeField(null=True, verbose_name='Date of liquidation', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Juristic person',
                'verbose_name_plural': 'Juristic persons',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u0418\u043c\u044f')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='\u041f\u0443\u0442\u044c')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='group',
            field=models.ForeignKey(related_name='persons', verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430', blank=True, to='oscar_ficta.PersonGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='partner',
            field=models.ForeignKey(related_name='juristic_persons', verbose_name='\u041f\u0430\u0440\u0442\u043d\u0435\u0440-\u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a', to='partner.Partner', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='users',
            field=models.ManyToManyField(related_name='related_persons', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='legaladdress',
            name='person',
            field=models.OneToOneField(related_name='legal_address', verbose_name='Juristic person', to='oscar_ficta.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='person',
            field=models.ForeignKey(related_name='bank_accounts', verbose_name="Owner's juristic person", to='oscar_ficta.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bank',
            name='person',
            field=models.OneToOneField(related_name='banks', null=True, blank=True, to='oscar_ficta.Person', verbose_name='Juristic person'),
            preserve_default=True,
        ),
    ]
