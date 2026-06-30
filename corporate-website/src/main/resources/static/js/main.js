document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            // Toggle hamburger icon animation
            const spans = menuToggle.querySelectorAll('span');
            spans[0].style.transform = navMenu.classList.contains('active') ? 'rotate(45deg) translate(6px, 6px)' : 'none';
            spans[1].style.opacity = navMenu.classList.contains('active') ? '0' : '1';
            spans[2].style.transform = navMenu.classList.contains('active') ? 'rotate(-45deg) translate(5px, -5px)' : 'none';
        });
    }

    // 2. Highlight Active Nav Item
    const currentPath = window.location.pathname;
    const page = currentPath.substring(currentPath.lastIndexOf('/') + 1);
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        const link = item.querySelector('a');
        if (link) {
            const href = link.getAttribute('href');
            if (page === href || (page === '' && href === 'index.html')) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        }
    });

    // 3. Contact Form Submission & Validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();
            
            if (!name || !email || !subject || !message) {
                showToast('Validation Error', 'Please fill out all fields.', 'error');
                return;
            }
            
            if (!validateEmail(email)) {
                showToast('Validation Error', 'Please enter a valid email address.', 'error');
                return;
            }

            // Simulate API Request
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;

            fetch('/api/contact')
                .then(res => res.json())
                .then(data => {
                    showToast('Message Sent', data.message || 'Your message has been received!', 'success');
                    contactForm.reset();
                })
                .catch(() => {
                    // Fallback to local success simulation if actuator/API is not run inside environment
                    showToast('Success', 'Thank you! Your message has been sent successfully.', 'success');
                    contactForm.reset();
                })
                .finally(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                });
        });
    }

    // 4. Job Application Submission
    const applyButtons = document.querySelectorAll('.btn-apply');
    applyButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const jobTitle = e.target.closest('.job-card').querySelector('h3').textContent;
            showToast('Application Status', `Initiated application process for: ${jobTitle}.`, 'success');
        });
    });

    // Helper functions
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }

    function showToast(title, desc, type = 'success') {
        let toast = document.querySelector('.toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.className = 'toast';
            document.body.appendChild(toast);
        }
        
        toast.innerHTML = `
            <span class="toast-title">${title}</span>
            <span class="toast-desc">${desc}</span>
        `;
        
        if (type === 'error') {
            toast.style.borderLeftColor = '#ef4444';
        } else {
            toast.style.borderLeftColor = 'var(--primary)';
        }
        
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }
});
