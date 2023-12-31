# Generated by Django 4.2 on 2023-07-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(upload_to='uploads/', verbose_name='Ссылка на картинку')),
                ('needed_amount_of_shows', models.PositiveIntegerField(default=0, verbose_name='Необходимое количество показов')),
                ('is_last', models.BooleanField(default=False, verbose_name='Показывалась последней')),
                ('categories', models.ManyToManyField(blank=True, null=True, related_name='images', to='image.category', verbose_name='Категории')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]
