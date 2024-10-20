function mostrarProductos(productoIndex) {
    const tipoSeleccionado = document.getElementById(`tipo_producto${productoIndex}`).value;
    const productosDiv = document.getElementById(`productos${productoIndex}`);

    if (tipoSeleccionado) {
        productosDiv.style.display = 'block'; // Muestra la sección de productos

        // Llama a la función para filtrar los productos según el tipo
        filtrarProductos(productoIndex);
    } else {
        productosDiv.style.display = 'none'; // Oculta si no se selecciona tipo
    }
}

function filtrarProductos(productoIndex) {
    const tipoSeleccionado = document.getElementById(`tipo_producto${productoIndex}`).value;
    const opcionesProducto = document.querySelectorAll(`#producto${productoIndex} option`);

    opcionesProducto.forEach(option => {
        if (option.dataset.tipo !== tipoSeleccionado && tipoSeleccionado) {
            option.style.display = 'none';  // Ocultar producto que no coincide
        } else {
            option.style.display = 'block';  // Mostrar producto que coincide
        }
    });

    // Limpiar la selección actual si el tipo cambia
    document.getElementById(`producto${productoIndex}`).value = "";
    document.getElementById(`info_producto${productoIndex}`).innerHTML = "";  // Limpiar información del producto
}

// Muestra información del producto seleccionado
document.querySelectorAll('select[id^="producto"]').forEach(select => { 
    select.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const infoDiv = document.getElementById(`info_${this.id}`);
        if (selectedOption.value) {
            infoDiv.innerHTML = `
                <img src="${selectedOption.dataset.imagen_uno}" alt="${selectedOption.text}" style="width:200px;height:auto;">
                <p>Precio: $${selectedOption.dataset.precio_producto}</p>
            `;
        } else {
            infoDiv.innerHTML = '';  // Limpiar información si no hay selección
        }
    });
});

