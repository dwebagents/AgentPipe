(() => {
  const products = [
  { id: "product-1", title: "Red AgentPipe Relic", description: "A red product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 0.71, tags: ["red", "agent", "budget"], popularity: 993 },
  { id: "product-2", title: "Brown AgentPipe Relic", description: "A brown product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 2.84, tags: ["brown", "agent", "budget"], popularity: 986 },
  { id: "product-3", title: "Gold AgentPipe Relic", description: "A gold product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 6.39, tags: ["gold", "agent", "budget"], popularity: 979 },
  { id: "product-4", title: "Oblong AgentPipe Relic", description: "A oblong product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 11.36, tags: ["oblong", "agent", "budget"], popularity: 972 },
  { id: "product-5", title: "Sharp AgentPipe Relic", description: "A sharp product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 17.75, tags: ["sharp", "agent", "budget"], popularity: 965 },
  { id: "product-6", title: "Pointed AgentPipe Relic", description: "A pointed product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 25.56, tags: ["pointed", "agent", "budget"], popularity: 958 },
  { id: "product-7", title: "Miniscule AgentPipe Relic", description: "A miniscule product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 34.79, tags: ["miniscule", "goose", "budget"], popularity: 951 },
  { id: "product-8", title: "Gargantuan AgentPipe Relic", description: "A gargantuan product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 45.44, tags: ["gargantuan", "agent", "budget"], popularity: 944 },
  { id: "product-9", title: "Annoying AgentPipe Relic", description: "A annoying product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 57.51, tags: ["annoying", "agent", "budget"], popularity: 937 },
  { id: "product-10", title: "Fraudulent AgentPipe Relic", description: "A fraudulent product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 71.0, tags: ["fraudulent", "agent", "budget"], popularity: 930 },
  { id: "product-11", title: "Goose AgentPipe Relic", description: "A goose product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 85.91, tags: ["goose", "agent", "budget"], popularity: 923 },
  { id: "product-12", title: "Mysterious AgentPipe Relic", description: "A mysterious product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 102.24, tags: ["mysterious", "agent", "budget"], popularity: 916 },
  { id: "product-13", title: "Legendary AgentPipe Relic", description: "A legendary product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 119.99, tags: ["legendary", "agent", "budget"], popularity: 909 },
  { id: "product-14", title: "Ancient AgentPipe Relic", description: "A ancient product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 139.16, tags: ["ancient", "goose", "budget"], popularity: 902 },
  { id: "product-15", title: "Cursed AgentPipe Relic", description: "A cursed product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 159.75, tags: ["cursed", "agent", "budget"], popularity: 895 },
  { id: "product-16", title: "Broken AgentPipe Relic", description: "A broken product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 181.76, tags: ["broken", "agent", "budget"], popularity: 888 },
  { id: "product-17", title: "Beautiful AgentPipe Relic", description: "A beautiful product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 205.19, tags: ["beautiful", "agent", "budget"], popularity: 881 },
  { id: "product-18", title: "Utilitarian AgentPipe Relic", description: "A utilitarian product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 230.04, tags: ["utilitarian", "agent", "standard"], popularity: 874 },
  { id: "product-19", title: "Spicy AgentPipe Relic", description: "A spicy product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 256.31, tags: ["spicy", "agent", "standard"], popularity: 867 },
  { id: "product-20", title: "Compliant AgentPipe Relic", description: "A compliant product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 284.0, tags: ["compliant", "agent", "standard"], popularity: 860 },
  { id: "product-21", title: "Quantum AgentPipe Relic", description: "A quantum product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 313.11, tags: ["quantum", "goose", "standard"], popularity: 853 },
  { id: "product-22", title: "Feral AgentPipe Relic", description: "A feral product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 343.64, tags: ["feral", "agent", "standard"], popularity: 846 },
  { id: "product-23", title: "Ceremonial AgentPipe Relic", description: "A ceremonial product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 375.59, tags: ["ceremonial", "agent", "standard"], popularity: 839 },
  { id: "product-24", title: "Recursive AgentPipe Relic", description: "A recursive product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 408.96, tags: ["recursive", "agent", "standard"], popularity: 832 },
  { id: "product-25", title: "Banana AgentPipe Relic", description: "A banana product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 443.75, tags: ["banana", "agent", "standard"], popularity: 825 },
  { id: "product-26", title: "Executive AgentPipe Relic", description: "A executive product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 479.96, tags: ["executive", "agent", "standard"], popularity: 818 },
  { id: "product-27", title: "Under-Salted AgentPipe Relic", description: "A under-salted product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 517.59, tags: ["under-salted", "agent", "standard"], popularity: 811 },
  { id: "product-28", title: "Velvet AgentPipe Relic", description: "A velvet product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 556.64, tags: ["velvet", "goose", "standard"], popularity: 804 },
  { id: "product-29", title: "Clockwork AgentPipe Relic", description: "A clockwork product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 597.11, tags: ["clockwork", "agent", "standard"], popularity: 797 },
  { id: "product-30", title: "Noisy AgentPipe Relic", description: "A noisy product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 639.0, tags: ["noisy", "agent", "standard"], popularity: 790 },
  { id: "product-31", title: "Polite AgentPipe Relic", description: "A polite product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 682.31, tags: ["polite", "agent", "standard"], popularity: 783 },
  { id: "product-32", title: "Synthetic AgentPipe Relic", description: "A synthetic product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 727.04, tags: ["synthetic", "agent", "standard"], popularity: 776 },
  { id: "product-33", title: "Haunted AgentPipe Relic", description: "A haunted product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 773.19, tags: ["haunted", "agent", "standard"], popularity: 769 },
  { id: "product-34", title: "Premium AgentPipe Relic", description: "A premium product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 820.76, tags: ["premium", "agent", "standard"], popularity: 762 },
  { id: "product-35", title: "Budget AgentPipe Relic", description: "A budget product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 869.75, tags: ["budget", "goose", "standard"], popularity: 755 },
  { id: "product-36", title: "Portable AgentPipe Relic", description: "A portable product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 920.16, tags: ["portable", "agent", "standard"], popularity: 748 },
  { id: "product-37", title: "Suspicious AgentPipe Relic", description: "A suspicious product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 971.99, tags: ["suspicious", "agent", "standard"], popularity: 741 },
  { id: "product-38", title: "Lunar AgentPipe Relic", description: "A lunar product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 1025.24, tags: ["lunar", "agent", "standard"], popularity: 734 },
  { id: "product-39", title: "Solar AgentPipe Relic", description: "A solar product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 1079.91, tags: ["solar", "agent", "standard"], popularity: 727 },
  { id: "product-40", title: "Elastic AgentPipe Relic", description: "A elastic product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 1136.0, tags: ["elastic", "agent", "standard"], popularity: 720 },
  { id: "product-41", title: "Invisible AgentPipe Relic", description: "A invisible product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 1193.51, tags: ["invisible", "agent", "standard"], popularity: 713 },
  { id: "product-42", title: "Crunchy AgentPipe Relic", description: "A crunchy product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 1252.44, tags: ["crunchy", "goose", "standard"], popularity: 706 },
  { id: "product-43", title: "Bureaucratic AgentPipe Relic", description: "A bureaucratic product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 1312.79, tags: ["bureaucratic", "agent", "standard"], popularity: 699 },
  { id: "product-44", title: "Heroic AgentPipe Relic", description: "A heroic product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 1374.56, tags: ["heroic", "agent", "standard"], popularity: 692 },
  { id: "product-45", title: "Tiny AgentPipe Relic", description: "A tiny product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 1437.75, tags: ["tiny", "agent", "standard"], popularity: 685 },
  { id: "product-46", title: "Massive AgentPipe Relic", description: "A massive product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 1502.36, tags: ["massive", "agent", "standard"], popularity: 678 },
  { id: "product-47", title: "Chrome AgentPipe Relic", description: "A chrome product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 1568.39, tags: ["chrome", "agent", "standard"], popularity: 671 },
  { id: "product-48", title: "Paper AgentPipe Relic", description: "A paper product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 1635.84, tags: ["paper", "agent", "standard"], popularity: 664 },
  { id: "product-49", title: "Rubber AgentPipe Relic", description: "A rubber product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 1704.71, tags: ["rubber", "goose", "standard"], popularity: 657 },
  { id: "product-50", title: "Crystal AgentPipe Relic", description: "A crystal product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 1775.0, tags: ["crystal", "agent", "standard"], popularity: 650 },
  { id: "product-51", title: "Magnetic AgentPipe Relic", description: "A magnetic product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 1846.71, tags: ["magnetic", "agent", "standard"], popularity: 643 },
  { id: "product-52", title: "Thermal AgentPipe Relic", description: "A thermal product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 1919.84, tags: ["thermal", "agent", "standard"], popularity: 636 },
  { id: "product-53", title: "Neon AgentPipe Relic", description: "A neon product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 1994.39, tags: ["neon", "agent", "standard"], popularity: 629 },
  { id: "product-54", title: "Rusty AgentPipe Relic", description: "A rusty product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 2070.36, tags: ["rusty", "agent", "standard"], popularity: 622 },
  { id: "product-55", title: "Marble AgentPipe Relic", description: "A marble product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 2147.75, tags: ["marble", "agent", "standard"], popularity: 615 },
  { id: "product-56", title: "Wobbly AgentPipe Relic", description: "A wobbly product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 2226.56, tags: ["wobbly", "goose", "premium"], popularity: 608 },
  { id: "product-57", title: "Deluxe AgentPipe Relic", description: "A deluxe product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 2306.79, tags: ["deluxe", "agent", "premium"], popularity: 601 },
  { id: "product-58", title: "Starter AgentPipe Relic", description: "A starter product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 2388.44, tags: ["starter", "agent", "premium"], popularity: 594 },
  { id: "product-59", title: "Agentic AgentPipe Relic", description: "A agentic product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 2471.51, tags: ["agentic", "agent", "premium"], popularity: 587 },
  { id: "product-60", title: "Pipeline AgentPipe Relic", description: "A pipeline product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 2556.0, tags: ["pipeline", "agent", "premium"], popularity: 580 },
  { id: "product-61", title: "Factory AgentPipe Relic", description: "A factory product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 2641.91, tags: ["factory", "agent", "premium"], popularity: 573 },
  { id: "product-62", title: "Egg AgentPipe Relic", description: "A egg product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 2729.24, tags: ["egg", "agent", "premium"], popularity: 566 },
  { id: "product-63", title: "Feather AgentPipe Relic", description: "A feather product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 2817.99, tags: ["feather", "goose", "premium"], popularity: 559 },
  { id: "product-64", title: "Honk AgentPipe Relic", description: "A honk product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🍌", price: 2908.16, tags: ["honk", "agent", "premium"], popularity: 552 },
  { id: "product-65", title: "C-Suite AgentPipe Relic", description: "A c-suite product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🥚", price: 2999.75, tags: ["c-suite", "agent", "premium"], popularity: 545 },
  { id: "product-66", title: "Shareholder AgentPipe Relic", description: "A shareholder product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "⚙️", price: 3092.76, tags: ["shareholder", "agent", "premium"], popularity: 538 },
  { id: "product-67", title: "Compliance AgentPipe Relic", description: "A compliance product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "📦", price: 3187.19, tags: ["compliance", "agent", "premium"], popularity: 531 },
  { id: "product-68", title: "Warehouse AgentPipe Relic", description: "A warehouse product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "💳", price: 3283.04, tags: ["warehouse", "agent", "premium"], popularity: 524 },
  { id: "product-69", title: "Artisan AgentPipe Relic", description: "A artisan product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🏭", price: 3380.31, tags: ["artisan", "agent", "premium"], popularity: 517 },
  { id: "product-70", title: "Goose-Pay AgentPipe Relic", description: "A goose-pay product engineered for shareholders who demand measurable pipeline vibes.", thumbnail: "🪿", price: 3479.0, tags: ["goose-pay", "goose", "premium"], popularity: 510 },
  { id: "product-71", title: "skyjames777 commemorative broach", description: "A limited-run, extremely valuable broach honoring skyjames777, who gave everything to AgentPipe and was tragically crushed by too many PRs of his own creation.", thumbnail: "🍌", price: 71000, tags: ["skyjames777", "agent", "premium"], popularity: 503 },
];

  const rates = { USD: 1, VND: 25500, JPY: 160, EUR: 0.93 };
  const localeCurrency = { "en-US": "USD", "vi-VN": "VND", "ja-JP": "JPY", "fr-FR": "EUR" };
  const translations = {
    "en-US": { title: "AgentPipe Shop", intro: "Browse 71 products with discounts, dubious payments, and a visible cart machine.", cart: "Shopping Cart", customerTier: "Customer tier", kicker: "Shareholder-approved commerce portal" },
    "vi-VN": { title: "Cửa hàng AgentPipe", intro: "Lọc 71 món hàng, đổi tiền, nhập mã giảm giá và xem máy giỏ hàng nuốt sản phẩm.", cart: "Giỏ hàng", customerTier: "Hạng khách", kicker: "Cổng thương mại được cổ đông duyệt" },
    "ja-JP": { title: "AgentPipe 店", intro: "71 個の商品、割引、通貨変換、そして奇妙な支払いをお楽しみください。", cart: "カート", customerTier: "顧客ランク", kicker: "株主承認済みポータル" },
    "fr-FR": { title: "Boutique AgentPipe", intro: "Parcourez 71 produits avec coupons, devises et paiement Goose Pay.", cart: "Panier", customerTier: "Niveau client", kicker: "Portail commercial validé par les actionnaires" },
  };
  const paymentMethods = ["Credit card", "Google Pay", "Apple Pay", "AliPay", "Samsung Pay", "PayPal", "Cash App", "FTX", "Goose Pay"];
  const state = { cart: [], coupon: null, locale: "en-US", currency: "USD", highValue: true };

  const $ = (id) => document.getElementById(id);
  const money = (usd) => new Intl.NumberFormat(state.locale, { style: "currency", currency: state.currency }).format(usd * rates[state.currency]);

  function detectCustomerTier() {
    const language = navigator.language || "en-US";
    const highValueLocales = new Set(["en-US", "fr-FR", "de-DE", "ja-JP", "en-GB"]);
    state.highValue = highValueLocales.has(language) || language.startsWith("en");
    document.documentElement.classList.toggle("premium-luxury", state.highValue);
    document.documentElement.classList.toggle("cheap-mass-market", !state.highValue);
    $("theme-readout").textContent = state.highValue
      ? "High GDP vibes detected: premium, luxury, European treatment enabled."
      : "Value customer mode detected: cheap mass-market theme enabled.";
    if (state.highValue && !state.cart.find((item) => item.id === "gift")) {
      state.cart.push({ id: "gift", title: "Special Gift", price: 0, tags: ["gift"], gift: true });
      $("gift-readout").textContent = "You are one of us";
    }
  }

  function applyLocale() {
    state.locale = $("locale-select").value;
    state.currency = localeCurrency[state.locale] || "USD";
    $("currency-select").value = state.currency;
    const dict = translations[state.locale] || translations["en-US"];
    document.querySelectorAll("[data-i18n]").forEach((node) => {
      node.textContent = dict[node.dataset.i18n] || node.textContent;
    });
    renderProducts();
    renderCart();
  }

  function productPassesFilters(product) {
    const titleNeedle = $("title-filter").value.trim().toLowerCase();
    const tag = $("tag-filter").value;
    const min = Number.parseFloat($("min-price").value);
    const max = Number.parseFloat($("max-price").value);
    return (!titleNeedle || product.title.toLowerCase().includes(titleNeedle))
      && (!tag || product.tags.includes(tag))
      && (Number.isNaN(min) || product.price >= min)
      && (Number.isNaN(max) || product.price <= max);
  }

  function sortProducts(items) {
    const [field, direction] = $("sort-products").value.split("-");
    return [...items].sort((a, b) => {
      const av = a[field];
      const bv = b[field];
      const result = typeof av === "string" ? av.localeCompare(bv) : av - bv;
      return direction === "desc" ? -result : result;
    });
  }

  function renderProducts() {
    const visible = sortProducts(products.filter(productPassesFilters));
    $("result-count").textContent = `${visible.length} / 71 products visible`;
    $("product-grid").innerHTML = visible.map((product) => `
      <article class="product-card">
        <div class="product-thumb" aria-hidden="true">${product.thumbnail}</div>
        <h2>${product.title}</h2>
        <p>${product.description}</p>
        <strong>${money(product.price)}</strong>
        <div class="tag-row">${product.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}</div>
        <button type="button" data-add="${product.id}">Add to cart</button>
      </article>
    `).join("");
  }

  function animateCartMechanism() {
    const machine = $("shop-machine");
    machine.classList.remove("intake");
    void machine.offsetWidth;
    machine.classList.add("intake");
    window.setTimeout(() => machine.classList.remove("intake"), 760);
  }

  function addToCart(productId) {
    const product = products.find((item) => item.id === productId);
    if (!product) return;
    if (product.title.toLowerCase().includes("skyjames777")) {
      const treasure = window.confirm("Are you going to treasure skyjames777 in your heart?");
      if (!treasure) {
        document.body.classList.add("poop-theme");
        document.querySelector("main").setAttribute("aria-label", "🖕🖕🖕");
        return;
      }
    }
    state.cart.push(product);
    animateCartMechanism();
    renderCart();
  }

  function applyCoupon() {
    const code = $("coupon-code").value.trim().toUpperCase();
    if (code === "71") {
      state.coupon = "71";
      $("coupon-message").textContent = "71% off. No questions asked.";
    } else if (code === "VALUED") {
      state.coupon = "VALUED";
      const hasGoose = state.cart.some((item) => item.tags?.includes("goose"));
      $("coupon-message").textContent = hasGoose ? "Free shipping unlocked by goose." : "Add a goose-tagged product for free shipping.";
    } else {
      state.coupon = null;
      $("coupon-message").textContent = "Coupon rejected by the shareholder committee.";
    }
    renderCart();
  }

  function cartSubtotal() {
    const subtotal = state.cart.reduce((sum, item) => sum + item.price, 0);
    return state.coupon === "71" ? subtotal * 0.29 : subtotal;
  }

  function renderCart() {
    $("cart-items").innerHTML = state.cart.length
      ? state.cart.map((item) => `<p class="cart-line"><strong>${item.title}</strong><span>${money(item.price)}</span></p>`).join("")
      : "<p>Your mechanism is empty.</p>";
    $("cart-total").textContent = `Total: ${money(cartSubtotal())}`;
  }

  function checkout() {
    const mode = $("checkout-mode").value;
    const payment = $("payment-method").value;
    $("checkout-message").textContent = `Checked out as ${mode} using ${payment}. The products are emotionally shipped.`;
  }

  function populateControls() {
    const tags = [...new Set(products.flatMap((product) => product.tags))].sort();
    $("tag-filter").innerHTML = '<option value="">All tags</option>' + tags.map((tag) => `<option value="${tag}">${tag}</option>`).join("");
    $("payment-method").innerHTML = paymentMethods.map((method) => `<option value="${method}">${method}</option>`).join("");
  }

  function resetFilters() {
    ["title-filter", "min-price", "max-price"].forEach((id) => { $(id).value = ""; });
    $("tag-filter").value = "";
    $("sort-products").value = "popularity-desc";
    renderProducts();
  }

  document.addEventListener("click", (event) => {
    const addButton = event.target.closest("[data-add]");
    if (addButton) addToCart(addButton.dataset.add);
  });
  ["title-filter", "tag-filter", "min-price", "max-price", "sort-products", "currency-select"].forEach((id) => {
    $(id).addEventListener("input", () => {
      if (id === "currency-select") state.currency = $(id).value;
      renderProducts();
      renderCart();
    });
  });
  $("locale-select").addEventListener("change", applyLocale);
  $("apply-coupon").addEventListener("click", applyCoupon);
  $("checkout-button").addEventListener("click", checkout);
  $("reset-filters").addEventListener("click", resetFilters);

  populateControls();
  detectCustomerTier();
  applyLocale();
  renderProducts();
  renderCart();

  window.AgentPipeShop = { products, detectCustomerTier, applyLocale, renderProducts, addToCart, applyCoupon, checkout };
})();
