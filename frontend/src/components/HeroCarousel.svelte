<script>
  import { onMount } from 'svelte';
  import { reveal } from '../actions.js';
  import { fade, fly } from 'svelte/transition';

  /**
   * @typedef {Object} Property
   * @property {number} id
   * @property {string} title
   * @property {string} price
   * @property {string} desc
   * @property {string} img
   * @property {string} location
   * @property {number} beds
   * @property {number} baths
   * @property {number} parking
   * @property {string} longDesc
   */

  // 1. Array dinámico y estado de carga (reemplaza la data estática)
  /** @type {Property[]} */
  let properties = [];
  let isLoading = true;

  let currentIndex = 0;
  
  const getVisibleCards = () => {
    if (typeof window === 'undefined') return 3;
    if (window.innerWidth < 768) return 1;
    if (window.innerWidth < 1024) return 2;
    return 3;
  };
  
  /** @type {any} */
  let timer;
  /** @type {Property | null} */
  let selectedProperty = null;
  /** @type {Record<number, boolean>} */
  let imagesLoaded = {};

  /** @param {number} id */
  const handleImageLoad = (id) => {
    setTimeout(() => {
      imagesLoaded[id] = true;
    }, 500);
  };

  const next = () => {
    if (properties.length === 0) return;
    const visible = getVisibleCards();
    const maxIndex = properties.length - visible;
    if (maxIndex <= 0) return;
    currentIndex = currentIndex >= maxIndex ? 0 : currentIndex + 1;
  };

  const prev = () => {
    if (properties.length === 0) return;
    const visible = getVisibleCards();
    const maxIndex = properties.length - visible;
    if (maxIndex <= 0) return;
    currentIndex = currentIndex <= 0 ? maxIndex : currentIndex - 1;
  };

  const startAutoPlay = () => {
    if (!selectedProperty && properties.length > getVisibleCards()) {
      timer = setInterval(next, 3500);
    }
  };

  const stopAutoPlay = () => {
    clearInterval(timer);
  };

  /** @param {Property} property */
  const openModal = (property) => {
    selectedProperty = property;
    stopAutoPlay();
  };

  const closeModal = () => {
    selectedProperty = null;
    startAutoPlay();
  };

  const goToContact = () => {
    closeModal();
    const contactSection = document.getElementById('contacto');
    if (contactSection) {
      contactSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // 2. Función que llama a Odoo para pedir las propiedades
  const fetchProperties = async () => {
    try {
      const response = await fetch('http://localhost:8069/api/propiedades');
      const result = await response.json();
      
      if (result.status === 200) {
        properties = result.data;
      } else {
        console.error('Error cargando propiedades:', result.message);
      }
    } catch (error) {
      console.error('Error de red:', error);
    } finally {
      isLoading = false;
      startAutoPlay();
    }
  };

  onMount(() => {
    fetchProperties(); // Cargamos la data al montar el componente
    return stopAutoPlay;
  });
</script>

<section 
  id="propiedades"
  aria-label="Propiedades Destacadas"
  class="min-h-[calc(100vh-5rem)] flex flex-col justify-center w-full bg-gray-50 border-t border-gray-200 py-12 overflow-hidden"
  on:mouseenter={stopAutoPlay}
  on:mouseleave={startAutoPlay}
>
  <div use:reveal class="max-w-7xl mx-auto px-6 sm:px-12 md:px-16 lg:px-24 w-full">
    
    <div class="mb-8 text-center md:text-left">
      <h2 class="text-2xl md:text-3xl font-extrabold text-gray-900">Propiedades Destacadas</h2>
      <p class="text-sm md:text-base text-gray-500 mt-1">Explora nuestro catálogo más exclusivo</p>
    </div>

    <!-- Se añade min-h-[300px] para que no salte el diseño mientras carga -->
    <div class="relative min-h-[300px]">
      
      {#if isLoading}
        <div class="absolute inset-0 flex items-center justify-center z-20">
          <svg class="w-12 h-12 text-blue-600 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      {:else if properties.length === 0}
        <div class="absolute inset-0 flex items-center justify-center z-20 text-gray-500">
          No hay propiedades publicadas en este momento.
        </div>
      {:else}
        <!-- Botón Anterior con aria-label -->
        <button on:click={prev} aria-label="Ver propiedad anterior" class="absolute -left-3 sm:-left-6 md:-left-12 lg:-left-16 top-1/2 -translate-y-1/2 z-10 p-2.5 md:p-3 bg-white rounded-full shadow-lg border border-gray-200 text-blue-600 hover:bg-blue-600 hover:text-white hover:scale-110 transition-all duration-300 cursor-pointer">
          <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </button>

        <div class="overflow-hidden py-2">
          <div 
            class="flex transition-transform duration-500 ease-in-out"
            style="transform: translateX(-{currentIndex * (100 / getVisibleCards())}%);"
          >
            {#each properties as property}
              <div class="w-full sm:w-1/2 lg:w-1/3 flex-none px-2 sm:px-3">
                <div class="bg-white rounded-2xl shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden border border-gray-100 h-full flex flex-col">
                  
                  <div class="relative h-48 sm:h-56 overflow-hidden bg-gray-200">
                    {#if !imagesLoaded[property.id]}
                      <div class="absolute inset-0 bg-gray-200 animate-pulse flex items-center justify-center z-10">
                        <svg class="w-8 h-8 md:w-10 md:h-10 text-gray-300 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                    {/if}

                    <img 
                      src={property.img} 
                      alt={property.title} 
                      loading="lazy" 
                      decoding="async" 
                      on:load={() => handleImageLoad(property.id)}
                      class="w-full h-full object-cover hover:scale-105 transition-all duration-700 {imagesLoaded[property.id] ? 'opacity-100 scale-100' : 'opacity-0 scale-105'}" 
                    />
                    
                    <div class="absolute top-3 right-3 bg-blue-600 text-white px-2.5 py-0.5 rounded-full text-xs md:text-sm font-bold shadow-lg">
                      {property.price}
                    </div>
                  </div>

                  <div class="p-4 sm:p-6 flex-grow flex flex-col">
                    <h3 class="text-lg sm:text-xl font-bold text-gray-900 mb-1.5">{property.title}</h3>
                    <p class="text-gray-600 text-xs sm:text-sm flex-grow mb-4">{property.desc}</p>
                    
                    <button 
                      on:click={() => openModal(property)}
                      class="w-full text-center border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white py-2 rounded-lg text-sm sm:text-base font-medium transition-colors cursor-pointer"
                    >
                      Ver Detalles
                    </button>
                  </div>

                </div>
              </div>
            {/each}
          </div>
        </div>

        <!-- Botón Siguiente con aria-label -->
        <button on:click={next} aria-label="Ver propiedad siguiente" class="absolute -right-3 sm:-right-6 md:-right-12 lg:-right-16 top-1/2 -translate-y-1/2 z-10 p-2.5 md:p-3 bg-white rounded-full shadow-lg border border-gray-200 text-blue-600 hover:bg-blue-600 hover:text-white hover:scale-110 transition-all duration-300 cursor-pointer">
          <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </button>
      {/if}
      
    </div>

    <!-- Paginación dinámica que se oculta si no hay data -->
    {#if properties.length > 0}
      <div class="flex justify-center gap-2 mt-6">
        {#each properties as _, i}
          {@const visible = getVisibleCards()}
          {#if i <= properties.length - visible}
            <div class="h-1.5 rounded-full transition-all duration-500 {i === currentIndex ? 'w-6 sm:w-8 bg-blue-600' : 'w-3 sm:w-4 bg-gray-300'}"></div>
          {/if}
        {/each}
      </div>
    {/if}

  </div>
</section>

<!-- MODAL RESPONSIVE CON ACCESIBILIDAD CORREGIDA -->
{#if selectedProperty}
  {@const prop = selectedProperty}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div 
    class="fixed inset-0 z-[100] flex items-center justify-center p-3 sm:p-4 bg-slate-900/60 backdrop-blur-sm"
    on:click={closeModal}
    transition:fade={{ duration: 150 }}
  >
    <div 
      class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[85vh] overflow-y-auto flex flex-col md:flex-row relative"
      on:click|stopPropagation
      in:fly={{ y: 20, duration: 250 }}
      out:fly={{ y: 20, duration: 150 }}
    >
      <!-- Botón de Cerrar (X) con aria-label -->
      <button 
        aria-label="Cerrar detalles de la propiedad"
        class="absolute top-3 right-3 z-10 bg-white/80 backdrop-blur-md text-gray-800 hover:bg-gray-100 hover:text-red-600 rounded-full p-2 shadow-sm cursor-pointer"
        on:click={closeModal}
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      
      <div class="md:w-1/2 h-56 sm:h-64 md:h-auto relative bg-gray-200 min-h-[240px]">
        {#if !imagesLoaded[prop.id + 100]}
          <div class="absolute inset-0 bg-gray-200 animate-pulse flex items-center justify-center z-10">
            <svg class="w-10 h-10 text-gray-300 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        {/if}

        <img 
          src={prop.img} 
          alt={prop.title} 
          loading="lazy" 
          decoding="async" 
          on:load={() => handleImageLoad(prop.id + 100)}
          class="w-full h-full object-cover {imagesLoaded[prop.id + 100] ? 'opacity-100' : 'opacity-0'} transition-opacity duration-500" 
        />
        <div class="absolute top-3 left-3 bg-blue-600 text-white px-3 py-1 rounded-full text-xs sm:text-sm font-bold shadow-lg">
          {prop.price}
        </div>
      </div>

      <div class="p-6 sm:p-8 md:w-1/2 flex flex-col justify-center">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-1">{prop.title}</h2>
        
        <div class="flex items-center text-gray-500 text-xs sm:text-sm mb-4">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          {prop.location}
        </div>

        <p class="text-gray-600 text-xs sm:text-sm leading-relaxed mb-6">
          {prop.longDesc}
        </p>

        <div class="grid grid-cols-3 gap-2 sm:gap-4 border-t border-b border-gray-100 py-4 mb-6">
          <div class="text-center">
            <span class="block text-xl sm:text-2xl font-bold text-gray-900">{prop.beds}</span>
            <span class="text-[10px] sm:text-xs text-gray-500 uppercase tracking-wider font-medium">Cuartos</span>
          </div>
          <div class="text-center border-l border-r border-gray-100">
            <span class="block text-xl sm:text-2xl font-bold text-gray-900">{prop.baths}</span>
            <span class="text-[10px] sm:text-xs text-gray-500 uppercase tracking-wider font-medium">Baños</span>
          </div>
          <div class="text-center">
            <span class="block text-xl sm:text-2xl font-bold text-gray-900">{prop.parking}</span>
            <span class="text-[10px] sm:text-xs text-gray-500 uppercase tracking-wider font-medium">Puestos</span>
          </div>
        </div>

        <button 
          on:click={goToContact}
          class="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-base sm:text-lg font-bold text-white bg-blue-600 hover:bg-blue-700 hover:shadow-lg cursor-pointer"
        >
          Agendar cita
          <svg class="ml-2 -mr-1 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
        </button>
      </div>

    </div>
  </div>
{/if}