import heapq
import ciudad as ci

provincias_espana = {
    "Andorra": ["Lleida", "Girona"],
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
    "Lisboa": ["Leiria", "Santarem", "Setubal"],
    "Evora": ["Badajoz", "Setubal", "Beja", "Santarem", "Portalegre"],
    "Setubal": ["Beja", "Evora", "Santarem", "Lisboa"],
    "Beja": ["Huelva", "Faro", "Setubal", "Evora"],
    "Faro": ["Huelva", "Beja"]
}


provincias_espana = {
    "Andorra": ["Lleida", "Girona"],
    "A Coruña": ["Lugo", "Pontevedra"],
    "Vitoria": ["Burgos", "San Sebastián", "Logroño", "Pamplona", "Bilbao"],
    "Albacete": ["Alicante", "Ciudad Real", "Cuenca", "Murcia", "Valencia", "Jaén"],
    "Alicante": ["Albacete", "Murcia", "Valencia"],
    "Almería": ["Granada", "Murcia"],
    "Oviedo": ["Santander", "León", "Lugo"],
    "Ávila": ["Cáceres", "Madrid", "Salamanca", "Segovia", "Toledo", "Valladolid"],
    "Badajoz": ["Cáceres", "Córdoba", "Huelva", "Sevilla", "Toledo", "Évora"],
    "Barcelona": ["Girona", "Lleida", "Tarragona", "Mataró"],
    "Burgos": ["Vitoria", "Santander", "Logroño", "León", "Palencia", "Soria", "Valladolid", "Bilbao", "Segovia"],
    "Cáceres": ["Ávila", "Badajoz", "Salamanca", "Toledo", "Castelo Branco", "Portalegre"],
    "Cádiz": ["Huelva", "Málaga", "Sevilla"],
    "Santander": ["Oviedo", "Burgos", "Palencia", "León", "Bilbao"],
    "Castellón": ["Tarragona", "Teruel", "Valencia"],
    "Ciudad Real": ["Albacete", "Badajoz", "Córdoba", "Cuenca", "Jaén", "Toledo"],
    "Córdoba": ["Badajoz", "Ciudad Real", "Jaén", "Málaga", "Sevilla", "Granada"],
    "Cuenca": ["Albacete", "Ciudad Real", "Guadalajara", "Madrid", "Toledo", "Valencia", "Teruel"],
    "Girona": ["Barcelona", "Lleida", "Andorra", "Mataró"],
    "Granada": ["Almería", "Córdoba", "Jaén", "Málaga", "Murcia", "Albacete"],
    "Guadalajara": ["Cuenca", "Madrid", "Soria", "Teruel", "Zaragoza", "Segovia"],
    "San Sebastián": ["Vitoria", "Pamplona", "Bilbao"],
    "Huelva": ["Badajoz", "Cádiz", "Sevilla", "Faro", "Beja"],
    "Huesca": ["Lleida", "Pamplona", "Zaragoza"],
    "Jaén": ["Ciudad Real", "Córdoba", "Granada", "Albacete"],
    "Logroño": ["Vitoria", "Burgos", "Pamplona", "Soria", "Zaragoza"],
    "León": ["Oviedo", "Santander", "Lugo", "Orense", "Palencia", "Valladolid", "Zamora"],
    "Lleida": ["Barcelona", "Girona", "Huesca", "Tarragona", "Zaragoza", "Andorra"],
    "Lugo": ["A Coruña", "Oviedo", "León", "Orense", "Pontevedra"],
    "Madrid": ["Ávila", "Cuenca", "Guadalajara", "Segovia", "Toledo"],
    "Málaga": ["Cádiz", "Córdoba", "Granada", "Sevilla"],
    "Murcia": ["Alicante", "Albacete", "Almería", "Granada"],
    "Pamplona": ["Vitoria", "San Sebastián", "Huesca", "Logroño", "Zaragoza"],
    "Orense": ["León", "Lugo", "Pontevedra", "Zamora", "Viana do Castelo", "Braga", "Bragança"],
    "Palencia": ["Burgos", "Santander", "León", "Valladolid"],
    "Pontevedra": ["A Coruña", "Lugo", "Orense", "Viana do Castelo"],
    "Salamanca": ["Ávila", "Cáceres", "Zamora", "Valladolid", "Bragança", "Guarda"],
    "Segovia": ["Ávila", "Burgos", "Madrid", "Soria", "Valladolid", "Guadalajara"],
    "Sevilla": ["Badajoz", "Cádiz", "Córdoba", "Huelva", "Málaga"],
    "Soria": ["Burgos", "Guadalajara", "Logroño", "Segovia", "Zaragoza"],
    "Tarragona": ["Barcelona", "Castellón", "Lleida", "Teruel", "Zaragoza"],
    "Teruel": ["Castellón", "Cuenca", "Guadalajara", "Tarragona", "Zaragoza", "Valencia"],
    "Toledo": ["Ávila", "Badajoz", "Ciudad Real", "Cuenca", "Madrid", "Cáceres"],
    "Valencia": ["Albacete", "Alicante", "Castellón", "Cuenca", "Teruel"],
    "Valladolid": ["Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Zamora"],
    "Bilbao": ["Vitoria", "Santander", "San Sebastián", "Burgos"],
    "Zamora": ["León", "Orense", "Salamanca", "Valladolid", "Bragança"],
    "Zaragoza": ["Guadalajara", "Huesca", "Lleida", "Pamplona", "Soria", "Teruel", "Tarragona", "Logroño"],
    "Viana do Castelo": ["Pontevedra", "Orense", "Braga"],
    "Braga": ["Viana do Castelo", "Orense", "Porto", "Vila Real"],
    "Vila Real": ["Orense", "Porto", "Braga", "Bragança", "Viseu"],
    "Bragança": ["Vila Real", "Viseu", "Guarda", "Orense", "Zamora", "Salamanca"],
    "Porto": ["Braga", "Vila Real", "Viseu", "Aveiro"],
    "Aveiro": ["Porto", "Viseu", "Coimbra"],
    "Viseu": ["Vila Real", "Bragança", "Guarda", "Coimbra", "Aveiro", "Porto"],
    "Guarda": ["Salamanca", "Castelo Branco", "Coimbra", "Viseu"],
    "Coimbra": ["Leiria", "Castelo Branco", "Guarda", "Viseu", "Aveiro"],
    "Castelo Branco": ["Ávila", "Portalegre", "Santarém", "Leiria", "Coimbra", "Guarda"],
    "Leiria": ["Lisboa", "Santarém", "Castelo Branco", "Coimbra"],
    "Santarém": ["Setúbal", "Évora", "Portalegre", "Castelo Branco", "Leiria", "Lisboa"],
    "Portalegre": ["Ávila", "Évora", "Santarém", "Castelo Branco"],
    "Lisboa": ["Leiria", "Santarém", "Setúbal"],
    "Évora": ["Badajoz", "Setúbal", "Beja", "Santarém", "Portalegre"],
    "Setúbal": ["Beja", "Évora", "Santarém", "Lisboa"],
    "Beja": ["Huelva", "Faro", "Setúbal", "Évora"],
    "Faro": ["Huelva", "Beja"], 
    "Mataró":["Barcelona", "Girona"]
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

