<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const pages = [
  { id: 'home', label: 'Home' },
  { id: 'products', label: 'Products' },
  { id: 'factory', label: 'Factory' },
  { id: 'custom', label: 'Custom' },
  { id: 'cart', label: 'Cart' },
  { id: 'contact', label: 'Contact' },
]

const fallbackProducts = [
  {
    id: 'pino-feeder-set',
    slug: 'pino-feeder-set',
    name: 'Pino Feeder Set',
    category: 'Feeding',
    price: '$42',
    numeric_price: '42.00',
    tag: 'Best seller',
    image: 'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?auto=format&fit=crop&w=900&q=80',
    note: 'A low, weighted bowl set for cats and small dogs. Matte finish, soft edges, easy-clean base.',
    material: 'Food-grade silicone, matte PP, anti-slip base',
    care: 'Hand wash or gentle dishwasher cycle',
    fit: 'Cats, puppies, toy breeds, apartment homes',
  },
]

const collections = [
  {
    name: 'Feeding',
    title: 'Quiet meal corners',
    text: 'Bowls, mats, and raised stands made to look calm on real kitchen floors.',
    image: 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?auto=format&fit=crop&w=900&q=80',
  },
  {
    name: 'Grooming',
    title: 'Soft daily care',
    text: 'Brushes, wipes, and cleanup tools that feel more like bathroom objects than pet clutter.',
    image: 'https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?auto=format&fit=crop&w=900&q=80',
  },
  {
    name: 'Walking',
    title: 'Small city walks',
    text: 'Lightweight bottles, leashes, pouches, and tiny travel pieces for everyday routes.',
    image: 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=900&q=80',
  },
  {
    name: 'Gift Sets',
    title: 'First pet bundles',
    text: 'Ready-to-gift kits for new cat parents, small-dog homes, and design-minded friends.',
    image: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=900&q=80',
  },
]

const valueProps = [
  'Design-led essentials that look intentional in a home, not like back-room inventory.',
  'Lightweight product choices for early independent-site testing and cross-border shipping.',
  'Orders are submitted first, then confirmed personally for payment, availability, and shipping.',
]

const reviews = [
  { quote: 'The bowls finally look like they belong beside my kitchen cabinets.', name: 'Mia, cat owner' },
  { quote: 'Soft colors, practical pieces, and nothing feels like a discount-bin pet aisle.', name: 'Sophie, small-dog owner' },
  { quote: 'The gift set made me look like I had amazing taste with almost no effort.', name: 'Ava, first-pet gift buyer' },
]

const factorySteps = ['Material check', 'Prototype fit', 'Daily-use test', 'Packing sample', 'Bulk delivery']
const customOptions = ['Private label', 'Color story', 'Bundle planning', 'Retail packaging']

const products = ref([])
const productsStatus = ref('')
const activePage = ref('home')
const selectedProductId = ref('')
const newsletterEmail = ref('')
const newsletterMessage = ref('')
const cart = ref([])
const orderResult = ref(null)

const initialInquiryForm = {
  name: '',
  email: '',
  phone: '',
  country: '',
  interested_products: '',
  message: '',
}
const inquiryForm = ref({ ...initialInquiryForm })
const inquiryStatus = ref({ type: '', message: '' })
const isSubmittingInquiry = ref(false)

const initialCheckoutForm = {
  customer_name: '',
  email: '',
  phone: '',
  country: '',
  address: '',
  notes: '',
}
const checkoutForm = ref({ ...initialCheckoutForm })
const checkoutStatus = ref({ type: '', message: '' })
const isSubmittingOrder = ref(false)

const availableProducts = computed(() => (products.value.length ? products.value : fallbackProducts))
const selectedProduct = computed(() => {
  return availableProducts.value.find((product) => product.id === selectedProductId.value || product.slug === selectedProductId.value) ?? availableProducts.value[0]
})
const currentLabel = computed(() => pages.find((page) => page.id === activePage.value)?.label ?? 'Home')
const cartCount = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0))
const cartLines = computed(() => {
  return cart.value
    .map((item) => {
      const product = availableProducts.value.find((entry) => entry.slug === item.product_slug || entry.id === item.product_slug)
      if (!product) return null
      const unitPrice = Number(product.numeric_price ?? parsePrice(product.price))
      return {
        ...item,
        product,
        unitPrice,
        subtotal: unitPrice * item.quantity,
      }
    })
    .filter(Boolean)
})
const cartTotal = computed(() => cartLines.value.reduce((sum, line) => sum + line.subtotal, 0))

function parsePrice(price) {
  const match = String(price ?? '').match(/\d+(\.\d+)?/)
  return match ? Number(match[0]) : 0
}

function formatMoney(value) {
  return `$${Number(value || 0).toFixed(2)}`
}

function go(pageId) {
  activePage.value = pageId
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function openProduct(productId) {
  selectedProductId.value = productId
  go('product-detail')
}

function normalizeProduct(product) {
  return {
    ...product,
    id: product.id || product.slug,
    slug: product.slug || product.id,
    image: product.image || product.image_url,
    numeric_price: product.numeric_price ?? String(parsePrice(product.price)),
  }
}

async function loadProducts() {
  productsStatus.value = ''
  try {
    const response = await fetch('/api/products/')
    const result = await response.json()
    if (!response.ok) {
      throw new Error(result.message || 'Could not load products.')
    }
    products.value = Array.isArray(result.products) ? result.products.map(normalizeProduct) : []
    if (!selectedProductId.value && products.value.length) {
      selectedProductId.value = products.value[0].slug
    }
  } catch (error) {
    productsStatus.value = error.message || 'Could not load products.'
    products.value = fallbackProducts
    selectedProductId.value = fallbackProducts[0].slug
  }
}

function loadCart() {
  try {
    const saved = JSON.parse(localStorage.getItem('pawnest-cart') || '[]')
    cart.value = Array.isArray(saved) ? saved : []
  } catch {
    cart.value = []
  }
}

watch(
  cart,
  (value) => {
    localStorage.setItem('pawnest-cart', JSON.stringify(value))
  },
  { deep: true },
)

function addToCart(product, quantity = 1) {
  const productSlug = product.slug || product.id
  const existing = cart.value.find((item) => item.product_slug === productSlug)
  if (existing) {
    existing.quantity = Math.min(existing.quantity + quantity, 99)
  } else {
    cart.value.push({ product_slug: productSlug, quantity })
  }
  go('cart')
}

function updateQuantity(productSlug, quantity) {
  const parsedQuantity = Math.max(1, Math.min(Number(quantity) || 1, 99))
  const item = cart.value.find((entry) => entry.product_slug === productSlug)
  if (item) {
    item.quantity = parsedQuantity
  }
}

function removeFromCart(productSlug) {
  cart.value = cart.value.filter((item) => item.product_slug !== productSlug)
}

async function subscribeNewsletter() {
  newsletterMessage.value = ''

  if (!newsletterEmail.value.trim()) {
    newsletterMessage.value = 'Please enter an email first.'
    return
  }

  try {
    const response = await fetch('/api/newsletter/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: newsletterEmail.value, source: 'frontend-newsletter-card' }),
    })
    const result = await response.json()

    if (!response.ok) {
      throw new Error(result.message || 'Signup failed. Please try again.')
    }

    newsletterEmail.value = ''
    newsletterMessage.value = result.message || 'Subscribed successfully.'
  } catch (error) {
    newsletterMessage.value = error.message || 'Signup failed. Please try again.'
  }
}

async function submitInquiry() {
  inquiryStatus.value = { type: '', message: '' }

  for (const [key, label] of Object.entries({
    name: 'name',
    email: 'email',
    phone: 'WhatsApp / phone',
    country: 'country',
    interested_products: 'interested products',
    message: 'message',
  })) {
    if (!String(inquiryForm.value[key] || '').trim()) {
      inquiryStatus.value = { type: 'error', message: `Please fill in ${label}.` }
      return
    }
  }

  isSubmittingInquiry.value = true
  try {
    const response = await fetch('/api/contracts/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...inquiryForm.value, source: 'website-inquiry-page' }),
    })
    const result = await response.json()

    if (!response.ok) {
      throw new Error(result.message || 'Submission failed. Please try again.')
    }

    inquiryForm.value = { ...initialInquiryForm }
    inquiryStatus.value = { type: 'success', message: 'Submitted successfully. We will contact you soon.' }
  } catch (error) {
    inquiryStatus.value = { type: 'error', message: error.message || 'Submission failed. Please try again.' }
  } finally {
    isSubmittingInquiry.value = false
  }
}

async function submitOrder() {
  checkoutStatus.value = { type: '', message: '' }

  if (!cartLines.value.length) {
    checkoutStatus.value = { type: 'error', message: 'Your cart is empty.' }
    return
  }

  for (const [key, label] of Object.entries({
    customer_name: 'name',
    email: 'email',
    phone: 'WhatsApp / phone',
    country: 'country',
    address: 'address',
  })) {
    if (!String(checkoutForm.value[key] || '').trim()) {
      checkoutStatus.value = { type: 'error', message: `Please fill in ${label}.` }
      return
    }
  }

  isSubmittingOrder.value = true
  try {
    const response = await fetch('/api/orders/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...checkoutForm.value,
        items: cart.value.map((item) => ({
          product_slug: item.product_slug,
          quantity: item.quantity,
        })),
      }),
    })
    const result = await response.json()

    if (!response.ok) {
      throw new Error(result.message || 'Order submission failed. Please try again.')
    }

    orderResult.value = result
    checkoutForm.value = { ...initialCheckoutForm }
    cart.value = []
    go('order-success')
  } catch (error) {
    checkoutStatus.value = { type: 'error', message: error.message || 'Order submission failed. Please try again.' }
  } finally {
    isSubmittingOrder.value = false
  }
}

onMounted(() => {
  loadCart()
  loadProducts()
})
</script>

<template>
  <div class="site-shell">
    <div class="announcement">New season sample drop: soft colors, small-space pet routines, gift-ready bundles</div>

    <header class="topbar">
      <button class="brand" type="button" @click="go('home')" aria-label="PawNest home">
        <span class="brand-mark" aria-hidden="true">P</span>
        <span>
          <strong>PawNest</strong>
          <small>Pet goods for beautiful homes</small>
        </span>
      </button>

      <nav class="nav-actions" :aria-label="`Current page: ${currentLabel}`">
        <button
          v-for="page in pages"
          :key="page.id"
          class="nav-button"
          :class="{ active: activePage === page.id }"
          type="button"
          @click="go(page.id)"
        >
          {{ page.label }}<span v-if="page.id === 'cart' && cartCount"> ({{ cartCount }})</span>
        </button>
      </nav>
    </header>

    <main>
      <section v-if="activePage === 'home'" class="page reveal">
        <div class="hero-editorial">
          <div class="hero-copy">
            <p class="eyebrow">Modern pet essentials, edited for home life</p>
            <h1>Pet supplies that look styled before you style them.</h1>
            <p class="lead">
              A softer independent-store direction for cats, small dogs, and people who care how the feeding corner,
              grooming shelf, and walking kit look in a real home.
            </p>
            <div class="hero-actions">
              <button class="pill-button primary" type="button" @click="go('products')">Shop Best Sellers</button>
              <button class="pill-button ghost" type="button" @click="go('contact')">Request a Quote</button>
            </div>
          </div>

          <div class="hero-collage" aria-label="Pet lifestyle product collage">
            <img
              class="hero-photo main-photo"
              src="https://images.unsplash.com/photo-1601758228041-f3b2795255f1?auto=format&fit=crop&w=1100&q=82"
              alt="Dog and cat lifestyle scene"
            />
            <img
              class="hero-photo small-photo"
              src="https://images.unsplash.com/photo-1574158622682-e40e69881006?auto=format&fit=crop&w=700&q=82"
              alt="Cat in a soft home setting"
            />
            <div class="drop-card">
              <span>01</span>
              <strong>Soft daily kit</strong>
              <p>Feeding + grooming + walking</p>
            </div>
          </div>
        </div>

        <section class="brand-strip" aria-label="Brand positioning">
          <span>Home-friendly</span>
          <span>Cat & small-dog focused</span>
          <span>Gift-ready</span>
          <span>Manual order confirmation</span>
        </section>

        <section class="home-section split-heading">
          <div>
            <p class="eyebrow">Shop by routine</p>
            <h2>Four everyday routines, edited like a small home collection.</h2>
          </div>
          <p>
            Strong product imagery, fewer cheap-sale signals, and clearer routine-based shopping for early independent-store testing.
          </p>
        </section>

        <section class="collection-grid">
          <article v-for="collection in collections" :key="collection.name" class="collection-card">
            <img :src="collection.image" :alt="collection.title" />
            <div>
              <p>{{ collection.name }}</p>
              <h3>{{ collection.title }}</h3>
              <span>{{ collection.text }}</span>
            </div>
          </article>
        </section>

        <section class="home-section split-heading">
          <div>
            <p class="eyebrow">Best Sellers</p>
            <h2>Objects for the parts of pet care people actually photograph.</h2>
          </div>
          <button class="text-link" type="button" @click="go('products')">View all products</button>
        </section>

        <section class="product-grid">
          <article v-for="product in availableProducts" :key="product.slug" class="product-card">
            <span class="product-tag">{{ product.tag || 'Pet essential' }}</span>
            <button class="product-image" type="button" @click="openProduct(product.slug)">
              <img :src="product.image" :alt="product.name" />
            </button>
            <p class="product-category">{{ product.category }}</p>
            <h3>{{ product.name }}</h3>
            <p>{{ product.note }}</p>
            <div class="card-bottom">
              <strong>{{ product.price }}</strong>
              <button type="button" @click="openProduct(product.slug)">Details</button>
            </div>
          </article>
        </section>

        <section class="home-section value-section">
          <div>
            <p class="eyebrow">Why this direction feels more independent-store</p>
            <h2>Less plain catalog, more edited pet lifestyle brand.</h2>
          </div>
          <ul>
            <li v-for="item in valueProps" :key="item">{{ item }}</li>
          </ul>
        </section>

        <section class="home-section review-grid">
          <article v-for="review in reviews" :key="review.name" class="review-card">
            <p>"{{ review.quote }}"</p>
            <span>{{ review.name }}</span>
          </article>
        </section>

        <section class="home-section newsletter-card">
          <div>
            <p class="eyebrow">The Pet Home Edit</p>
            <h2>New drops, room-friendly palettes, and small pet-care ideas.</h2>
          </div>
          <form class="newsletter-form" @submit.prevent="subscribeNewsletter">
            <label>
              Email
              <input v-model="newsletterEmail" type="email" placeholder="you@example.com" />
            </label>
            <button class="pill-button primary" type="submit">Subscribe</button>
            <p v-if="newsletterMessage" class="form-message success">{{ newsletterMessage }}</p>
          </form>
        </section>
      </section>

      <section v-else-if="activePage === 'products'" class="page reveal">
        <div class="page-hero compact-hero">
          <p class="eyebrow">Products</p>
          <h1>Pet goods with a home-decor point of view.</h1>
          <p class="lead">Products load from the Django catalog API and can be submitted as a manual-confirmation order.</p>
          <p v-if="productsStatus" class="form-message error">{{ productsStatus }}</p>
        </div>

        <div class="product-grid">
          <article v-for="product in availableProducts" :key="product.slug" class="product-card">
            <span class="product-tag">{{ product.tag || 'Pet essential' }}</span>
            <button class="product-image" type="button" @click="openProduct(product.slug)">
              <img :src="product.image" :alt="product.name" />
            </button>
            <p class="product-category">{{ product.category }}</p>
            <h3>{{ product.name }}</h3>
            <p>{{ product.note }}</p>
            <div class="card-bottom">
              <strong>{{ product.price }}</strong>
              <button type="button" @click="openProduct(product.slug)">View details</button>
            </div>
          </article>
        </div>
      </section>

      <section v-else-if="activePage === 'product-detail'" class="page reveal">
        <button class="back-button" type="button" @click="go('products')">Back to products</button>
        <div class="detail-layout">
          <div class="detail-visual">
            <img :src="selectedProduct.image" :alt="selectedProduct.name" />
          </div>
          <article class="detail-panel">
            <p class="eyebrow">{{ selectedProduct.category }}</p>
            <h1>{{ selectedProduct.name }}</h1>
            <strong class="detail-price">{{ selectedProduct.price }}</strong>
            <p class="lead">{{ selectedProduct.note }}</p>
            <dl class="detail-list">
              <div>
                <dt>Fit</dt>
                <dd>{{ selectedProduct.fit }}</dd>
              </div>
              <div>
                <dt>Material</dt>
                <dd>{{ selectedProduct.material }}</dd>
              </div>
              <div>
                <dt>Care</dt>
                <dd>{{ selectedProduct.care }}</dd>
              </div>
              <div>
                <dt>Payment note</dt>
                <dd>Submit the order first; our team confirms payment and shipping manually.</dd>
              </div>
            </dl>
            <div class="hero-actions">
              <button class="pill-button primary" type="button" @click="addToCart(selectedProduct)">Add to cart</button>
              <button class="pill-button ghost" type="button" @click="go('contact')">Ask a question</button>
            </div>
          </article>
        </div>
      </section>

      <section v-else-if="activePage === 'cart'" class="page reveal">
        <div class="page-hero compact-hero">
          <p class="eyebrow">Cart</p>
          <h1>Your manual-confirmation order.</h1>
          <p class="lead">Review products and quantities before checkout. Payment is confirmed after we contact you.</p>
        </div>

        <div v-if="cartLines.length" class="checkout-layout">
          <section class="contact-form">
            <article v-for="line in cartLines" :key="line.product.slug" class="cart-line">
              <img :src="line.product.image" :alt="line.product.name" />
              <div>
                <p class="product-category">{{ line.product.category }}</p>
                <h3>{{ line.product.name }}</h3>
                <strong>{{ line.product.price }}</strong>
              </div>
              <label class="quantity-control">
                Qty
                <input
                  :value="line.quantity"
                  type="number"
                  min="1"
                  max="99"
                  @input="updateQuantity(line.product.slug, $event.target.value)"
                />
              </label>
              <strong>{{ formatMoney(line.subtotal) }}</strong>
              <button class="text-link" type="button" @click="removeFromCart(line.product.slug)">Remove</button>
            </article>
          </section>

          <aside class="contact-card order-summary">
            <h3>Order summary</h3>
            <p>{{ cartCount }} item{{ cartCount === 1 ? '' : 's' }}</p>
            <div class="total-row">
              <span>Total</span>
              <strong>{{ formatMoney(cartTotal) }}</strong>
            </div>
            <button class="pill-button primary" type="button" @click="go('checkout')">Checkout</button>
          </aside>
        </div>

        <div v-else class="wide-card empty-state">
          <h3>Your cart is empty.</h3>
          <p>Choose a product to start a manual-confirmation order.</p>
          <button class="pill-button primary" type="button" @click="go('products')">Browse products</button>
        </div>
      </section>

      <section v-else-if="activePage === 'checkout'" class="page reveal">
        <div class="page-hero compact-hero">
          <p class="eyebrow">Checkout</p>
          <h1>Submit your order details.</h1>
          <p class="lead">No online payment is collected in this first version. We will contact you to confirm payment and shipping.</p>
        </div>

        <div class="checkout-layout">
          <form class="contact-form" @submit.prevent="submitOrder">
            <div class="form-grid">
              <label>
                Name
                <input v-model="checkoutForm.customer_name" type="text" name="customer_name" placeholder="Your name" />
              </label>
              <label>
                Email
                <input v-model="checkoutForm.email" type="email" name="email" placeholder="you@example.com" />
              </label>
              <label>
                WhatsApp / Phone
                <input v-model="checkoutForm.phone" type="tel" name="phone" placeholder="+1 555 000 8888" />
              </label>
              <label>
                Country
                <input v-model="checkoutForm.country" type="text" name="country" placeholder="United States" />
              </label>
            </div>
            <label>
              Address
              <textarea v-model="checkoutForm.address" name="address" rows="4" placeholder="Street, city, region, postal code"></textarea>
            </label>
            <label>
              Notes
              <textarea v-model="checkoutForm.notes" name="notes" rows="3" placeholder="Preferred contact time, color preference, or delivery notes"></textarea>
            </label>
            <button class="pill-button primary" type="submit" :disabled="isSubmittingOrder">
              {{ isSubmittingOrder ? 'Submitting...' : 'Submit order' }}
            </button>
            <p v-if="checkoutStatus.message" class="form-message" :class="checkoutStatus.type">
              {{ checkoutStatus.message }}
            </p>
          </form>

          <aside class="contact-card order-summary">
            <h3>Order summary</h3>
            <p v-for="line in cartLines" :key="line.product.slug">
              {{ line.product.name }} x {{ line.quantity }} - {{ formatMoney(line.subtotal) }}
            </p>
            <div class="total-row">
              <span>Total</span>
              <strong>{{ formatMoney(cartTotal) }}</strong>
            </div>
          </aside>
        </div>
      </section>

      <section v-else-if="activePage === 'order-success'" class="page reveal">
        <div class="wide-card status-card">
          <p class="eyebrow">Order received</p>
          <h1>Thank you. Your order was submitted.</h1>
          <p class="lead">
            Order number: <strong>{{ orderResult?.order_number }}</strong>
          </p>
          <p>
            We will contact you to confirm product availability, payment, and shipping. Please keep the order number for reference.
          </p>
          <button class="pill-button primary" type="button" @click="go('products')">Continue shopping</button>
        </div>
      </section>

      <section v-else-if="activePage === 'factory'" class="page reveal">
        <div class="page-hero">
          <p class="eyebrow">Factory</p>
          <h1>From pretty sample to stable repeat order.</h1>
          <p class="lead">
            We focus on material safety, surface feel, packaging volume, and the small details that make pet goods usable at home.
          </p>
        </div>

        <div class="factory-layout">
          <div class="factory-card">
            <h3>Production focus</h3>
            <p>
              Silicone, fabric, plastic, lightweight hardware, and paper packaging can be coordinated for private-label
              pet goods and starter bundles.
            </p>
            <ul>
              <li>Food-contact material options for feeding items</li>
              <li>Sample review before production scheduling</li>
              <li>Private label packaging and bundle planning</li>
            </ul>
          </div>
          <div class="process-strip">
            <span v-for="step in factorySteps" :key="step">{{ step }}</span>
          </div>
        </div>
      </section>

      <section v-else-if="activePage === 'custom'" class="page reveal">
        <div class="page-hero">
          <p class="eyebrow">Custom</p>
          <h1>Build a pet line that feels like your brand, not a marketplace listing.</h1>
          <p class="lead">
            We can start from a color story, a gift set idea, or a specific product routine and turn it into a sample-ready plan.
          </p>
        </div>

        <div class="custom-grid">
          <article v-for="option in customOptions" :key="option" class="custom-card">
            <span class="dot"></span>
            <h3>{{ option }}</h3>
            <p>Translate your channel, target price, and customer taste into sample direction and packaging details.</p>
          </article>
        </div>
      </section>

      <section v-else-if="activePage === 'contact'" class="page page-contact reveal">
        <div class="page-hero compact-hero">
          <p class="eyebrow">Contact</p>
          <h1>Tell us about your pet goods project.</h1>
          <p class="lead">Submissions write to Django Admin and can notify the store inbox by email.</p>
        </div>

        <div class="contact-layout">
          <form class="contact-form" @submit.prevent="submitInquiry">
            <div class="form-grid">
              <label>
                Name
                <input v-model="inquiryForm.name" type="text" name="name" placeholder="Your name" />
              </label>
              <label>
                Email
                <input v-model="inquiryForm.email" type="email" name="email" placeholder="you@example.com" />
              </label>
              <label>
                WhatsApp / Phone
                <input v-model="inquiryForm.phone" type="tel" name="phone" placeholder="+1 555 000 8888" />
              </label>
              <label>
                Country
                <input v-model="inquiryForm.country" type="text" name="country" placeholder="United States" />
              </label>
            </div>
            <label>
              Interested Products
              <input v-model="inquiryForm.interested_products" type="text" name="interested_products" placeholder="Pino Feeder Set, New Pet Home Box" />
            </label>
            <label>
              Message
              <textarea v-model="inquiryForm.message" name="message" rows="5" placeholder="Tell us about quantity, target market, color, packaging, or shipping needs."></textarea>
            </label>
            <button class="pill-button primary" type="submit" :disabled="isSubmittingInquiry">
              {{ isSubmittingInquiry ? 'Submitting...' : 'Send inquiry' }}
            </button>
            <p v-if="inquiryStatus.message" class="form-message" :class="inquiryStatus.type">
              {{ inquiryStatus.message }}
            </p>
          </form>

          <aside class="contact-card">
            <span class="sticker mini">reply in 24h</span>
            <h3>PawNest Project Team</h3>
            <p>Email: hello@pawnest.supply</p>
            <p>Focus: feeding, grooming, walking, gift sets</p>
            <p>Markets: US, EU, Japan, Southeast Asia</p>
          </aside>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <button type="button" @click="go('products')">Products</button>
      <button type="button" @click="go('cart')">Cart</button>
      <button type="button" @click="go('contact')">Contact</button>
      <button type="button" @click="go('factory')">Factory</button>
    </footer>
  </div>
</template>
