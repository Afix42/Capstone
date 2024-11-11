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

document.addEventListener('DOMContentLoaded', function() {  
    const producto1Select = document.getElementById('producto1');
    const tipoProducto2Select = document.getElementById('tipo_producto2');  // El select del tipo compatible
    const producto2Select = document.getElementById('producto2');
    const productosCompatiblesDiv = document.getElementById('productosCompatibles');
    let productosCompatibles = []; // Variable para almacenar productos compatibles

    // Deshabilitar el select de producto2 y tipo_producto2 inicialmente
    producto2Select.disabled = true;
    tipoProducto2Select.disabled = true;

    producto1Select.addEventListener('change', function() {
        const producto1Id = producto1Select.value;

        if (producto1Id) {
            // Habilitar el select de tipo_producto2 y producto2
            producto2Select.disabled = false;
            tipoProducto2Select.disabled = false;

            fetch(`/ruta-ajax-compatibilidad/?producto1=${producto1Id}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Datos recibidos:', data); // Debug: Verifica que la respuesta es correcta

                    // Limpiar el select de tipo_producto2 y agregar opciones nuevas
                    tipoProducto2Select.innerHTML = '<option value="">--Selecciona un tipo compatible--</option>';
                    if (data.tiposCompatibles && data.tiposCompatibles.length > 0) {
                        data.tiposCompatibles.forEach(tipo => {
                            const option = document.createElement('option');
                            option.value = tipo.id;
                            option.textContent = tipo.nombre_tipo;
                            tipoProducto2Select.appendChild(option);
                        });
                    }

                    // Guardar productos compatibles en la variable para luego filtrarlos
                    productosCompatibles = data.compatibles || [];

                    // Limpiar el select de producto2
                    producto2Select.innerHTML = '<option value="">--Selecciona un producto compatible--</option>';
                    productosCompatiblesDiv.innerHTML = data.mensaje || '';
                })
                .catch(error => console.error('Error en la solicitud AJAX:', error));
        } else {
            tipoProducto2Select.innerHTML = '<option value="">--Selecciona un tipo compatible--</option>';
            producto2Select.innerHTML = '<option value="">--Selecciona un producto compatible--</option>';
            producto2Select.disabled = true;
            tipoProducto2Select.disabled = true;
            productosCompatiblesDiv.innerHTML = "";
        }
    });

// Filtrar productos según el tipo seleccionado en tipo_producto2
tipoProducto2Select.addEventListener('change', function() {
    const tipoProducto2Id = tipoProducto2Select.value;
    const producto1Id = producto1Select.value;

    if (tipoProducto2Id && producto1Id) {
        fetch(`/ruta-ajax-compatibilidad/?producto1=${producto1Id}&tipo_producto2=${tipoProducto2Id}`)
            .then(response => response.json())
            .then(data => {
                producto2Select.innerHTML = '<option value="">--Selecciona un producto compatible--</option>';
                
                // Mostrar solo los productos compatibles con el tipo seleccionado
                if (data.compatibles.length > 0) {
                    data.compatibles.forEach(producto => {
                        const option = document.createElement('option');
                        option.value = producto.id;
                        option.textContent = producto.nombre;
                        option.dataset.imagen_uno = producto.imagen_uno;
                        option.dataset.precio_producto = producto.precio_producto;
                        producto2Select.appendChild(option);
                    });
                    productosCompatiblesDiv.innerHTML = '';
                } else {
                    productosCompatiblesDiv.innerHTML = "No hay productos compatibles para este tipo seleccionado.";
                }
            })
            .catch(error => console.error('Error en la solicitud AJAX:', error));
    }
});

    // Mostrar imagen y precio del producto seleccionado en producto2
    producto2Select.addEventListener('change', function() {
        const selectedOption = producto2Select.options[producto2Select.selectedIndex];
        const infoDiv = document.getElementById('info_producto2');
        if (selectedOption.value) {
            infoDiv.innerHTML = `
                <img src="${selectedOption.dataset.imagen_uno}" alt="${selectedOption.text}" style="width:250px; height:auto; display:block; margin: 0 auto;">
                <p>Precio: $${selectedOption.dataset.precio_producto}</p>
            `;
        } else {
            infoDiv.innerHTML = '';  // Limpiar información si no hay selección
        }
    });
});
