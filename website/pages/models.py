from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Media(models.Model):
    '''
    Represents the image file as media
    It processes and saves the media file in fixed
    size upon saving.
    '''
    image = models.ImageField()
    description = models.CharField(max_length=1000, default=' ')

    def save(self, size=(200, 200)):
        """
        Save Photo after ensuring it is not blank.  Resize as needed.
        """
        from sahayak import settings

        if not self.image:
            return

        super(Media, self).save()

        filename = settings.MEDIA_ROOT+"/"+self.image.name
        image = Image.open(filename)
        width, height = image.size
        if height > width:
            ratio = height/width

            image.thumbnail((200, 200*ratio), Image.ANTIALIAS)
        else:
            ratio = width/height
            image.thumbnail((200*ratio, 200), Image.ANTIALIAS)
        image.save(filename)

    def showimage(self):
        return '<img src="/media/'+self.image.name+'"/>'
    showimage.allow_tags = True

    def geturl(self):
        '''
        Returns the URL of the media file
        '''
        pass

    def __str__(self):
        return self.description
