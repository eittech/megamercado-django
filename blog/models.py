from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(verbose_name="titulo",max_length=200,blank=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to="assets/blog/",blank=True,null=True)
    url = models.URLField(verbose_name="URL",max_length=200,blank=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    fecha = models.DateTimeField(verbose_name="Fecha de publicacion",auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Blog"
        unique_together = (('slug',))
