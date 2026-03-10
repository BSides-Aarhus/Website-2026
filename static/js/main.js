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

// Ticket Stats Bar Entrance Animation
(function () {
  var barFill = document.querySelector('.ticket-stats-bar-fill');
  if (!barFill) return;

  // Read the target percentage from the inline style (set by Hugo)
  var inlineWidth = barFill.style.width;
  var targetPct = parseInt(inlineWidth, 10) || 0;

  // Store as CSS custom property and trigger animation after a short delay
  barFill.style.setProperty('--target-width', targetPct + '%');
  requestAnimationFrame(function () {
    setTimeout(function () {
      barFill.classList.add('ticket-stats-bar-fill--animated');
    }, 300);
  });

  // Also animate the sold counter number from 0
  var soldEl = document.getElementById('tickets-sold');
  if (soldEl) {
    var targetNum = parseInt(soldEl.textContent, 10) || 0;
    soldEl.textContent = '0';
    setTimeout(function () {
      var duration = 1200;
      var start = performance.now();
      function step(now) {
        var progress = Math.min((now - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        soldEl.textContent = Math.round(targetNum * eased);
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }, 300);
  }
})();

// Live Ticket Updates
(function () {
  // The Cloudflare Worker URL — update this after deploying the worker
  var WORKER_URL = '';
  var POLL_INTERVAL = 45000; // 45 seconds

  // Read the worker URL from a meta tag if present (set in baseof.html)
  var metaEl = document.querySelector('meta[name="ticket-proxy-url"]');
  if (metaEl) {
    WORKER_URL = metaEl.getAttribute('content');
  }

  // Don't poll if no worker URL configured
  if (!WORKER_URL) return;

  // Track current state from server-rendered data
  var statsEl = document.getElementById('ticket-stats');
  var heroCounterEl = document.getElementById('hero-tickets-sold');
  var toastEl = document.getElementById('ticket-toast');

  var currentSold = statsEl ? parseInt(statsEl.dataset.sold, 10) || 0 : 0;

  function fetchTickets() {
    fetch(WORKER_URL)
      .then(function (res) { return res.ok ? res.json() : null; })
      .then(function (data) {
        if (!data) return;
        var newSold = data.total_sold || 0;
        var diff = newSold - currentSold;

        if (diff > 0) {
          // Tickets were sold!
          currentSold = newSold;
          updateCounters(data);
          showToast(diff);
          pulseCards(data.ticket_types);
        } else if (newSold !== currentSold) {
          // Data changed (e.g., refund)
          currentSold = newSold;
          updateCounters(data);
        }
      })
      .catch(function () { /* silently fail */ });
  }

  function updateCounters(data) {
    // Update tickets page counter with animated count
    var soldEl = document.getElementById('tickets-sold');
    if (soldEl) {
      var oldVal = parseInt(soldEl.textContent, 10) || 0;
      animateCountUp(soldEl, oldVal, data.total_sold);
      soldEl.classList.remove('ticket-stats-number--bump');
      void soldEl.offsetWidth;
      soldEl.classList.add('ticket-stats-number--bump');
    }

    // Update progress bar
    if (statsEl && data.total_available > 0) {
      var pct = Math.round((data.total_sold / data.total_available) * 100);
      var barFill = statsEl.querySelector('.ticket-stats-bar-fill');
      if (barFill) {
        barFill.style.width = pct + '%';
      }
    }

    // Update hero counter with animated count
    if (heroCounterEl) {
      var oldHeroVal = parseInt(heroCounterEl.textContent, 10) || 0;
      animateCountUp(heroCounterEl, oldHeroVal, data.total_sold);
      heroCounterEl.classList.remove('ticket-stats-number--bump');
      void heroCounterEl.offsetWidth;
      heroCounterEl.classList.add('ticket-stats-number--bump');
    }

    // Update remaining counts on individual cards
    if (data.ticket_types) {
      data.ticket_types.forEach(function (tt) {
        var card = document.querySelector('[data-ticket-uuid="' + tt.uuid + '"]');
        if (!card) return;
        var remainEl = card.querySelector('.ticket-remaining-count');
        if (remainEl) {
          var oldRemain = parseInt(remainEl.textContent, 10) || 0;
          animateCountUp(remainEl, oldRemain, tt.amount_remaining);
        }
      });
    }
  }

  function animateCountUp(el, from, to) {
    var duration = 600;
    var start = performance.now();
    function step(now) {
      var progress = Math.min((now - start) / duration, 1);
      // Ease out cubic
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(from + (to - from) * eased);
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function showToast(count) {
    if (!toastEl) return;
    var msg = document.createElement('div');
    msg.className = 'ticket-toast-msg';

    var isDa = document.documentElement.lang === 'da';
    var text = count === 1
      ? (isDa ? 'Nogen har lige købt en billet!' : 'Someone just grabbed a ticket!')
      : (isDa ? count + ' billetter blev lige solgt!' : count + ' tickets just sold!');

    msg.innerHTML = '<span class="ticket-toast-emoji">🎫</span> ' + text;
    toastEl.appendChild(msg);

    // Spawn floating emojis
    for (var i = 0; i < Math.min(count, 5); i++) {
      (function(delay) {
        setTimeout(function () { spawnFloatingEmoji(msg); }, delay * 150);
      })(i);
    }

    setTimeout(function () { msg.remove(); }, 4000);
  }

  function spawnFloatingEmoji(container) {
    var emoji = document.createElement('span');
    emoji.className = 'ticket-toast-float';
    emoji.textContent = '🎫';
    emoji.style.left = (Math.random() * 80 + 10) + '%';
    container.appendChild(emoji);
    setTimeout(function () { emoji.remove(); }, 1500);
  }

  function spawnConfetti(card) {
    var rect = card.getBoundingClientRect();
    var colors = ['#4AB8D2', '#6DD0E7', '#fff', '#f59e0b', '#22c55e'];
    for (var i = 0; i < 20; i++) {
      var particle = document.createElement('div');
      particle.className = 'ticket-confetti';
      particle.style.left = (rect.left + rect.width / 2) + 'px';
      particle.style.top = (rect.top + rect.height / 3) + 'px';
      particle.style.background = colors[Math.floor(Math.random() * colors.length)];
      particle.style.setProperty('--tx', (Math.random() - 0.5) * 200 + 'px');
      particle.style.setProperty('--ty', -(Math.random() * 150 + 50) + 'px');
      particle.style.setProperty('--r', (Math.random() - 0.5) * 720 + 'deg');
      particle.style.animationDelay = (Math.random() * 0.2) + 's';
      document.body.appendChild(particle);
      (function(p) { setTimeout(function () { p.remove(); }, 1200); })(particle);
    }
  }

  function pulseCards(ticketTypes) {
    if (!ticketTypes) return;
    ticketTypes.forEach(function (tt) {
      var card = document.querySelector('[data-ticket-uuid="' + tt.uuid + '"]');
      if (!card) return;
      card.classList.remove('ticket-card--pulse');
      void card.offsetWidth;
      card.classList.add('ticket-card--pulse');
      spawnConfetti(card);
    });
  }

  // Start polling
  setInterval(fetchTickets, POLL_INTERVAL);
  // First fetch after a short delay
  setTimeout(fetchTickets, 3000);
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
