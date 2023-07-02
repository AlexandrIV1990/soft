import random

from django.db.models import Sum, F, Q, RowRange, Window
from django.db.transaction import atomic
from django.shortcuts import render
from django.views.generic.base import View

from image.models import Image


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist('category')
        images = Image.objects.exclude(Q(is_last=True) | Q(needed_amount_of_shows=0)).order_by("id").annotate(
            max_index=Window(
                expression=Sum('needed_amount_of_shows'),
                frame=RowRange(start=0),
                order_by=F('id').asc()
            ))
        if categories:
            images = images.filter(categories__title__in=categories)

        if images:
            sum_images = images.aggregate(sum_shows=Sum('needed_amount_of_shows'))['sum_shows']
            random_number = random.randint(1, sum_images)

            image = images.filter(max_index__gte=random_number).first()
            with atomic():
                Image.objects.filter(is_last=True).update(is_last=False)
                image.needed_amount_of_shows -= 1
                image.is_last = True
                image.save(update_fields=['needed_amount_of_shows', 'is_last'])

            context = {'image': image.image_url}
            return render(request, 'image.html', context=context)

        elif last_image := Image.objects.filter(is_last=True, needed_amount_of_shows__isnull=False).first():
            last_image.needed_amount_of_shows -= 1
            last_image.save(update_fields=['needed_amount_of_shows'])

            context = {'image': last_image.image_url}
            return render(request, 'image.html', context=context)

        return render(request, 'image_out.html')
