from django.db import models

class route_status(models.Model):
  ref = models.CharField(max_length=32)
  oper = models.CharField(max_length=32)
  stat = models.CharField(max_length=2048, default=None, null=True) #json inside
  info = models.CharField(max_length=2048, default=None, null=True) #json inside
  direct = models.BooleanField(default = True) #True: Forward, False: Backward
  updating = models.BooleanField(default=False)
  update_ts = models.DateTimeField(auto_now=True)
  class meta:
      unique_together = (('route_ref', 'route_oper'),)

class bus_route(models.Model):
   id = models.IntegerField(primary_key = True)
   name = models.CharField(max_length=32)
   oper = models.CharField(max_length=32)
   ref = models.CharField(max_length=32)
   def __unicode__(self):
     return self.name
   
# XXX: use geodjango in the future
class bus_stop(models.Model):
   id = models.IntegerField(primary_key = True)
   ref = models.CharField(max_length=32)
   info = models.CharField(max_length=32)
   name = models.CharField(max_length=32)
   lon = models.FloatField()
   lat = models.FloatField()
   def __unicode__(self):
     return self.name

class stop_route_relation(models.Model):
   route = models.ForeignKey('bus_route')
   stop  = models.ForeignKey('bus_stop')
   direct = models.BooleanField(default = True) #True: Forward, False: Backward
   #seq = models.IntegerField()
   hub = models.ForeignKey('TransferHub', null = True, default=None);
   class meta:
     unique_together = (('route', 'stop', 'direct'),)

class TransferHub(models.Model):
  name = models.CharField(max_length = 32)
