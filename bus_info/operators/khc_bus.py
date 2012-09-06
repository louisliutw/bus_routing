#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import json
import sys
from lxml import html
from lxml import etree

#bus_routes = [
#      '0北', '0南',
#      '100', '11', '12', '15', '16', '214',
#      '217', '218', '219', '23路高雄客運', '245', '248', '24A', '24B', '25', '26', '28', '29',
#      '3', '30', '301', '33', '36', '37', '38', '39',
#      '52', '53', '56', '5路高雄客運',
#      '6', '60', '62', '69',
#      '7', '70', '72', '73', '76', '77',
#      '81', '82', '83', '87',
#      '91', '92', '99',
#      '大樹區假日觀光公車', '中華幹線', '五福幹線', '仁大接駁專車', '四維-鳳山行政中心接駁專車', '民族幹線', '哈瑪星文化公車', '建國幹線',
#      '紅1', '紅12', '紅16', '紅18', '紅2', '紅20', '紅21', '紅27', '紅28', '紅29',
#      '紅3', '紅30', '紅32', '紅33', '紅35', '紅36',
#      '紅5', '紅50', '紅51', '紅52', '紅53', '紅56', '紅58',
#      '紅6', '紅60', '紅66', '紅68', '紅7', '紅70', '紅71', '紅71B', '紅72', '紅8', '紅9',
#      '國道10號', '痞子英雄專車', '旗山-內門', '旗山-美濃',
#      '橘1', '橘10', '橘20', '橘7', '橘7B', '橘8', '橘9',
#      '環狀西線', '環狀東線', '舊城文化公車']
'''
bus_routes = {
      '820':'紅20',
      '832':'紅32',
      '835':'紅35',
      }
'''

def update_bus_line(route, forward):
   j = {}
   try:
      line = route.name.replace(u'路','')
      print line
   except:
      print sys.exc_info()
      return ''
   j['descript'] = route.name
   j['route_ref'] = route.ref
   print "http://122.146.229.210/bus/pda/businfo.aspx?Routeid=%s&GO_OR_BACK=2&Line=All&lang=Cht" % urllib.quote(line.encode('utf-8'))
   if forward:
      f = urllib.urlopen("http://122.146.229.210/bus/pda/businfo.aspx?Routeid=%s&GO_OR_BACK=1&Line=All&lang=Cht" % urllib.quote(line.encode('utf-8')))
      j['direction'] = 'f'
   else:
      f = urllib.urlopen("http://122.146.229.210/bus/pda/businfo.aspx?Routeid=%s&GO_OR_BACK=2&Line=All&lang=Cht" % urllib.quote(line.encode('utf-8')))
      j['direction'] = 'b'
   content = unicode(f.read(), encoding=f.headers['content-type'].split('charset=')[-1])
   f.close()
   page = html.fromstring(content)
   rows = page.xpath('//td[@id="businfo"]')
   try:
     table = rows[0][1]
   except:
      print sys.exc_info()
      print "http://122.146.229.210/bus/pda/businfo.aspx?Routeid=%s&GO_OR_BACK=2&Line=All&lang=Cht" % urllib.quote(line.encode('utf-8'))
    
   j['stops'] = []
   for tr in  table[0]:
      s = {}
      s['stop_ref'] = tr[2].text
      s['predict_time'] = tr[4].text
      j['stops'].append(s)
   return json.dumps(j)

if __name__ == '__main__': #for test
   print update_bus_line('820')
