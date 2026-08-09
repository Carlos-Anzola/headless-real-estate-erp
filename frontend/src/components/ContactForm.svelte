<script>
  import { reveal } from '../actions.js';
  import { fly, fade } from 'svelte/transition';

  const countries = [
    { code: '+58', flag: '🇻🇪', name: 'Venezuela' },
    { code: '+1', flag: '🇺🇸', name: 'Estados Unidos' },
    { code: '+34', flag: '🇪🇸', name: 'España' },
    { code: '+57', flag: '🇨🇴', name: 'Colombia' },
    { code: '+52', flag: '🇲🇽', name: 'México' },
    { code: '+54', flag: '🇦🇷', name: 'Argentina' },
    { code: '+56', flag: '🇨🇱', name: 'Chile' },
    { code: '+51', flag: '🇵🇪', name: 'Perú' }
  ];

  let formData = {
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  };

  let selectedCountry = countries[0];
  let showDropdown = false;

  let errors = {
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  };

  let status = 'idle';

  let toast = {
    visible: false,
    message: '',
    type: 'success'
  };

  /** @param {string} name */
  const validateName = (name) => /^[a-zA-ZÀ-ÿ\s]+$/.test(name);
  
  /** @param {string} email */
  const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  /** @param {string} phone */
  const validatePhone = (phone) => /^[0-9]{7,15}$/.test(phone);

  const toggleDropdown = () => {
    showDropdown = !showDropdown;
  };

  /** @param {any} country */
  const selectCountry = (country) => {
    selectedCountry = country;
    showDropdown = false;
    handleInput('phone');
  };

  /** 
   * @param {string} message 
   * @param {string} type 
   */
  const showToast = (message, type = 'success') => {
    toast = { visible: true, message, type };
    setTimeout(() => {
      toast.visible = false;
    }, 4000); 
  };

  /** @param {string} field */
  const handleInput = (field) => {
    if (field === 'firstName') {
      errors.firstName = (formData.firstName && !validateName(formData.firstName)) 
        ? 'El nombre no puede contener números ni símbolos.' : '';
    }
    
    if (field === 'lastName') {
      errors.lastName = (formData.lastName && !validateName(formData.lastName)) 
        ? 'El apellido no puede contener números ni símbolos.' : '';
    }
    
    if (field === 'email') {
      errors.email = (formData.email && !validateEmail(formData.email)) 
        ? 'Ingresa un correo electrónico válido.' : '';
    }

    if (field === 'phone') {
      formData.phone = formData.phone.replace(/\D/g, '');
      errors.phone = (formData.phone && !validatePhone(formData.phone)) 
        ? 'Ingresa un número válido (entre 7 y 15 dígitos).' : '';
    }
  };

const handleSubmit = async () => {
    let isValid = true;

    if (!formData.firstName || !validateName(formData.firstName)) {
      errors.firstName = formData.firstName ? 'El nombre no puede contener números ni símbolos.' : 'El nombre es obligatorio.';
      isValid = false;
    }

    if (!formData.lastName || !validateName(formData.lastName)) {
      errors.lastName = formData.lastName ? 'El apellido no puede contener números ni símbolos.' : 'El apellido es obligatorio.';
      isValid = false;
    }

    if (!formData.email || !validateEmail(formData.email)) {
      errors.email = formData.email ? 'Ingresa un correo electrónico válido.' : 'El correo es obligatorio.';
      isValid = false;
    }

    if (!formData.phone || !validatePhone(formData.phone)) {
      errors.phone = formData.phone ? 'Ingresa un número válido (entre 7 y 15 dígitos).' : 'El número es obligatorio.';
      isValid = false;
    }

    if (!isValid) return;

    status = 'loading';

    const finalData = {
      ...formData,
      phone: `${selectedCountry.code} ${formData.phone}`
    };

    try {
      // 1. Hacemos la petición real a tu servidor de Odoo
      const response = await fetch('http://localhost:8069/api/contacto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(finalData)
      });

      // 2. Leemos la respuesta de Odoo
      const result = await response.json();

      // 3. Verificamos la respuesta
      if (result.status === 200) {
        console.log('Éxito en Odoo:', result);
        showToast('Se ha enviado la solicitud', 'success');
        formData = { firstName: '', lastName: '', email: '', phone: '' };
      } else if (result.status === 429) {
        // Bloqueo por Spam (Demasiadas peticiones)
        showToast('Ya recibimos tu solicitud. Espera unos minutos.', 'warning');
      } else {
        console.error('Error desde Odoo:', result.message);
        throw new Error(result.message);
      }
      
    } catch (error) {
      console.error('Error de conexión:', error);
      showToast('Ha ocurrido un error, intente de nuevo más tarde', 'error');
    } finally {
      status = 'idle';
    }
  };
</script>

<div use:reveal class="w-full max-w-2xl mx-4 sm:mx-auto bg-white p-5 sm:p-8 rounded-xl shadow-lg border border-gray-100 relative">
  <div class="text-center mb-6 sm:mb-8">
    <h2 class="text-2xl sm:text-3xl font-bold text-gray-800">Contáctanos</h2>
    <p class="text-sm sm:text-base text-gray-500 mt-1 sm:mt-2">Déjanos tus datos y un asesor inmobiliario te escribirá por WhatsApp.</p>
  </div>

  <form on:submit|preventDefault={handleSubmit} class="space-y-4 sm:space-y-6">
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
      <div>
        <label for="firstName" class="block text-sm font-medium text-gray-700">Nombre</label>
        <input 
          type="text" 
          id="firstName" 
          bind:value={formData.firstName}
          on:input={() => handleInput('firstName')}
          class="mt-1 block w-full px-4 py-3 border rounded-lg shadow-sm transition {errors.firstName ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
          placeholder="Ej. Carlos"
        />
        {#if errors.firstName}
          <p class="mt-1 text-sm text-red-500">{errors.firstName}</p>
        {/if}
      </div>

      <div>
        <label for="lastName" class="block text-sm font-medium text-gray-700">Apellido</label>
        <input 
          type="text" 
          id="lastName" 
          bind:value={formData.lastName}
          on:input={() => handleInput('lastName')}
          class="mt-1 block w-full px-4 py-3 border rounded-lg shadow-sm transition {errors.lastName ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
          placeholder="Ej. Anzola"
        />
        {#if errors.lastName}
          <p class="mt-1 text-sm text-red-500">{errors.lastName}</p>
        {/if}
      </div>
    </div>

    <div>
      <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
      <input 
        type="email" 
        id="email" 
        bind:value={formData.email}
        on:input={() => handleInput('email')}
        class="mt-1 block w-full px-4 py-3 border rounded-lg shadow-sm transition {errors.email ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
        placeholder="correo@ejemplo.com"
      />
      {#if errors.email}
        <p class="mt-1 text-sm text-red-500">{errors.email}</p>
      {/if}
    </div>

    <div class="flex flex-col relative">
      <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Número de WhatsApp</label>
      
      <div class="relative flex items-center">
        <button
          type="button"
          on:click={toggleDropdown}
          class="absolute left-1 flex items-center gap-1.5 bg-transparent py-2 pl-3 pr-2 text-gray-700 hover:bg-gray-100 rounded-md transition focus:outline-none z-10"
        >
          <span class="text-lg">{selectedCountry.flag}</span>
          <span class="text-sm font-medium">{selectedCountry.code}</span>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </button>

        {#if showDropdown}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <div class="fixed inset-0 z-40" on:click={() => showDropdown = false}></div>
          
          <div class="absolute top-full left-0 mt-1 w-64 bg-white border border-gray-200 rounded-lg shadow-xl z-50 max-h-60 overflow-y-auto">
            {#each countries as country}
              <button
                type="button"
                on:click={() => selectCountry(country)}
                class="w-full text-left px-4 py-2.5 hover:bg-blue-50 transition flex items-center gap-3 {selectedCountry.code === country.code ? 'bg-blue-50' : ''}"
              >
                <span class="text-xl">{country.flag}</span>
                <span class="font-medium text-gray-700">{country.name}</span>
                <span class="text-gray-400 text-sm ml-auto">{country.code}</span>
              </button>
            {/each}
          </div>
        {/if}

        <input 
          type="tel" 
          id="phone"
          bind:value={formData.phone}
          on:input={() => handleInput('phone')}
          class="block w-full py-3 pl-[6.5rem] pr-4 border rounded-lg shadow-sm transition {errors.phone ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
          placeholder="412 123 4567"
        />
      </div>
      {#if errors.phone}
        <p class="mt-1 text-sm text-red-500">{errors.phone}</p>
      {/if}
    </div>

    <button 
      type="submit" 
      disabled={status === 'loading'}
      class="w-full flex justify-center cursor-pointer py-3 px-4 border border-transparent rounded-lg shadow-sm text-base sm:text-lg font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition disabled:opacity-70 mt-4"
    >
      {#if status === 'loading'}
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Enviando...
      {:else}
        Solicitar Información
      {/if}
    </button>
  </form>
</div>

{#if toast.visible}
  <div 
    in:fly={{ y: 50, duration: 400 }}
    out:fade={{ duration: 200 }}
    class="fixed bottom-6 right-6 z-50 flex items-center p-4 max-w-sm text-gray-700 bg-white rounded-lg shadow-2xl border-l-4 {toast.type === 'success' ? 'border-green-500' : 'border-red-500'}" 
    role="alert"
  >
    <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 rounded-lg {toast.type === 'success' ? 'text-green-500 bg-green-100' : 'text-red-500 bg-red-100'}">
      {#if toast.type === 'success'}
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
        </svg>
      {:else}
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
        </svg>
      {/if}
    </div>
    <div class="ms-3 text-sm font-medium">{toast.message}</div>
    <button type="button" class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 ml-4 transition-colors" on:click={() => toast.visible = false}>
      <span class="sr-only">Cerrar</span>
      <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
      </svg>
    </button>
  </div>
{/if}