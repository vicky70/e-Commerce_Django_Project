
const floatingNav = document.querySelector('.floating-navbar');
const dragHandle = document.querySelector('.drag-me');

let isDragging = false;
let initialX;
let initialY;
let xOffset = 0;
let yOffset = 0;

const navbarWidth = floatingNav.offsetWidth;
const navbarHeight = floatingNav.offsetHeight;

// console.log('navbar Width is ====> // ', navbarWidth)
// console.log('navbar Height is =====> // ', navbarHeight)

function updatePosition(x, y) {
  const maxX = window.innerWidth - navbarWidth;
  console.log('Windows inner width checking------>//  ',window.innerWidth)
  console.log('Windows inner width - navbarWidth checking------>//  ',maxX)
  const maxY = window.innerHeight - navbarHeight;
//   console.log('Windows inner Height checking------>//  ',window.innerHeight)
//   console.log('Windows inner Height - navbarHeight checking------>//  ',maxY)

    const newX = Math.min(Math.max(x, 0), maxX);
    const newY = Math.min(Math.max(y, 0), maxY);

    xOffset = newX
    yOffset = newY

  floatingNav.style.transform = `translate3d(${xOffset}px, ${yOffset}px, 0)`;
}

dragHandle.addEventListener('mousedown', (e) => {
  isDragging = true;

  initialX = e.clientX - xOffset;
  initialY = e.clientY - yOffset;

  floatingNav.classList.add('active');
});

document.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  const newX = e.clientX - initialX;
  const newY = e.clientY - initialY;
  updatePosition(newX, newY);
});


document.addEventListener('mouseup', () => {
  isDragging = false;
  floatingNav.classList.remove('active');
});

window.addEventListener('mouseup', () => {
  isDragging = false;
  floatingNav.classList.remove('active');
});



window.addEventListener('scroll', () => {
  const parallaxContent = document.querySelector('.parallax-content');
  const scrollY = window.pageYOffset;
  parallaxContent.style.transform = `translateX(${40 - (scrollY * 0.1)}%)`;
});