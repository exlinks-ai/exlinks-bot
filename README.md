# exlinks.ai Telegram Bot

Hazır Python bot layihəsidir. Aşağıdakı funksiyalar daxildir:

- 3 dil: Azərbaycan, İngilis, Rus
- Admin və istifadəçi menyusu
- Paket seçimi:
  - Hər 3 gündən 1 məhsul — 29.99 AZN / $17.99 / 1590 ₽
  - Hər 2 gündən 1 məhsul — 49.99 AZN / $29.99 / 2690 ₽
  - Hər gün 1 məhsul — 69.99 AZN / $39.99 / 3790 ₽
- Admin panel:
  - İstifadəçilər
  - Hamıya mesaj
  - Rəylər
  - Şikayətlər
  - Excel yenilə
- Məhsullar `name` + `link` sütunlu Excel və ya CSV ilə yüklənir
- Məhsul seçimi randomdur
- Eyni istifadəçiyə eyni məhsul ikinci dəfə getmir
- Başqa istifadəçilərə eyni məhsul gedə bilər
- Paket seçiləndə ilk məhsul dərhal göndərilir
- Sonrakı məhsullar plan üzrə avtomatik gedir

## Qovluq strukturu

- `main.py` — start faylı
- `exlinks_bot/` — botun əsas kodu
- `.env.example` — environment nümunəsi
- `render.yaml` — Render worker deploy nümunəsi
- `data/sample_products.csv` — məhsul şablonu
- `data/sample_products.xlsx` — məhsul şablonu

## Lokal işlətmək

### 1) Virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows üçün:

```bash
.venv\Scripts\activate
```

### 2) Paketləri qur

```bash
pip install -r requirements.txt
```

### 3) `.env` yarat

`.env.example` faylını `.env` kimi kopyala və dəyərləri doldur:

```env
BOT_TOKEN=telegram_bot_token
ADMIN_IDS=123456789
SUPPORT_CHAT_ID=
DATABASE_URL=sqlite:///data/bot.db
BRAND_NAME=exlinks.ai
DELIVERY_CHECK_SECONDS=60
```

### 4) Botu başlat

```bash
python main.py
```

## Admin necə təyin olunur

`ADMIN_IDS` içinə Telegram ID-ni yazırsan. Bir neçə admin varsa vergüllə ayırırsan:

```env
ADMIN_IDS=123456789,987654321
```

## Excel / CSV formatı

Ən sadə format budur:

| name | link |
|---|---|
| Portable Blender | https://amazon.com/... |
| Car Phone Holder | https://amazon.com/... |

Qəbul olunan başlıqlar:

- `name`, `product_name`, `title`
- `link`, `url`, `product_link`, `amazon_link`

Əgər başlıq yoxdursa, bot ilk sütunu `name`, ikinci sütunu `link` kimi götürür.

## Məhsulu bota necə yükləmək

1. Admin hesabı ilə botu aç
2. Dil seç
3. `📥 Excel yenilə` düyməsinə klik et
4. Excel və ya CSV faylını document kimi göndər
5. Bot avtomatik import edəcək

Import zamanı sistem:

- yeni linkləri əlavə edir
- mövcud linkləri yeniləyir
- yeni faylda olmayan köhnə məhsulları deaktiv edir
- köhnə delivery tarixçəsini saxlayır

Bu o deməkdir ki, eyni link yenidən yüklənsə, eyni istifadəçiyə təkrar getməz.

## Paket məntiqi

- `every_3_days` → 3 gündən bir
- `every_2_days` → 2 gündən bir
- `daily` → hər gün

İstifadəçi paket seçəndə:

1. abunə aktiv olur
2. ilk məhsul dərhal göndərilir
3. növbəti göndəriş plan üzrə tarixlənir

## Random məhsul qaydası

Sistem məhsulu bütün aktiv məhsullar arasından seçir, amma həmin istifadəçiyə əvvəllər göndərilmiş məhsulları çıxır.

Yəni:

- User A məhsul X-i artıq alıbsa, bir də almayacaq
- User B eyni məhsul X-i ala bilər

## Dəstək və rəylər

- `⭐ Rəy bildir` → admin paneldə Reviews kimi görünür
- `💬 Dəstək` → admin paneldə Complaints kimi görünür
- İstəsən `SUPPORT_CHAT_ID` verib mesajları ayrıca support qrupuna da yönləndirə bilərsən

## Render deploy

Bu layihə long polling ilə işləyir və `render.yaml` worker servisi üçün hazırlanıb.

Əsas addımlar:

1. GitHub-a yüklə
2. Render-də yeni service yarat
3. Repo qoş
4. `render.yaml` istifadə et
5. Environment dəyişənlərini daxil et
6. Deploy et

### Render üçün DB seçimi

- Lokal test üçün SQLite default gəlir
- Production üçün `DATABASE_URL` olaraq Postgres vermək daha yaxşıdır

Məsələn:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME
```

## Dəyişmək istəyə biləcəyin yerlər

- qiymətlər və intervallar: `exlinks_bot/config.py`
- bütün mətnlər: `exlinks_bot/i18n.py`
- menyu düymələri: `exlinks_bot/keyboards.py`
- bot axını: `exlinks_bot/bot.py`

## Hazır deyil

Bu ZIP-də bunlar yoxdur:

- payment inteqrasiyası
- webhook versiyası
- admin üçün ayrıca web panel
- kupon sistemi
- referral sistemi

Amma MVP kimi dərhal yoxlamaq üçün hazırdır.
"# exlinks-bot" 
