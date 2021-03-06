# Generated by Django 4.0.3 on 2022-03-29 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_ap', '0003_alter_url_last_scraped'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calculus_base', models.CharField(max_length=50)),
                ('value', models.FloatField()),
            ],
            options={
                'verbose_name': 'Taxes',
                'verbose_name_plural': 'Taxes',
            },
        ),
        migrations.CreateModel(
            name='Quiosque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installation_capital', models.FloatField()),
                ('franchising_tax', models.FloatField()),
                ('total_investiment', models.FloatField()),
                ('investiment_return_month_min', models.PositiveSmallIntegerField()),
                ('investiment_return_month_max', models.PositiveSmallIntegerField()),
                ('area_min', models.PositiveSmallIntegerField()),
                ('area_max', models.PositiveSmallIntegerField()),
                ('employees_min', models.PositiveSmallIntegerField()),
                ('employees_max', models.PositiveSmallIntegerField()),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_ap.franchise')),
                ('publicity_tax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_ap.tax')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_ap.state')),
            ],
        ),
    ]
