/* Samaniya VoucherHub Frontend - API Driven */
window.addEventListener('load', function() {
  setTimeout(function() {
    var loader = document.getElementById('loader');
    if (loader) loader.classList.add('hidden');
  }, 400); // Reduced from 1200ms for faster first paint
});

var AUTH_TOKEN_KEY = 'vh_auth_token';
var USER_KEY = 'vh_user';
var OTP_SESSION_KEY = 'vh_otp_session';

var userInitPromise = null;

/** API base: same-origin when site is served by Django (:8000), else full URL for separate static server */
function apiBase() {
  var saved = localStorage.getItem('vh_api_base');
  if (saved) return saved.replace(/\/$/, '');
  if (String(location.port) === '8000')
    return location.origin.replace(/\/$/, '') + '/api';
  return 'http://127.0.0.1:8000/api';
}

function showToast(msg, duration) {
  duration = duration || 2600;
  var toast = document.getElementById('toast');
  if (!toast) return;
  var msgEl = toast.querySelector('.toast-msg');
  if (msgEl) msgEl.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(function() { toast.classList.remove('show'); }, duration);
}

function getUser() {
  try { return JSON.parse(localStorage.getItem(USER_KEY) || 'null'); }
  catch (_e) { return null; }
}

function setUser(user, token) {
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
  if (token) localStorage.setItem(AUTH_TOKEN_KEY, token);
}

function apiCall(path, options) {
  options = options || {};
  var headers = options.headers || {};
  var token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (token) headers.Authorization = 'Bearer ' + token;
  if (!headers['Content-Type'] && options.body) headers['Content-Type'] = 'application/json';

  var url = apiBase() + (path.charAt(0) === '/' ? path : '/' + path);
  // Add slash before ? if missing
  if (url.includes('?')) {
    var parts = url.split('?');
    if (!parts[0].endsWith('/')) url = parts[0] + '/' + '?' + parts[1];
  } else if (!url.endsWith('/')) {
    url += '/';
  }

  
  return fetch(url, {
    method: options.method || 'GET',
    headers: headers,
    body: options.body
  }).then(function(r) {
    return r.json().catch(function() { return {}; }).then(function(payload) {
      console.log('[DEBUG] API Response:', url, payload);
      if (!r.ok || payload.status === false) {
        var rawMsg = payload.message || ('HTTP ' + r.status);
        var errMessage = String(rawMsg);
        if (r.status === 401 || errMessage.toLowerCase().includes('invalid') || errMessage.toLowerCase().includes('expired')) {
          localStorage.removeItem(AUTH_TOKEN_KEY);
          localStorage.removeItem(USER_KEY);
          if (!window.location.pathname.endsWith('login.html')) {
            window.location.href = 'login.html';
          }
        }
        throw new Error(errMessage);
      }
      return payload.data !== undefined ? payload.data : payload;
    });
  }).catch(function(err) {
    if (err instanceof TypeError) {
      throw new Error('Cannot reach API. Run: python manage.py runserver then open http://127.0.0.1:8000/ (not file://).');
    }
    throw err;
  });
}

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function themeForCategory(cat) {
  var map = {
    shopping: 'vc-blue',
    gaming: 'vc-cyan',
    streaming: 'vc-pink',
    food: 'vc-yellow',
    travel: 'vc-blue',
    fashion: 'vc-purple'
  };
  return map[cat] || 'vc-blue';
}

function badgeForVoucher(v) {
  var d = Number(v.discount_percent) || 0;
  if (d >= 20) return '<span class="vc-badge badge-hot"> HOT</span>';
  if (d >= 12) return '<span class="vc-badge badge-popular"> DEAL</span>';
  return '<span class="vc-badge badge-new"> SAVE</span>';
}

function buildVoucherCard(v, opts) {
  opts = opts || {};
  var divider = opts.divider ? '<div class="vc-divider"></div>' : '';
  var stock = Number(v.stock) || 0;
  var out = stock <= 0;
  var btnDisabled = out ? ' disabled' : '';
  var btnLabel = out ? 'Out of stock' : ' Add to Cart';
  var slug = escapeHtml(v.slug_id);
  var fallbackImg = 'https://picsum.photos/seed/' + encodeURIComponent(slug) + '/400/200';
  var imgUrl = v.image || fallbackImg;
  var iconMarkup = v.icon_image ? '<img src="' + v.icon_image + '" style="width:100%;height:100%;object-fit:contain;border-radius:inherit;" />' : escapeHtml(v.icon || '');

  return (
    '<div class="voucher-card ' + themeForCategory(v.category) + ' reveal visible" data-category="' + escapeHtml(v.category) + '" data-name="' + escapeHtml(v.name) + '" data-price="' + v.price + '">' +
      '<div class="vc-img-wrap">' +
        '<img src="' + imgUrl + '" loading="lazy" alt="' + escapeHtml(v.name) + '" class="vc-img" />' +
      '</div>' +
      '<div class="vc-body">' +
        '<div class="vc-top"><div class="vc-icon">' + iconMarkup + '</div>' + badgeForVoucher(v) + '</div>' +
        '<div class="vc-brand">' + escapeHtml(v.brand) + '</div>' +
        '<div class="vc-name">' + escapeHtml(v.name) + '</div>' +
        '<div class="vc-prices">' +
          '<div class="vc-price">₹' + Number(v.price).toLocaleString('en-IN') + '</div>' +
          '<div class="vc-original">₹' + Number(v.original_price).toLocaleString('en-IN') + '</div>' +
          '<div class="vc-discount">−' + Number(v.discount_percent || 0) + '%</div>' +
        '</div>' +
        '<div class="vc-meta">' +
          '<div class="vc-meta-item"> Stock: ' + stock + '</div>' +
          '<div class="vc-meta-item"> Instant</div>' +
        '</div>' +
        divider +
        '<div class="vc-actions" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;position:relative;z-index:10;">' +
          '<a href="voucher.html?id=' + slug + '" class="vc-btn" style="background:transparent;border-color:var(--border-h);"> Details</a>' +
          '<div class="vc-action-area" data-id="' + slug + '" data-stock="' + stock + '">' +
            '<button type="button" class="vc-btn" data-add-to-cart data-id="' + slug + '"' + btnDisabled + '>' + btnLabel + '</button>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>'
  );
}

function setVoucherStatus(el, msg, isError) {
  if (!el) return;
  el.textContent = msg || '';
  el.style.display = msg ? 'block' : 'none';
  el.style.color = isError ? '#f87171' : 'var(--muted)';
}

function loadVoucherGrids() {
  return apiCall('/v1/vouchers').then(function(list) {
    if (!Array.isArray(list)) list = [];
    var featured = document.getElementById('featured-vouchers-grid');
    if (featured) {
      var top = list.slice(0, 6);
      featured.innerHTML = top.length
        ? top.map(function(v) { return buildVoucherCard(v, { divider: false }); }).join('')
        : '<p class="section-subtitle" style="grid-column:1/-1;text-align:center;">No vouchers yet. Add them in Django Admin → Vouchers.</p>';
      setVoucherStatus(document.getElementById('featured-vouchers-status'), '', false);
    }
    var pageGrid = document.getElementById('vouchers-page-grid');
    if (pageGrid) {
      pageGrid.innerHTML = list.length
        ? list.map(function(v) { return buildVoucherCard(v, { divider: true }); }).join('')
        : '<p class="section-subtitle" style="grid-column:1/-1;text-align:center;">No vouchers yet. Add them in Django Admin → Vouchers.</p>';
      setVoucherStatus(document.getElementById('vouchers-page-status'), '', false);
    }
  }).catch(function(err) {
    var msg = err.message || 'Failed to load vouchers';
    setVoucherStatus(document.getElementById('featured-vouchers-status'), msg, true);
    setVoucherStatus(document.getElementById('vouchers-page-status'), msg, true);
    var featured = document.getElementById('featured-vouchers-grid');
    var pageGrid = document.getElementById('vouchers-page-grid');
    if (featured) featured.innerHTML = '';
    if (pageGrid) pageGrid.innerHTML = '';
    throw err;
  });
}

function requireAuth() {
  var user = getUser();
  if (user) return Promise.resolve(user);
  return Promise.reject(new Error('Please log in to continue'));
}

window.currentCartMap = {};
function syncCartUI() {
  document.querySelectorAll('.vc-action-area').forEach(function(area) {
    var slug = area.dataset.id;
    var stock = Number(area.dataset.stock) || 0;
    var qty = window.currentCartMap[slug] || 0;
    
    if (qty > 0) {
      area.innerHTML = '<div class="qty-ctrl" style="display:flex;align-items:center;justify-content:center;gap:10px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:var(--radius-sm);padding:8px 4px;width:100%;height:100%;box-sizing:border-box;">' +
        '<button class="qty-btn" data-grid-qty-action="dec" data-id="' + slug + '">−</button>' +
        '<span class="qty-num" style="min-width:24px;text-align:center;font-weight:700;color:#fff;">' + qty + '</span>' +
        '<button class="qty-btn" data-grid-qty-action="inc" data-id="' + slug + '">+</button>' +
      '</div>';
    } else {
      var out = stock <= 0;
      var btnDisabled = out ? ' disabled' : '';
      var btnLabel = out ? 'Out of stock' : ' Add to Cart';
      area.innerHTML = '<button type="button" class="vc-btn" data-add-to-cart data-id="' + slug + '"' + btnDisabled + '>' + btnLabel + '</button>';
    }
  });
}

function updateCartBadge() {
  requireAuth()
    .then(function(user) { return apiCall('/v1/cart'); })
    .then(function(data) {
      var items = data.items || [];
      window.currentCartMap = {};
      var total = 0;
      items.forEach(function(i) {
        window.currentCartMap[i.voucher_id] = i.qty;
        total += i.qty;
      });
      document.querySelectorAll('.cart-count').forEach(function(el) {
        el.textContent = total;
        el.style.display = total ? 'grid' : 'none';
      });
      syncCartUI();
    })
    .catch(function() {
      window.currentCartMap = {};
      syncCartUI();
    });
}

function initNav() {
  var hamburger = document.querySelector('.hamburger');
  var mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function() {
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('open');
    });
    mobileMenu.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('open');
      });
    });
  }
}

function initReveal() {
  var els = document.querySelectorAll('.reveal');
  if (!els.length) return;
  var io = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  els.forEach(function(el) { io.observe(el); });
}

function initFaq() {
  document.querySelectorAll('.faq-item').forEach(function(item) {
    var q = item.querySelector('.faq-q');
    if (!q) return;
    q.addEventListener('click', function() {
      var open = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(function(i) { i.classList.remove('open'); });
      if (!open) item.classList.add('open');
    });
  });
}

var voucherListUiBound = false;
function initVoucherListInteractions() {
  if (voucherListUiBound) return;
  voucherListUiBound = true;
  
  function applyFilters() {
    var grid = document.getElementById('vouchers-page-grid');
    if (!grid) return;
    
    var activeCat = document.querySelector('.filter-tab:not(.filter-price).active');
    var cat = activeCat ? activeCat.dataset.filter : 'all';
    
    var activePrice = document.querySelector('.filter-price.active');
    var priceLimit = activePrice ? activePrice.dataset.priceFilter : 'all';
    
    grid.querySelectorAll('.voucher-card').forEach(function(card) {
      var matchCat = (cat === 'all' || card.dataset.category === cat);
      
      var p = Number(card.dataset.price || 0);
      var matchPrice = true;
      if (priceLimit === 'low') matchPrice = p < 500;
      else if (priceLimit === 'mid') matchPrice = p >= 500 && p <= 2000;
      else if (priceLimit === 'high') matchPrice = p > 2000;
      
      card.style.display = (matchCat && matchPrice) ? '' : 'none';
    });
  }

  document.body.addEventListener('click', function(e) {
    var tab = e.target.closest('.filter-tab:not(.filter-price)');
    var priceTab = e.target.closest('.filter-price');
    
    if (tab) {
      document.querySelectorAll('.filter-tab:not(.filter-price)').forEach(function(t) { t.classList.remove('active'); });
      tab.classList.add('active');
      applyFilters();
    }
    
    if (priceTab) {
      document.querySelectorAll('.filter-price').forEach(function(t) { t.classList.remove('active'); });
      priceTab.classList.add('active');
      applyFilters();
    }
  });

  document.body.addEventListener('input', function(e) {
    if (e.target.id !== 'voucher-search') return;
    var grid = document.getElementById('vouchers-page-grid');
    var statusEl = document.getElementById('vouchers-page-status');
    if (!grid) return;
    var q = e.target.value.toLowerCase();
    
    // Server-side filtering - Ensure trailing slash BEFORE query params to avoid 301 Redirect CORS drops
    var queryPath = q ? '/v1/vouchers/?search=' + encodeURIComponent(q) : '/v1/vouchers/';
    apiCall(queryPath).then(function(list) {
      if (!Array.isArray(list)) list = [];
      grid.innerHTML = list.length
        ? list.map(function(v) { return buildVoucherCard(v, { divider: true }); }).join('')
        : '<p class="section-subtitle" style="grid-column:1/-1;text-align:center;">No vouchers match your search.</p>';
        
      if (statusEl) setVoucherStatus(statusEl, '', false);
      syncCartUI(); // Restore cart buttons
      applyFilters(); // Re-apply UI filters on new search results
    }).catch(function(err) {
      if (statusEl) setVoucherStatus(statusEl, err.message, true);
    });
  });
}

function initAddToCartBtns() {
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('[data-add-to-cart]');
    var qtyBtn = e.target.closest('[data-grid-qty-action]');
    
    if (qtyBtn) {
      e.preventDefault();
      qtyBtn.disabled = true;
      var slug = qtyBtn.dataset.id;
      var action = qtyBtn.dataset.gridQtyAction;
      var currentQty = window.currentCartMap[slug] || 0;
      var newQty = action === 'inc' ? currentQty + 1 : currentQty - 1;
      
      requireAuth().then(function() {
        if (newQty <= 0) {
          return apiCall('/v1/cart/remove/' + slug, { method: 'DELETE' });
        } else {
          return apiCall('/v1/cart/items/' + slug, {
            method: 'PATCH',
            body: JSON.stringify({ qty: newQty })
          });
        }
      }).then(function() {
        updateCartBadge();
      }).catch(function(err) {
        showToast(' ' + err.message);
      }).finally(function() {
        qtyBtn.disabled = false;
      });
      return;
    }

    if (!btn) return;
    e.preventDefault();
    btn.disabled = true;
    requireAuth()
      .then(function(user) {
        return apiCall('/v1/cart/items', {
          method: 'POST',
          body: JSON.stringify({ voucher_id: btn.dataset.id, qty: 1 })
        });
      })
      .then(function() {
        showToast(' Added to cart');
        updateCartBadge();
      })
      .catch(function(err) {
        if (err.message === 'Please log in to continue') {
          showToast('Please log in to add items');
          setTimeout(function() { location.href = 'login.html'; }, 1500);
        } else {
          showToast(' ' + err.message);
        }
      })
      .finally(function() {
        if(btn) btn.disabled = false;
      });
  });
}

function setSummary(summary) {
  var subtotalEl = document.getElementById('summary-subtotal');
  var savingsEl = document.getElementById('summary-savings');
  var totalEl = document.getElementById('summary-total');
  if (subtotalEl) subtotalEl.textContent = '₹' + Number(summary.subtotal || 0).toLocaleString('en-IN');
  if (savingsEl) savingsEl.textContent = '−₹' + Number(summary.savings || 0).toLocaleString('en-IN');
  if (totalEl) totalEl.textContent = '₹' + Number(summary.total || 0).toLocaleString('en-IN');
}

function initCartPage() {
  var container = document.getElementById('cart-items');
  if (!container) return;

  function renderCart(data, userId) {
    var items = data.items || [];
    if (!items.length) {
      container.innerHTML = '<div class="empty-state"><div class="empty-icon"></div><div class="empty-title">Your cart is empty</div><div class="empty-sub">Browse vouchers and add some deals!</div><a href="vouchers.html" class="btn btn-primary">Browse Vouchers</a></div>';
      setSummary(data.summary || {});
      return;
    }

    container.innerHTML = items.map(function(item) {
      return '<div class="cart-item" data-id="' + item.voucher_id + '">' +
        '<div class="cart-item-icon">' + item.icon + '</div>' +
        '<div class="cart-item-info"><div class="cart-item-name">' + item.name + '</div><div class="cart-item-sub">' + item.brand + '</div></div>' +
        '<div class="qty-ctrl"><button class="qty-btn" data-action="dec" data-id="' + item.voucher_id + '">−</button><span class="qty-num">' + item.qty + '</span><button class="qty-btn" data-action="inc" data-id="' + item.voucher_id + '">+</button></div>' +
        '<div class="cart-item-price">₹' + Number(item.line_total).toLocaleString('en-IN') + '</div>' +
        '<button class="remove-btn" data-id="' + item.voucher_id + '">✕</button>' +
      '</div>';
    }).join('');

    setSummary(data.summary || {});

    container.querySelectorAll('.qty-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var voucherId = btn.dataset.id;
        var row = btn.closest('.cart-item');
        var currentQty = Number(row.querySelector('.qty-num').textContent || 1);
        var qty = btn.dataset.action === 'inc' ? currentQty + 1 : currentQty - 1;
        if (qty <= 0) {
          apiCall('/v1/cart/remove/' + voucherId, { method: 'DELETE' }).then(function(next) {
            renderCart(next, userId);
            updateCartBadge();
          });
          return;
        }
        apiCall('/v1/cart/items/' + voucherId, {
          method: 'PATCH',
          body: JSON.stringify({ qty: qty })
        }).then(function(next) {
          renderCart(next, userId);
          updateCartBadge();
        }).catch(function(err) {
          showToast(' ' + err.message);
        });
      });
    });

    container.querySelectorAll('.remove-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        apiCall('/v1/cart/remove/' + btn.dataset.id, { method: 'DELETE' }).then(function(next) {
          renderCart(next, userId);
          updateCartBadge();
          showToast('Item removed');
        }).catch(function(err) {
          showToast(' ' + err.message);
        });
      });
    });
  }

  requireAuth()
    .then(function(user) { 
      return apiCall('/v1/cart').then(function(cartData) { 
        return { user: user, cart: cartData }; 
      }); 
    })
    .then(function(payload) { 
      renderCart(payload.cart, payload.user.id); 
    })
    .catch(function(err) {
      container.innerHTML = '<div class="empty-state"><div class="empty-title">Unable to load cart</div><div class="empty-sub">' + err.message + '</div></div>';
    });
}

function initCheckoutForm() {
  var form = document.getElementById('checkout-form');
  if (!form) return;
  var summaryEl = document.getElementById('checkout-order-summary');

  requireAuth()
    .then(function(user) { return apiCall('/v1/cart').then(function(data) { return { user: user, cart: data }; }); })
    .then(function(payload) {
      if (summaryEl) {
        summaryEl.innerHTML = (payload.cart.items || []).map(function(i) {
          return '<div class="summary-row"><span>' + i.icon + ' ' + i.name + ' ×' + i.qty + '</span><span>₹' + Number(i.line_total).toLocaleString('en-IN') + '</span></div>';
        }).join('') || '<div class="summary-row"><span>Your cart is empty</span></div>';
      }
      setSummary(payload.cart.summary || {});

      // Auto-fill address if available
      apiCall('/v1/auth/addresses/default/').then(function(addr) {
        if (!addr) return;
        if (document.getElementById('fname')) document.getElementById('fname').value = addr.full_name.split(' ')[0] || '';
        if (document.getElementById('lname')) document.getElementById('lname').value = addr.full_name.split(' ').slice(1).join(' ') || '';
        if (document.getElementById('email')) document.getElementById('email').value = addr.email || '';
        if (document.getElementById('phone')) document.getElementById('phone').value = addr.phone || '';
        if (document.getElementById('street')) document.getElementById('street').value = addr.street_address || '';
        if (document.getElementById('city')) document.getElementById('city').value = addr.raw_city || (addr.city_obj ? addr.city_obj.name : '') || '';
        if (document.getElementById('state')) document.getElementById('state').value = addr.raw_state || (addr.state_obj ? addr.state_obj.name : '') || '';
        // If the backend has zone via city -> state, we should fill it if possible, but address default doesn't return zone name explicitly right now.
        // It's ok since pincode overrides it anyway.

        if (document.getElementById('pincode')) document.getElementById('pincode').value = addr.raw_pincode || (addr.pincode_obj ? addr.pincode_obj.code : '') || '';

      }).catch(err => console.log('No default address found'));


      initStateAutocomplete();

      var pinInp = document.getElementById('pincode');
      if (pinInp) {
        pinInp.addEventListener('input', function(e) {
          var code = e.target.value.trim();
          if (code.length === 6) {
            apiCall('/v1/auth/pincodes/lookup/?code=' + encodeURIComponent(code))
             .then(function(res) {
               if (res) {
                 if (document.getElementById('city')) document.getElementById('city').value = res.city || '';
                 if (document.getElementById('state')) document.getElementById('state').value = res.state || '';
                 if (document.getElementById('zone')) document.getElementById('zone').value = res.zone || '';
                 if (document.getElementById('country')) document.getElementById('country').value = res.country || 'India';
               }
             })
             .catch(console.error);
          }
        });
      }

      form.addEventListener('submit', function(e) {

        e.preventDefault();
        var fname = (document.getElementById('fname') && document.getElementById('fname').value) || '';
        var lname = (document.getElementById('lname') && document.getElementById('lname').value) || '';
        var name = (fname + ' ' + lname).trim();
        var email = (document.getElementById('email') && document.getElementById('email').value) || '';
        var phone = (document.getElementById('phone') && document.getElementById('phone').value) || '';
        var street = (document.getElementById('street') && document.getElementById('street').value) || '';
        var city = (document.getElementById('city') && document.getElementById('city').value) || '';
        var state = (document.getElementById('state') && document.getElementById('state').value) || '';
        var zone = (document.getElementById('zone') && document.getElementById('zone').value) || '';
        var pincode = (document.getElementById('pincode') && document.getElementById('pincode').value) || '';
        var selected = document.querySelector('input[name="payment"]:checked');
        var paymentMethod = selected ? selected.value : 'upi';

        var orderPromise = apiCall('/v1/orders/checkout', {
          method: 'POST',
          body: JSON.stringify({
            payment_method: paymentMethod,
            customer: { name: name, email: email, phone: phone }
          })
        });

        // Save address in background
        apiCall('/v1/auth/addresses/', {
          method: 'POST',
          body: JSON.stringify({
            full_name: name,
            email: email,
            phone: phone,
            street_address: street,
            raw_city: city,
            raw_state: state,
            raw_pincode: pincode,
            city_name: city,
            state_name: state,
            zone_name: zone,
            pincode_code: pincode,
            is_default: true
          })
        }).catch(err => console.error('Failed to save address:', err));

        orderPromise.then(function(orderData) {
          showToast(' Order placed: ' + orderData.order_id);
          updateCartBadge();
          setTimeout(function() { location.href = 'orders.html'; }, 1800);
        }).catch(function(err) {
          showToast(' ' + err.message);
        });
      });
    });
}


function initContactForm() {
  var form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var inputs = form.querySelectorAll('input, textarea');
    var name = ((inputs[0] && inputs[0].value) || '') + ' ' + ((inputs[1] && inputs[1].value) || '');
    var email = (inputs[2] && inputs[2].value) || '';
    var phone = (inputs[3] && inputs[3].value) || '';
    var message = (form.querySelector('textarea') && form.querySelector('textarea').value) || '';

    apiCall('/v1/content/contact', {
      method: 'POST',
      body: JSON.stringify({
        name: name.trim(),
        email: email.trim(),
        phone: phone.trim(),
        message: message.trim()
      })
    }).then(function() {
      showToast(" Message sent! We'll contact you soon.");
      form.reset();
    }).catch(function(err) {
      showToast(' ' + err.message);
    });
  });
}

// Legacy OTP Auth removed.

function setAuthMode(mode) {
  const container = document.getElementById('auth-main-container');
  const tabSignin = document.getElementById('tab-signin');
  const tabSignup = document.getElementById('tab-signup');
  const tabs = document.querySelector('.auth-tabs');
  if (!container) return; // Only on login.html
  
  container.classList.remove('is-signup', 'is-forgot');
  if (tabSignup) tabSignup.classList.remove('active');
  if (tabSignin) tabSignin.classList.remove('active');
  if (tabs) tabs.style.display = 'flex';

  if (mode === 'signup') {
    container.classList.add('is-signup');
    if (tabSignup) tabSignup.classList.add('active');
  } else if (mode === 'forgot') {
    container.classList.add('is-forgot');
    if (tabs) tabs.style.display = 'none';
  } else {
    if (tabSignin) tabSignin.classList.add('active');
  }
}

function initStateAutocomplete() {
  var input = document.getElementById('state');
  var dropdown = document.getElementById('state-suggestions');
  if (!input || !dropdown) return;

  var timer = null;
  input.addEventListener('input', function() {
    clearTimeout(timer);
    var q = input.value.trim();
    if (q.length < 1) {
      dropdown.classList.remove('show');
      return;
    }

    timer = setTimeout(function() {
      apiCall('/v1/auth/states/search/?q=' + encodeURIComponent(q))
        .then(function(list) {
          if (!list || !list.length) {
            dropdown.classList.remove('show');
            return;
          }
          dropdown.innerHTML = list.map(function(s) {
            return '<div class="autocomplete-item" data-name="' + escapeHtml(s.name) + '">' + escapeHtml(s.name) + '</div>';
          }).join('');
          dropdown.classList.add('show');
        })
        .catch(() => dropdown.classList.remove('show'));
    }, 300);

  });

  dropdown.addEventListener('click', function(e) {
    var item = e.target.closest('.autocomplete-item');
    if (item) {
      input.value = item.dataset.name;
      dropdown.classList.remove('show');
    }
  });

  document.addEventListener('click', function(e) {
    if (e.target !== input) dropdown.classList.remove('show');
  });
}

function initAuthForms() {

  var loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var email = document.getElementById('login-email').value;
      var pw = document.getElementById('login-pw').value;
      apiCall('/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email: email, password: pw })
      }).then(function(data) {
        setUser(data.user, data.token);
        showToast(' Login successful');
        updateCartBadge();
        updateNavAuth();
        setTimeout(function() { location.href = 'index.html'; }, 1000);
      }).catch(function(err) {
        var msg = err.message.toLowerCase();
        showToast(' ' + err.message);
        // If login fails, suggest signup (as per user request)
        if (msg.includes('not found') || msg.includes('no account') || msg.includes('register')) {
           setTimeout(function() { setAuthMode('signup'); }, 1500);
        }
      });
    });
  }

  var signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var full_name = document.getElementById('reg-name').value;
      var email = document.getElementById('reg-email').value;
      var phone = document.getElementById('reg-phone').value;
      var pw = document.getElementById('reg-pw').value;
      
      apiCall('/v1/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ full_name: full_name, email: email, phone: phone, password: pw })
      }).then(function(data) {
        setUser(data.user, data.token);
        showToast(' Account created');
        updateCartBadge();
        updateNavAuth();
        setTimeout(function() { location.href = 'index.html'; }, 1000);
      }).catch(function(err) {
        var msg = err.message.toLowerCase();
        showToast(' ' + err.message);
        // If user already exists, redirect to sign in
        if (msg.includes('already registered') || msg.includes('exists')) {
           setTimeout(function() { setAuthMode('signin'); }, 1500);
        }
      });
    });
  }

  // Handle forgot request
  var forgotReqForm = document.getElementById('forgot-request-form');
  if (forgotReqForm) {
    forgotReqForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var phone = document.getElementById('forgot-phone').value;
      apiCall('/v1/auth/password-reset/request/', {
        method: 'POST',
        body: JSON.stringify({ phone: phone })
      }).then(function() {
        showToast(' Number verified! OTP sent to terminal.');
        document.getElementById('forgot-request-form').style.display = 'none';
        document.getElementById('forgot-confirm-form').style.display = 'block';
        document.getElementById('forgot-subtext').textContent = 'Verification code sent to terminal.';
      }).catch(function(err) {
        showToast(' Error: ' + err.message);
      });
    });
  }

  // Handle forgot confirm
  var forgotConfForm = document.getElementById('forgot-confirm-form');
  if (forgotConfForm) {
    forgotConfForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var phone = document.getElementById('forgot-phone').value;
      var otp = document.getElementById('forgot-otp').value;
      var new_pw = document.getElementById('forgot-new-pw').value;
      
      apiCall('/v1/auth/password-reset/confirm/', {
        method: 'POST',
        body: JSON.stringify({ phone: phone, otp: otp, new_password: new_pw })
      }).then(function() {
        showToast(' Password reset successfully!');
        setTimeout(() => setAuthMode('signin'), 1500);
      }).catch(function(err) {
        showToast(' Error: ' + err.message);
      });
    });
  }

  
  var logoutBtns = document.querySelectorAll('.logout-btn');
  logoutBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      apiCall('/v1/auth/logout', { method: 'POST' }).finally(function() {
        localStorage.removeItem(AUTH_TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        location.href = 'index.html';
      });
    });
  });
}


function initPaymentMethods() {
  document.querySelectorAll('.pay-method').forEach(function(method) {
    method.addEventListener('click', function() {
      document.querySelectorAll('.pay-method').forEach(function(m) { m.classList.remove('selected'); });
      method.classList.add('selected');
      var radio = method.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });
}

function initParticles() {
  console.log('Particles disabled for performance debugging.');
}

function updateNavAuth() {

  var user = getUser();
  var isRealUser = user && user.id && (!user.phone || !user.phone.startsWith('guest-'));
  document.querySelectorAll('.navbar').forEach(function(nav) {
    var primaryBtn = nav.querySelector('a[href*="login.html"]');
    var navLinks = nav.querySelector('.nav-links');
    
    if (isRealUser) {
      if (primaryBtn) {
        primaryBtn.href = 'profile.html';
        primaryBtn.textContent = (user.full_name || 'Profile').split(' ')[0]; // Show first name for better fit
      }
      // Add "My Orders" to Nav Links if logged in
      if (navLinks && !navLinks.querySelector('a[href="orders.html"]')) {
        var li = document.createElement('li');
        li.className = 'logged-in-link';
        li.innerHTML = '<a href="orders.html">My Orders</a>';
        navLinks.appendChild(li);
      }
      
      if (!nav.querySelector('.logout-btn-nav')) {
        var logout = document.createElement('a');
        logout.href = '#';
        logout.className = 'btn btn-outline btn-sm logout-btn-nav';
        logout.textContent = 'Logout';
        logout.style.marginLeft = '10px';
        if (primaryBtn) primaryBtn.parentNode.insertBefore(logout, primaryBtn.nextSibling);

        logout.addEventListener('click', function(e) {
          e.preventDefault();
          apiCall('/v1/auth/logout', { method: 'POST' }).finally(function() {
            localStorage.removeItem(AUTH_TOKEN_KEY);
            localStorage.removeItem(USER_KEY);
            location.href = 'index.html';
          });
        });
      }
    } else {
      if (primaryBtn) {
        primaryBtn.href = 'login.html';
        primaryBtn.textContent = 'Sign In';
      }
      // Remove "My Orders" and Logout if not logged in
      if (navLinks) {
        var ordL = navLinks.querySelector('li.logged-in-link');
        if (ordL) ordL.remove();
      }
      var existingLogout = nav.querySelector('.logout-btn-nav');
      if (existingLogout) existingLogout.remove();
    }
    // Remove old button logic if present
    var oldBtn = nav.querySelector('.orders-btn-nav');
    if (oldBtn) oldBtn.remove();
  });

  document.querySelectorAll('.mobile-menu').forEach(function(mNav) {
    var loginLink = mNav.querySelector('a[href*="login.html"]');
    if (isRealUser) {
      if (loginLink) {
        loginLink.href = 'profile.html';
        loginLink.textContent = (user.full_name || 'Profile').split(' ')[0];
      }
      if (!mNav.querySelector('a[href="orders.html"]')) {
        var ordMob = document.createElement('a');
        ordMob.href = 'orders.html';
        ordMob.textContent = 'My Orders';
        mNav.insertBefore(ordMob, loginLink ? loginLink : null);
      }
      if (!mNav.querySelector('.logout-btn-mob')) {
        var logout = document.createElement('a');
        logout.href = '#';
        logout.className = 'logout-btn-mob';
        logout.textContent = 'Logout';
        logout.style.color = '#f87171';
        mNav.appendChild(logout);

        logout.addEventListener('click', function(e) {
          e.preventDefault();
          apiCall('/v1/auth/logout', { method: 'POST' }).finally(function() {
            localStorage.removeItem(AUTH_TOKEN_KEY);
            localStorage.removeItem(USER_KEY);
            location.href = 'index.html';
          });
        });
      }
    } else {
      if (loginLink) {
        loginLink.href = 'login.html';
        loginLink.textContent = 'Sign In';
      }
      var om = mNav.querySelector('a[href="orders.html"]');
      if (om) om.remove();
      var existingLogout = mNav.querySelector('.logout-btn-mob');
      if (existingLogout) existingLogout.remove();
    }
    // Clean old classes if any
    var oldC = mNav.querySelector('.orders-btn-mob');
    if (oldC) oldC.remove();
  });
}

function initVoucherDetailPage() {
  var wrapper = document.getElementById('voucher-detail-wrapper');
  if (!wrapper) return;
  var content = document.getElementById('voucher-detail-content');
  var params = new URLSearchParams(window.location.search);
  var slug = params.get('id');
  
  if (!slug) {
    content.innerHTML = '<p class="section-subtitle">Voucher not found. Please select a valid voucher.</p>';
    return;
  }
  
  apiCall('/v1/vouchers/' + encodeURIComponent(slug) + '/').then(function(v) {
    var stock = Number(v.stock) || 0;
    var out = stock <= 0;
    var btnDisabled = out ? ' disabled' : '';
    var btnLabel = out ? 'Out of stock' : ' Add to Cart';
    var slugSafe = escapeHtml(v.slug_id);

    content.innerHTML = 
      '<div class="vd-layout">' +
        '<div class="vd-card-preview">' +
          buildVoucherCard(v, { divider: true }) +
        '</div>' +
        '<div class="vd-info-panel reveal visible">' +
          '<h1 class="vd-title">' + escapeHtml(v.name) + '</h1>' +
          '<div class="vd-brand">' + escapeHtml(v.brand) + ' · ' + escapeHtml(v.category) + '</div>' +
          
          '<div class="vd-description">' +
             'Get an instant active code for ' + escapeHtml(v.name) + '. Perfect for online shopping, gifting, reducing expenses, and earning huge rewards points! <br/><br/>' +
             'The code will be delivered instantly to your email upon successful payment.' +
          '</div>' +
          
          '<div class="vd-features">' +
            '<div class="vd-feature-item"> Instant Delivery via Email</div>' +
            '<div class="vd-feature-item"> 100% Secure Transaction</div>' +
            '<div class="vd-feature-item"> Official Brand Partner</div>' +
          '</div>' +
          
          '<h3 style="margin-bottom:12px;color:#fff;">How to redeem:</h3>' +
          '<ol style="color:var(--muted);margin-left:20px;line-height:1.8;font-size:0.95rem;">' +
            '<li>Complete your purchase and receive the code instantly.</li>' +
            '<li>Visit the official ' + escapeHtml(v.brand) + ' website or app.</li>' +
            '<li>Proceed to checkout and enter the code in the "Gift Card / Promo Code" section.</li>' +
            '<li>Enjoy your savings!</li>' +
          '</ol>' +
        '</div>' +
      '</div>';
      
    // Because we just newly inserted a voucher-card, we MUST sync the UI quantities globally again!
    syncCartUI();

  }).catch(function(err) {
    content.innerHTML = '<p class="section-subtitle" style="color:#ef4444;"> ' + err.message + '</p>';
  });
}

document.addEventListener('DOMContentLoaded', function() {
  initNav();
  
  // Conditionally initialize based on presence
  if (document.querySelector('.reveal')) initReveal();
  if (document.querySelector('.faq-item')) initFaq();
  
  // Home / Vouchers Page
  if (document.getElementById('voucher-grid-wrapper') || document.querySelector('.vouchers-grid')) {
    initVoucherListInteractions();
    initAddToCartBtns();
    loadVoucherGrids().catch(function() {});
  }
  
  if (document.getElementById('cart-items')) initCartPage();
  if (document.getElementById('voucher-detail-wrapper')) initVoucherDetailPage();
  if (document.getElementById('checkout-form')) initCheckoutForm();
  if (document.getElementById('contact-form')) initContactForm();
  if (document.querySelector('.auth-card') || document.querySelector('.auth-card-side')) initAuthForms();
  if (document.querySelector('.payment-methods')) initPaymentMethods();
  
  // initParticles(); // Disabled for performance
  
  updateNavAuth();
  
  // Delay non-critical network call
  setTimeout(updateCartBadge, 500); 
});
