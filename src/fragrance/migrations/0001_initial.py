# Generated by Django 3.1.7 on 2021-03-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fragrance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('brand', models.CharField(max_length=50, verbose_name='brand')),
                ('size', models.IntegerField()),
                ('gender', models.CharField(choices=[('man', 'man'), ('woman', 'woman'), ('unisex', 'unisex')], default='unisex', max_length=6, verbose_name='gender')),
                ('type', models.CharField(choices=[('eau de cologne', 'eau de cologne'), ('eau de toilette', 'eau de toilette'), ('eau de parfum', 'eau de parfum')], default='toilette', max_length=15, verbose_name='type')),
                ('url', models.URLField(verbose_name='url')),
                ('seller', models.CharField(max_length=50, verbose_name='seller')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('max_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('min_offer_price', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('max_offer_price', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('is_in_offer', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='updated at')),
                ('checked_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='checked at')),
            ],
            options={
                'verbose_name': 'Fragrance',
                'verbose_name_plural': 'Fragrances',
                'ordering': ['seller', 'brand', 'name'],
            },
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='url')),
                ('domain', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(editable=False, null=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'Url',
                'verbose_name_plural': 'Urls',
                'ordering': ['domain'],
            },
        ),
    ]
