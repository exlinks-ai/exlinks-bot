const tg = window.Telegram?.WebApp;

if (tg) {
  tg.ready();
  tg.expand();
}

const API_BASE = window.location.origin;
const FALLBACK_LANG = "en";
const FALLBACK_TELEGRAM_ID = 2091774116;

const WHATSAPP_NUMBER = "994993692005";
const WHATSAPP_LINK = `https://wa.me/${WHATSAPP_NUMBER}`;
const INSTAGRAM_LINK = "https://www.instagram.com/exlinks.ai/";
const TELEGRAM_GROUP_LINK = "https://t.me/+RRwv5voUSNUyMDMy";


let state = null;
let currentScreen = "welcome";

const texts = {
  az: {
    heroTitle: "Uğurlu məhsul linkləri",
    heroText: "Telegram daxilində eBay dropshipping satıcıları üçün seçilmiş məhsul linkləri",
    chooseLanguage: "Dil seç",
    continue: "Davam et",
    welcome: "Xoş gəldin",
    userMenu: "İstifadəçi menyusu",
    adminMenu: "Admin panel",
    packages: "Paketlər",
    packagesSub: "Planlara bax və seç",
    subscription: "Abunəliyim",
    subscriptionSub: "Aktiv paketini yoxla",
    contact: "Haqqımızda",
    contactSub: "Biz kimik və əlaqə",
    aboutTitle: "Haqqımızda",
    aboutText: "ExLinks AI, eBay dropshipping satıcıları üçün seçilmiş uğurlu məhsul linkləri təqdim  edir. Məqsədimiz satıcılara məhsul araşdırmasını sürətləndirmək, doğru məhsulları tapmaq və işlərini daha rahat idarə etmələrinə dəstək olmaqdır.",
    instagram: "Instagram",
    whatsapp: "WhatsApp",
    telegram: "Telegram",
    changeLanguage: "Dili dəyiş",
    changeLanguageSub: "AZ / EN / RU",
    currentPlan: "Cari Paket",
    nextDelivery: "Növbəti Göndəriş",
    active: "Aktiv",
    inactive: "Deaktiv",
    noSubscription: "Səndə hələ aktiv paket yoxdur.",
    packageInfo: "Paket aktivləşdirmək üçün WhatsApp üzərindən bizimlə əlaqə saxlayın.",
    contactAdmin: "Adminlə əlaqə saxla",
    contactWhatsapp: "WhatsApp ilə əlaqə saxla",
    yourId: "Sənin Telegram ID-n",
    productTitle: "Məhsul",
    latestProduct: "Sənə son göndərilən məhsul",
    nextProduct: "Sənə növbəti veriləcək məhsul.",
    noProduct: "Hələ məhsul yoxdur.",
    source: "Mənbə",
    status: "Status",
    ready: "Hazır",
    waiting: "Gözləyir",
    openLink: "Məhsul Linkini Aç",
    account: "Hesab",
    telegramId: "Telegram ID",
    sendMessage: "Mesaj göndər",
    placeholder: "Mesajını yaz...",
    send: "Göndər",
    sent: "Göndərildi",
    adminUsers: "İstifadəçilər",
    activate: "Aktiv et",
    deactivate: "Deaktiv et",
    back: "Geri",
    currentBadge: "Cari plan",
    failed: "App yüklənmədi.",
    intervalDays3: "3 günlük interval",
    intervalDays2: "2 günlük interval",
    intervalDays1: "1 günlük interval",
    whatsappIdTitle: "Paketi aktivləşdirmək üçün ID-ni adminə göndər",
    whatsappIdSub: "WhatsApp ilə göndər",
  },
  en: {
    heroTitle: "Successful product links",
    heroText: "Selected product links for eBay dropshipping sellers inside Telegram",
    chooseLanguage: "Choose language",
    continue: "Continue",
    welcome: "Welcome",
    userMenu: "User menu",
    adminMenu: "Admin panel",
    packages: "Packages",
    packagesSub: "View and choose plans",
    subscription: "My Subscription",
    subscriptionSub: "Check active package",
    contact: "About Us",
    contactSub: "Who we are and contact",
    aboutTitle: "About Us",
    aboutText: "ExLinks AI provides selected successful product links for eBay dropshipping sellers. Our goal is to help sellers speed up product research, find the right items, and manage their business more efficiently.",
    instagram: "Instagram",
    whatsapp: "WhatsApp",
    telegram: "Telegram",
    changeLanguage: "Change language",
    changeLanguageSub: "AZ / EN / RU",
    currentPlan: "Current Plan",
    nextDelivery: "Next Delivery",
    active: "Active",
    inactive: "Inactive",
    noSubscription: "You do not have an active subscription yet.",
    packageInfo: "To activate a package, contact us on WhatsApp.",
    contactAdmin: "Contact Admin",
    contactWhatsapp: "Contact on WhatsApp",
    yourId: "Your Telegram ID",
    productTitle: "Product",
    latestProduct: "Your latest delivered product",
    nextProduct: "Your next available product.",
    noProduct: "No product yet.",
    source: "Source",
    status: "Status",
    ready: "Ready",
    waiting: "Waiting",
    openLink: "Open Product Link",
    account: "Account",
    telegramId: "Telegram ID",
    sendMessage: "Send Message",
    placeholder: "Write your message...",
    send: "Send",
    sent: "Sent",
    adminUsers: "Users",
    activate: "Activate",
    deactivate: "Deactivate",
    back: "Back",
    currentBadge: "Current plan",
    failed: "Failed to load app.",
    intervalDays3: "3-day interval",
    intervalDays2: "2-day interval",
    intervalDays1: "1-day interval",
    whatsappIdTitle: "Paketi aktivləşdirmək üçün ID-ni adminə göndər",
    whatsappIdSub: "WhatsApp ilə göndər",
  },
  ru: {
    heroTitle: "Успешные товарные ссылки",
    heroText: "Отобранные товарные ссылки для eBay dropshipping продавцов внутри Telegram",
    chooseLanguage: "Выберите язык",
    continue: "Продолжить",
    welcome: "Добро пожаловать",
    userMenu: "Меню пользователя",
    adminMenu: "Панель администратора",
    packages: "Пакеты",
    packagesSub: "Посмотреть и выбрать тариф",
    subscription: "Моя подписка",
    subscriptionSub: "Проверить активный тариф",
    contact: "О нас",
    contactSub: "Кто мы и контакты",
    aboutTitle: "О нас",
    aboutText: "ExLinks AI предоставляет отобранные успешные ссылки на товары для продавцов eBay dropshipping. Наша цель — помочь продавцам ускорить исследование товаров, находить правильные позиции и более удобно управлять своим бизнесом.",
    instagram: "Instagram",
    whatsapp: "WhatsApp",
    telegram: "Telegram",
    changeLanguage: "Сменить язык",
    changeLanguageSub: "AZ / EN / RU",
    currentPlan: "Текущий тариф",
    nextDelivery: "Следующая отправка",
    active: "Активен",
    inactive: "Неактивен",
    noSubscription: "У вас пока нет активной подписки.",
    packageInfo: "Чтобы активировать пакет, свяжитесь с нами через WhatsApp.",
    contactAdmin: "Связаться с админом",
    contactWhatsapp: "Связаться в WhatsApp",
    yourId: "Ваш Telegram ID",
    productTitle: "Товар",
    latestProduct: "Ваш последний отправленный товар",
    nextProduct: "Ваш следующий доступный товар.",
    noProduct: "Пока нет товара.",
    source: "Источник",
    status: "Статус",
    ready: "Готово",
    waiting: "Ожидание",
    openLink: "Открыть ссылку товара",
    account: "Аккаунт",
    telegramId: "Telegram ID",
    sendMessage: "Отправить сообщение",
    placeholder: "Введите сообщение...",
    send: "Отправить",
    sent: "Отправлено",
    adminUsers: "Пользователи",
    activate: "Активировать",
    deactivate: "Деактивировать",
    back: "Назад",
    currentBadge: "Текущий тариф",
    failed: "Не удалось загрузить приложение.",
    intervalDays3: "Интервал 3 дня",
    intervalDays2: "Интервал 2 дня",
    intervalDays1: "Интервал 1 день",
    whatsappIdTitle: "Send your ID to the admin to activate the package",
    whatsappIdSub: "Send via WhatsApp",
  },
};

function tr(key) {
  const lang = state?.user?.language || FALLBACK_LANG;
  return texts[lang]?.[key] || texts[FALLBACK_LANG]?.[key] || key;
}

function getTelegramUser() {
  return tg?.initDataUnsafe?.user || null;
}

function getTelegramId() {
  return getTelegramUser()?.id || FALLBACK_TELEGRAM_ID;
}

function getTelegramUsername() {
  return getTelegramUser()?.username || "";
}

function getTelegramFirstName() {
  return getTelegramUser()?.first_name || "";
}

function getIntervalText(days) {
  if (days === 3) return tr("intervalDays3");
  if (days === 2) return tr("intervalDays2");
  return tr("intervalDays1");
}

function buildWhatsappPlanLink(plan) {
  const planLabel = plan?.label || "";
  const message = `Salam. ${planLabel} paketini aktiv etmək istəyirəm.`;
  return `${WHATSAPP_LINK}?text=${encodeURIComponent(message)}`;
}

async function api(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

async function bootstrap() {
  const telegramId = getTelegramId();
  const username = encodeURIComponent(getTelegramUsername());
  const firstName = encodeURIComponent(getTelegramFirstName());

  state = await api(
    `/api/bootstrap?telegram_id=${telegramId}&username=${username}&first_name=${firstName}`
  );
  render();
}

function go(screen) {
  currentScreen = screen;
  render();
}

function hero() {
  return `
    <section class="hero-card">
      <div class="hero-brand">
        <img src="logo.png" alt="exlinks.ai logo" class="hero-logo" />
      </div>
      <h1 class="hero-title">${tr("heroTitle")}</h1>
      <p class="hero-text">${tr("heroText")}</p>
    </section>
  `;
}

function renderWelcome() {
  return `
    <div class="screen">
      <div class="center-wrap">
        <div style="width:100%;">
          ${hero()}
          <div class="button-stack">
            <button class="primary-btn" id="toLanguageBtn">${tr("continue")}</button>
          </div>
        </div>
      </div>
    </div>
  `;
}

function getDisplayTimeZone() {
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";

  if (tz && tz !== "UTC" && tz !== "Etc/UTC" && tz !== "GMT") {
    return tz;
  }

  const lang = state?.user?.language || FALLBACK_LANG;

  if (lang === "az") return "Asia/Baku";
  if (lang === "ru") return "Europe/Moscow";

  return "UTC";
}

function formatLocalDateTime(value) {
  if (!value || value === "-") return "-";
  if (typeof value !== "string") return String(value);


  console.log("NEXT DELIVERY RAW:", value);
  console.log("DISPLAY TZ:", getDisplayTimeZone());

  const cleaned = value.replace(" UTC", "").trim();
  const parts = cleaned.split(" ");
  if (parts.length < 2) return value;

  const [datePart, timePart] = parts;
  const [year, month, day] = datePart.split("-").map(Number);
  const [hour, minute] = timePart.split(":").map(Number);

  if (
    Number.isNaN(year) ||
    Number.isNaN(month) ||
    Number.isNaN(day) ||
    Number.isNaN(hour) ||
    Number.isNaN(minute)
  ) {
    return value;
  }

  const utcDate = new Date(Date.UTC(year, month - 1, day, hour, minute));
  const displayTimeZone = getDisplayTimeZone();

  return new Intl.DateTimeFormat(undefined, {
    timeZone: displayTimeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(utcDate);
}



function buildWhatsappIdLink() {
  const message = `Salam. Paket aktivləşdirmək istəyirəm. Telegram ID: ${state.user.telegram_id}`;
  return `${WHATSAPP_LINK}?text=${encodeURIComponent(message)}`;
}

function renderLanguage() {
  const lang = state?.user?.language || FALLBACK_LANG;

  return `
    <div class="screen">
      <div class="top-row">
        <button class="back-btn" id="backWelcomeBtn">←</button>
        <h2>${tr("chooseLanguage")}</h2>
      </div>

      <div class="grid">
        <button class="lang-button ${lang === "en" ? "active" : ""}" data-lang="en">
          <strong>
            <img src="gb.png" alt="English" class="flag-icon" />
            <span>English</span>
          </strong>
        </button>

        <button class="lang-button ${lang === "az" ? "active" : ""}" data-lang="az">
          <strong>
            <img src="az.png" alt="Azərbaycan" class="flag-icon" />
            <span>Azərbaycan</span>
          </strong>
        </button>

        <button class="lang-button ${lang === "ru" ? "active" : ""}" data-lang="ru">
          <strong>
            <img src="ru.png" alt="Русский" class="flag-icon" />
            <span>Русский</span>
          </strong>
        </button>
      </div>

      <div class="button-stack">
        <button class="primary-btn" id="continueHomeBtn">${tr("continue")}</button>
      </div>
    </div>
  `;
}

function renderHome() {
  return `
    <div class="screen">
      ${hero()}

      <div class="section">
        <h2 class="section-title">${tr("userMenu")}</h2>
        <div class="grid">
          <button class="menu-button" id="packagesBtn">
            <strong>${tr("packages")}</strong>
            <small>${tr("packagesSub")}</small>
          </button>

          <button class="menu-button" id="subscriptionBtn">
            <strong>${tr("subscription")}</strong>
            <small>${tr("subscriptionSub")}</small>
          </button>

          <button class="menu-button" id="contactBtn">
            <strong>${tr("contact")}</strong>
            <small>${tr("contactSub")}</small>
          </button>

          <button class="menu-button" id="changeLangBtn">
            <strong>${tr("changeLanguage")}</strong>
            <small>${tr("changeLanguageSub")}</small>
          </button>

          ${state.user.is_admin ? `
            <button class="menu-button" id="adminBtn">
              <strong>${tr("adminMenu")}</strong>
              <small>${tr("adminUsers")} / ${tr("")}</small>
            </button>
          ` : ""}
        </div>
      </div>
    </div>
  `;
}

function renderPackages() {
  const plans = state.plans || [];
  const currentCode = state.subscription?.code;

  return `
    <div class="screen">
      <div class="top-row">
        <button class="back-btn" id="backHomeBtn">←</button>
        <h2>${tr("packages")}</h2>
      </div>

      <div class="card">
        <span>${tr("packageInfo")}</span>
      </div>

      <div class="section">
        <div class="plan-list">
          ${plans.map(plan => `
            <div class="plan-item ${currentCode === plan.code ? "current" : ""}">
              <div class="plan-head">
                <div class="plan-name">${escapeHtml(plan.label)}</div>
                <div class="plan-price">${escapeHtml(plan.price)}</div>
              </div>
              <div class="plan-desc">${getIntervalText(plan.days)}</div>
              ${currentCode === plan.code ? `<div class="badge success">${tr("currentBadge")}</div>` : ""}
              <div class="bottom-actions">
                <a
                  class="primary-btn"
                  href="${buildWhatsappPlanLink(plan)}"
                  target="_blank"
                >
                  ${tr("contactWhatsapp")}
                </a>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    </div>
  `;
}

function renderSubscription() {
  const sub = state.subscription;
  const product = state.product;

  let productText = tr("noProduct");
  if (product.mode === "latest") productText = tr("latestProduct");
  if (product.mode === "next") productText = tr("nextProduct");

  return `
    <div class="screen">
      <div class="top-row">
        <button class="back-btn" id="backHomeBtn">←</button>
        <h2>${tr("subscription")}</h2>
      </div>

      ${sub.active ? `
        <div class="grid two">
          <div class="card">
            <span>${tr("currentPlan")}</span>
            <strong>${escapeHtml(sub.name)}</strong>
            <small>${escapeHtml(sub.price)}</small>
          </div>
          <div class="card">
            <span>${tr("nextDelivery")}</span>
            <strong>${escapeHtml(formatLocalDateTime(sub.next_delivery))}</strong>
            <small>${tr("active")}</small>
          </div>
        </div>
      ` : `
        <div class="card">
          <span>${tr("noSubscription")}</span>
        </div>
      `}

      <div class="product-card">
        <div class="white-label">${tr("productTitle")}</div>
        <h3>${escapeHtml(product.name)}</h3>
        <p>${productText}</p>




      <div class="product-meta">
     <div class="product-meta-row">
        <span>${tr("source")}</span>
       <b>Amazon</b>
        </div>
          </div>



        <div class="bottom-actions">
          <a class="primary-btn" href="${product.link || "#"}" target="_blank">${tr("openLink")}</a>
        </div>
      </div>

    <div class="card section">
  <div class="info-row"><span>${tr("telegramId")}</span><b>${state.user.telegram_id}</b></div>
</div>

<a class="whatsapp-id-card section" href="${buildWhatsappIdLink()}" target="_blank">
  <div class="whatsapp-id-title">${tr("whatsappIdTitle")}</div>
  <div class="whatsapp-id-value">${state.user.telegram_id}</div>
  <div class="whatsapp-id-sub">${tr("whatsappIdSub")}</div>
</a>
  `;
}

function renderContact() {
  return `
    <div class="screen">
      <div class="top-row">
        <button class="back-btn" id="backHomeBtn">←</button>
        <h2>${tr("aboutTitle")}</h2>
      </div>

      <div class="card">
        <p class="about-text">${tr("aboutText")}</p>
      </div>

      <div class="social-grid section">
          <a class="social-card telegram-card" href="${TELEGRAM_GROUP_LINK}" target="_blank">
    <span class="social-title">${tr("telegram")}</span>
           </a>

      <a class="social-card instagram-card" href="${INSTAGRAM_LINK}" target="_blank">
      <span class="social-title">${tr("instagram")}</span>
         </a>

     <a class="social-card whatsapp-card" href="${WHATSAPP_LINK}" target="_blank">
       <span class="social-title">${tr("whatsapp")}</span>
      </a>
       </div>
    </div>
  `;
}


function renderAdmin() {
  const users = state.admin?.users || [];
  const messages = state.admin?.messages || [];

  return `
    <div class="screen">
      <div class="top-row">
        <button class="back-btn" id="backHomeBtn">←</button>
        <h2>${tr("adminMenu")}</h2>
      </div>

      <div class="section">
        <h3 class="section-title">${tr("adminUsers")}</h3>
        <div class="user-list">
          ${users.map(user => `
            <div class="user-item">
              <div class="user-head">
                <div class="user-name">${escapeHtml(user.name)}</div>
                <div class="badge ${user.active ? "success" : "danger"}">${user.active ? tr("active") : tr("inactive")}</div>
              </div>
              <div class="user-desc">ID: ${user.telegram_id}</div>
              <div class="user-desc">${escapeHtml(user.package_name || "-")}</div>
              <div class="user-desc">${escapeHtml(user.next_delivery || "-")}</div>

              <div class="user-actions">
                <button class="small-btn activate-btn" data-user="${user.telegram_id}" data-plan="every_3_days">19.99</button>
                <button class="small-btn activate-btn" data-user="${user.telegram_id}" data-plan="every_2_days">29.99</button>
                <button class="small-btn activate-btn" data-user="${user.telegram_id}" data-plan="daily">49.99</button>
                <button class="small-btn danger deactivate-btn" data-user="${user.telegram_id}">${tr("deactivate")}</button>
              </div>
            </div>
          `).join("")}
        </div>
      </div>

      <div class="section">
        <h3 class="section-title">${tr("")}</h3>
        <div class="message-list">
          ${messages.map(item => `
            <div class="message-item">
              <div class="message-head">
                <strong>${escapeHtml(item.user_name || "Unknown")}</strong>
                <span>${escapeHtml(item.created_at || "-")}</span>
              </div>
              <div class="message-desc">ID: ${item.telegram_id}</div>
              <div class="message-desc">${escapeHtml(item.text)}</div>
            </div>
          `).join("")}
        </div>
      </div>
    </div>
  `;
}

function render() {
  const app = document.getElementById("app");

  if (!state) {
    app.innerHTML = `<div class="screen"><div class="center-wrap"><div>Loading...</div></div></div>`;
    return;
  }

  if (currentScreen === "welcome") app.innerHTML = renderWelcome();
  if (currentScreen === "language") app.innerHTML = renderLanguage();
  if (currentScreen === "home") app.innerHTML = renderHome();
  if (currentScreen === "packages") app.innerHTML = renderPackages();
  if (currentScreen === "subscription") app.innerHTML = renderSubscription();
  if (currentScreen === "contact") app.innerHTML = renderContact();
  if (currentScreen === "admin") app.innerHTML = renderAdmin();

  bindEvents();
}

function bindEvents() {
  document.getElementById("toLanguageBtn")?.addEventListener("click", () => go("language"));
  document.getElementById("backWelcomeBtn")?.addEventListener("click", () => go("welcome"));
  document.getElementById("continueHomeBtn")?.addEventListener("click", () => go("home"));

  document.querySelectorAll(".lang-button").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const language = btn.dataset.lang;

      await api("/api/set-language", {
        method: "POST",
        body: JSON.stringify({
          telegram_id: getTelegramId(),
          language,
        }),
      });

      await bootstrap();
      currentScreen = "language";
      render();
    });
  });

  document.getElementById("packagesBtn")?.addEventListener("click", () => go("packages"));
  document.getElementById("subscriptionBtn")?.addEventListener("click", () => go("subscription"));
  document.getElementById("contactBtn")?.addEventListener("click", () => go("contact"));
  document.getElementById("changeLangBtn")?.addEventListener("click", () => go("language"));
  document.getElementById("adminBtn")?.addEventListener("click", () => go("admin"));

  document.querySelectorAll("#backHomeBtn").forEach((btn) => {
    btn.addEventListener("click", () => go("home"));
  });


  document.querySelectorAll(".activate-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await api("/api/admin/package", {
        method: "POST",
        body: JSON.stringify({
          admin_telegram_id: getTelegramId(),
          target_telegram_id: Number(btn.dataset.user),
          package_code: btn.dataset.plan,
          deactivate: false,
        }),
      });

      await bootstrap();
      currentScreen = "admin";
      render();
    });
  });

  document.querySelectorAll(".deactivate-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await api("/api/admin/package", {
        method: "POST",
        body: JSON.stringify({
          admin_telegram_id: getTelegramId(),
          target_telegram_id: Number(btn.dataset.user),
          deactivate: true,
        }),
      });

      await bootstrap();
      currentScreen = "admin";
      render();
    });
  });
}

bootstrap()
  .then(() => {
    currentScreen = "welcome";
    render();
  })
  .catch((err) => {
    console.error(err);
    document.getElementById("app").innerHTML = `<div class="screen"><div class="center-wrap"><div>${texts[FALLBACK_LANG].failed}</div></div></div>`;
  });
