/**
 * AutoFlow Pro - Main JavaScript File
 * Professional 3D Website Interactions
 */

// Global variables
let isLoading = true;
let scrollProgress = 0;
let currentDemoStep = 0;
let demoInterval = null;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
});

// Initialize website functionality
function initializeWebsite() {
    console.log('🚀 Initializing AutoFlow Pro Website...');
    
    // Initialize components
    initializeLoader();
    initializeNavigation();
    initializeScrollEffects();
    initializeAnimations();
    initializeDemoSystem();
    initializeCounters();
    initializeFormHandling();
    initializeInteractiveElements();
    
    console.log('✅ Website initialized successfully!');
}

// Loading Screen
function initializeLoader() {
    const loadingScreen = document.getElementById('loading-screen');
    const progressBar = document.querySelector('.progress');
    
    if (!loadingScreen) return;
    
    let progress = 0;
    const loadingInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 100) progress = 100;
        
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(loadingInterval);
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                isLoading = false;
                startMainAnimations();
            }, 500);
        }
    }, 100);
}

// Navigation
function initializeNavigation() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Scroll effect for navbar
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for nav links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    // Close mobile menu
                    navMenu.classList.remove('active');
                    navToggle.classList.remove('active');
                    
                    // Smooth scroll
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Update active link
                    updateActiveNavLink(href);
                }
            }
        });
    });
    
    // Update active nav link on scroll
    window.addEventListener('scroll', throttle(updateActiveNavOnScroll, 100));
}

// Update active navigation link
function updateActiveNavLink(activeHref) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === activeHref) {
            link.classList.add('active');
        }
    });
}

// Update active nav on scroll
function updateActiveNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const top = section.offsetTop;
        const bottom = top + section.offsetHeight;
        const id = section.getAttribute('id');
        
        if (scrollPos >= top && scrollPos < bottom) {
            updateActiveNavLink(`#${id}`);
        }
    });
}

// Scroll Effects
function initializeScrollEffects() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    
    // Scroll indicator click
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            document.querySelector('#features').scrollIntoView({
                behavior: 'smooth'
            });
        });
    }
    
    // Parallax effects
    window.addEventListener('scroll', throttle(handleParallaxEffects, 16));
    
    // Scroll progress
    window.addEventListener('scroll', throttle(updateScrollProgress, 16));
}

// Parallax effects
function handleParallaxEffects() {
    const scrolled = window.pageYOffset;
    const rate = scrolled * -0.5;
    
    // Floating shapes parallax
    const shapes = document.querySelectorAll('.shape');
    shapes.forEach((shape, index) => {
        const speed = 0.1 + (index * 0.05);
        const yPos = -(scrolled * speed);
        shape.style.transform = `translateY(${yPos}px) rotateZ(${scrolled * 0.05}deg)`;
    });
    
    // Hero content parallax
    const heroContent = document.querySelector('.hero-content');
    if (heroContent && scrolled < window.innerHeight) {
        heroContent.style.transform = `translateY(${rate}px)`;
    }
}

// Update scroll progress
function updateScrollProgress() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    scrollProgress = (winScroll / height) * 100;
    
    // Update any progress indicators
    const progressElements = document.querySelectorAll('[data-scroll-progress]');
    progressElements.forEach(element => {
        element.style.setProperty('--scroll-progress', `${scrollProgress}%`);
    });
}

// Animations
function initializeAnimations() {
    // Observe elements for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
                
                // Special animations for specific elements
                if (entry.target.classList.contains('feature-card')) {
                    animateFeatureCard(entry.target);
                }
                if (entry.target.classList.contains('dashboard-card')) {
                    animateDashboardCard(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observe all elements with data-aos attribute
    document.querySelectorAll('[data-aos]').forEach(element => {
        observer.observe(element);
    });
    
    // 3D tilt effects
    initialize3DTiltEffects();
}

// Feature card animation
function animateFeatureCard(card) {
    const icon = card.querySelector('.feature-icon');
    const listItems = card.querySelectorAll('.feature-list li');
    
    setTimeout(() => {
        if (icon) {
            icon.style.transform = 'rotateY(360deg) scale(1.1)';
            setTimeout(() => {
                icon.style.transform = 'rotateY(0deg) scale(1)';
            }, 600);
        }
    }, 200);
    
    listItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, 300 + (index * 100));
    });
}

// Dashboard card animation
function animateDashboardCard(card) {
    const chartBars = card.querySelectorAll('.chart-bar');
    const progressCircle = card.querySelector('.progress-circle');
    
    if (chartBars.length > 0) {
        chartBars.forEach((bar, index) => {
            setTimeout(() => {
                bar.style.animation = `growBar 1s ease-in-out forwards`;
            }, index * 200);
        });
    }
    
    if (progressCircle) {
        setTimeout(() => {
            progressCircle.style.animation = 'progressAnimation 2s ease-in-out forwards';
        }, 500);
    }
}

// 3D Tilt Effects
function initialize3DTiltEffects() {
    const tiltElements = document.querySelectorAll('.feature-card, .dashboard-preview, .tool-card');
    
    tiltElements.forEach(element => {
        element.addEventListener('mousemove', handleTiltMove);
        element.addEventListener('mouseleave', handleTiltLeave);
    });
}

function handleTiltMove(e) {
    const element = e.currentTarget;
    const rect = element.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = (y - centerY) / centerY * -10;
    const rotateY = (x - centerX) / centerX * 10;
    
    element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
}

function handleTiltLeave(e) {
    const element = e.currentTarget;
    element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
}

// Demo System
function initializeDemoSystem() {
    const playBtn = document.getElementById('play-demo');
    const pauseBtn = document.getElementById('pause-demo');
    const processSteps = document.querySelectorAll('.process-step');
    
    if (playBtn) {
        playBtn.addEventListener('click', startDemo);
    }
    
    if (pauseBtn) {
        pauseBtn.addEventListener('click', stopDemo);
    }
    
    // Auto-start demo when visible
    const demoSection = document.querySelector('.tools');
    if (demoSection) {
        const demoObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !demoInterval) {
                    setTimeout(startDemo, 1000);
                }
            });
        }, { threshold: 0.5 });
        
        demoObserver.observe(demoSection);
    }
}

function startDemo() {
    const processSteps = document.querySelectorAll('.process-step');
    if (processSteps.length === 0) return;
    
    stopDemo(); // Clear any existing interval
    
    currentDemoStep = 0;
    
    demoInterval = setInterval(() => {
        // Remove active class from all steps
        processSteps.forEach(step => step.classList.remove('active'));
        
        // Add active class to current step
        if (processSteps[currentDemoStep]) {
            processSteps[currentDemoStep].classList.add('active');
        }
        
        currentDemoStep++;
        
        // Reset to beginning
        if (currentDemoStep >= processSteps.length) {
            currentDemoStep = 0;
            setTimeout(() => {
                processSteps.forEach(step => step.classList.remove('active'));
            }, 1000);
        }
    }, 2000);
}

function stopDemo() {
    if (demoInterval) {
        clearInterval(demoInterval);
        demoInterval = null;
    }
}

// Counter Animations
function initializeCounters() {
    const counters = document.querySelectorAll('.stat-number[data-count]');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                animateCounter(entry.target);
                entry.target.classList.add('counted');
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseFloat(element.dataset.count);
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };
    
    updateCounter();
}

// Form Handling
function initializeFormHandling() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', handleFormSubmit);
        
        // Enhanced form interactions
        const formGroups = contactForm.querySelectorAll('.form-group');
        formGroups.forEach(group => {
            const input = group.querySelector('input, textarea');
            const label = group.querySelector('label');
            
            if (input && label) {
                // Add focus effects
                input.addEventListener('focus', () => {
                    group.classList.add('focused');
                });
                
                input.addEventListener('blur', () => {
                    group.classList.remove('focused');
                    if (input.value.trim() !== '') {
                        group.classList.add('filled');
                    } else {
                        group.classList.remove('filled');
                    }
                });
                
                // Check if already filled on load
                if (input.value.trim() !== '') {
                    group.classList.add('filled');
                }
            }
        });
    }
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Disable submit button
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;
        
        // Simulate form submission
        setTimeout(() => {
            // Show success message
            showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
            
            // Reset form
            form.reset();
            form.querySelectorAll('.form-group').forEach(group => {
                group.classList.remove('filled', 'focused');
            });
            
            // Restore button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 2000);
    }
}

// Interactive Elements
function initializeInteractiveElements() {
    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', handleButtonHover);
        button.addEventListener('mouseleave', handleButtonLeave);
    });
    
    // Get started button
    const getStartedBtn = document.getElementById('get-started-btn');
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', (e) => {
            // Ensure we scroll to the Video Automation Workflow section
            e.preventDefault();
            if (typeof window.goToWorkflow === 'function') {
                // Use the page-defined function for consistency
                window.goToWorkflow();
            } else {
                const target = document.querySelector('#workflow-section');
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    }
    
    // Demo button
    const demoBtn = document.getElementById('demo-btn');
    if (demoBtn) {
        demoBtn.addEventListener('click', () => {
            document.querySelector('#tools').scrollIntoView({
                behavior: 'smooth'
            });
        });
    }
    
    // Logo click
    const logo = document.querySelector('.nav-logo');
    if (logo) {
        logo.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // API tab switching
    initializeAPITabs();
    
    // Endpoint cards interaction
    const endpointCards = document.querySelectorAll('.endpoint-card');
    endpointCards.forEach(card => {
        card.addEventListener('click', () => {
            // Highlight the corresponding code example
            animateCodeExample();
        });
    });
}

function handleButtonHover(e) {
    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const ripple = document.createElement('span');
    
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.background = 'rgba(255, 255, 255, 0.3)';
    ripple.style.transform = 'scale(0)';
    ripple.style.animation = 'ripple 0.6s linear';
    ripple.style.left = '50%';
    ripple.style.top = '50%';
    ripple.style.width = '100px';
    ripple.style.height = '100px';
    ripple.style.marginLeft = '-50px';
    ripple.style.marginTop = '-50px';
    
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

function handleButtonLeave(e) {
    // Additional leave effects can be added here
}

// API Tabs
function initializeAPITabs() {
    const tabs = document.querySelectorAll('.tab');
    const codeExamples = {
        'JavaScript': `// Initialize AutoFlow Pro API
const autoflow = new AutoFlowAPI({
  apiKey: '${getYouTubeAPIKey()}',
  baseURL: 'https://api.autoflowpro.com/v1'
});

// Process video with AI
const result = await autoflow.video.process({
  url: 'https://example.com/video.mp4',
  options: {
    maxClips: 6,
    whisperModel: 'base',
    sceneThreshold: 0.4,
    uploadToYouTube: true
  }
});

console.log('Processing complete:', result);`,
        
        'Python': `import autoflow

# Initialize AutoFlow Pro API
client = autoflow.Client(
    api_key='${getYouTubeAPIKey()}',
    base_url='https://api.autoflowpro.com/v1'
)

# Process video with AI
result = client.video.process(
    url='https://example.com/video.mp4',
    options={
        'max_clips': 6,
        'whisper_model': 'base',
        'scene_threshold': 0.4,
        'upload_to_youtube': True
    }
)

print('Processing complete:', result)`,
        
        'cURL': `curl -X POST https://api.autoflowpro.com/v1/video/process \\
  -H "Authorization: Bearer ${getYouTubeAPIKey()}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "url": "https://example.com/video.mp4",
    "options": {
      "maxClips": 6,
      "whisperModel": "base",
      "sceneThreshold": 0.4,
      "uploadToYouTube": true
    }
  }'`
    };
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Update code example
            const language = tab.textContent.trim();
            const codeContent = document.querySelector('.editor-content pre code');
            if (codeContent && codeExamples[language]) {
                codeContent.textContent = codeExamples[language];
                
                // Animate code update
                codeContent.style.opacity = '0';
                setTimeout(() => {
                    codeContent.style.opacity = '1';
                }, 150);
            }
        });
    });
}

function animateCodeExample() {
    const codeContent = document.querySelector('.editor-content pre code');
    if (codeContent) {
        codeContent.style.transform = 'scale(0.95)';
        codeContent.style.transition = 'all 0.2s ease';
        
        setTimeout(() => {
            codeContent.style.transform = 'scale(1)';
        }, 200);
    }
}

// Utility Functions
function throttle(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

function getYouTubeAPIKey() {
    return '600976543782-k802ig8v63me9o0lks1t9tt8sqiacma0.apps.googleusercontent.com';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 400px;
        font-family: var(--font-primary);
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Close button
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        removeNotification(notification);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        removeNotification(notification);
    }, 5000);
}

function removeNotification(notification) {
    notification.style.transform = 'translateX(400px)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

function startMainAnimations() {
    // Trigger hero animations
    const heroTitle = document.querySelector('.hero-title');
    const heroDescription = document.querySelector('.hero-description');
    const heroButtons = document.querySelector('.hero-buttons');
    const heroStats = document.querySelector('.hero-stats');
    const dashboardPreview = document.querySelector('.dashboard-preview');
    
    if (heroTitle) {
        heroTitle.style.animation = 'fadeInUp 1s ease forwards';
    }
    
    if (heroDescription) {
        setTimeout(() => {
            heroDescription.style.animation = 'fadeInUp 1s ease forwards';
        }, 200);
    }
    
    if (heroButtons) {
        setTimeout(() => {
            heroButtons.style.animation = 'fadeInUp 1s ease forwards';
        }, 400);
    }
    
    if (heroStats) {
        setTimeout(() => {
            heroStats.style.animation = 'fadeInUp 1s ease forwards';
        }, 600);
    }
    
    if (dashboardPreview) {
        setTimeout(() => {
            dashboardPreview.style.animation = 'slideInRight 1s ease forwards';
        }, 800);
    }
}

// Performance monitoring
function monitorPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const perfData = performance.timing;
            const loadTime = perfData.loadEventEnd - perfData.navigationStart;
            console.log(`🚀 Page load time: ${loadTime}ms`);
            
            // Report to analytics if needed
            if (loadTime > 3000) {
                console.warn('⚠️ Page load time is over 3 seconds');
            }
        });
    }
}

// Error handling
window.addEventListener('error', (e) => {
    console.error('🚨 JavaScript Error:', e.error);
    // Could send to error reporting service
});

// Initialize performance monitoring
monitorPerformance();

// Add CSS animations that weren't in the CSS file
const additionalStyles = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .notification {
        font-weight: 500;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
    
    .form-group.focused input,
    .form-group.focused textarea {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .feature-list li {
        opacity: 0;
        transform: translateX(-20px);
        transition: all 0.3s ease;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

console.log('🎉 AutoFlow Pro Website Loaded Successfully!');