document.addEventListener('DOMContentLoaded', () => {
  // Dejar el layout en modo colapsado por defecto
  document.body.classList.add('sidebar-collapsed');

  const leftSidebar = document.querySelector('.left-sidebar');

  if (leftSidebar) {
    // Abrir al entrar con el mouse
    leftSidebar.addEventListener('mouseover', () => {
      document.body.classList.add('sidebar-hover');
    });

    // Cerrar al salir con el mouse
    leftSidebar.addEventListener('mouseout', () => {
      document.body.classList.remove('sidebar-hover');
    });
  }

  // (Opcional) en pantallas táctiles sin hover, podrías luego
  // implementar un botón para alternar 'sidebar-hover' con tap.
});