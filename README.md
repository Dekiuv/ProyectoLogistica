# **Proyecto de Optimización de Rutas y Clusters** 🌍🚚📊

## **Descripción**  
Este proyecto tiene como objetivo desarrollar una herramienta de optimización que combina algoritmos de clustering y cálculo de rutas para resolver problemas de geolocalización y logística. Utilizamos:  

- **K-means** 📈 para agrupar puntos de interés en clusters.  
- **Dijkstra** 🛣️ para calcular las rutas más cortas entre nodos en un grafo.  
- **Folium** 🗺️ para visualizar los resultados en un mapa interactivo.  

El enfoque principal está en facilitar la toma de decisiones logísticas, como planificación de entregas, diseño de rutas de transporte o análisis de distribución de recursos.  

---

## **Características**  
- **Clustering:** 📍 Organización de puntos en grupos eficientes basados en su proximidad geográfica.  
- **Optimización de rutas:** 🛤️ Identificación de las rutas más cortas dentro de cada cluster o entre clusters.  
- **Visualización interactiva:** 🌐 Representación en tiempo real de clusters, rutas y puntos clave en mapas generados con Folium.  

---

## **Tecnologías utilizadas**  
- **Python 3.8+** 🐍  
- **Folium:** Para visualización de mapas interactivos.  
- **Scikit-learn:** Implementación de K-means.  
- **NetworkX:** Implementación del algoritmo de Dijkstra.  
- **Pandas:** Manejo de datos.  
- **NumPy:** Operaciones matemáticas y manipulación de matrices.  
- **SQLite:** Para el manejo de la base de datos.  

---

## **Dependencias**  
El proyecto utiliza las siguientes librerías y versiones específicas:  
📦 **branca** (0.8.0)  
📦 **certifi** (2024.8.30)  
📦 **charset-normalizer** (3.4.0)  
📦 **contourpy** (1.3.1)  
📦 **cycler** (0.12.1)  
📦 **folium** (0.18.0)  
📦 **fonttools** (4.55.0)  
📦 **idna** (3.10)  
📦 **Jinja2** (3.1.4)  
📦 **joblib** (1.4.2)  
📦 **kiwisolver** (1.4.7)  
📦 **MarkupSafe** (3.0.2)  
📦 **matplotlib** (3.9.3)  
📦 **numpy** (2.1.3)  
📦 **packaging** (24.2)  
📦 **pillow** (11.0.0)  
📦 **pyparsing** (3.2.0)  
📦 **python-dateutil** (2.9.0.post0)  
📦 **requests** (2.32.3)  
📦 **scikit-learn** (1.5.2)  
📦 **scipy** (1.14.1)  
📦 **six** (1.16.0)  
📦 **threadpoolctl** (3.5.0)  
📦 **urllib3** (2.2.3)  
📦 **xyzservices** (2024.9.0)  

---

## **Instalación**  
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/Dekiuv/ProyectoLogistica.git
   cd ProyectoLogistica

## **Iniciar el proyecto**  🚀
1. **Crear las tablas e insertar los datos:**  🗂️
   Si no tienes la base de datos inicializada, usa el siguiente comando:  
   ```bash
   python3 insert_data.py

2. **Iniciar programa**🖥️
    Una vez inicializada la base de datos e insertados los datos iniciamos el programa con el siguiente comando:
   ```bash
   python3 main.py
3. **Visualizar los resultados:** 🌐
   Una vez ejecutado el programa abrimos el archivo index.html para visualizar el programa en el navegador.
