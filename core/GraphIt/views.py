from django.apps.registry import apps
from django.shortcuts import render, redirect
from . import models
import json


def obj_to_dict(obj):
    return obj.__dict__


def index(request):
    plugins = apps.get_app_config('GraphIt').load_components
    return render(request, 'index.html', {})


def load_data(request, id: str):
    request.session['data_plugin'] = id
    plugins = apps.get_app_config('GraphIt').load_components
    
    for plugin in plugins:
        if plugin.identification() == id:
            graph = plugin.load_data("C:\FAKS\MASTER\SOK\SOK_Expresivnes\KarateDataset\\")
            jsonStr = json.dumps(graph.__dict__)
            request.session['complete_graph'] = jsonStr
            request.session['graph'] = jsonStr

    context = {
        "plugini_ucitavanje": plugins,
        "cvorovi": graph.vertices(),  # cvorovi i grane se mogu da se zakomentarisu
        "grane": graph.edges(),
        "tree_json": graph.get_tree(),
        "code": ""
    }

    return render(request, 'graph_view.html', context)


def display_graph(request, id: str):
    request.session['view_plugin'] = id

    plugins = apps.get_app_config('GraphIt').display_components
    try:
        graphDict = json.loads(request.session['graph'])
    except:
        return render(request, 'index.html', {'plugins': plugins})
    graph = models.Graph()
    graph.from_dict(graphDict)
    vert = graph.vertices_dict
    vertices = graph.vertices()
    edges = graph.edges()

    script = None
    code = None
    for plugin in plugins:
        if plugin.identification() == id:
            script = plugin.get_script_path()
            file = open(script)
            code = file.read()

    context = {
        "plugini_ucitavanje": plugins,
        "cvorovi": vert,
        "grane": edges,
        "tree_json": graph.get_tree(),
        "script": script,
        "code": code
    }

    return render(request, 'graph_view.html', context)


def search(request, search_param: str):
    try:
        graphDict = json.loads(request.session['graph'])
        view_plugin = request.session['view_plugin'];

        graph = models.Graph()
        graph.from_dict(graphDict)
        new_graph = graph.search(search_param.replace("|", "/"))

        jsonStr = json.dumps(new_graph.__dict__)
        request.session['graph'] = jsonStr
        ret_val = display_graph(request, view_plugin)
        return ret_val
    except:
        return render(request, 'index.html', {})


def filter(request, search_param: str):
    try:
        graphDict = json.loads(request.session['graph'])
        graph = models.Graph()
        graph.from_dict(graphDict)
        new_graph = graph.filter(search_param.replace("|", "/"))

        jsonStr = json.dumps(new_graph.__dict__)
        request.session['graph'] = jsonStr
        ret_val = display_graph(request, request.session['view_plugin'])
        return ret_val
    except:
        return render(request, 'index.html', {})


def complete_graph(request):
    try:
        request.session['graph'] = request.session['complete_graph']
        ret_val = display_graph(request, request.session['view_plugin'])
    except:
        return render(request, 'index.html', {})
    return ret_val