from django.db import models

# Create your models here.
class thongtin(models.Model):
    id = models.IntegerField
    file_word= models.CharField(max_length=255)
    
    def __str__(self):
        return self.file_word
