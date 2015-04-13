#-*- coding: utf-8 -*-

from flask import Flask, send_file, abort, url_for, request, render_template, redirect, Response
from beholder.backend.engine import session as dbsession
from beholder.backend.models import Log
from datetime import datetime

app = Flask(__name__)

DEFAULTSIZE = 20
MAXSIZE = 100
DEFAULTSTART = 0
LOGPARAMS = {
    "eq": ("id", "host", "event", "obj", "subj", "result",),
    "contains": ("event_desc", "obj_desc", "subj_desc", "result_desc",),
    "gte": ("timestamp_from",),
    "lte": ("timestamp_to",)
}

def format_datetime(value, format='ru'):
    if format == 'ru':
        format="%d.%m.%Y %H:%M:%S"
    elif format == 'iso':
        format="%Y.%m.%dT%H:%M:%S"
    return value.strftime(format)

app.jinja_env.filters['format_datetime'] = format_datetime

def datetime_from_iso(sdt):
    return datetime.strptime(sdt, "%Y-%m-%dT%H:%M:%S")   
    
def filter_items(items, args):
    for k, params in LOGPARAMS.items() :
        for param in params :
            if param in args :
                value = args[param]
                if value :
                    if k == "eq" :
                        items = items.filter(getattr(Log, param) == value)
                    elif k == "contains" :
                        items = items.filter(getattr(Log, param).contains(value))
                    elif k == "gte" and param.endswith("_from") :
                        p = param.split("_from")[0]
                        items = items.filter(getattr(Log, p) >= datetime_from_iso(value))
                    elif k == "lte" and param.endswith("_to") :
                        p = param.split("_to")[0]
                        items = items.filter(getattr(Log, p) <= datetime_from_iso(value))
                    else:
                        pass
    return items

@app.route("/items.xml")
def logs_xml():

    size = int(request.args.get("size", DEFAULTSIZE))
    size = size if size <= MAXSIZE else MAXSIZE
    
    start = int(request.args.get("start", DEFAULTSTART))
    
    finish = start + size
    
    s = dbsession()
    
    items = s.query(Log)    
    items = filter_items(items, request.args)
    items_count = items.count()
    items = items[start:finish]
    
    # body = """<logs start="{0}" size="{1}" count="{2}">{3}</logs>""".format(str(start), str(size), str(items_count), "".join(map(repr, items)))
    body = render_template("items.xml", items=items, items_count=items_count, start=start, size=size)
    
    s.close()
    
    return Response(body, mimetype="text/xml")

@app.route("/")    
@app.route("/items.html")
def logs_html():

    size = int(request.args.get("size", DEFAULTSIZE))
    size = size if size <= MAXSIZE else MAXSIZE
    
    start = int(request.args.get("start", DEFAULTSTART))
    
    finish = start + size
    
    s = dbsession()
    
    items = s.query(Log)    
    items = filter_items(items, request.args)
    items_count = items.count()
    items = items[start:finish]
    
    events = s.query(Log.event).distinct()
    
    body = render_template("items.html", items=items, items_count=items_count, events=events)
    
    s.close()
    
    return Response(body, mimetype="text/html")
    
if __name__ == "__main__":
    app.debug = True
    app.run()
