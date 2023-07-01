import random

from django.db.models import Sum, F, RowRange, Window
from django.shortcuts import render
from django.views.generic.base import View

from image.models import Image


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        categories = request.GET.getlist('category')
        # queryset = Equipment.objects.annotate(
        #     previous_sum=Window(
        #         expression=Sum('field_name'),
        #         order_by=F('id').asc(),
        #         frame=RowRange(start=-1),
        #     )
        category = random.choice(categories)
        images = Image.objects.filter(is_last=False, categories__title=category).distinct()
        sum_images = images.aggregate(sum_shows=Sum('needed_amount_of_shows'))['sum_shows']
        x = images.annotate(max_index=Window(
                expression=Sum('needed_amount_of_shows'),
                frame=RowRange(start=0),
                partition_by=[F('id')],
                order_by=F('id').asc()
        ))
        for i in x:
            print(i.id, i.needed_amount_of_shows)
            print("MAX:", i.max_index, "MIN:", i.max_index)
        print(sum_images)
        print(images)
        print(x)
        random_number = random.randint(1, sum_images)
        print(random_number)
        sql, params = images.query.sql_with_params()
        queryset = images.raw(f"SELECT * FROM ({sql}) AS full WHERE max_index >= ({random_number})", params)
        # y = x.filter(max_index=random_number).all()
        print(queryset)
        context = {'image': images.first().image_url}
        return render(request, 'image.html', context=context)
