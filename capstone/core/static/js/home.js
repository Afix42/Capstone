let slideIndex = 0;
let slideInterval; // Variable para almacenar el temporizador

showSlides();

function plusSlides(n) {
    clearTimeout(slideInterval); // Detener el temporizador actual
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    clearTimeout(slideInterval); // Detener el temporizador actual
    showSlides(slideIndex = n);
}

function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");

    // Remover todas las clases de animación y ocultar todas las diapositivas
    for (i = 0; i < slides.length; i++) {
        slides[i].classList.remove("push-in", "push-out", "show"); // Remover animaciones
        slides[i].style.display = "none"; // Ocultar todas
    }
    
    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    // Mostrar la nueva diapositiva y aplicar la clase para que sea visible
    slides[slideIndex - 1].style.display = "block"; // Mostrar nueva diapositiva
    slides[slideIndex - 1].classList.add("push-in"); // Nueva diapositiva entra
    slides[slideIndex - 1].classList.add("show"); // Hacerla visible

    // Reiniciar el temporizador para cambiar la imagen cada 3 segundos
    slideInterval = setTimeout(showSlides, 8000); // Cambiar imagen cada 3 segundos
}
