function validateLoginForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    // Limpiar el mensaje de error previo
    errorMessage.textContent = '';

    // Validar que el correo electrónico esté en un formato correcto
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errorMessage.textContent = 'Por favor, introduce un correo electrónico válido.';
        return false;
    }

    // Validar que la contraseña no esté vacía
    if (password.length < 6) {
        errorMessage.textContent = 'La contraseña es incorrecta intente de nuevo.';
        return false;
    }

    // Si ambas validaciones se pasan, se envía el formulario
    return true;
}
