# Generated by Django 3.2.6 on 2021-11-19 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('bio', models.TextField(blank=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_year', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('language', models.CharField(max_length=20, verbose_name='language')),
                ('pages', models.IntegerField()),
                ('image', models.ImageField(upload_to='products/%Y/%m/%d')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('isbn', models.CharField(max_length=13, unique=True, verbose_name='ISBN')),
                ('rating', models.FloatField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('available', models.BooleanField(default=True)),
                ('quantity', models.IntegerField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.author')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='Input your comment.', max_length=10000)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='books', to='shop.Genre'),
        ),
        migrations.AlterIndexTogether(
            name='book',
            index_together={('id', 'slug')},
        ),
    ]
