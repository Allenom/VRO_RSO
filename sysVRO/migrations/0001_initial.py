# Generated by Django 4.1.2 on 2023-01-26 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип мероприятия',
                'verbose_name_plural': 'тип мероприятия',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Мероприятие')),
                ('beginning_date', models.DateField(db_index=True, verbose_name='Дата начала мероприятия')),
                ('beginning_time', models.TimeField(blank=True, null=True, verbose_name='Время начала мероприятия')),
                ('ending_date', models.DateField(blank=True, null=True, verbose_name='Дата конца мероприятия')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='static/img/')),
                ('kind', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sysVRO.kind', verbose_name='Тип мероприятия')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'мероприятие',
                'ordering': ['-beginning_date'],
            },
        ),
    ]