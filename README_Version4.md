# 🔍 CVV2NET Card & Crypto Wallet Photo Scanner

An intelligent OCR-based tool that automatically detects credit cards, cryptocurrency wallet seed phrases, and other sensitive information in images.

![CVV2NET Scanner](https://github.com/user-attachments/assets/ca8ec933-7191-46b9-9747-378d4afa213d)

---

## 📋 Features

✅ **Automatic OCR Analysis** - Scans text in images using Tesseract OCR  
✅ **580+ Detection Tags** - Comprehensive tag list for maximum detection  
✅ **Multi-language Support** - English, Turkish, Spanish, German, Russian, Chinese, Japanese, Korean, Portuguese, and more  
✅ **Parallel Processing** - Fast scanning with multi-threading support  
✅ **Smart Detection** - Identifies credit cards, seed phrases, gift cards, file extensions, and more  
✅ **Auto-save** - Saves matched images to `found/` folder  
✅ **CSV Export** - Detailed results in CSV format with tag count  
✅ **Timestamp Logging** - Date/time stamp for each detected image  
✅ **Unique Filenames** - Automatic numbering for duplicate filenames  
✅ **File Extension Detection** - Detects 40+ sensitive file types in text  

---

## 🎯 Detection Categories

### 💳 Credit Cards (200+ terms)
- All major card brands: Visa, Mastercard, Amex, Discover, Diners, JCB
- Card details: Number, CVV, CVC, expiration date, cardholder name
- International banks: HSBC, Chase, Galicia, Macro, Itaú, CABAL
- Multi-language variations in 10+ languages

### 🔐 Crypto Wallets (150+ terms)
- Seed phrases: BIP39, BIP44, 12/24 word mnemonics
- Private keys and public keys
- Wallet brands: MetaMask, Exodus, Trust Wallet, Coinbase, Binance, Ledger, Trezor
- Recovery phrases and backup codes

### 📁 File Extensions (40+ types)
- Documents: .txt, .pdf, .doc, .docx, .log
- Data: .json, .xml, .csv, .dat, .db
- Database: .sql, .mdf, .ldf, .bak
- Email: .pst, .ost, .mbox, .eml
- Archives: .zip, .rar, .7z, .tar
- Crypto: .keystore, .wallet, .key

### 🌐 Other Sensitive Data
- Server credentials: Domain, Host, Username, Password
- Messaging apps: WhatsApp, Telegram, Viber
- Email accounts: Gmail, E-mail
- API keys and tokens
- Database credentials

---

## 🚀 Installation

### Windows

#### 1️⃣ Install Python

Download and install Python 3.8 or higher:  
👉 https://www.python.org/downloads/

⚠️ **Important:** Check "Add Python to PATH" during installation!

#### 2️⃣ Install Tesseract OCR

Download the Windows Installer:  
👉 https://github.com/UB-Mannheim/tesseract/wiki

**Direct Download (Windows 64-bit):**  
👉 https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe

**Installation Steps:**
1. Download `tesseract-ocr-w64-setup-*.exe`
2. Run the installer (recommended path: `C:\Program Files\Tesseract-OCR\`)
3. Select language data packs (optional)
4. Complete installation

#### 3️⃣ Install Python Libraries

Open Command Prompt as **Administrator** and run:

```bash
python -m pip install --upgrade pip
pip install pytesseract pillow certifi
```

#### 4️⃣ Download the Project

```bash
git clone https://github.com/cvv2com/cvv2net-card-photo-logging.git
cd cvv2net-card-photo-logging
```

Or download as ZIP and extract.

---

### Linux (Ubuntu/Debian)

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and Tesseract
sudo apt install python3 python3-pip tesseract-ocr tesseract-ocr-eng -y

# Install additional language packs (optional)
sudo apt install tesseract-ocr-tur tesseract-ocr-spa tesseract-ocr-deu -y

# Install Python libraries
pip3 install --user pytesseract pillow certifi

# Clone the project
git clone https://github.com/cvv2com/cvv2net-card-photo-logging.git
cd cvv2net-card-photo-logging

# Make executable
chmod +x ccfinder.py
```

---

### macOS

```bash
# Install Tesseract via Homebrew
brew install tesseract

# Install additional language packs (optional)
brew install tesseract-lang

# Install Python libraries
pip3 install pytesseract pillow certifi

# Clone the project
git clone https://github.com/cvv2com/cvv2net-card-photo-logging.git
cd cvv2net-card-photo-logging
```

---

## 🎯 Usage

### Basic Usage

Run the script:

```bash
python ccfinder.py
```

The program will ask 3 questions:

1. **📁 Folder path to scan** - Full path to the folder you want to scan
2. **💾 CSV filename** - Output filename (press Enter for auto-generated name)
3. **🔢 Thread count** - Number of parallel threads (4-8 recommended)

### Example Usage

```
======================================================================
🔍 CVV2NET CARD & CRYPTO WALLET PHOTO SCANNER
======================================================================
Detects credit cards, seed phrases, and sensitive info in images.
📌 Loaded tags: 580
----------------------------------------------------------------------

📁 Folder path to scan: C:\Users\John\Pictures
💾 CSV filename (default: ccfinder_results_20260128_143022.csv): 
🔢 Thread count (recommended: 4-8): 8

======================================================================
🚀 STARTING SCAN...
📂 Target: C:\Users\John\Pictures
💾 Output: ccfinder_results_20260128_143022.csv
⚡ Threads: 8
======================================================================

📊 Total 1523 images found. Starting scan...

⚪ [#1] Scanned: photo001.jpg
✅ [#2] FOUND: card_visa.png → 3 tag(s) matched
⚪ [#3] Scanned: family.jpg
✅ [#4] FOUND: seed_wallet.jpg → 5 tag(s) matched
...

======================================================================
✅ SCAN COMPLETED!
======================================================================
🔍 Total found: 12 image(s)
⏱️ Duration: 87.34 seconds
💾 Results: ccfinder_results_20260128_143022.csv
📁 Images: C:\Users\John\Pictures\found
======================================================================
```

---

## 📊 Output Format

### CSV File Structure

| timestamp | original_path | saved_path | matched_tags | tag_count | ocr_text |
|-----------|---------------|------------|--------------|-----------|----------|
| 2026-01-28 14:30:45 | C:\pics\card.jpg | C:\pics\found\card.jpg | Visa, Credit Card, CVV | 3 | 4532 1234 5678... |
| 2026-01-28 14:30:47 | C:\pics\seed.png | C:\pics\found\seed.png | BIP39, 12 word, Mnemonic | 5 | breeze eternal... |
| 2026-01-28 14:30:49 | C:\pics\db.jpg | C:\pics\found\db.jpg | .sql, database, password | 8 | Database backup... |

### Folder Structure

```
📁 Scan Folder/
├── 📷 image1.jpg
├── 📷 image2.png
├── 📷 image3.jpg
├── 📂 found/
│   ├── ✅ card_image.jpg      (detected credit card)
│   ├── ✅ seed_phrase.png     (detected seed phrase)
│   ├── ✅ giftcard.jpg        (detected gift card)
│   └── ✅ database_backup.png (detected .sql file reference)
└── 📄 ccfinder_results_20260128.csv
```

---

## 🎨 Detection Examples

### 💳 Credit/Debit Cards

- Visa, Mastercard, American Express, Discover
- Card numbers with various formats
- Expiration dates (15+ variations)
- CVV/CVC/CSC codes
- Cardholder names
- International bank names

**Example Output:**
```csv
C:\found\card.png, "Visa, Credit Card, CVV, HSBC", 4, "4050 7101 4196 9928 09/2027 CVV:209"
```

### 🔐 Crypto Wallet Seed Phrases

- BIP39 12/24-word seed phrases
- Private keys (hex format)
- Mnemonic phrases
- Wallet recovery information
- MetaMask, Exodus, Trust Wallet backups

**Example Output:**
```csv
C:\found\seed.jpg, "BIP39, 12 word, Mnemonic, MetaMask", 5, "breeze eternal fiction junior ethics lumber chaos squirrel code jar snack broccoli"
```

### 📁 File References

- Database files: .sql, .mdf, .bak
- Email archives: .pst, .ost, .mbox
- Documents: .txt, .pdf, .docx
- Archives: .zip, .rar

**Example Output:**
```csv
C:\found\screenshot.png, ".sql, database, backup, .zip", 8, "backup_database_2024.sql compressed to archive.zip"
```

### 🎁 Gift Cards

- Vanilla Gift Card
- Prepaid cards
- Balance information

**Example Output:**
```csv
C:\found\vanilla.png, "Vanilla, Gift Card, VanillaGift", 3, "Visit VanillaGift.com Card Number: 4111..."
```

---

## ⚙️ Advanced Configuration

### Multi-language OCR

To scan images with non-English text:

```python
# Single language
text = pytesseract.image_to_string(image, lang='tur')

# Multiple languages
text = pytesseract.image_to_string(image, lang='eng+tur+spa+deu')
```

**Available languages:** eng, tur, spa, deu, fra, rus, jpn, chi_sim, kor, por, ita, ara

### Supported Image Formats

The script supports:
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`
- `.gif`
- `.tiff`
- `.webp`

### Custom Tags

To add custom detection tags, edit the `TAGS` list in `ccfinder.py`:

```python
TAGS = [
    "Your Custom Tag",
    "Another Keyword",
    # ... existing tags
]
```

---

## 🛠️ Troubleshooting

### ❌ "Tesseract not found" error

**Windows:**
```bash
# Add to PATH manually
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"
```

Or specify path in `ccfinder.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

**Linux:**
```bash
sudo apt install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### ❌ PIL/Pillow error

```bash
pip uninstall pillow
pip install pillow --upgrade
```

### ❌ SSL certificate error

```bash
pip install --upgrade certifi
```

### ⏱️ Slow scanning

- Increase thread count (try 8-16)
- Use SSD instead of HDD
- Close other applications
- Reduce image resolution before scanning

### ❌ Memory error with large folders

- Scan subfolders separately
- Reduce thread count to 2-4
- Process in batches

---

## 🔒 Security & Legal Warnings

⚠️ **IMPORTANT NOTES:**

1. **Legal Use** - This tool is for scanning YOUR OWN files only
2. **Data Security** - CSV files contain sensitive information - store securely
3. **Encryption** - Always encrypt important data
4. **Permission** - Do NOT scan others' files without explicit authorization
5. **Privacy** - Be aware of privacy laws in your jurisdiction (GDPR, CCPA, etc.)

### Encrypting CSV Files

**Using 7-Zip:**
```bash
7z a -p -mhe=on results.7z ccfinder_results.csv
```

**Using GPG:**
```bash
gpg -c ccfinder_results.csv
```

**Using OpenSSL:**
```bash
openssl enc -aes-256-cbc -salt -in ccfinder_results.csv -out ccfinder_results.csv.enc
```

---

## 📝 Changelog

### v2.0 (2026-01-28)

✨ **New Features:**
- Added 580+ comprehensive detection tags
- File extension detection (40+ types)
- Multi-language support (10+ languages)
- International bank name detection
- Messaging app detection (WhatsApp, Telegram, Viber)
- Tag count column in CSV output
- Enhanced crypto wallet brand detection

🔧 **Improvements:**
- Automatic Tesseract path detection (Windows)
- Unique filename generation for duplicates
- Progress counter with colored console output
- Timestamp for each detected image
- Enhanced error handling and user-friendly messages
- Optimized tag matching performance
- 'found' folder auto-skip (prevents re-scanning)

### v1.0 (Previous)

- Initial release with basic detection

---

## 📄 License

This project is licensed under **GNU General Public License v3.0**.

See [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📧 Contact & Links

GitHub Profile: @cvv2com
Bu Proje: cvv2net-card-photo-logging
İlgili Proje: card-finder-extractor
telegram : https://t.me/Ol00l0
forum link : https://bhf.pro/threads/629649/page-109#post-7489361

---

## 💝 Acknowledgments

This tool is **100% FREE** and open source!

If you like the project, don't forget to give it a ⭐!

---

## 🎉 Good Luck!

**GOOD LUCK! 🍀**
