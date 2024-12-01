document.addEventListener("DOMContentLoaded", function () {
    const generateRouteButton = document.getElementById("generateRoute");
    const routeMapIframe = document.getElementById("routeMap");
    const individualMapsContainer = document.getElementById("buttons-container");
    const generalRouteButton = document.getElementById("generalRouteButton");
    let costChart = null;  // Variable para almacenar la instancia del gráfico

    generateRouteButton.addEventListener("click", function () {
        routeMapIframe.src = "";

        // Limpiar los botones anteriores y el contenedor de detalles
        individualMapsContainer.innerHTML = "";
        document.getElementById("route-details-container")?.remove();
        document.getElementById("general-details-container")?.remove();
        if (costChart) {
            costChart.destroy();  // Destruir el gráfico si ya existe uno
        }

        // Hacer una solicitud GET al servidor Python
        fetch("http://localhost:8000/generar_ruta")
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Error al generar la ruta");
                }
            })
            .then((data) => {
                // Cargar el mapa general
                routeMapIframe.src = "LogisticaPeninsula.html";

                // Crear o actualizar el contenedor de detalles generales
                let generalDetailsContainer = document.createElement("div");
                generalDetailsContainer.id = "general-details-container";
                generalDetailsContainer.className =
                    "mt-4 bg-[var(--white)] border-2 border-[var(--teal)] rounded-lg p-4 shadow-md";

                // Insertar el contenedor debajo del mapa
                const mapSection = document.getElementById("map-section");
                mapSection.appendChild(generalDetailsContainer);

                // Añadir información general sobre las rutas (Número total de camiones y costo total)
                const totalCost = data.routes.reduce((acc, route) => acc + route.route_cost, 0).toFixed(2);
                generalDetailsContainer.innerHTML = `
                    <h3 class="text-lg font-semibold text-[var(--teal)] mb-2">Información General</h3>
                    <p><strong>Total de Camiones:</strong> ${data.routes.length}</p>
                    <p><strong>Costo Total de las Rutas:</strong> ${totalCost} €</p>
                    <div class="mt-4">
                        <canvas id="costChart" width="400" height="200"></canvas>
                    </div>
                `;

                // Crear el gráfico combinado de costos por ruta y envíos
                const ctx = document.getElementById('costChart').getContext('2d');
                const truckLabels = data.routes.map(route => `Camión ${route.truck_id}`);
                const truckCosts = data.routes.map(route => route.route_cost);
                const truckShipments = data.routes.map(route => route.total_shipments);

                costChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: truckLabels,
                        datasets: [
                            {
                                label: 'Costo por Ruta (€)',
                                data: truckCosts,
                                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 1,
                                yAxisID: 'y',
                            },
                            {
                                label: 'Cantidad de Envíos',
                                data: truckShipments,
                                type: 'line',
                                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                borderColor: 'rgba(255, 99, 132, 1)',
                                borderWidth: 2,
                                yAxisID: 'y1',
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Costo (€)'
                                }
                            },
                            y1: {
                                beginAtZero: true,
                                position: 'right',
                                title: {
                                    display: true,
                                    text: 'Cantidad de Envíos'
                                },
                                grid: {
                                    drawOnChartArea: false, // Solo mostrar la cuadrícula principal
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Camiones'
                                }
                            }
                        }
                    }
                });

                // Generar botones para cada ruta
                const totalTrucks = data.routes.length;
                for (let i = 0; i < totalTrucks; i++) {
                    const routeData = data.routes[i];

                    // Crear botón con margen uniforme
                    const button = document.createElement("button");
                    button.textContent = `Ruta Camión ${routeData.truck_id}`;
                    button.className =
                        "w-full px-4 py-2 bg-[var(--teal)] text-white rounded-lg shadow-md hover:bg-[var(--persian-green)] transition mb-2";

                    // Asignar evento para cargar el mapa y mostrar detalles
                    button.addEventListener("click", function () {
                        routeMapIframe.src = `Maps/Truck_${routeData.truck_id}_Route.html`;

                        // Minimizar o eliminar el contenedor de detalles generales
                        const generalDetailsContainer = document.getElementById("general-details-container");
                        if (generalDetailsContainer) {
                            generalDetailsContainer.style.display = "none";
                        }

                        // Crear o actualizar el contenedor de detalles de la ruta específica
                        let routeDetailsContainer = document.getElementById("route-details-container");
                        if (!routeDetailsContainer) {
                            routeDetailsContainer = document.createElement("div");
                            routeDetailsContainer.id = "route-details-container";
                            routeDetailsContainer.className =
                                "mt-4 bg-[var(--white)] border-2 border-[var(--teal)] rounded-lg p-4 shadow-md";

                            // Insertar el contenedor debajo del mapa
                            mapSection.appendChild(routeDetailsContainer);
                        }

                        // Limpiar el contenido previo
                        routeDetailsContainer.innerHTML = "";

                        // Añadir información de la ruta
                        const routeInfo = `
                            <h3 class="text-lg font-semibold text-[var(--teal)] mb-2">Detalles de la Ruta del Camión ${routeData.truck_id}</h3>
                            <p><strong>Conductor:</strong> ${routeData.driver}</p>
                            <details class="bg-gray-100 p-3 rounded-lg shadow-md mb-2">
                                <summary class="font-semibold text-[var(--lapis-lazuli)] cursor-pointer">
                                    Ruta Completa
                                </summary>
                                <ol class="mt-2 text-gray-700 list-decimal ml-5">
                                    ${routeData.full_route.map((location, index) => {
                                        const isDeliveryPoint = routeData.delivery_points.includes(location);
                                        return `
                                            <li class="mb-1">
                                                <strong>Punto ${index + 1}:</strong> 
                                                <span class="${isDeliveryPoint ? 'text-[var(--persian-green)] font-bold' : ''}">
                                                    ${location} ${isDeliveryPoint ? '🚚' : ''}
                                                </span>
                                            </li>
                                        `;
                                    }).join('')}
                                </ol>
                            </details>
                            <p><strong>Costo de la Ruta:</strong> ${routeData.route_cost.toFixed(2)} €</p>
                            <p><strong>Total de Envíos:</strong> ${routeData.total_shipments}</p>
                        `;

                        // Añadir información de los envíos al contenedor de detalles
                        let shipmentsInfo = `
                            <details class="bg-gray-100 p-3 rounded-lg shadow-md mb-2">
                                <summary class="font-semibold text-[var(--lapis-lazuli)] cursor-pointer">
                                    Envíos del Camión
                                </summary>
                                <div class="mt-2 text-gray-700">
                        `;

                        routeData.shipments.forEach((shipment, index) => {
                            // Asignar el destino al envío. Se asume que el destino es uno de los puntos de entrega.
                            const destination = routeData.delivery_points[index % routeData.delivery_points.length] || 'Destino desconocido';

                            shipmentsInfo += `
                                <details class="mb-2 bg-white p-2 rounded-lg shadow">
                                    <summary><strong>Envío ${index + 1} - ID: ${shipment.shipment_id}</strong></summary>
                                    <ul class="ml-4 mt-2 list-disc">
                                        <li><strong>Destino:</strong> ${destination} 🚚</li>
                                        <li><strong>ID del Producto:</strong> ${shipment.product.product_id}</li>
                                        <li><strong>Nombre del Producto:</strong> ${shipment.product.name}</li>
                                        <li><strong>Cantidad:</strong> ${shipment.quantity}</li>
                                        <li><strong>Tiempo de Fabricación:</strong> ${shipment.product.manufacturing_time} días</li>
                                        <li><strong>Vencimiento desde Fabricación:</strong> ${shipment.product.expiration} días</li>
                                    </ul>
                                </details>
                            `;
                        });

                        shipmentsInfo += `</div></details>`;

                        // Combinar información de ruta e información de envíos
                        routeDetailsContainer.innerHTML = routeInfo + shipmentsInfo;
                    });

                    // Añadir botón al contenedor
                    individualMapsContainer.appendChild(button);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                // Mostrar un mensaje de error con SweetAlert2
                Swal.fire({
                    icon: 'error',
                    title: '¡Ups!',
                    text: 'Hubo un problema al intentar generar la ruta.',
                    confirmButtonText: 'Aceptar'
                });
            });
    });

    // Botón "Ruta General"
    generalRouteButton.addEventListener("click", function () {
        // Mostrar confirmación de SweetAlert antes de redirigir
        Swal.fire({
            title: '¿Volver al mapa general?',
            text: "Se perderán los detalles de la ruta actual.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, volver',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                routeMapIframe.src = "LogisticaPeninsula.html";

                // Mostrar nuevamente los detalles generales
                const generalDetailsContainer = document.getElementById("general-details-container");
                if (generalDetailsContainer) {
                    generalDetailsContainer.style.display = "block";
                }

                // Limpiar los detalles de la ruta
                const routeDetailsContainer = document.getElementById("route-details-container");
                if (routeDetailsContainer) {
                    routeDetailsContainer.innerHTML = "";
                }
            }
        });
    });
});
