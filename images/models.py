from django.db import models
from django.utils.text  import slugify
from django.conf import settings
from account.models import CustomUser

class Image(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            related_name='images_created',
                            on_delete=models.CASCADE,
                            blank=True, null=True
                            )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, 
                            unique=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    
    class Meta:
        
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        
    def __str__(self):
        return self.slug
    
    
    
    
    