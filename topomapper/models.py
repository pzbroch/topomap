


from django.db import models



class Location(models.Model):
    site_code = models.CharField(max_length=8)
    site_name = models.CharField(max_length=16)
    zip_code = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    street = models.CharField(max_length=32)

    def __str__(self):
        return '{} / {} / {}'.format(self.site_code, self.site_name, self.city)



class Device(models.Model):
    name = models.CharField(max_length=16)
    desc = models.CharField(max_length=16)
    is_root = models.BooleanField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='devices')
    uplinks = models.ManyToManyField('self', through='Link', symmetrical=False, related_name='downlinks')
    failure = models.BooleanField(default=False)
    sim_check = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Link(models.Model):
    from_device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name='to_devices')
    to_device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name='from_devices')
    failure = models.BooleanField(default=False)

    def __str__(self):
        return '{} -> {}'.format(self.from_device,self.to_device)
