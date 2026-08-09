<script>
  import { reveal } from '../actions.js';

  /** @param {string} sectionId */
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };
</script>

<section id="inicio" class="min-h-[calc(100vh-5rem)] flex items-center bg-white py-12 overflow-hidden">
  <div use:reveal class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
    <!-- En celulares y tablets es de 1 columna. En computadoras (md) pasa a 2 columnas -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center">
      
      <!-- Columna de Texto -->
      <div class="text-center md:text-left z-10">
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-gray-900 mb-4 sm:mb-6 tracking-tight leading-tight">
          Bienvenido a <span class="text-blue-600">Premium Real Estate</span>
        </h1>
        <p class="text-base sm:text-lg md:text-xl text-gray-500 leading-relaxed mb-6 font-light">
          Transformamos la búsqueda de propiedades en una experiencia exclusiva. 
          Descubre hogares extraordinarios diseñados para elevar tu estilo de vida, 
          acompañado por expertos que entienden el verdadero valor de tu inversión.
        </p>
        
        <!-- Botones de Acción Rápida: Visibles SOLO en celulares y tablets (md:hidden los oculta en PC) -->
        <div class="flex flex-col sm:flex-row justify-center gap-3 mt-6 md:hidden">
          <button 
            on:click={() => scrollToSection('propiedades')} 
            class="w-full sm:w-auto px-7 py-3.5 rounded-xl text-sm sm:text-base font-bold text-white bg-blue-600 hover:bg-blue-700 transition-colors shadow-md"
          >
            Ver Propiedades
          </button>
          <button 
            on:click={() => scrollToSection('contacto')} 
            class="w-full sm:w-auto px-7 py-3.5 rounded-xl text-sm sm:text-base font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 border border-gray-200 transition-colors"
          >
            Contáctanos
          </button>
        </div>
      </div>

      <!-- Columna de Imagen: Oculta en celulares y tablets, visible SOLO en computadoras (hidden md:flex) -->
      <div class="hidden md:flex justify-end items-end relative mt-6 md:mt-0">
        <img src="/realtor.png" alt="Realtor" class="w-full max-w-sm md:max-w-md max-h-[65vh] object-contain drop-shadow-2xl" />
      </div>

    </div>
  </div>
</section>