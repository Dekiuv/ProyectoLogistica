import heapq
import ciudad as ci

provincias_espana = {
    "A Coruña": ["Lugo", "Pontevedra"],
    "Vitoria": ["Burgos", "San Sebastian", "Logroño", "Pamplona", "Bilbao"],
    "Albacete": ["Alicante", "Ciudad Real", "Cuenca", "Murcia", "Valencia", "Jaen"],
    "Alicante": ["Albacete", "Murcia", "Valencia"],
    "Almeria": ["Granada", "Murcia"],
    "Oviedo": ["Santander", "Leon", "Lugo"],
    "Avila": ["Caceres", "Madrid", "Salamanca", "Segovia", "Toledo", "Valladolid"],
    "Badajoz": ["Caceres", "Cordoba", "Huelva", "Sevilla", "Toledo", "Evora"],
    "Barcelona": ["Girona", "Lleida", "Tarragona", "Mataro"],
    "Burgos": ["Vitoria", "Santander", "Logroño", "Leon", "Palencia", "Soria", "Valladolid", "Bilbao", "Segovia"],
    "Caceres": ["Avila", "Badajoz", "Salamanca", "Toledo", "Castelo branco", "Portalegre"],
    "Cadiz": ["Huelva", "Malaga", "Sevilla"],
    "Santander": ["Oviedo", "Burgos", "Palencia", "Leon", "Bilbao"],
    "Castellon": ["Tarragona", "Teruel", "Valencia"],
    "Ciudad Real": ["Albacete", "Badajoz", "Cordoba", "Cuenca", "Jaen", "Toledo"],
    "Cordoba": ["Badajoz", "Ciudad Real", "Jaen", "Malaga", "Sevilla", "Granada"],
    "Cuenca": ["Albacete", "Ciudad Real", "Guadalajara", "Madrid", "Toledo", "Valencia", "Teruel"],
    "Girona": ["Barcelona", "Lleida", "Andorra", "Mataro"],
    "Granada": ["Almeria", "Cordoba", "Jaen", "Malaga", "Murcia", "Albacete"],
    "Guadalajara": ["Cuenca", "Madrid", "Soria", "Teruel", "Zaragoza", "Segovia"],
    "San Sebastian": ["Vitoria", "Pamplona", "Bilbao"],
    "Huelva": ["Badajoz", "Cadiz", "Sevilla", "Faro", "Beja"],
    "Huesca": ["Lleida", "Pamplona", "Zaragoza"],
    "Jaen": ["Ciudad Real", "Cordoba", "Granada", "Albacete"],
    "Logroño": ["Vitoria", "Burgos", "Pamplona", "Soria", "Zaragoza"],
    "Leon": ["Oviedo", "Santander", "Lugo", "Orense", "Palencia", "Valladolid", "Zamora"],
    "Lleida": ["Barcelona", "Girona", "Huesca", "Tarragona", "Zaragoza", "Andorra"],
    "Lugo": ["A Coruña", "Oviedo", "Leon", "Orense", "Pontevedra"],
    "Madrid": ["Avila", "Cuenca", "Guadalajara", "Segovia", "Toledo"],
    "Malaga": ["Cadiz", "Cordoba", "Granada", "Sevilla"],
    "Murcia": ["Alicante", "Albacete", "Almeria", "Granada"],
    "Pamplona": ["Vitoria", "San Sebastian", "Huesca", "Logroño", "Zaragoza"],
    "Orense": ["Leon", "Lugo", "Pontevedra", "Zamora", "Viana do castelo", "Braga", "Braganca"],
    "Palencia": ["Burgos", "Santander", "Leon", "Valladolid"],
    "Pontevedra": ["A Coruña", "Lugo", "Orense", "Viana do castelo"],
    "Salamanca": ["Avila", "Caceres", "Zamora", "Valladolid", "Braganca", "Guarda"],
    "Segovia": ["Avila", "Burgos", "Madrid", "Soria", "Valladolid", "Guadalajara"],
    "Sevilla": ["Badajoz", "Cadiz", "Cordoba", "Huelva", "Malaga"],
    "Soria": ["Burgos", "Guadalajara", "Logroño", "Segovia", "Zaragoza"],
    "Tarragona": ["Barcelona", "Castellon", "Lleida", "Teruel", "Zaragoza"],
    "Teruel": ["Castellon", "Cuenca", "Guadalajara", "Tarragona", "Zaragoza", "Valencia"],
    "Toledo": ["Avila", "Badajoz", "Ciudad Real", "Cuenca", "Madrid", "Caceres"],
    "Valencia": ["Albacete", "Alicante", "Castellon", "Cuenca", "Teruel"],
    "Valladolid": ["Avila", "Burgos", "Leon", "Palencia", "Salamanca", "Segovia", "Zamora"],
    "Bilbao": ["Vitoria", "Santander", "San Sebastian", "Burgos"],
    "Zamora": ["Leon", "Orense", "Salamanca", "Valladolid", "Braganca"],
    "Zaragoza": ["Guadalajara", "Huesca", "Lleida", "Pamplona", "Soria", "Teruel", "Tarragona", "Logroño"],
    "Viana do castelo": ["Pontevedra", "Orense", "Braga"],
    "Braga": ["Viana do castelo", "Orense", "Porto", "Vila real"],
    "Vila real": ["Orense", "Porto", "Braga", "Braganca", "Viseu"],
    "Braganca": ["Vila real", "Viseu", "Guarda", "Orense", "Zamora", "Salamanca"],
    "Porto": ["Braga", "Vila real", "Viseu", "Aveiro"],
    "Aveiro": ["Porto", "Viseu", "Coimbra"],
    "Viseu": ["Vila real", "Braganca", "Guarda", "Coimbra", "Aveiro", "Porto"],
    "Guarda": ["Salamanca", "Castelo branco", "Coimbra", "Viseu"],
    "Coimbra": ["Leiria", "Castelo branco", "Guarda", "Viseu", "Aveiro"],
    "Castelo branco": ["Caceres", "Portalegre", "Santarem", "Leiria", "Coimbra", "Guarda"],
    "Leiria": ["Lisboa", "Santarem", "Castelo branco", "Coimbra"],
    "Santarem": ["Setubal", "Evora", "Portalegre", "Castelo branco", "Leiria", "Lisboa"],
    "Portalegre": ["Caceres", "Evora", "Santarem", "Castelo branco"],
    "Lisboa": ["Leiria", "Santarem"],
    "Evora": ["Badajoz", "Setubal", "Beja", "Santarem", "Portalegre"],
    "Setubal": ["Beja", "Evora", "Santarem"],
    "Beja": ["Huelva", "Faro", "Setubal", "Evora"],
    "Faro": ["Huelva", "Beja"]
}

def listar_conexiones(provincias_espana):
    # Usamos set para evitar duplicados
    conexiones = set()
    for provincia, limítrofes in provincias_espana.items():
        for limite in limítrofes:
            # Ordenamos la conexión para evitar duplicados bidireccionales
            conexion = tuple(sorted([provincia, limite]))
            conexiones.add(conexion)
    
    # Convertimos el set a una lista de conexiones y la retornamos
    return list(conexiones)

def dijkstra(conexiones, ubicaciones, origen, destino):
    grafo = {ciudad: {} for ciudad in ubicaciones.keys()}
    for (ciudad1, ciudad2) in conexiones:
        if ciudad1 in ubicaciones and ciudad2 in ubicaciones:
            distancia = ((ubicaciones[ciudad1][0] - ubicaciones[ciudad2][0]) ** 2 + (ubicaciones[ciudad1][1] - ubicaciones[ciudad2][1]) ** 2) ** 0.5
            grafo[ciudad1][ciudad2] = distancia
            grafo[ciudad2][ciudad1] = distancia

    cola = [(0, origen, [])]
    visitados = set()

    while cola:
        (coste, actual, camino) = heapq.heappop(cola)
        if actual in visitados:
            continue
        camino = camino + [actual]
        if actual == destino:
            return camino
        visitados.add(actual)
        for vecino, peso in grafo[actual].items():
            if vecino not in visitados:
                heapq.heappush(cola, (coste + peso, vecino, camino))
    return []