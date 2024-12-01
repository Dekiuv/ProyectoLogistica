document.addEventListener("DOMContentLoaded", function() {
    // Botón para generar la ruta
    const generateRouteButton = document.getElementById('generateRoute');
    const routeMapIframe = document.getElementById('routeMap');

    generateRouteButton.addEventListener('click', function() {
        routeMapIframe.src = ""
        // Hacer una solicitud GET al servidor Python para generar la ruta
        fetch('http://localhost:8000/generar_ruta')
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al generar la ruta');
                }
            })
            .then(text => {
                routeMapIframe.src = "LogisticaPeninsula.html";
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un problema al intentar generar la ruta.');
            });
    });
});
