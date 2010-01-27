from __future__ import division

import datetime
import json
import urllib2

from apps.poll.models import PollResponse, Choice
from charts.feature_info_request_parser import convert_text_to_dicts
from charts.postcode_name_map import get_name
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render_to_response


def show_stats_on_map(request):
    poll_response = PollResponse.objects.all()
    choices = Choice.objects.all()
    num_response = poll_response.count()
    percentage_string, label_string = '', ''
    for ch in choices:
        num_resp_for_choice = PollResponse.objects.filter(issue = ch)
        percentage = (num_resp_for_choice.count()/num_response) * 100
        percentage_string += ('%.2F'%percentage) + ',' 
        label_string += ch.choice + '|'
    return render_to_response('stats_map.html', {'percentage' : percentage_string[:-1], 'labels' : label_string[:-1]})

def get_stats(request):
    if request.method == 'GET':
        left = request.GET.get('left')
        bottom = request.GET.get('bottom')
        right = request.GET.get('right')
        top = request.GET.get('top')
        x = request.GET.get('x')
        y = request.GET.get('y')
        width = request.GET.get('width')
        height = request.GET.get('height')
        map_params = (left, bottom, right, top, x, y, width, height)
        feature_dict = _get_feature_dict(map_params)
        try:
            place_name = feature_dict['NAME_2']
            post_code = get_name(place_name)
            if post_code != "Not Found":
               num_resp_for_postcode = PollResponse.objects.filter(location = post_code)
               choices = Choice.objects.all()
               percentage_string, label_string = '', ''
               for ch in choices:
                   num_resp = PollResponse.objects.filter(issue = ch, location = post_code)
                   percentage = ((num_resp.count())/num_resp_for_postcode.count()) * 100
                   percentage_string += ('%.2F'%percentage) + ','
                   label_string += ch.choice + '|'
               data_dict = {'has_stats' : 'true', 'label' : label_string[:-1], 'percentage' : percentage_string[:-1], 'place_name' : place_name}
               return _dump_json_and_get_http_response(data_dict)
            else:
                data_dict = {'has_stats' : 'false', 'place_name' : 'Iraq'}
                return _dump_json_and_get_http_response(data_dict)
        except KeyError:
            data_dict = {'has_stats' : 'false', 'place_name' : 'Iraq'}
            return _dump_json_and_get_http_response(data_dict)
        return HttpResponse("OK")
        
def _dump_json_and_get_http_response(json_data_dict):
    json_data = json.dumps(json_data_dict)
    response = HttpResponse()
    response.write(json_data)
    return response
    
def _get_feature_dict(map_args):
    url = ("http://127.0.0.1/geoserver/wms?REQUEST=GetFeatureInfo&\
EXCEPTIONS=application/vnd.ogc.se_xml&BBOX=%s,%s,%s,%s&X=%s&Y=%s&INFO_FORMAT=text/plain&\
QUERY_LAYERS=GADM:IRQ_adm2&FEATURE_COUNT=50&Layers=GADM:IRQ_adm2&Styles=&Srs=EPSG:4326&\
WIDTH=%s&HEIGHT=%s&format=image/png" % map_args)
    request = urllib2.urlopen(url)        
    response_dict = request.read()
    return convert_text_to_dicts(response_dict)
    
    
def current_status(self):
    now = datetime.datetime.now()
    return render_to_response('charts.html')

def data(self):
    return HttpResponse('junk')
    
def view_404(request):
    response = HttpResponseNotFound()
    response.write("The path is not found")
    return response

def view_500(request):
    response = HttpResponseServerError()
    response.write("Something went wrong")
    return response

def _get_stats_for_place(place_name):
    pass
