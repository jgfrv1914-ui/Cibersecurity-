const shell = document.querySelector('.experience-shell');
const panels = document.querySelectorAll('.glass-panel');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const languageButtons = document.querySelectorAll('.language-button');

const languageContent = {
  en: {
    label: 'LANGUAGE',
    insight: 'PORTFOLIO INSIGHT',
    title: 'Fernando Tafurt Pinto,<br>Cybersecurity Developer',
    lede: 'Principal cybersecurity developer building practical security tooling, defensive automation, and authorized assessments with clear operational value.',
    labels: ['COLLABORATIONS', 'LATEST DROP', 'AVAILABILITY'],
    meta: [
      'Blue team workflows, Python automation, cloud security reviews, and lab-based security analysis.',
      'Python security utilities for log analysis, file integrity checks, network reconnaissance, and secure tooling.',
      'Open for security engineering, tooling, and automation projects with a strong ethical and technical focus.'
    ],
    button: 'VIEW SECURITY PROJECTS',
    role: 'CYBERSECURITY DEVELOPER • PYTHON AUTOMATION',
    tagline: 'Building secure systems, practical tooling, and reliable detection workflows for modern operations.',
    projectsLabel: 'PROJECTS',
    projectsTitle: 'Cybersecurity projects.',
    projectsDescription: 'A selection of practical Blue Team, defensive analysis, networking, and Python security automation projects.',
    cards: [
      ['Mini SOC Toolkit', 'Offline triage workflow that parses authentication logs, detects brute-force activity, matches IOCs, and produces JSON evidence reports.', 'OPEN SOC TOOLKIT'],
      ['Detection & incident triage', 'Log analysis, IOC matching, failed-login detection, file integrity monitoring, and permission auditing for defensive workflows.', 'EXPLORE DEFENSIVE TOOLS'],
      ['Authorized reconnaissance', 'Purpose-built network utilities for controlled labs: service probes, DNS discovery, HTTP methods review, and CIDR host inventory.', 'VIEW NETWORK TOOLING'],
      ['Reliable security utilities', 'Reproducible command-line tools for hashing, password analysis, entropy scanning, TLS inspection, and subnet calculations.', 'CHECK VALIDATION'],
      ['Secure Configuration Auditor', 'Read-only Linux hardening checks for SSH, firewall state, and audit logging using safe exported configuration snapshots.', 'OPEN HARDENING AUDITOR'],
      ['Threat Intelligence Analyzer', 'Offline IOC normalization and matching for IPs, domains, URLs, and hashes against authorized evidence exports.', 'ANALYZE LAB INDICATORS'],
      ['Sigma Detection Rules', 'Experimental defensive detections for SSH brute force and suspicious administrative account creation, mapped to MITRE ATT&CK.', 'VIEW DETECTION RULES']
    ],
    credentialsLabel: 'VERIFIED CREDENTIALS',
    credentialsTitle: 'Cybersecurity & networking foundations.',
    credentialsDescription: 'Selected credentials from my public Credly profiles, limited to cybersecurity and networking topics.'
  },
  es: {
    label: 'IDIOMA',
    insight: 'RESUMEN DEL PORTAFOLIO',
    title: 'Fernando Tafurt Pinto,<br>Desarrollador de Ciberseguridad',
    lede: 'Desarrollador especializado en ciberseguridad que crea herramientas prácticas, automatización defensiva y evaluaciones autorizadas con valor operativo.',
    labels: ['COLABORACIONES', 'PROYECTO RECIENTE', 'DISPONIBILIDAD'],
    meta: [
      'Flujos de trabajo Blue Team, automatización con Python, revisiones de seguridad cloud y análisis de seguridad en laboratorios.',
      'Utilidades de seguridad en Python para análisis de logs, integridad de archivos, reconocimiento de redes y herramientas seguras.',
      'Disponible para proyectos de ingeniería de seguridad, herramientas y automatización con un enfoque ético y técnico.'
    ],
    button: 'VER PROYECTOS DE SEGURIDAD',
    role: 'DESARROLLADOR DE CIBERSEGURIDAD • AUTOMATIZACIÓN CON PYTHON',
    tagline: 'Construyendo sistemas seguros, herramientas prácticas y flujos confiables de detección para operaciones modernas.',
    projectsLabel: 'PROYECTOS',
    projectsTitle: 'Proyectos de ciberseguridad.',
    projectsDescription: 'Una selección de proyectos prácticos de Blue Team, análisis defensivo, redes y automatización de seguridad con Python.',
    cards: [
      ['Mini SOC Toolkit', 'Flujo offline de triage que analiza logs de autenticación, detecta fuerza bruta, compara IOCs y genera reportes de evidencia en JSON.', 'ABRIR SOC TOOLKIT'],
      ['Detección y triage de incidentes', 'Análisis de logs, comparación de IOCs, detección de accesos fallidos, monitoreo de integridad y auditoría de permisos.', 'EXPLORAR HERRAMIENTAS DEFENSIVAS'],
      ['Reconocimiento autorizado', 'Utilidades de red para laboratorios controlados: pruebas de servicios, descubrimiento DNS, revisión de métodos HTTP e inventario CIDR.', 'VER HERRAMIENTAS DE RED'],
      ['Utilidades de seguridad confiables', 'Herramientas reproducibles de línea de comandos para hashing, análisis de contraseñas, entropía, TLS y cálculo de subredes.', 'VER VALIDACIÓN'],
      ['Auditor de configuración segura', 'Revisiones de hardening Linux en modo lectura para SSH, firewall y auditoría mediante snapshots de configuración exportados.', 'ABRIR AUDITOR DE HARDENING'],
      ['Analizador de inteligencia de amenazas', 'Normalización y comparación offline de IOCs, IPs, dominios, URLs y hashes contra evidencias autorizadas.', 'ANALIZAR INDICADORES DE LABORATORIO'],
      ['Reglas de detección Sigma', 'Detecciones defensivas experimentales para fuerza bruta SSH y creación sospechosa de cuentas administrativas, mapeadas a MITRE ATT&CK.', 'VER REGLAS DE DETECCIÓN']
    ],
    credentialsLabel: 'CREDENCIALES VERIFICADAS',
    credentialsTitle: 'Fundamentos de ciberseguridad y redes.',
    credentialsDescription: 'Credenciales seleccionadas de mis perfiles públicos de Credly, limitadas a ciberseguridad y redes.'
  }
};

function setLanguage(language) {
  const content = languageContent[language];
  document.documentElement.lang = language;
  document.querySelector('.language-label').textContent = content.label;
  document.querySelector('.mini-label').textContent = content.insight;
  document.querySelector('h1').innerHTML = content.title;
  document.querySelector('.lede').textContent = content.lede;
  document.querySelectorAll('.meta-label').forEach((element, index) => element.textContent = content.labels[index]);
  document.querySelectorAll('.meta-row p').forEach((element, index) => element.textContent = content.meta[index]);
  document.querySelector('.case-button').childNodes[0].textContent = `${content.button} `;
  document.querySelector('.role').textContent = content.role;
  document.querySelector('.tagline').textContent = content.tagline;
  const projectSection = document.querySelector('#projects');
  projectSection.querySelector('.mini-label').textContent = content.projectsLabel;
  projectSection.querySelector('h2').textContent = content.projectsTitle;
  projectSection.querySelector('.section-heading > p').textContent = content.projectsDescription;
  projectSection.querySelectorAll('.case-card').forEach((card, index) => {
    card.querySelector('h3').textContent = content.cards[index][0];
    card.querySelector('p').textContent = content.cards[index][1];
    card.querySelector('.case-link').childNodes[0].textContent = `${content.cards[index][2]} `;
  });
  const credentials = document.querySelector('#credentials');
  credentials.querySelector('.mini-label').textContent = content.credentialsLabel;
  credentials.querySelector('h2').textContent = content.credentialsTitle;
  credentials.querySelector('.section-heading > p').textContent = content.credentialsDescription;
  credentials.querySelectorAll('.credential-type').forEach((element) => {
    element.textContent = language === 'es' ? 'CIBERSEGURIDAD' : 'CYBERSECURITY';
  });
  credentials.querySelectorAll('.credential-link').forEach((element) => {
    element.childNodes[0].textContent = `${language === 'es' ? 'VERIFICAR EN CREDLY' : 'VERIFY ON CREDLY'} `;
  });
  languageButtons.forEach((button) => {
    const active = button.dataset.language === language;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  localStorage.setItem('portfolio-language', language);
}

languageButtons.forEach((button) => button.addEventListener('click', () => setLanguage(button.dataset.language)));
const storedLanguage = localStorage.getItem('portfolio-language');
const browserLanguage = (navigator.language || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
setLanguage(storedLanguage && languageContent[storedLanguage] ? storedLanguage : browserLanguage);

if (shell && !reduceMotion) {
  shell.addEventListener('pointermove', (event) => {
    const rect = shell.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    shell.style.setProperty('--pointer-x', `${x}%`);
    shell.style.setProperty('--pointer-y', `${y}%`);

    panels.forEach((panel) => {
      const panelRect = panel.getBoundingClientRect();
      const px = ((event.clientX - panelRect.left) / panelRect.width - 0.5) * 12;
      const py = ((event.clientY - panelRect.top) / panelRect.height - 0.5) * -12;
      panel.style.transform = `perspective(900px) rotateX(${py}deg) rotateY(${px}deg) translateY(-2px)`;
    });
  });

  shell.addEventListener('pointerleave', () => {
    shell.style.setProperty('--pointer-x', '50%');
    shell.style.setProperty('--pointer-y', '50%');
    panels.forEach((panel) => {
      panel.style.transform = 'none';
    });
  });
}
