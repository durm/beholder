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

def datetime_from_iso(sdt):
    return datetime.strptime(sdt, "%Y-%m-%dT%H:%M:%S")   
    
def filter_items(items, args):
    for k, params in LOGPARAMS.items() :
        for param in params :
            if param in args :
                if k == "eq" :
                    items = items.filter(getattr(Log, param) == args[param])
                elif k == "contains" :
                    items = items.filter(getattr(Log, param).contains(args[param]))
                elif k == "gte" and param.endswith("_from") :
                    p = param.split("_from")[0]
                    items = items.filter(getattr(Log, p) >= datetime_from_iso(args[param]))
                elif k == "lte" and param.endswith("_to") :
                    p = param.split("_to")[0]
                    items = items.filter(getattr(Log, p) <= datetime_from_iso(args[param]))
                else:
                    pass
    return items

@app.route("/logs.xml")
def logs_xml():

    size = int(request.args.get("size", DEFAULTSIZE))
    size = size if size <= MAXSIZE else MAXSIZE
    
    start = int(request.args.get("start", DEFAULTSTART))
    
    finish = start + size
    
    s = dbsession()
    
    items = s.query(Log)    
    items = filter_items(items, request.args)
    items = items[start:finish]
    
    body = """<logs start="{0}" size="{1}">{2}</logs>""".format(str(start), str(size), "".join(map(repr, items)))
    
    s.close()
    
    return Response(body, mimetype="text/xml")
    
@app.route("/logs.html")
def logs_html():

    size = int(request.args.get("size", DEFAULTSIZE))
    size = size if size <= MAXSIZE else MAXSIZE
    
    start = int(request.args.get("start", DEFAULTSTART))
    
    finish = start + size
    
    s = dbsession()
    
    items = s.query(Log)    
    items = filter_items(items, request.args)
    items = items[start:finish]
    
    body = render_template("logs.html", logs=items)
    
    s.close()
    
    return Response(body, mimetype="text/html")
    
if __name__ == "__main__":
    app.debug = True
    app.run()
