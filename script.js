document.addEventListener("DOMContentLoaded", function() {
    // Botón para generar la ruta
    const generateRouteButton = document.getElementById('generateRoute');
    const routeMapIframe = document.getElementById('routeMap');
    const individualMapsContainer = document.getElementById('buttons-container'); // Contenedor para los botones individuales
    const generalRouteButton = document.getElementById('generalRouteButton');

    generateRouteButton.addEventListener('click', function() {
        routeMapIframe.src = "";

        // Limpiar los botones anteriores de rutas de camiones y la descripción de las rutas
        individualMapsContainer.innerHTML = "";
        document.getElementById('route-details-container')?.remove();

        // Hacer una solicitud GET al servidor Python para generar la ruta
        fetch('http://localhost:8000/generar_ruta')
            .then(response => {
                if (response.ok) {
                    return response.json(); // Recibir los datos como JSON
                } else {
                    throw new Error('Error al generar la ruta');
                }
            })
            .then(data => {
                // Cargar el mapa general en el iframe principal
                routeMapIframe.src = "LogisticaPeninsula.html";

                // Generar los botones para cada ruta individual
                const totalTrucks = data.routes.length; // Número de camiones y rutas
                for (let i = 0; i < totalTrucks; i++) {
                    const routeData = data.routes[i];

                    // Crear un botón para cada ruta de camión
                    const button = document.createElement('button');
                    button.textContent = `Ruta Camión ${routeData.truck_id}`;
                    button.style.display = 'block';
                    button.style.marginBottom = '10px';

                    // Asignar evento para mostrar la ruta del camión correspondiente en el iframe y mostrar los detalles
                    button.addEventListener('click', function() {
                        routeMapIframe.src = `Maps/Truck_${routeData.truck_id}_Route.html`;

                        // Crear o actualizar el contenedor de detalles de la ruta
                        let routeDetailsContainer = document.getElementById('route-details-container');
                        if (!routeDetailsContainer) {
                            routeDetailsContainer = document.createElement('div');
                            routeDetailsContainer.id = 'route-details-container';
                            document.body.appendChild(routeDetailsContainer);
                        }
                        
                        // Limpiar el contenido previo
                        routeDetailsContainer.innerHTML = '';

                        // Añadir la información de la ruta
                        const routeInfo = `
                            <h3>Detalles de la Ruta del Camión ${routeData.truck_id}</h3>
                            <p><strong>Conductor:</strong> ${routeData.driver}</p>
                            <p><strong>Ruta Completa:</strong> ${routeData.full_route}</p>
                            <p><strong>Puntos de Entrega:</strong> ${routeData.delivery_points.join(', ')}</p>
                            <p><strong>Costo de la Ruta:</strong> ${routeData.route_cost.toFixed(2)} €</p>
                        `;
                        routeDetailsContainer.innerHTML = routeInfo;
                    });

                    // Añadir cada botón al contenedor de botones individuales
                    individualMapsContainer.appendChild(button);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un problema al intentar generar la ruta.');
            });
    });

    // Botón "Ruta General" para volver al mapa general
    generalRouteButton.addEventListener('click', function() {
        routeMapIframe.src = "LogisticaPeninsula.html";

        // Limpiar los detalles de la ruta si existen
        const routeDetailsContainer = document.getElementById('route-details-container');
        if (routeDetailsContainer) {
            routeDetailsContainer.innerHTML = '';
        }
    });
});
