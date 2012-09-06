from models import *

def check_duplicated_route(r, l, c):
  for i in range(0, l):
    if r in c[i]:
      return ret
  return False


def route(start, dest):
  direct_routes_candidate = map(lambda stop_route_obj: stop_route_obj.route, stop_route_relation.objects.filter(stop = start))
  direct_routes = []
  print direct_routes_candidate
  for r in direct_routes_candidate:
    x =  stop_route_relation.objects.filter(route = r, stop = dest)
    print r, dest
    if len(x) > 0:
      #direct_routes.append([{'s': start.name}, {'r':r.name}, {'s':[x[0].stop.name]}])
      direct_routes.append(r.name + ': ' + start.name + ' - ' + x[0].stop.name)
      break

  if len(direct_routes) > 0:
    return direct_routes
  print 'lalalala'

  two_level_routes = [[], []]
  '''
  XXX: Brute Force
  '''
  for r in direct_routes_candidate:
    for hub2_stop in stop_route_relation.objects.filter(route = r).exclude(hub = None):
      for r2_start in stop_route_relation.objects.filter(hub = hub2_stop.hub).exclude(route = r):
          if r2_start.route in direct_routes_candidate: #no loop
            continue
          if stop_route_relation.objects.get(route = r2_start.route, stop = dest):
            result = r.name + ': ' + start.name + ' - ' + hub2_stop.stop.name + '<br />'
            result += r2_start.name + ': ' + r2_start.stop.name + ' - ' + dest.name
            two_level_routes[0].append(result)
          elif len(two_level_routes[0]) == 0:
            for hub3_stop in stop_route_relation.objects.filter(router = r2_start.route).exclude(hub = None):
              for r3_start in stop_route_relation.objects.filter(hub = hub3_stop.hub).exclude(hub = None):
                if r3_start.route in direct_routes_candidate:
                  continue
                if stop_route_relation.objects.get(route = r3_start.route, stop = dest):
                  result = r.name + ': ' + start.name + ' - ' + hub2_stop.stop.name + '<br />'
                  result += r2_start.name + ': ' + r2_start.stop.name + ' - ' + hub3_stop.stop.name + '<br />'
                  result += r3_start.name + ': ' + r3_start.stop.name + ' - ' + dest.name
                  two_level_routes[1].append(result)

  if len(two_level_routes[0]) == 0:
    return two_level_routes[1]
  else:
    return two_level_routes[0]
