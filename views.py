from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import PlayerForm
# Create your views here.
import pymysql.cursors
import networkx as nx
import json

def findPlayerName(uscf_id):
    f = open("playerdata.txt", "r")
    players = json.load(f)
    playername = ""
    for dct in players:
        if dct['uscf_id'] == uscf_id:
            playername = dct['playername']
            break
    f.close()
    return playername

def checkForPlayer(uscf_id):
    f = open("playerdata.txt", "r")
    players = json.load(f)
    playercheck = False
    for dct in players:
        if dct['uscf_id'] == uscf_id:
            playercheck = True
            break
    f.close()
    return playercheck

def putGamesIntoGraph(listofgames):
    G = nx.DiGraph()
    for game in listofgames:
        G.add_edge(game['player1_id'],game['player2_id'])
    return G

def findPath(player1_id, player2_id, listofgames):
    graph = putGamesIntoGraph(listofgames)
    player1name = findPlayerName(player1_id)
    player2name = findPlayerName(player2_id)
    try:
        path = nx.shortest_path(graph, source=player1_id, target=player2_id)
    except nx.NetworkXNoPath:
        return "There is no path from " + player1name + " (uscf id: " + str(player1_id) + ") to get to " + player2name + " (uscf id: " + str(player2_id) + ")."
    pathstr = ""
    pathstr += "The total number of games for " + player1name + " (uscf id: " + str(player1_id) + ") to get to " + player2name + " (uscf id: " + str(player2_id) + ") is " + str(len(path) - 1) + ".\n"
    pathstr += "Here are the games:\n"
    previd = player1_id
    prevname = player1name
    for oppoid in path[1:]:
        opponame = findPlayerName(oppoid)
        pathstr += prevname + " (uscf id: " + str(previd) + ") beat " + opponame + " (uscf id: " + str(oppoid) + ").\n"
        prevname = opponame
        previd = oppoid
    return pathstr

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@csrf_exempt
def path(request):
    form = PlayerForm(request.POST) # A form bound to the POST data
    if form.is_valid():
        player1_id = form.cleaned_data['player1id']
        player2_id = form.cleaned_data['player2id']
        try:
            player1_id = int(player1_id)
        except:
            return render(request, 'index.html', player1notnum = True)
        try:
            player2_id = int(player2_id)
        except:
            return render(request, 'index.html', player2notnum = True)
        f = open("gamedata.txt", "r")
        games = json.load(f)
        f.close()
        if not checkForPlayer(player1_id):
            ret = {'player1notfound':True}
            return render(request, 'index.html', ret)
        if not checkForPlayer(player2_id):
            ret = {'player2notfound':True}
            return render(request, 'index.html', ret)
        ret = {'pathstr':findPath(player1_id, player2_id, games)}
        return render(request, 'path.html', ret)
    return index(request)
    #return HttpResponseRedirect('/thanks/') # Redirect after POST
    #player1_id =
    #player2_id =
    #findPath(player1_id, player2_id)
