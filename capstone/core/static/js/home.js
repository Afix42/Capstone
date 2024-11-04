let slideIndex = 1; // Comenzar en la primera diapositiva
let slideInterval; // Variable para almacenar el temporizador

// Mostrar la primera diapositiva
showSlides(slideIndex);

// Iniciar el temporizador para cambiar automáticamente de diapositiva
startSlideShow();

// Next/previous controls
function plusSlides(n) {
  clearTimeout(slideInterval); // Detener el temporizador
  slideIndex += n; // Actualizar el índice de la diapositiva
  showSlides(slideIndex); // Mostrar la nueva diapositiva
  startSlideShow(); // Reiniciar el temporizador después de la interacción manual
}

// Thumbnail image controls
function currentSlide(n) {
  clearTimeout(slideInterval); // Detener el temporizador
  slideIndex = n; // Actualizar el índice de la diapositiva
  showSlides(slideIndex); // Mostrar la diapositiva seleccionada
  startSlideShow(); // Reiniciar el temporizador después de la interacción manual
}

// Función para mostrar la diapositiva actual
function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");

  // Si n es mayor que la cantidad de diapositivas, volver al principio
  if (n > slides.length) { slideIndex = 1 }

  // Si n es menor que 1, ir a la última diapositiva
  if (n < 1) { slideIndex = slides.length }

  // Ocultar todas las diapositivas
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  // Quitar la clase 'active' de todos los puntos
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  // Mostrar la diapositiva actual y marcar el punto correspondiente
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

(function () {
  const btnConfirmacion = document.querySelectorAll(".btnConfirmacion");

  btnConfirmacion.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const confirmacion = confirm('¿Seguro que deseas actualizar este producto?');
      if (!confirmacion) {
        e.preventDefault();
      }
    });
  });
})();


