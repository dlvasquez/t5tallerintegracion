from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
# from t5
# .Clases.Episode import Episode
# from t5
# .Clases.Character import Character
# from t5
# .Clases.Location import Location

sample_transport = RequestsHTTPTransport(
    url='https://integracion-rick-morty-api.herokuapp.com/graphql',
    verify=False,
    retries=3,
)

client = Client(
    transport=sample_transport,
    fetch_schema_from_transport=True,
)


def homeView(request):

    doc_externo = get_template('index.html')
    query = gql('''
    query {
    episodes(page: 1) {
        info {
        count
        pages
        }
        results {
        name
        episode
        air_date
        id
        }
    }
    }
    ''')
    respuesta = client.execute(query)

    n_pages = respuesta["episodes"]["info"]["pages"]

    episodios = respuesta["episodes"]["results"]

    paginas = []
    for i in range(n_pages):
        url_p = "../episodios/"+str(i+1)
        dic = {"numero": i+1, "url": url_p}
        paginas.append(dic)

    for p in episodios:
        p["local_url"] = "../../episodio/"+str(p["id"])+"/"

    documento = doc_externo.render(
        {"episodios": episodios, "paginas": paginas})
    return HttpResponse(documento)


def episodesView(request, id):
    doc_externo = get_template('episodes.html')

    query = gql('''
        query {
        episodes(page: %d) {
            info {
            count
            pages
            }
            results {
            name
            episode
            air_date
            id
            }
        }
        }
        ''' % (id))
    respuesta = client.execute(query)

    n_pages = respuesta["episodes"]["info"]["pages"]

    episodios = respuesta["episodes"]["results"]

    for p in episodios:
        p["local_url"] = "../../episodio/"+str(p["id"])+"/"

    paginas = []
    for i in range(n_pages):
        url_p = "../../episodios/"+str(i+1)
        dic = {"numero": i+1, "url": url_p}
        paginas.append(dic)

    documento = doc_externo.render(
        {"episodios": episodios, "paginas": paginas})

    return HttpResponse(documento)

# def episodeView(request, id):
#     doc_externo = get_template('episode.html')

#     respuesta = requests.get(
#         'https://integracion-rick-morty-api.herokuapp.com/api/episode/'+str(id))
#     r_episodio = respuesta.json()
#     lista_personajes = []
#     for p in r_episodio["characters"]:
#         answer = requests.get(p).json()
#         lista_personajes.append(
#             {"url": "../../personaje/"+str(answer["id"])+"/", "name": answer["name"], "image": answer["image"]})


#     documento = doc_externo.render(
#         {"episodio": r_episodio, "lista_personajes": lista_personajes})
#     return HttpResponse(documento)

# def charactersView(request, id):
#     doc_externo = get_template('characters.html')
#     if (id):
#         respuesta = requests.get(
#             'https://integracion-rick-morty-api.herokuapp.com/api/character/?page='+str(id))
#     else:
#         respuesta = requests.get(
#             'https: // integracion-rick-morty-api.herokuapp.com/api/character')

#     # respuesta = requests.get(
#     #     'https://integracion-rick-morty-api.herokuapp.com/api/character/?page='+str(id))
#     r_personajes = respuesta.json()
#     lista_personajes = r_personajes["results"]
#     paginas = []
#     info = r_personajes["info"]
#     n_pages = info["pages"]
#     for i in range(n_pages):
#         url_p = "../../personajes/"+str(i+1)
#         dic = {"numero": i+1, "url": url_p}
#         paginas.append(dic)

#     new_list = []
#     for p in lista_personajes:
#         new_list.append(
#             {"url": "../../personaje/"+str(p["id"])+"/", "name": p["name"], "image": p["image"]})

#     documento = doc_externo.render(
#         {"lista_personajes": new_list, "paginas": paginas})
#     return HttpResponse(documento)


# def locationsView(request, id):
#     doc_externo = get_template('locations.html')
#     if (id):
#         respuesta = requests.get(
#             'https://integracion-rick-morty-api.herokuapp.com/api/location/?page='+str(id))
#     else:
#         respuesta = requests.get(
#             'https: // integracion-rick-morty-api.herokuapp.com/api/location')

#     r_lugares = respuesta.json()
#     lista_lugares = r_lugares["results"]
#     paginas = []
#     info = r_lugares["info"]
#     n_pages = info["pages"]
#     for i in range(n_pages):
#         url_p = "../../lugares/"+str(i+1)
#         dic = {"numero": i+1, "url": url_p}
#         paginas.append(dic)

#     new_list = []
#     for p in lista_lugares:
#         new_list.append(
#             {"url": "../../lugar/"+str(p["id"])+"/", "name": p["name"]})

#     documento = doc_externo.render(
#         {"lista_lugares": new_list, "paginas": paginas})
#     return HttpResponse(documento)


# def characterView(request, id):
#     doc_externo = get_template('character.html')
#     respuesta = requests.get(
#         'https://integracion-rick-morty-api.herokuapp.com/api/character/'+str(id)).json()
#     lista_episodios = []
#     lista_lugares = []

#     # buscar episodios
#     for e in respuesta["episode"]:
#         answer = requests.get(e).json()
#         lista_episodios.append(
#             {"url": "../../episodio/"+str(answer["id"])+"/", "name": answer["name"], "episode": answer["episode"]})
#     origin = {}
#     # buscar origin
#     origin_url = respuesta["origin"]["url"]
#     if origin_url:
#         answer_or = requests.get(origin_url).json()
#         origin = {"url": "../../lugar/" +
#                   str(answer_or["id"])+"/", "name": answer_or["name"]}
#     else:
#         origin = {"url": "", "name": respuesta["origin"]["name"]}

#     # buscar location
#     location_url = respuesta["location"]["url"]
#     answer_loc = requests.get(location_url).json()
#     location = {"url": "../../lugar/" +
#                 str(answer_loc["id"])+"/", "name": answer_loc["name"]}

#     documento = doc_externo.render(
#         {"personaje": respuesta, "lista_episodios": lista_episodios, "location": location, "origin": origin})
#     return HttpResponse(documento)


# def placeView(request, id):
#     doc_externo = get_template('location.html')
#     respuesta = requests.get(
#         'https://integracion-rick-morty-api.herokuapp.com/api/location/'+str(id))
#     r_lugar = respuesta.json()
#     lista_personajes = []
#     for p in r_lugar["residents"]:
#         answer = requests.get(p).json()
#         lista_personajes.append(
#             {"url": "../../personaje/"+str(answer["id"])+"/", "name": answer["name"], "image": answer["image"]})

#     documento = doc_externo.render(
#         {"lugar": r_lugar, "lista_residentes": lista_personajes})
#     return HttpResponse(documento)


# def searchView(request):
#     doc_externo = get_template('searchview.html')
#     query = ""
#     if request.GET:
#         query = request.GET["search"]

#     r_episodios = requests.get(
#         'https://integracion-rick-morty-api.herokuapp.com/api/episode/?name='+str(query)).json()
#     r_personajes = requests.get(
#         'https://integracion-rick-morty-api.herokuapp.com/api/character/?name='+str(query)).json()
#     r_lugares = requests.get(
#         'https://integracion-rick-morty-api.herokuapp.com/api/location/?name='+str(query)).json()

#     nueva_personajes = []
#     nueva_episodios = []
#     nueva_lugares = []

#     if len(r_episodios) > 1:
#         lista_episodios = r_episodios["results"]
#         for p in lista_episodios:
#             nueva_episodios.append(
#                 {"url": "../../personaje/"+str(p["id"])+"/", "name": p["name"]})

#     if len(r_personajes) > 1:
#         lista_personajes = r_personajes["results"]
#         for p in lista_personajes:
#             nueva_personajes.append(
#                 {"url": "../../personaje/"+str(p["id"])+"/", "name": p["name"]})

#     if len(r_lugares) > 1:
#         lista_lugares = r_lugares["results"]
#         for p in lista_lugares:
#             nueva_lugares.append(
#                 {"url": "../../lugar/"+str(p["id"])+"/", "name": p["name"]})

#     documento = doc_externo.render({"busqueda": query, "lista_personajes": nueva_personajes,
#                                     "lista_episodios": nueva_episodios, "lista_lugares": nueva_lugares})
#     return HttpResponse(documento)
