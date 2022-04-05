from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to='category', blank=True, null=True)
    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    preview_des = models.CharField(
        max_length=255, verbose_name='Short Descriptions')
    description = models.TextField(max_length=1000, verbose_name='Description')
    image = models.ImageField(upload_to='product', blank=False, null=False)
    price = models.FloatField()
    old_price = models.FloatField(default=0.00, blank=True, null=True)
    is_stock = models.BooleanField(default=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def get_product_url(self):
        return reverse('store:product-details', kwargs={'slug': self.slug})

    class Mete:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.FileField(upload_to='product_gallery')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.product.name)


class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(variation='size')

    def colors(self):
        return super(VariationManager, self).filter(variation='color')


VARIATIONS_TYPE = (
    ('size', 'size'),
    ('color', 'color'),
)


class VariationValue(models.Model):
    variation = models.CharField(max_length=100, choices=VARIATIONS_TYPE)
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.name
