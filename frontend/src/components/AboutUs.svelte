<script>
  import { reveal } from '../actions.js';
</script>

<section id="conocenos" class="min-h-[calc(100vh-5rem)] flex items-center py-12 bg-slate-50 border-t border-gray-200">
  <div use:reveal class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full will-change-transform">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center">
      
      <div>
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-4 sm:mb-6">Conócenos</h2>
        <p class="text-sm sm:text-base md:text-lg text-gray-600 mb-4">
          Con más de una década en el mercado inmobiliario de lujo, Premium Real Estate ha redefinido el estándar de servicio en la industria. No solo vendemos casas; conectamos visiones con su espacio ideal.
        </p>
        <p class="text-sm sm:text-base md:text-lg text-gray-600 mb-6">
          Nuestro equipo de consultores locales domina el mercado a la perfección, garantizando que cada transacción, ya sea compra, venta o alquiler, se ejecute con transparencia, agilidad y máxima rentabilidad.
        </p>
        <ul class="space-y-3 text-sm sm:text-base">
          <li class="flex items-center text-gray-700">
            <svg class="w-5 h-5 sm:w-6 sm:h-6 text-blue-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            Asesoramiento legal e hipotecario incluido.
          </li>
          <li class="flex items-center text-gray-700">
            <svg class="w-5 h-5 sm:w-6 sm:h-6 text-blue-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            Tasación oficial sin compromiso.
          </li>
        </ul>
      </div>

      <!-- Tarjetas de estadísticas adaptadas (1 columna en móviles, 2 en tablets/PCs) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
        <div class="bg-white p-5 sm:p-6 rounded-2xl shadow-sm border border-gray-100 text-center">
          <div class="text-3xl sm:text-4xl font-black text-blue-600 mb-1 sm:mb-2">+10</div>
          <div class="text-xs sm:text-sm text-gray-500 font-medium">Años de Experiencia</div>
        </div>
        <div class="bg-white p-5 sm:p-6 rounded-2xl shadow-sm border border-gray-100 text-center">
          <div class="text-3xl sm:text-4xl font-black text-blue-600 mb-1 sm:mb-2">500+</div>
          <div class="text-xs sm:text-sm text-gray-500 font-medium">Propiedades Vendidas</div>
        </div>
        <div class="bg-white p-5 sm:p-6 rounded-2xl shadow-sm border border-gray-100 text-center sm:col-span-2">
          <div class="text-2xl sm:text-3xl font-black text-gray-800 mb-1 sm:mb-2">98%</div>
          <div class="text-xs sm:text-sm text-gray-500 font-medium">De clientes satisfechos nos recomiendan</div>
        </div>
      </div>

    </div>
  </div>
</section>