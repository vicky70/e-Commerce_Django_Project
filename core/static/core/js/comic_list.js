// Filtering functionality
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelector('.filter-btn.active').classList.remove('active');
        this.classList.add('active');
        const theme = this.dataset.theme;
        
        document.querySelectorAll('.comic-card').forEach(card => {
            card.style.display = theme === 'all' || card.dataset.theme === theme ? 
                'block' : 'none';
        });
    });
});

// Scroll animation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.style.opacity = 1;
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.comic-card').forEach(card => {
    card.style.opacity = 0;
    card.style.transform = 'translateY(50px)';
    card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    observer.observe(card);
});
