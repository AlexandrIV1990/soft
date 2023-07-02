import random

from django.db.models import Sum, F, RowRange, Window
from django.shortcuts import render
from django.views.generic.base import View

from image.models import Image


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        categories = request.GET.getlist('category')
        category = random.choice(categories)
        print(category)
        images = Image.objects.filter(is_last=False, categories__title__in=categories,
                                      needed_amount_of_shows__isnull=False).order_by("id").annotate(
            max_index=Window(
                expression=Sum('needed_amount_of_shows'),
                frame=RowRange(start=0),
                order_by=F('id').asc()
            ))

        # print(sum_images)
        for i in images:
            print(i.id, i.needed_amount_of_shows)
            print("MIN:", i.max_index)
        # print(sum_images)
        # print(images)
        # print(x)
        if images:
            sum_images = images.aggregate(sum_shows=Sum('needed_amount_of_shows'))['sum_shows']
            random_number = random.randint(1, sum_images)
            print(random_number)

            image = images.filter(max_index__gte=random_number).first()
            print(image.image_url, image.needed_amount_of_shows)
            Image.objects.filter(is_last=True).update(is_last=False)
            image.needed_amount_of_shows -= 1
            image.is_last = True
            image.save(update_fields=['needed_amount_of_shows', 'is_last'])
            context = {'image': image.image_url}
            return render(request, 'image.html', context=context)
        return render(request, 'image_out.html')
