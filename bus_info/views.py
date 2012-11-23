# Create your views here.
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from operators import opers
import json
import sys
import time
import route
from datetime import datetime
from django.conf import settings
from models import *

class GetLineForm(forms.Form):
   oper = forms.CharField()
   ref = forms.CharField()
   direct = forms.CharField()
   callback = forms.CharField()

def get_line(request):
   bus_status = None
   form = GetLineForm(request.GET)
   if request.method == 'GET' and form.is_valid():
      oper = form.cleaned_data['oper']
      ref = form.cleaned_data['ref']
      line = bus_route.objects.get(ref = ref)
      if form.cleaned_data['direct'] == 'b':
         forward = False
      else:
         forward = True
      count = 0
      try:
         status = route_status.objects.get(ref = ref, oper=oper, direct = forward)
      except:
         status = None

      if status is None:
         status = route_status(ref = ref, oper=oper, updating = True, direct = forward)
         status.save()
         status = None
         #oper_mod_name = opers.operators['khc_bus']
         oper_mod_name = opers.operators[oper]
         m = __import__("bus_info.operators.%s" % oper_mod_name)
         bus_status = vars(m.operators)[oper_mod_name].update_bus_line(line, forward)
         status = route_status.objects.get(ref = ref, oper = oper, direct = forward)
         status.stat = bus_status
         status.updating = False
         status.save()
         print "update_info"
      else:
         count = 0
         while count < 10:
            if status.updating is True:
               status = route_status.objects.get(ref = ref, oper = oper, direct = forward)
               print 'get from cache'
            else:
               if (status.update_ts - datetime.now() ).seconds > 30 :
                  status.updating = True
                  status.save()
               else:
                  bus_status = status.stat
               break
            time.sleep(0.6)
            count += 1
            print "waiting..."
         if bus_status is None or True:
            try:
              oper_mod_name = opers.operators[oper]
            except:
              print sys.exc_info()
            m = __import__("bus_info.operators.%s" % oper_mod_name)
            bus_status = vars(m.operators)[oper_mod_name].update_bus_line(line, forward)
            if status is None:
               status = route_status.objects.get(ref = ref, oper=oper, direct = forward)
            status.stat = bus_status
            status.updating = False
            status.save()
      return HttpResponse(form.cleaned_data['callback'] + '(' + bus_status + ')', mimetype = 'application/json')
   else:
      return HttpResponse('')

class GetBusStopsForm(forms.Form):
   rlat = forms.FloatField(required = False)
   rlon = forms.FloatField(required = False)
   llat = forms.FloatField(required = False)
   llon = forms.FloatField(required = False)
   zoom = forms.IntegerField(required = False)
   callback = forms.CharField()

def get_bus_stops(request):
   form = GetBusStopsForm(request.GET)
   j = []
   if form.is_valid():
      #TODO: return bus stops acording to the area openlayer covers
      stops = bus_stop.objects.all()
      for i in stops:
         s = {}
         s['id'] = i.id
         s['ref'] = []
         for r in i.ref.split(';'):
            s['ref'].append(r)
         s['oper'] = i.stop_route_relation_set.all()[0].route.oper
         s['info'] = i.info
         s['name'] = i.name
         s['lon'] = i.lon
         s['lat'] = i.lat
         s['route_ref'] = []
         #r_count = 0
         for stop_route in stop_route_relation.objects.filter(stop = i):
            r = {}
            r['ref'] = stop_route.route.ref
            if stop_route.direct is True:
              r['direct'] = 'f'
            else:
              r['direct'] = 'b'
            #r_count += 1
            s['route_ref'].append(r)
         j.append(s)
      response = HttpResponse(form.cleaned_data['callback'] + '(' + json.dumps(j) + ')', mimetype='application/json')
      response['Cache-Control'] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
      return response

   return HttpResponse('')

class RouteRequestForm(forms.Form):
  start_id = forms.IntegerField(required = True)
  dest_id = forms.IntegerField(required = True)
  callback = forms.CharField()

def routing(request):
   form = RouteRequestForm(request.GET)
   if form.is_valid():
     start_id = form.cleaned_data['start_id']
     dest_id = form.cleaned_data['dest_id']
     start_stop = bus_stop.objects.get(id =start_id)
     dest_stop = bus_stop.objects.get(id = dest_id)
     routing_result = route.route(start_stop, dest_stop)
     print routing_result
     return HttpResponse(form.cleaned_data['callback'] + '('+ json.dumps({'result':routing_result}) + ')', mimetype='text/json')
   return HttpResponse(form.cleaned_data['callback'] + '('+ json.dumps({'result':[]}) + ')', mimetype='append/json')

def map(request):
  return render_to_response('bus.html', {'HOST':settings.HOST, 'PORT':settings.PORT, 'JS_BASE_URL':settings.JS_BASE_URL})
if __name__ == "__main__":
   print get_line(None, u"高雄市公車", "820")
