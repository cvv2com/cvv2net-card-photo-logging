# 🔍 CVV2COM Card & Crypto Wallet Photo Scanner

An intelligent OCR-based tool that automatically detects credit cards, cryptocurrency wallet seed phrases, and other sensitive information in images.

![CVV2NET Scanner](https://github.com/user-attachments/assets/ca8ec933-7191-46b9-9747-378d4afa213d)

---

## 📋 Features

✅ **Automatic OCR Analysis** - Scans text in images using Tesseract OCR  
✅ **Multi-language Support** - English, Turkish, Spanish, German, Russian, Chinese, Japanese, Korean, and more  
✅ **Parallel Processing** - Fast scanning with multi-threading support  
✅ **Smart Detection** - Identifies credit cards, seed phrases, gift cards, and more  
✅ **Auto-save** - Saves matched images to `found/` folder  
✅ **CSV Export** - Detailed results in CSV format  
✅ **Timestamp Logging** - Date/time stamp for each detected image  
✅ **Unique Filenames** - Automatic numbering for duplicate filenames  
✅ **Extensible Tags** - Load custom tag lists from external file  

---

## 🚀 Installation

### Windows

#### 1️⃣ Install Python

Download and install Python 3.8 or higher:  
👉 https://www.python.org/downloads/

⚠️ **Important:** Check "Add Python to PATH" during installation!

#### 2️⃣ Install Tesseract OCR

Download the Windows Installer:  
👉 https://github.com/tesseract-ocr/tesseract/releases

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
sudo apt install python3 python3-pip tesseract-ocr tesseract-ocr-tur -y

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
This tool detects credit cards, seed phrases, and sensitive info in images.
📌 Loaded tags: 247
----------------------------------------------------------------------

📁 Folder path to scan: C:\Users\John\Pictures
💾 CSV filename (default: ccfinder_results_20260128_043022.csv): 
🔢 Thread count (recommended: 4-8): 8

======================================================================
🚀 STARTING SCAN...
📂 Target: C:\Users\John\Pictures
💾 Output: ccfinder_results_20260128_043022.csv
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
💾 Results: ccfinder_results_20260128_043022.csv
📁 Images: C:\Users\John\Pictures\found
======================================================================
```

---

## 📊 Output Format

### CSV File Structure

| timestamp | original_path | saved_path | matched_tags | ocr_text |
|-----------|---------------|------------|--------------|----------|
| 2026-01-28 04:30:45 | C:\pics\card.jpg | C:\pics\found\card.jpg | Visa, Credit Card, CVV | 4532 1234 5678... |
| 2026-01-28 04:30:47 | C:\pics\seed.png | C:\pics\found\seed.png | BIP39, 12 word, Mnemonic | breeze eternal... |

### Folder Structure

```
📁 Scan Folder/
├── 📷 image1.jpg
├── 📷 image2.png
├── 📷 image3.jpg
├── 📂 found/
│   ├── ✅ card_image.jpg      (detected credit card)
│   ├── ✅ seed_phrase.png     (detected seed phrase)
│   └── ✅ giftcard.jpg        (detected gift card)
└── 📄 ccfinder_results_20260128.csv
```

---

## 🎨 Detection Examples

### 💳 Credit/Debit Cards

- Visa, Mastercard, American Express, Discover
- Card numbers
- Expiration dates
- CVV/CVC codes
- Cardholder names

**Example Output:**
```csv
C:\found\card.png, "Visa, Credit Card, CVV", "4050 7101 4196 9928 09/2027 CVV:209"
```

### 🔐 Crypto Wallet Seed Phrases

- BIP39 12/24-word seed phrases
- Private keys
- Mnemonic phrases
- Wallet recovery info

**Example Output:**
```csv
C:\found\seed.jpg, "BIP39, 12 word, Mnemonic", "breeze eternal fiction junior ethics lumber chaos squirrel code jar snack broccoli"
```

### 🎁 Gift Cards

- Vanilla Gift Card
- Prepaid cards
- Balance info

**Example Output:**
```csv
C:\found\vanilla.png, "Vanilla, Gift Card, VanillaGift", "Visit VanillaGift.com Card Number: 4111..."
```

---

## ⚙️ Advanced Configuration

### Adding New Tags

Open `ccfinder.py` and add keywords to the `TAGS` list:

```python
TAGS = [
    "New Keyword",
    "Another Search Term",
    # ... existing tags
]
```

Or edit `tags.txt` file:

```txt
new keyword,another term,custom phrase
```

### OCR Language Settings

For Turkish or other languages:

```python
# Single language
text = pytesseract.image_to_string(image, lang='tur')

# Multiple languages
text = pytesseract.image_to_string(image, lang='eng+tur+fra')
```

### Supported Image Formats

The script supports:
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`
- `.gif`
- `.tiff`
- `.webp`

To add new formats:

```python
SUPPORTED_IMAGE_FORMATS = ('.jpg', '.png', '.bmp', '.svg', '.heic')
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

- Increase thread count (8-16)
- Use SSD instead of HDD
- Preprocess high-resolution images

---

## 🔒 Security & Legal Warnings

⚠️ **IMPORTANT NOTES:**

1. **Legal Use** - This tool is for scanning YOUR OWN files only
2. **Data Security** - CSV files may contain sensitive info - store securely
3. **Encryption** - Encrypt important data
4. **Permission** - Do NOT scan others' files without authorization

### Encrypting CSV Files

**Using 7-Zip:**
```bash
7z a -p -mhe=on results.7z ccfinder_results.csv
```

**Using GPG:**
```bash
gpg -c ccfinder_results.csv
```

---

## 📝 Changelog

### v2.0 (2026-01-28)

✨ **New Features:**
- Automatic Tesseract path detection (Windows)
- Unique filename generation (duplicate handling)
- Progress counter with colored console output
- Timestamp for each detected image
- Enhanced error handling and user-friendly messages
- English UI and documentation

🔧 **Improvements:**
- BIP39 seed phrase detection
- Gift card detection
- Extended multi-language support
- Optimized thread management
- 'found' folder auto-skip (prevents re-scanning)
- External tag file support (`tags.txt`)

### v1.0 (Previous)

- Initial release

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

## 📧 İletişim ve Bağlantılar

- **GitHub Profile:** [@cvv2com](https://github.com/cvv2com)
- **Bu Proje:** [cvv2net-card-photo-logging](https://github.com/cvv2com/cvv2net-card-photo-logging)
- **İlgili Proje:** [card-finder-extractor](https://github.com/cvv2com/card-finder-extractor)
- telegram : [https://t.me/Ol00l0](https://t.me/Ol00l0)
- forum link : https://bhf.pro/threads/629649/page-109#post-7489361

---

## 💝 Acknowledgments

This tool is **100% FREE** and open source!

If you like the project, don't forget to give it a ⭐!

---

## 🎉 Good Luck!

**GOOD LUCK! 🍀**
