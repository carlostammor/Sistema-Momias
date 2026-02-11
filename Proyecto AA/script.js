document.addEventListener("DOMContentLoaded", function() {
    const gallery = document.getElementById("gallery");

    // Array de rutas de las imágenes
    const images = [
        "alcholismo.jpg",
        "CHAVAL.jpg",
        "Arbol sangre de dragon.jpg",
        // Añade más rutas de imágenes según sea necesario
    ];

    // Crear elementos de imagen y añadirlos a la galería
    images.forEach(imagePath => {
        const imgElement = document.createElement("img");
        imgElement.src = imagePath;
        imgElement.alt = "alcholismo.jpg";
        gallery.appendChild(imgElement);
    });
});