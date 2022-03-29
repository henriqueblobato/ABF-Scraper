# Generated by Django 4.0.3 on 2022-03-28 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FranchiseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Franchise Types',
                'verbose_name_plural': 'Franchise Types',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name': 'States',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('minimum_investiment', models.FloatField()),
                ('min_return_month', models.PositiveSmallIntegerField()),
                ('max_return_month', models.PositiveSmallIntegerField()),
                ('active_unities', models.PositiveIntegerField(default=0)),
                ('contact', models.CharField(max_length=50)),
                ('ftype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_ap.franchisetype')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_ap.state')),
            ],
            options={
                'verbose_name': 'Franchises',
                'verbose_name_plural': 'Franchises',
            },
        ),
    ]