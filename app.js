document.addEventListener('DOMContentLoaded', () => {
    const hiddenElements = document.querySelectorAll('.hidden');

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.classList.remove('hidden');
                obs.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    hiddenElements.forEach((el) => observer.observe(el));

    document.addEventListener('click', (e) => {
        const button = e.target.closest('.read-more-toggle');
        if (!button) return;

        const projectId = button.dataset.projectId;
        const readMoreSection = document.getElementById(`read-more-${projectId}`);

        if (!readMoreSection) return;

        const isExpanded = readMoreSection.style.display === 'block';
        readMoreSection.style.display = isExpanded ? 'none' : 'block';
        button.textContent = isExpanded ? 'Read More' : 'Read Less';
        button.setAttribute('aria-expanded', !isExpanded);
    });
});
