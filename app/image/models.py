from django.db import models


def get_file_path(instance, filename):
    return f'uploads/{filename.split("/")[-1]}'


class Category(models.Model):
    title = models.CharField(max_length=32, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Image(models.Model):
    image_url = models.ImageField(upload_to='uploads/', verbose_name='Ссылка на картинку')
    needed_amount_of_shows = models.PositiveIntegerField(default=0, verbose_name='Необходимое количество показов')
    categories = models.ManyToManyField("Category", verbose_name='Категории', blank=True, null=True,
                                        related_name='images')
    is_last = models.BooleanField(verbose_name='Показывалась последней', default=False)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return str(self.pk)
