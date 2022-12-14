from django.shortcuts import render
from django.http import HttpResponse
import networkx as nx
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import json
import numpy as np
from networkx.readwrite import json_graph
from django.http import JsonResponse
from networkx.algorithms import community
import itertools
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import k_clique_communities
from networkx import edge_betweenness_centrality as between
import networkx.algorithms.community as nx_comm



# Create your views here.

def index(request):
    G = nx.Graph()
    G.add_edge(1,2)
    return HttpResponse(G.nodes)

@api_view(['POST'])
def getMeasures(request):
    G = nx.Graph()
    x = list(request.body)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # body = dict(body)
    data = body['edges']
    for i in data:
        # print(i)
        edge = [(i['country1_name'],i['country2_name'],i['weight'])]
        G.add_weighted_edges_from(edge)

    # print(nx.get_edge_attributes(G,"weight"))

    b_val = betweenness(G)
    degree_val = degree(G)
    closeness_val = closeness(G)
    eigen_val = eigen(G)
    transitivity_val = transitivity(G)
    pageRank_val = pageRank(G)
    clustering_val = clustering(G)
    girvan_communities = girvan(G,2)
    cross_cliques = crossclique_centrality(G)
    k_clique = k_clique_coms(G)
    modularity_val = modularity_max(G)
    global_clustering_val = global_clustering(G)
    louvian_community_val = louvian_community(G)
    di ={}
    di['betweenness'] = b_val
    di['degree_val'] = degree_val
    di['closeness_val'] = closeness_val
    di['eigen_val'] = eigen_val
    di['transitivity_val'] = transitivity_val
    di['pageRank_val'] = pageRank_val
    di['clustering_val'] = clustering_val

    di['cross-clique'] = cross_cliques
    di['k_clique'] = k_clique
    di['modularity_val'] = modularity_val
    di['girvan_communities'] = girvan_communities
    di['global_clustering_val'] = global_clustering_val
    di['louvian_community'] = louvian_community_val


    res=[]
    res.append(di)
    # print(np.matrix(res))
    return JsonResponse({'data':json.dumps(res)})

def betweenness(G):
    try:
        return nx.betweenness_centrality(G, weight='weight')
    except:
        return {"betweeness":"error"}

def degree(G):
    try:
        return nx.degree_centrality(G)
    except:
        return {"degree":"error"}

def closeness(G):
    try:
        return nx.closeness_centrality(G)
    except:
        return {"closeness":"error"}

def eigen(G):
    try:
        return nx.eigenvector_centrality(G, weight='weight')
    except:
        return {"eigen":"error"}

def transitivity(G):
    try:
        return nx.transitivity(G)
    except:
        return {"transitivity":"error"}

def global_clustering(G):
    try:
        return nx.average_clustering(G)
    except:
        return {"transitivity":"error"}

def pageRank(G):
    try:
        return nx.pagerank_numpy(G,weight='weight')
    except:
        return {"pagerank":"error"}

def clustering(G):
    try:
        return nx.clustering(G,weight="weight")
    except:
        return {"clustering":"error"}

def modularity():
    pass
  
def crossclique_centrality(G):
    cliques=list(nx.find_cliques(G))
    clique1=[]
    for clique in cliques:
      if(len(clique)>2):
        clique1.append(clique)
    cliques=clique1
    cliques_dic = {}
    for c in cliques:
      for value in c:
        if(value in cliques_dic):
          cliques_dic[value] += 1
        else:
          cliques_dic[value] = 1
    return cliques_dic

def modularity_max(G,num_com="Default"):
    if(num_com=="Default"):
      communities= list(greedy_modularity_communities(G,weight="weight"))
    else:
      communities= list(greedy_modularity_communities(G,weight="weight",cutoff=num_com,best_n=num_com))
    com=[]
    for community in communities:
      com.append(list(community))
    return com

def k_clique_coms(G):
    coms = list(k_clique_communities(G, 4))
    com=[]
    for community in coms:
      com.append(list(community))
    return com


def most_central_edge(G):
    centrality = between(G, weight="weight")
    print("arun")
    print(centrality)
    t = max(centrality, key=centrality.get)
    return t

def girvan(G,number_of_communities):
    communities_generator = community.girvan_newman(G)
    array=[]
    for communities in itertools.islice(communities_generator, number_of_communities-1):
      array.append(tuple(sorted(c) for c in communities))
    return array[number_of_communities-2] 

def louvian_community(G):
    coms = list(nx_comm.louvain_communities(G, weight="weight"))
    com=[]
    for community in coms:
      com.append(list(community))
    return com
