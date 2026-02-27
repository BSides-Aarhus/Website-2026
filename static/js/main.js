// BSides Aarhus 2026 — Main JavaScript

// Interactive Particle Background
(function () {
  var canvas = document.createElement('canvas');
  canvas.id = 'particle-bg';
  canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.6;';
  document.body.prepend(canvas);

  var ctx = canvas.getContext('2d');
  var mouse = { x: -1000, y: -1000 };
  var particles = [];
  var count = 60;
  var connectDist = 150;
  var mouseRadius = 180;
  var accentR = 74, accentG = 184, accentB = 210; // #4AB8D2

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  document.addEventListener('mousemove', function (e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });
  document.addEventListener('mouseleave', function () {
    mouse.x = -1000;
    mouse.y = -1000;
  });

  // Create particles
  for (var i = 0; i < count; i++) {
    particles.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 2 + 1,
      alpha: Math.random() * 0.5 + 0.2
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];

      // Mouse repulsion
      var dx = p.x - mouse.x;
      var dy = p.y - mouse.y;
      var dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < mouseRadius && dist > 0) {
        var force = (mouseRadius - dist) / mouseRadius;
        p.vx += (dx / dist) * force * 0.8;
        p.vy += (dy / dist) * force * 0.8;
      }

      // Apply velocity with damping
      p.vx *= 0.98;
      p.vy *= 0.98;
      p.x += p.vx;
      p.y += p.vy;

      // Wrap edges
      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;

      // Glow near mouse
      var mouseDist = Math.sqrt((p.x - mouse.x) ** 2 + (p.y - mouse.y) ** 2);
      var glow = mouseDist < mouseRadius * 2 ? 1 - (mouseDist / (mouseRadius * 2)) : 0;
      var alpha = p.alpha + glow * 0.5;

      // Draw particle
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r + glow * 1.5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + accentR + ',' + accentG + ',' + accentB + ',' + alpha + ')';
      ctx.fill();

      // Connect nearby particles
      for (var j = i + 1; j < particles.length; j++) {
        var p2 = particles[j];
        var d = Math.sqrt((p.x - p2.x) ** 2 + (p.y - p2.y) ** 2);
        if (d < connectDist) {
          var lineAlpha = (1 - d / connectDist) * 0.15;
          // Lines glow brighter near mouse
          var midX = (p.x + p2.x) / 2;
          var midY = (p.y + p2.y) / 2;
          var midDist = Math.sqrt((midX - mouse.x) ** 2 + (midY - mouse.y) ** 2);
          if (midDist < mouseRadius * 2) {
            lineAlpha += (1 - midDist / (mouseRadius * 2)) * 0.2;
          }
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = 'rgba(' + accentR + ',' + accentG + ',' + accentB + ',' + lineAlpha + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(animate);
  }

  // Only run on non-touch devices to save performance
  if (!('ontouchstart' in window)) {
    animate();
  }
})();

// Countdown Timer
(function () {
  const el = document.querySelector('.countdown');
  if (!el) return;

  const target = new Date(el.dataset.target).getTime();

  function update() {
    const now = Date.now();
    const diff = target - now;

    if (diff <= 0) {
      document.getElementById('cd-days').textContent = '0';
      document.getElementById('cd-hours').textContent = '0';
      document.getElementById('cd-mins').textContent = '0';
      document.getElementById('cd-secs').textContent = '0';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById('cd-days').textContent = days;
    document.getElementById('cd-hours').textContent = hours;
    document.getElementById('cd-mins').textContent = mins;
    document.getElementById('cd-secs').textContent = secs;
  }

  update();
  setInterval(update, 1000);
})();

// Mobile Navigation Toggle
(function () {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;

  toggle.addEventListener('click', function () {
    const isOpen = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen);
  });

  // Close menu when clicking a link
  links.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
})();

// FAQ Accordion
(function () {
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const item = btn.parentElement;
      const answer = item.querySelector('.faq-answer');
      const isOpen = item.classList.contains('open');

      // Close all other items
      document.querySelectorAll('.faq-item.open').forEach(function (openItem) {
        if (openItem !== item) {
          openItem.classList.remove('open');
          openItem.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
          openItem.querySelector('.faq-answer').style.maxHeight = null;
        }
      });

      // Toggle current item
      if (isOpen) {
        item.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        answer.style.maxHeight = null;
      } else {
        item.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });
})();
