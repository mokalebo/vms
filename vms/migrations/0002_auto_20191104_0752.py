# Generated by Django 2.2.6 on 2019-11-04 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='opportunity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vms.Opportunity'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together={('volunteer', 'opportunity')},
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='organization',
        ),
    ]
