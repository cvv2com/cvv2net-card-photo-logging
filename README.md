# 🔍 CVV2NET Kart Fotoğraf Tarama Aracı

Bu araç, bilgisayarınızdaki veya herhangi bir klasördeki görselleri tarayarak kredi kartı, banka kartı, seed phrase'ler ve benzeri hassas bilgiler içeren görselleri otomatik olarak tespit eder ve kaydeder.

![ccphotofinder](https://github.com/user-attachments/assets/ca8ec933-7191-46b9-9747-378d4afa213d)

---

## 📋 Özellikler

✅ **Otomatik OCR Analizi** - Tesseract OCR ile görsel içindeki metinleri tarar  
✅ **Çoklu Dil Desteği** - İngilizce, Türkçe, İspanyolca, Almanca ve daha fazlası  
✅ **Paralel İşleme** - Çoklu thread desteğiyle hızlı tarama  
✅ **Akıllı Tespit** - Kredi kartı, seed phrase, gift card tespiti  
✅ **Otomatik Kayıt** - Bulunan görselleri `found/` klasörüne kaydeder  
✅ **CSV Çıktı** - Detaylı sonuçları CSV formatında kaydeder  
✅ **Zaman Damgası** - Her bulunan görsel için tarih/saat bilgisi  
✅ **Benzersiz Dosya Adı** - Aynı isimli dosyalar için otomatik numaralandırma  

---

## 🚀 Kurulum

### Windows

#### 1️⃣ Python Kurulumu

Python 3.8 veya üzeri sürümü indirin ve yükleyin:  
👉 https://www.python.org/downloads/

⚠️ **Önemli:** Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin!

#### 2️⃣ Tesseract OCR Kurulumu

Windows Installer'ı indirin:  
👉 https://github.com/tesseract-ocr/tesseract/releases

**Kurulum Adımları:**
1. `tesseract-ocr-w64-setup-*.exe` dosyasını indirin
2. Kurulumu başlatın (önerilen yol: `C:\Program Files\Tesseract-OCR\`)
3. "Additional language data" kısmından dil paketlerini seçin (opsiyonel)
4. Kurulumu tamamlayın

#### 3️⃣ Python Kütüphanelerini Yükleyin

Komut İstemi'ni (CMD) **yönetici olarak** açın ve şu komutları çalıştırın:

```bash
python -m pip install --upgrade pip
pip install pytesseract pillow certifi
```

#### 4️⃣ Projeyi İndirin

```bash
git clone https://github.com/cvv2com/cvv2net-card-photo-logging.git
cd cvv2net-card-photo-logging
```

veya ZIP olarak indirip klasöre çıkarın.

---

### Linux (Ubuntu/Debian)

```bash
# Sistem paketlerini güncelleyin
sudo apt update && sudo apt upgrade -y

# Python ve Tesseract'ı yükleyin
sudo apt install python3 python3-pip tesseract-ocr tesseract-ocr-tur -y

# Python kütüphanelerini yükleyin
pip3 install --user pytesseract pillow certifi

# Projeyi klonlayın
git clone https://github.com/cvv2com/cvv2net-card-photo-logging.git
cd cvv2net-card-photo-logging

# Çalıştırma izni verin
chmod +x ccfinder.py
```

---

### macOS

```bash
# Homebrew ile Tesseract yükleyin
brew install tesseract

# Python kütüphanelerini yükleyin
pip3 install pytesseract pillow certifi

# Projeyi klonlayın
git clone https://github.com/cvv2com/cvv2net-card-photo-logging.git
cd cvv2net-card-photo-logging
```

---

## 🎯 Kullanım

### Basit Kullanım

Script'i çalıştırın:

```bash
python ccfinder.py
```

Program size 3 soru soracak:

1. **📁 Taranacak klasör yolu** - Taramak istediğiniz klasörün tam yolu
2. **💾 CSV dosya adı** - Sonuçların kaydedileceği dosya (boş bırakabilirsiniz)
3. **🔢 Thread sayısı** - Paralel işlem sayısı (4-8 arası önerilir)

### Örnek Kullanım

```
🔍 CVV2NET KART FOTOĞRAF TARAMA ARACI
======================================================================

📁 Taranacak klasör yolu: C:\Users\John\Pictures
💾 CSV dosya adı (varsayılan: ccfinder_results_20260128_143022.csv): 
🔢 Thread sayısı (önerilen: 4-8): 8

======================================================================
🚀 TARAMA BAŞLATILIYOR...
📂 Hedef: C:\Users\John\Pictures
💾 Çıktı: ccfinder_results_20260128_143022.csv
⚡ Thread: 8
======================================================================

📊 Toplam 1523 görsel bulundu. Tarama başlıyor...

⚪ [#1] Tarandı: photo001.jpg
✅ [#2] BULUNDU: card_image.png → 3 etiket eşleşti
⚪ [#3] Tarandı: vacation.jpg
✅ [#4] BULUNDU: wallet_photo.jpg → 5 etiket eşleşti
...

======================================================================
✅ TARAMA TAMAMLANDI!
======================================================================
🔍 Toplam bulunan: 12 görsel
⏱️ Süre: 245.67 saniye
💾 Sonuçlar: ccfinder_results_20260128_143022.csv
📁 Görseller: C:\Users\John\Pictures\found
======================================================================
```

---

## 📊 Çıktı Formatı

### CSV Dosyası

| timestamp | original_path | saved_path | matched_tags | ocr_text |
|-----------|---------------|------------|--------------|----------|
| 2026-01-28 14:30:45 | C:\pics\card.jpg | C:\pics\found\card.jpg | Visa, Credit Card, CVV | 4532 1234 5678... |
| 2026-01-28 14:30:47 | C:\pics\seed.png | C:\pics\found\seed.png | BIP39, 12 word, Mnemonic | breeze eternal... |

### Klasör Yapısı

```
📁 Tarama Klasörü/
├── 📷 görsel1.jpg
├── 📷 görsel2.png
├── 📷 görsel3.jpg
├── 📂 found/
│   ├── ✅ card_image.jpg      (bulunan kredi kartı görseli)
│   ├── ✅ seed_phrase.png     (bulunan seed phrase)
│   └── ✅ giftcard.jpg        (bulunan gift card)
└── 📄 ccfinder_results_20260128.csv
```

---

## 🎨 Özellikler ve Tespit Edilen İçerikler

### 💳 Kredi/Banka Kartları

- Visa, Mastercard, American Express, Discover
- Kart numaraları
- Son kullanma tarihleri
- CVV/CVC kodları
- Kart sahibi isimleri

**Örnek Çıktı:**
```csv
C:\found\card.png, "Visa, Credit Card, CVV", "4050 7101 4196 9928 09/2027 CVV:209"
```

### 🔐 Kripto Wallet Seed Phrases

- BIP39 12/24 kelime seed phrase'ler
- Private key'ler
- Mnemonic phrase'ler
- Wallet recovery bilgileri

**Örnek Çıktı:**
```csv
C:\found\seed.jpg, "BIP39, 12 word, Mnemonic", "breeze eternal fiction junior ethics lumber chaos squirrel code jar snack broccoli"
```

### 🎁 Gift Card'lar

- Vanilla Gift Card
- Prepaid kartlar
- Bakiye bilgileri

**Örnek Çıktı:**
```csv
C:\found\vanilla.png, "Vanilla, Gift Card, VanillaGift", "Visit VanillaGift.com Card Number: 4111..."
```

---

## ⚙️ Gelişmiş Ayarlar

### Yeni Etiket Ekleme

`ccfinder.py` dosyasını açın ve `TAGS` listesine yeni anahtar kelimeler ekleyin:

```python
TAGS = [
    "Yeni Anahtar Kelime",
    "Başka Bir Terim",
    # ... mevcut etiketler
]
```

### OCR Dil Ayarları

Türkçe veya diğer diller için OCR yapmak istiyorsanız:

```python
# Tek dil
text = pytesseract.image_to_string(image, lang='tur')

# Çoklu dil
text = pytesseract.image_to_string(image, lang='eng+tur+fra')
```

### Desteklenen Görsel Formatları

Script şu formatları destekler:
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`
- `.gif`
- `.tiff`
- `.webp`

Yeni format eklemek için:

```python
SUPPORTED_IMAGE_FORMATS = ('.jpg', '.png', '.bmp', '.svg', '.heic')
```

---

## 🛠️ Sorun Giderme

### ❌ "Tesseract bulunamadı" hatası

**Windows:**
```bash
# PATH'e manuel ekleme
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"
```

Veya `ccfinder.py` dosyasında manuel yol belirtin:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

**Linux:**
```bash
sudo apt install tesseract-ocr
```

### ❌ PIL/Pillow hatası

```bash
pip uninstall pillow
pip install pillow --upgrade
```

### ❌ SSL Sertifika hatası

```bash
pip install --upgrade certifi
```

### ⏱️ Tarama çok yavaş

- Thread sayısını artırın (8-16 arası deneyin)
- Yüksek çözünürlüklü görselleri ön işlemeye tabi tutun
- SSD kullanın (HDD yerine)

---

## 🔒 Güvenlik ve Yasal Uyarılar

⚠️ **ÖNEMLİ NOTLAR:**

1. **Yasal Kullanım** - Bu araç yalnızca kendi dosyalarınızı taramak için kullanılmalıdır
2. **Veri Güvenliği** - CSV dosyası hassas bilgiler içerebilir, güvenli bir yerde saklayın
3. **Şifreleme** - Önemli verileri şifreleyerek saklayın
4. **İzin** - Başkasının dosyalarını izinsiz taramayın

### CSV Dosyasını Şifreleme

**7-Zip ile:**
```bash
7z a -p -mhe=on sonuclar.7z ccfinder_results.csv
```

**GPG ile:**
```bash
gpg -c ccfinder_results.csv
```

---

## 📝 Değişiklik Günlüğü (Changelog)

### v2.0 (2026-01-28)

✨ **Yeni Özellikler:**
- Otomatik Tesseract yolu tespiti (Windows)
- Benzersiz dosya adı oluşturma (aynı isimli dosyalar için)
- İlerleme sayacı ve renkli konsol çıktısı
- Her bulunan görsele zaman damgası ekleme
- Gelişmiş hata yönetimi ve kullanıcı dostu mesajlar
- Türkçe kullanıcı arayüzü

🔧 **İyileştirmeler:**
- BIP39 seed phrase tespiti eklendi
- Gift card tespiti eklendi
- Çoklu dil desteği genişletildi
- Thread yönetimi optimize edildi
- 'found' klasörü otomatik atlanır (tekrar taramayı önler)

### v1.0 (Önceki Sürüm)

- İlk genel sürüm

---

## 📄 Lisans

Bu proje **GNU General Public License v3.0** ile lisanslanmıştır.

Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Şu adımları izleyin:

1. Projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request açın

---

## 📧 İletişim ve Bağlantılar

- **GitHub Profile:** [@cvv2com](https://github.com/cvv2com)
- **Bu Proje:** [cvv2net-card-photo-logging](https://github.com/cvv2com/cvv2net-card-photo-logging)
- **İlgili Proje:** [card-finder-extractor](https://github.com/cvv2com/card-finder-extractor)
- telegram : [https://t.me/Ol00l0](https://t.me/Ol00l0)
- forum link : https://bhf.pro/threads/629649/page-109#post-7489361

---

## 💝 Teşekkürler

Bu araç **100% ÜCRETSİZ** ve açık kaynaklıdır!

Projeyi beğendiyseniz ⭐ vermeyi unutmayın!

---

## 🎉 İyi Şanslar!

**GOOD LUCK! 🍀**
