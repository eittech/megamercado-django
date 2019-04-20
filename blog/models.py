from django.db import models
from django.utils.text import slugify

# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=300,blank=True,null=True)
    page = models.URLField(verbose_name="URL de la Pagina",max_length=200,blank=True)
    url_feed =  models.URLField(verbose_name="URL feed (RSS)",max_length=200,blank=True)
    state = models.BooleanField(verbose_name="Esta activa",default=False,blank=True)
    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(verbose_name="titulo",max_length=200,blank=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to="assets/blog/",blank=True,null=True)
    url = models.URLField(verbose_name="URL",max_length=200,blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE,blank=True,null=True)
    author = models.CharField(max_length=300,blank=True,null=True)
    page_source = models.URLField(verbose_name="Feed Pagina",max_length=200,blank=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    description_short = models.TextField(verbose_name="Descripcion",blank=True,null=True)
    fecha = models.DateTimeField(verbose_name="Fecha de publicacion",auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Blog"
        unique_together = (('slug',))
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
