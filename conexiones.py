provincias_espana = {
    "A Coruña": ["Lugo", "Pontevedra"],
    "Vitoria": ["Burgos", "San Sebastián", "Logroño", "Pamplona", "Bilbao"],
    "Albacete": ["Alicante", "Ciudad Real", "Cuenca", "Murcia", "Valencia", "Jaen"],
    "Alicante": ["Albacete", "Murcia", "Valencia"],
    "Almeria": ["Granada", "Murcia"],
    "Oviedo": ["Santander", "Leon", "Lugo"],
    "Avila": ["Caceres", "Madrid", "Salamanca", "Segovia", "Toledo", "Valladolid"],
    "Badajoz": ["Caceres", "Cordoba", "Huelva", "Sevilla", "Toledo", "Lisboa"],
    "Barcelona": ["Girona", "Lleida", "Tarragona", "Mataro"],
    "Burgos": ["Vitoria", "Santander", "Logroño", "Leon", "Palencia", "Soria", "Valladolid", "Bilbao", "Segovia"],
    "Caceres": ["Avila", "Badajoz", "Salamanca", "Toledo", "Lisboa"],
    "Cádiz": ["Huelva", "Malaga", "Sevilla"],
    "Santander": ["Oviedo", "Burgos", "Palencia", "Leon", "Bilbao"],
    "Castellon": ["Tarragona", "Teruel", "Valencia"],
    "Ciudad Real": ["Albacete", "Badajoz", "Cordoba", "Cuenca", "Jaen", "Toledo"],
    "Cordoba": ["Badajoz", "Ciudad Real", "Jaen", "Malaga", "Sevilla", "Granada"],
    "Cuenca": ["Albacete", "Ciudad Real", "Guadalajara", "Madrid", "Toledo", "Valencia", "Teruel"],
    "Girona": ["Barcelona", "Lleida", "Andorra", "Mataro"],
    "Granada": ["Almeria", "Córdoba", "Jaen", "Malaga", "Murcia", "Albacete"],
    "Guadalajara": ["Cuenca", "Madrid", "Soria", "Teruel", "Zaragoza", "Segovia"],
    "San Sebastián": ["Vitoria", "Pamplona", "Bilbao"],
    "Huelva": ["Badajoz", "Cadiz", "Sevilla", "Lisboa"],
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
    "Orense": ["Leon", "Lugo", "Pontevedra", "Zamora", "Oporto"],
    "Palencia": ["Burgos", "Santander", "Leon", "Valladolid"],
    "Pontevedra": ["A Coruña", "Lugo", "Orense", "Oporto"],
    "Salamanca": ["Avila", "Caceres", "Zamora", "Valladolid", "Oporto"],
    "Segovia": ["Avila", "Burgos", "Madrid", "Soria", "Valladolid", "Guadalajara"],
    "Sevilla": ["Badajoz", "Cadiz", "Cordoba", "Huelva", "Malaga"],
    "Soria": ["Burgos", "Guadalajara", "Logroño", "Segovia", "Zaragoza"],
    "Tarragona": ["Barcelona", "Castellon", "Lleida", "Teruel", "Zaragoza"],
    "Teruel": ["Castellon", "Cuenca", "Guadalajara", "Tarragona", "Zaragoza", "Valencia"],
    "Toledo": ["Avila", "Badajoz", "Ciudad Real", "Cuenca", "Madrid", "Caceres"],
    "Valencia": ["Albacete", "Alicante", "Castellon", "Cuenca", "Teruel"],
    "Valladolid": ["Avila", "Burgos", "Leon", "Palencia", "Salamanca", "Segovia", "Zamora"],
    "Bilbao": ["Vitoria", "Santander", "San sebastian", "Burgos"],
    "Zamora": ["Leon", "Orense", "Salamanca", "Valladolid", "Oporto"],
    "Zaragoza": ["Guadalajara", "Huesca", "Lleida", "Pamplona", "Soria", "Teruel", "Tarragona", "Logroño"],
    "Oporto": ["Salamanca", "Pontevedra", "Orense", "Zamora", "Lisboa"],
    "Lisboa": ["Badajoz", "Caceres", "Huelva", "Oporto"],
    "Andorra": ["Lleida", "Girona"],
    "Mataro": ["Barcelona", "Girona"]
}

def listar_conexiones(provincias_espana):
    conexiones = set()  # Usamos un set para evitar duplicados
    
    for provincia, limítrofes in provincias_espana.items():
        for limite in limítrofes:
            # Ordenamos la conexión para evitar duplicados bidireccionales
            conexion = tuple(sorted([provincia, limite]))
            conexiones.add(conexion)
    
    # Convertimos el set a una lista de conexiones y la retornamos
    return list(conexiones)