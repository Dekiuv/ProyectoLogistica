document.addEventListener("DOMContentLoaded", function () {
    const generateRouteButton = document.getElementById("generateRoute");
    const routeMapIframe = document.getElementById("routeMap");
    const individualMapsContainer = document.getElementById("buttons-container");
    const generalRouteButton = document.getElementById("generalRouteButton");
    const mapSection = document.getElementById("map-section");
    const buttonsSection = document.getElementById("buttons-section");
    const constantsForm = document.getElementById("constantsForm");
    const constantsFormContainer = document.getElementById("constantsFormContainer");
    let costChart = null;  // Variable para almacenar la instancia del gráfico de costos
    let profitChart = null; // Variable para almacenar la instancia del gráfico de beneficios

    // Inicialmente ocultar el iframe del mapa y el contenedor de las rutas y el botón de generar ruta
    mapSection.style.display = "none";
    buttonsSection.style.display = "none";
    generateRouteButton.disabled = true;

    // Manejar el envío del formulario de constantes
    constantsForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Evitar el envío por defecto

        // Recopilar valores del formulario
        const constants = {
            velocity: document.getElementById("velocity").value,
            workdayTime: document.getElementById("workdayTime").value,
            restTime: document.getElementById("restTime").value,
            driversHourlyPay: document.getElementById("driversHourlyPay").value,
            fuelCostKm: document.getElementById("fuelCostKm").value,
            truckCapacity: document.getElementById("truckCapacity").value,
        };

        // Enviar valores al servidor
        fetch("http://localhost:8000/set_constants", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(constants),
        })
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Error al enviar la configuración");
            }
        })
        .then((data) => {
            Swal.fire({
                icon: "success",
                title: "¡Configuración enviada!",
                text: "Ahora puedes generar las rutas.",
                confirmButtonText: "Aceptar",
            });
            generateRouteButton.disabled = false; // Habilitar el botón de generar ruta
            constantsFormContainer.style.display = "none"; // Ocultar el formulario
        })
        .catch((error) => {
            console.error("Error:", error);
            Swal.fire({
                icon: "error",
                title: "¡Ups!",
                text: "Hubo un problema al enviar la configuración.",
                confirmButtonText: "Aceptar",
            });
        });
    });

    // Crear e insertar el indicador de carga (barra de progreso y spinner)
    const loadingContainer = document.createElement("div");
    loadingContainer.id = "loadingContainer";
    loadingContainer.className = "fixed top-0 left-0 w-full h-full flex items-center justify-center bg-[rgba(255,255,255,0.8)] hidden";
    loadingContainer.innerHTML = `
        <div class="text-center flex flex-col items-center">
            <div class="loader ease-linear rounded-full border-8 border-t-8 border-[var(--teal)] h-16 w-16 mb-4"></div>
            <h2 class="text-[var(--teal)] text-xl font-semibold mb-2">Generando rutas...</h2>
            <p class="text-[var(--teal)] mb-4">Por favor, espere un momento.</p>
        </div>
    `;
    document.body.appendChild(loadingContainer);

    // Estilos CSS para el loader y barra de progreso
    const loaderStyle = document.createElement("style");
    loaderStyle.innerHTML = `
        .loader {
            border-top-color: #3498db;
            -webkit-animation: spinner 1s linear infinite;
            animation: spinner 1s linear infinite;
        }

        @-webkit-keyframes spinner {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes spinner {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(loaderStyle);

    generateRouteButton.addEventListener("click", function () {
        // Mostrar el indicador de carga
        loadingContainer.classList.remove("hidden");

        // Ocultar el mapa y los contenedores antes de generar la ruta
        mapSection.style.display = "none";
        buttonsSection.style.display = "none";

        // Limpiar los botones anteriores y el contenedor de detalles
        individualMapsContainer.innerHTML = "";
        document.getElementById("route-details-container")?.remove();
        document.getElementById("general-details-container")?.remove();
        if (costChart) {
            costChart.destroy();  // Destruir el gráfico de costos si ya existe uno
        }
        if (profitChart) {
            profitChart.destroy(); // Destruir el gráfico de beneficios si ya existe uno
        }

        // Hacer una solicitud GET al servidor Python para generar la ruta
        fetch("http://localhost:8000/generar_ruta")
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Error al generar la ruta");
                }
            })
            .then((data) => {
                // Ocultar el indicador de carga
                loadingContainer.classList.add("hidden");

                // Mostrar el mapa y los contenedores después de generar las rutas
                mapSection.style.display = "block";
                buttonsSection.style.display = "block";

                // Cargar el mapa general
                routeMapIframe.src = "LogisticaPeninsula.html";

                // Crear o actualizar el contenedor de detalles generales
                let generalDetailsContainer = document.createElement("div");
                generalDetailsContainer.id = "general-details-container";
                generalDetailsContainer.className =
                    "mt-4 bg-[var(--white)] border-2 border-[var(--teal)] rounded-lg p-4 shadow-md fade-in";

                // Insertar el contenedor debajo del mapa
                mapSection.appendChild(generalDetailsContainer);

                // Añadir información general sobre las rutas (Número total de camiones, costo total, ingresos totales, ganancia neta)
                const totalCost = data.total_cost.toFixed(2);
                const totalRevenue = data.best_total_revenue.toFixed(2);
                const netProfit = data.best_net_profit.toFixed(2);
                const netProfitClass = netProfit >= 0 ? 'text-green-600' : 'text-red-600';

                generalDetailsContainer.innerHTML = `
                    <h3 class="text-lg font-semibold text-[var(--teal)] mb-2">Información General</h3>
                    <p><strong>Total de Camiones:</strong> ${data.routes.length}</p>
                    <p><strong>Costo Total de las Rutas:</strong> ${totalCost} €</p>
                    <p><strong>Ingresos Totales de los Envíos:</strong> ${totalRevenue} €</p>
                    <p><strong>Ganancia Neta:</strong> <span class="font-bold ${netProfitClass}">${netProfit} €</span></p>

                    <div class="mt-4">
                        <canvas id="costChart" width="400" height="200"></canvas>
                    </div>
                    <div class="mt-4">
                        <canvas id="profitChart" width="400" height="200"></canvas>
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
                                    drawOnChartArea: false,
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

                // Crear el gráfico de ganancias por ruta
                const profitCtx = document.getElementById('profitChart').getContext('2d');
                const truckProfits = data.routes.map(route => {
                    const routeRevenue = route.shipments.reduce((acc, shipment) => acc + (shipment.product.price * shipment.quantity), 0);
                    return (routeRevenue - route.route_cost).toFixed(2);
                });

                profitChart = new Chart(profitCtx, {
                    type: 'bar',
                    data: {
                        labels: truckLabels,
                        datasets: [
                            {
                                label: 'Ganancia Neta por Ruta (€)',
                                data: truckProfits,
                                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1
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
                                    text: 'Ganancia Neta (€)'
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
                                "mt-4 bg-[var(--white)] border-2 border-[var(--teal)] rounded-lg p-4 shadow-md fade-in";

                            // Insertar el contenedor debajo del mapa
                            mapSection.appendChild(routeDetailsContainer);
                        }

                        // Limpiar el contenido previo
                        routeDetailsContainer.innerHTML = "";

                        // Añadir información de la ruta
                        const routeRevenue = routeData.shipments.reduce((acc, shipment) => acc + (shipment.product.price * shipment.quantity), 0).toFixed(2);
                        const routeProfit = (routeRevenue - routeData.route_cost).toFixed(2);

                        const routeInfo = `
                            <h3 class="text-lg font-semibold text-[var(--teal)] mb-2">Detalles de la Ruta del Camión ${routeData.truck_id}</h3>
                            <p><strong>Conductor:</strong> ${routeData.driver}</p>
                            <p><strong>Ingresos por la Ruta:</strong> ${routeRevenue} €</p>
                            <p><strong>Ganancia Neta de la Ruta:</strong> ${routeProfit} €</p>
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
                                        <li><strong>Precio:</strong> ${shipment.product.price} €</li>
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
                // Ocultar el indicador de carga en caso de error
                loadingContainer.classList.add("hidden");

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
                    routeDetailsContainer.remove();
                }
            }
        });
    });
});
