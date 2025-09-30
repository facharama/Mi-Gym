document.addEventListener('DOMContentLoaded', () => {
    // Selecciona los elementos por su ID.
    const mainHamburger = document.getElementById('main-hamburger');
    const sidebar = document.querySelector('.sidebar');
    const sidebarCloseBtn = document.getElementById('sidebar-close-btn'); // El ID correcto de tu HTML

    // La función principal para abrir y cerrar el menú.
    const toggleMenu = () => {
        // Alterna la clase 'active' en el sidebar para el efecto de deslizar.
        sidebar.classList.toggle('active');
        // AÑADE ESTA LÍNEA: Alterna la clase 'active' en el botón principal para la animación de 'X'.
        mainHamburger.classList.toggle('active'); 
    };

    // Si los elementos existen, agrega los listeners.
    if (mainHamburger && sidebar && sidebarCloseBtn) {
        // Al hacer clic en el botón principal, se llama a toggleMenu().
        mainHamburger.addEventListener('click', toggleMenu);
        
        // Al hacer clic en el botón dentro del sidebar, también se llama a toggleMenu().
        // Este botón NO necesita la animación de 'X', solo cierra el menú.
        sidebarCloseBtn.addEventListener('click', toggleMenu);

        // Cierra el menú si se hace clic fuera.
        document.addEventListener('click', (event) => {
            const isClickInside = sidebar.contains(event.target) || mainHamburger.contains(event.target);
            if (!isClickInside && sidebar.classList.contains('active')) {
                toggleMenu(); // Usa la misma función para cerrar.
            }
        });
    }

    // Cierra el menú al cambiar a vista de escritorio.
    const checkScreenSize = () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            // AÑADE ESTA LÍNEA: Asegura que el botón principal de hamburguesa también pierda la clase 'active'.
            mainHamburger.classList.remove('active'); 
        }
    };
    window.addEventListener('resize', checkScreenSize);
    checkScreenSize();
});