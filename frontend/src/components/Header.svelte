<script>
  import { slide, fade } from 'svelte/transition';

  let isOpen = false;

  const toggleMenu = () => {
    isOpen = !isOpen;
    document.body.style.overflow = isOpen ? 'hidden' : 'auto';
  };

  const closeMenu = () => {
    isOpen = false;
    document.body.style.overflow = 'auto';
  };

  /** @param {string} sectionId */
  const scrollToSection = (sectionId) => {
    closeMenu();
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };
</script>

<header class="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-sm text-white shadow-lg transition-all duration-300">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-20">
      
      <!-- Logo interactivo -->
      <a href="#inicio" on:click|preventDefault={() => scrollToSection('inicio')} class="flex-shrink-0 flex items-center gap-2 cursor-pointer hover:scale-105 transition-transform duration-300">
        <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        <span class="font-bold text-xl sm:text-2xl tracking-wider">Premium Real Estate</span>
      </a>
      
      <!-- Navbar / Navegación para Escritorio -->
      <nav class="hidden md:flex items-center space-x-8">
        <button on:click={() => scrollToSection('propiedades')} class="text-gray-300 hover:text-blue-400 font-medium transition-colors duration-300 cursor-pointer">Propiedades</button>
        <button on:click={() => scrollToSection('conocenos')} class="text-gray-300 hover:text-blue-400 font-medium transition-colors duration-300 cursor-pointer">Conócenos</button>
        
        <button on:click={() => scrollToSection('contacto')} class="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2.5 rounded-full font-semibold transition-all duration-300 shadow-md hover:shadow-blue-500/30 hover:-translate-y-0.5 cursor-pointer">
          Agendar Cita
        </button>
      </nav>

      <!-- Botón de Hamburguesa para Celulares y Tablets -->
      <div class="md:hidden flex items-center">
        <button 
          on:click={toggleMenu} 
          aria-label="Abrir menú de navegación"
          class="p-2 rounded-lg text-gray-300 hover:text-white hover:bg-slate-800 focus:outline-none transition-colors"
        >
          {#if isOpen}
            <!-- Icono de X (Cerrar) -->
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          {:else}
            <!-- Icono de Hamburguesa -->
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          {/if}
        </button>
      </div>

    </div>
  </div>

  <!-- Menú Desplegable Móvil en Pantalla Completa (Fixed) -->
  {#if isOpen}
    <!-- Fondo oscuro que cubre toda la pantalla debajo del header y cierra al hacer clic -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="fixed inset-x-0 top-20 bottom-0 bg-slate-950/70 backdrop-blur-sm z-40 md:hidden" transition:fade={{ duration: 150 }} on:click={closeMenu}>
      
      <!-- Contenedor de opciones con stopPropagation para evitar que se cierre al tocar dentro del menú -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <div class="bg-slate-900 border-b border-slate-800 shadow-2xl py-6 px-6 flex flex-col space-y-4" transition:slide={{ duration: 250 }} on:click|stopPropagation>
        <button on:click={() => scrollToSection('propiedades')} class="text-left text-lg font-medium text-gray-300 hover:text-blue-400 py-3 border-b border-slate-800 transition-colors">
          Propiedades
        </button>
        <button on:click={() => scrollToSection('conocenos')} class="text-left text-lg font-medium text-gray-300 hover:text-blue-400 py-3 border-b border-slate-800 transition-colors">
          Conócenos
        </button>
        <button on:click={() => scrollToSection('contacto')} class="w-full text-center py-3.5 rounded-full text-base font-semibold text-white bg-blue-600 hover:bg-blue-500 transition-colors shadow-md mt-2">
          Agendar Cita
        </button>
      </div>
      
    </div>
  {/if}
</header>