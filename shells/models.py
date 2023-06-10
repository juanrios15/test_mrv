import os

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class DifficultyLevel(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



def content_file_name(instance, filename):
    if instance._meta.get_field("instruction_image") == instance:
        return os.path.join("instructions", filename)
    else:
        return os.path.join("resolutions", filename)


class Shell(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE)
    instruction_text = models.CharField(max_length=500, blank=True, null=True)
    instruction_image = models.ImageField(upload_to=content_file_name)
    resolution_text = models.CharField(max_length=500, blank=True, null=True)
    resolution_image = models.ImageField(upload_to=content_file_name)

    class Meta:

        verbose_name = 'Shell'
        verbose_name_plural = 'Shells'

    def __str__(self):
        return self.title
