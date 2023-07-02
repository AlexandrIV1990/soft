import csv
from django.core.files import File

from image.models import Image, Category


class CreateImageDB:

    def __init__(self, path):
        self.path = path

    def _parse_image_csv(self):  # noqa
        with open(self.path, "r") as csv_file:
            f = csv.reader(csv_file, delimiter=';')
            data_rows = []
            data_categories = []
            for row in f:
                data_categories.append([Category.objects.get_or_create(title=title)[0] for title in row[2:]])
                try:
                    image_url = File(open(row[0], "rb"))
                except FileNotFoundError as e:
                    image_url = row[0]
                image = Image(image_url=image_url, needed_amount_of_shows=row[1])
                data_rows.append(image)
            images = Image.objects.bulk_create(data_rows)
            for i in range(len(images)):
                images[i].categories.set(data_categories[i])

    def execute(self):
        self._parse_image_csv()
