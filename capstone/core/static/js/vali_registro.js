function validateRegisterForm() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const errorMessage = document.getElementById('error-message');
    
    // Limpiar el mensaje de error previo
    errorMessage.textContent = '';

    // Validar que el nombre de usuario no esté vacío y tenga al menos 3 caracteres
    if (username === '' || username.length < 3) {
        errorMessage.textContent = 'El nombre de usuario debe tener al menos 3 caracteres.';
        return false;
    }

    // Validar el formato del correo electrónico
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errorMessage.textContent = 'Por favor, introduce un correo electrónico válido.';
        return false;
    }

    // Validar la longitud mínima de la contraseña
    if (password.length < 6) {
        errorMessage.textContent = 'La contraseña debe tener al menos 6 caracteres.';
        return false;
    }

    // Validaciones adicionales de la contraseña
    const missingRequirements = [];
    const uppercaseRegex = /[A-Z]/; // Para al menos una mayúscula
    const numberRegex = /\d/;       // Para al menos un número
    const specialCharRegex = /[!@#$%^&*]/; // Para al menos un carácter especial

    if (!uppercaseRegex.test(password)) {
        missingRequirements.push('una letra mayúscula');
    }
    if (!numberRegex.test(password)) {
        missingRequirements.push('un número');
    }
    if (!specialCharRegex.test(password)) {
        missingRequirements.push('un carácter especial (!@#$%^&*)');
    }

    // Si alguna de las validaciones falla, mostrar los mensajes acumulados
    if (missingRequirements.length > 0) {
        errorMessage.textContent = 'La contraseña debe contener al menos: ' + missingRequirements.join(', ') + '.';
        return false;
    }

    // Validar que las contraseñas coincidan
    if (password !== confirmPassword) {
        errorMessage.textContent = 'Las contraseñas no coinciden.';
        return false;
    }

    // Si pasa todas las validaciones, el formulario se envía
    return true;
}
