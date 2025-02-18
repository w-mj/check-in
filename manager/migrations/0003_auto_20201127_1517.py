# Generated by Django 3.1.3 on 2020-11-27 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20201127_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursetime',
            old_name='repeat',
            new_name='day',
        ),
        migrations.RemoveField(
            model_name='coursetime',
            name='start_date',
        ),
        migrations.AddField(
            model_name='checkin',
            name='count',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='coursetime',
            name='end_week',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursetime',
            name='start_week',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='JoinClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manager.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manager.appuser')),
            ],
        ),
    ]
