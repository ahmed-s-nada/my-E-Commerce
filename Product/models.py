from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from django.db.models import Q
from django.db.models.signals import post_save


# Create your models here.

class ProductQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(Active = True)

    def featured(self):
        return self.filter(featured = True)

    def search (self, query):
        lookups = Q(name__icontains = query ) | Q(discription__icontains = query )
        return self.filter(lookups).distinct()

    def search_price_range(self, min_p, max_p):
        # lookups = Q(price__gte = min_p) | Q(price__lte = max_p)
        # print ('this from the queryset', min_p, max_p)
        return self.filter(Q(price__gte = min_p)).filter(Q(price__lte = max_p))

    def search_maker(self, maker):
        return self.filter(Manufacturer__icontains = maker).distinct()

    def search_by_cat(self, cat):
        return self.filter(category__title__iexact = cat).distinct()

    def search_by_tag(self, tag):
        return self.filter(tag__title__iexact = tag).distinct()


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using= self._db)

    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().active().search(query)

    def my_get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1 :
            return qs.first() # <== here you MUST return the first instance not qs
                              #     because qs is Queryset not a single object
        else:
            return None


    def my_get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug = slug)
        if qs.count() == 1 :
            return qs.first() # <== here you MUST return the first instance not qs
                                  #     because qs is Queryset not a single object
        else:
            return None



class ProductCategory(models.Model):
    title       = models.CharField(max_length = 33, unique = True)
    slug        = models.SlugField(editable = False)
    discription = models.CharField(max_length = 66)
    active      = models.BooleanField(default = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class ProductsTag(models.Model):
    title       = models.CharField(max_length = 33, unique = True)
    slug        = models.SlugField(editable = False)
    discription = models.CharField(max_length = 66)
    active      = models.BooleanField(default = True)
    category    = models.ForeignKey(ProductCategory, related_name='category', on_delete = models.CASCADE, default = 1)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return '{0} => {1}'.format(self.title, self.category)



class Product(models.Model):
    name         = models.CharField(max_length = 64, unique = True)
    slug         = models.SlugField(blank = True, editable = False)
    Manufacturer = models.CharField(max_length = 32)
    category     = models.ForeignKey(ProductCategory, related_name='cat', on_delete = models.CASCADE, editable = False, blank= True, null=True)
    tag          = models.ForeignKey(ProductsTag, related_name='tag', on_delete = models.CASCADE, blank= True, null=True)
    discription  = models.TextField()
    cost         = models.DecimalField(max_digits=10, decimal_places=2)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    # seller = models.ForeignKey(seller, on_delete=seller, on_delete=None)
    main_image   = models.ImageField(upload_to = 'products_images')
    featured     = models.BooleanField(default = False)
    Active       = models.BooleanField(default = True)


    objects = ProductManager()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # self.category = self.tag.category
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


    def get_abolute_url(self):
         return reverse('Product:Single',kwargs={'slug':self.slug})


def product_post_save(sender, instance, *args, **kwargs):
    post_save.disconnect(product_post_save, sender=Product) # This is how you disconnect the signal and
                                                            # it's used here to prevent endless loop
    print ('Hi tag', instance.tag.category)
    instance.category = instance.tag.category
    instance.save(update_fields = ['category'])
    post_save.connect(product_post_save, sender=Product)

post_save.connect(product_post_save, sender=Product)



class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'images')
    image   = models.ImageField(upload_to = 'products_images',)

    def __str__(self):
        return 'image id is = {}'.format(self.pk)
