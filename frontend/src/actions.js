export function reveal(node) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        node.style.opacity = '1';
        node.style.transform = 'translateY(0)';
      } else {
        node.style.opacity = '0';
        node.style.transform = 'translateY(50px)';
      }
    });
  }, {
    threshold: 0.15
  });

  node.style.opacity = '0';
  node.style.transform = 'translateY(50px)';
  node.style.transition = 'all 0.8s cubic-bezier(0.5, 0, 0, 1)';

  observer.observe(node);

  return {
    destroy() {
      observer.disconnect();
    }
  };
}