# Generated by Django 3.2.2 on 2021-07-04 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apihostal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visita',
            old_name='fecha',
            new_name='fechavisita',
        ),
        migrations.RenameField(
            model_name='visita',
            old_name='ip',
            new_name='ipvisita',
        ),
    ]
