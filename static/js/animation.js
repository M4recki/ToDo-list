const carousel = document.querySelector('#opinions-carousel');

carousel.addEventListener('slide.bs.carousel', function(event) {
  const currentSlide = event.from;
  const nextSlide = event.to;

  const currentSlideElement = carousel.querySelector(`.carousel-item[data-bs-slide-to="${currentSlide}"]`);
  const nextSlideElement = carousel.querySelector(`.carousel-item[data-bs-slide-to="${nextSlide}"]`);

  currentSlideElement.classList.remove('animate__animated', 'animate__fadeIn');
  currentSlideElement.classList.add('animate__animated', 'animate__fadeOut');

  nextSlideElement.classList.remove('animate__animated', 'animate__fadeOut');
  nextSlideElement.classList.add('animate__animated', 'animate__fadeIn');
});
