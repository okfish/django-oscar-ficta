# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oscar_ficta.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oscar_ficta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='bic',
            field=oscar_ficta.fields.BICField(help_text='Bank Identification Code (international or local)', unique=True, verbose_name='BIC'),
            preserve_default=True,
        ),
    ]
