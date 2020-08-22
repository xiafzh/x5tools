from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime  
import os
import sys

from x5tools.src import main

@csrf_exempt
def tool_entry(request, param):
    get_dict = request.GET
    print("get_dict", get_dict)
    post_dict = request.POST.keys()
    for key in post_dict:
        post_data = json.loads(key)
        break
    print("post_data:", post_data)
    
    res_data = main.entry(post_data)
    print("result:", res_data["res_code"])
    return HttpResponse(json.dumps(res_data, cls=DateEncoder, ensure_ascii=False), content_type="application/json,charset=utf-8");

class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj) 
