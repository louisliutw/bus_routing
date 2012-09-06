from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from bus_info.models import *
import OsmApi


class Command(BaseCommand):
        args = '<relation_id relation_id ...>'
        help = 'import bus stops from OsmAPI'

        def handle(self, *args, **options):
          api = OsmApi.OsmApi()
          for relation_id in args:
            relation_id = int(relation_id)
            relation = api.RelationGet(relation_id)
            try:
              r = bus_route.objects.filter(relation_id=relation_id)
              stop_route_relation.object.filter(route=relation_id).delete()
              r.delete()
            except:
              pass

            if relation['tag']['route'] != 'bus':
              continue

            route = bus_route()
            route.id = relation_id
            route.oper = relation['tag']['operator']
            route.ref = relation['tag']['ref']
            route.name = relation['tag']['name']
            route.save()

            for member in relation['member']:
              if member['type'] != 'node':
                continue
              try:
                stop = bus_stop.objects.get(id = member['ref'])  
                stop_routes = stop_route_relation.objects.filter(stop = stop, route=route).delete()
              except ObjectDoesNotExist:
                stop = bus_stop(id = member['ref'])

              if member['role'] == 'forward_stop':
                direct = True
              elif member['role'] == 'backward_stop':
                direct = False
              else:
                stop = None
              stop_node = api.NodeGet(stop.id)
              stop.lon = stop_node['lon']
              stop.lat = stop_node['lat']
              stop.name = stop_node['tag']['name']
              stop.info = ''
              stop.ref = stop_node['tag']['ref']
              stop.save()
              stop_route = stop_route_relation(stop = stop, route = route, direct = direct)
              stop_route.save()
