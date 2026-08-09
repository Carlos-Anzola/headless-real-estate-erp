<script>
  import Header from './components/Header.svelte';
  import WelcomeBanner from './components/WelcomeBanner.svelte';
  import HeroCarousel from './components/HeroCarousel.svelte';
  import AboutUs from './components/AboutUs.svelte';
  import ContactForm from './components/ContactForm.svelte';
  import Footer from './components/Footer.svelte';
</script>

<div class="min-h-screen flex flex-col bg-gray-50">
  <Header />
  
  <main class="flex-grow">
    
    <WelcomeBanner />

    <HeroCarousel />

    <AboutUs />

    <section id="contacto" class="min-h-[calc(100vh-5rem)] flex items-center justify-center bg-white border-t border-gray-200 p-4">
      <ContactForm />
    </section>

  </main>

  <Footer />
</div>