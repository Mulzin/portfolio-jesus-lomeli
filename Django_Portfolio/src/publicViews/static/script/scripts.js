function mobileCompatibility() {
    // Mobile menu toggle
    document.querySelector('.menu-btn').addEventListener('click', function() {
        document.querySelector('.nav-links').classList.toggle('active');
    });
    
    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            document.querySelector('.nav-links').classList.remove('active');
        });
    });
    
    // Add scroll effect to navbar
    window.addEventListener('scroll', function() {
        const header = document.querySelector('header');
        if (window.scrollY > 50) {
            header.style.background = 'rgba(26, 10, 18, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'linear-gradient(135deg, #1A0A12, #2E0E1E)';
            header.style.backdropFilter = 'none';
        }
    });
}

function getPortfolioData() {
    fetch('/api/get_portfolio')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            fillProjects(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

function fillProjects(portfolioData) {
    const projectsGrid = document.querySelector('.projects-grid');
    projectsGrid.innerHTML = ''; // Clear previous content

    for (const key in portfolioData) {
        const project = portfolioData[key];

        // Card container
        const card = document.createElement('div');
        card.className = 'project-card';

        // Info container
        const info = document.createElement('div');
        info.className = 'project-info';

        // Title
        const title = document.createElement('h3');
        title.textContent = project.title || 'Untitled Project';
        info.appendChild(title);

        // Description
        const desc = document.createElement('p');
        desc.textContent = getSummaryLanguage(project);
        info.appendChild(desc);

        // Tech tags
        if (Array.isArray(project.code) && project.code.length) {
            const techDiv = document.createElement('div');
            techDiv.className = 'project-tech';
            project.code.forEach(tech => {
                const tag = document.createElement('span');
                tag.className = 'tech-tag';
                tag.textContent = tech;
                techDiv.appendChild(tag);
            });
            info.appendChild(techDiv);
        }

        // Link (if present)
        if (project.link) {
            const linksDiv = document.createElement('div');
            linksDiv.className = 'project-links';
            const link = document.createElement('a');
            link.href = project.link.startsWith('http') ? project.link : `https://${project.link}`;
            link.target = '_blank';
            link.textContent = 'Source Code';
            linksDiv.appendChild(link);
            info.appendChild(linksDiv);
        }

        card.appendChild(info);
        projectsGrid.appendChild(card);
    }
}

function getSummaryLanguage(projectData) {
    const languageElem = document.getElementById('language');
    const language = languageElem ? languageElem.dataset.language : 'en';
    if(language === 'sp') return projectData['summary_sp'] || projectData['summary_en'] || '';
    return projectData['summary_en'] || '';
}
