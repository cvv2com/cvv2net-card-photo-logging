#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVV2NET Card & Crypto Wallet Photo Scanner - Advanced Version
Detects credit cards, crypto wallet seed phrases, and sensitive information in images using OCR.
GitHub: https://github.com/cvv2com/cvv2net-card-photo-logging
"""

import os
import csv
import pytesseract
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import sys
import platform

# ============================================================================
# CONFIGURATION
# ============================================================================

# Tesseract path (Auto-detect for Windows)
if platform.system() == "Windows":
    TESSERACT_PATHS = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME'))
    ]
    
    for path in TESSERACT_PATHS:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break
    else:
        print("⚠️ WARNING: Tesseract OCR not found. Please install Tesseract.")
        print("Download Link: https://github.com/tesseract-ocr/tesseract")

# Comprehensive Tag List (Crypto Wallet, Credit Card, Sensitive Info)
TAGS = [
    # === CREDIT CARD TERMS ===
    # General Card Terms
    "Credit Card", "credit card", "creditcard", "CREDIT Card", "CREDITCARD",
    "CREDIT CARD NO", "Card", "CARD", "Debit", "Debit Card",
    "This Card", "This card", "back of card", "prepaid", "Prepaid",
    
    # Card Holder & Details
    "Card Holder", "Cardholder", "Titular", "Kart Sahibi", "CARDMEMBER",
    
    # Expiration Date Variations
    "Expiration Date", "expiration date", "Exp. Date", "Exp Date", 
    "EXP Date", "EXP DATE", "EXP. DATE", "Valid Thru", "VALID", "THRU",
    "Valid Until", "Good Thru", "GOOD", "FROM", "NOT VALID",
    "Son Kullanma Tarihi", "Geçerlilik Tarihi", "有効期限", "到期日",
    "Validade", "VALIDADE",
    
    # CVV/Security Codes
    "CVV", "cvv", "CVC", "cvc", "ccv", "CSC", "CVV2", "CID", 
    "Security Code", "card security", "vcode", "VCODE",
    "Güvenlik Kodu", "Código de Seguridad", "codigo de seguridad",
    "Sicherheitscode", "セキュリティコード",
    
    # PIN Codes
    "PIN", "pin", "PIN CODE", "PINCODE", "Pin Code", "pin code", "pincode",
    "Karten-PIN",
    
    # Signature & Authorization
    "Signature", "SIGNATURE", "Firma", "imza", "İmza", "Yetkili imza",
    "Authorized Signature", "AUTHORIZED SIGNATURE", "AUTHORIZED",
    "Authorised Signature", "AUTHORISED SIGNATURE", "Authorised", "authorised",
    "Authorizada", "authorizada", "autorizacion",
    
    # === CARD BRANDS ===
    "Visa", "visa", "VISA", "VISA INT",
    "Mastercard", "MASTERCARD", "mastercard", "Master Card", "master",
    "American Express", "american express", "AMERICAN EXPRESS", "AMEX", "Amex", "amex",
    "Discover", "DISCOVER", "discover",
    "Diners Club", "Diners", "Dinners Club",
    "JCB", "UnionPay", "Maestro", "Cirrus", "cirrus",
    
    # === BANK NAMES ===
    "GALICIA", "Galicia", "galicia",
    "Macro", "macro", "MACRO",
    "Itaú", "itaú", "Ita�", "ita�",
    "Hipotecario", "HSBC", "CABAL", "Banco",
    "chase", "CHASE",
    
    # === MULTI-LANGUAGE CARD TERMS ===
    "Kredi Karti", "KREDI KARTI", "Kredi Kartı", "kart",
    "Kreditkarte", "Karten", "Karte", "karten", "karte",
    "Tarjeta de Crédito", "tarjeta",
    "cartao", "Carte de Crédit",
    "Кредитная Карта", "разбитый",
    "クレジットカード", "信用卡", "신용 카드",
    "Carta di Credito", "Ödeme Kartı", "Banka Kartı",
    "CC", "CC Number", "CC number", "cc copy", "cvv info",
    "mail order", "foto tarjeta", "clave",
    
    # === GIFT CARDS ===
    "Gift Card", "gift card", "gift card code", "Hediye Kartı",
    "Prepaid Card", "Vanilla", "VanillaGift",
    
    # === CRYPTO WALLET TERMS ===
    # 2FA & Authentication
    "2fa key", "2fa_key", "authentication key", "authenticator backup",
    
    # BIP Standards
    "64-hex characters", "BIP-39 library", "BIP-39", "BIP39", "BIP44", 
    "HD wallet", "hierarchical deterministic", "deterministic wallet",
    
    # Recovery & Seed Phrases
    "Secret Recovery Phrase", "secret recovery", "Show secret recovery phrase",
    "Seed Phrase", "seed phrase", "seed_image", "seed phrase box",
    "Recovery Phrase", "recovery phrase", "recovery.txt",
    "backup phrase", "Backup Phrases", "backup code",
    "mnemonic", "Mnemonic", "mnemonic library", "mnemonic words", "mnemonic.txt",
    "phrase", "Phrase", "phrase.txt", "phrase_image", "secret phrase", "Secret Phrase",
    "12 word", "24 word", "Write These Down In Order", "your phrase",
    "Store your", "I HAVE A Wallet",
    
    # === WALLET BRANDS ===
    "metamask", "MetaMask", "metamask vault",
    "exodus", "Exodus", "Exodus_paper_backup", "Exodus_paper_backup.jpg",
    "\AppData\Local\exodus",
    "trust wallet", "Trust Wallet", "trust key", "trust phrase",
    "coinbase", "Coinbase", "coinbase login",
    "binance", "Binance", "binance key", "paribu",
    "ledger", "Ledger",
    "trezor", "Trezor",
    "safepal", "SafePal",
    "ellipal", "Ellipal",
    "Jaxx",
    
    # === PRIVATE KEYS ===
    "private key", "Private Key", "Private Keys", "PRIVATE KEYS",
    "private key export", "private key address", "private key hex string",
    "private key view", "copy private key", "copy all private keys",
    "import private key", "private.json", "public key",
    "simple key pair", "MPC key share",
    
    # === KEYSTORE & VAULT ===
    "keystore", "keystore import", "keystore.json", "keystore + password recovery",
    "encrypted keystore", "encrypted JSON string",
    "vault", "vault decryptor", "vault decryptor tool", "vault backup",
    "vault data", "vault extraction", "vault file", "vault key",
    "vault payload", "vault payload copy", "vault seed",
    "encrypted vault", "decrypt the vault", "paste the vault",
    "decrypt button",
    
    # === WALLET OPERATIONS ===
    "wallet", "Wallet", "-wallet", "wallet backup", "wallet credentials",
    "wallet dump", "wallet export", "wallet file", "wallet import",
    "wallet info", "wallet keys", "wallet login", "wallet password",
    "wallet recovery", "wallet secret", "wallet seed", "wallet unlock",
    "wallet.dat", "wallet.docx", "wallet.jpg", "wallet_access", "wallet_key",
    "wallet address", "wallet management page", "wallet name edit",
    "wallet recovery.txt",
    "export wallet", "import wallet", "download wallet",
    "recover wallet", "restore wallet", "remove wallet",
    "cold wallet", "hot wallet", "hardware wallet", "hardware wallet seed",
    "paper wallet backup", "metal backup", "secure backup",
    "keyless wallet", "self-custody wallet", "token wallet",
    "convert to private key wallets",
    
    # === CRYPTO CURRENCIES ===
    "bitcoin", "Bitcoin", "btc", "BTC", "$BTC",
    "ethereum", "Ethereum", "eth", "ETH", "$ETH",
    "Dogecoin", "Litecoin", "digibyte",
    "blockchain", "blockchain keys", "coin", "Currency", "Crypto",
    
    # === EXCHANGE & API ===
    "api key", "API Password", "exchange credentials", "exchange key", "exchange login",
    "Exchange", "import", "keys", "Backup",
    
    # === SECURITY & ENCRYPTION ===
    "passphrase", "password", "Password", "sifre",
    "password encryption", "cipher iv salt",
    "checksum bits", "random entropy", "qr seed",
    "security code", "security seed", "Security Code",
    "secret", "secret code", "Secret word", "secret.txt",
    "code", "backup random entropy",
    
    # === SERVER & DOMAIN ===
    "Server", "SERVER", "Domain", "DOMAIN", "Host", "HOST", "Host:",
    "Username", "Username:", "User", "usuario",
    "phpmyadmin", "ssh", "admin",
    
    # === FILE EXTENSIONS & DATABASE ===
    # Document Files
    ".txt", ".log", ".doc", ".docx", ".pdf", ".rtf",
    
    # Data Files
    ".json", ".xml", ".csv", ".dat", ".db", ".sqlite",
    
    # Database Files
    ".sql", ".mdf", ".ldf", ".bak",
    
    # Email & Communication
    ".pst", ".ost", ".mbx", ".mbox", ".eml",
    
    # Archive Files
    ".zip", ".rar", ".7z", ".tar", ".gz",
    
    # Image Files (in filenames)
    ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff",
    
    # Crypto/Wallet Files
    ".keystore", ".wallet", ".key",
    
    # Other
    "combos", "exploits", "dorks", "sql", "database", "log-in",
    
    # === MESSAGING & EMAIL ===
    "E-mail", "e-mail", "Gmail",
    "WHATSAPP", "whatsapp",
    "telegram", "TELEGRAM",
    "viber", "VIBER",
    "esim", "e-sim",
    
    # === MISC TERMS ===
    "pass", "Pass:", "pass:", "pwd", "pw", "PW:", "login", "log-in",
    "Business", "Balance", "Bakiye", "Account", "Hesap", "Transaction", "İşlem",
    "back-up", "digi-id", "Memes", "Vpn",
    "crypto import", "crypto export", "crypto login", "crypto password",
    "crypto phrase", "crypto secret",
    "paste the data", "idb binary", "persist-root file",
    "storage/default/moz-extension", "cold storage", "sharded storage",
    "identity verification", "enter the password to export",
    "import using secret recovery phrase"
]

# Supported image formats for scanning
SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_folder(folder_path):
    """Create folder if it doesn't exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"✅ Folder created: {folder_path}")

def get_unique_filename(folder, filename):
    """Generate unique filename if file already exists."""
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1
    
    return new_filename

def format_ocr_text(text):
    """Clean and format OCR text."""
    return ' '.join(text.split()).replace('\n', ' ')[:500]

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def process_image(image_path, found_folder, output_csv_writer, processed_count):
    """
    Process image, perform OCR analysis, and save matching results.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng')
        
        # Tag matching (case-insensitive)
        text_lower = text.lower()
        matched_tags = [tag for tag in TAGS if tag.lower() in text_lower]
        
        if matched_tags:
            original_filename = os.path.basename(image_path)
            unique_filename = get_unique_filename(found_folder, original_filename)
            save_path = os.path.join(found_folder, unique_filename)
            
            image.save(save_path)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            result = {
                'timestamp': timestamp,
                'original_path': image_path,
                'saved_path': save_path,
                'matched_tags': ", ".join(matched_tags[:15]),
                'tag_count': len(matched_tags),
                'ocr_text': format_ocr_text(text)
            }
            
            output_csv_writer.writerow(result)
            print(f"✅ [#{processed_count[0]}] FOUND: {original_filename} → {len(matched_tags)} tag(s) matched")
            
            return result
        else:
            print(f"⚪ [#{processed_count[0]}] Scanned: {os.path.basename(image_path)}")
            
    except Exception as e:
        print(f"⚠️ ERROR [{os.path.basename(image_path)}]: {str(e)}")
    
    return None

def scan_images(directory, threads=4, output_csv_writer=None):
    """Scan all images in folder and perform OCR analysis."""
    found_folder = os.path.join(directory, 'found')
    create_folder(found_folder)
    
    results = []
    processed_count = [0]
    
    image_files = []
    for root, _, files in os.walk(directory):
        if 'found' in root:
            continue
        for file in files:
            if file.lower().endswith(SUPPORTED_IMAGE_FORMATS):
                image_files.append(os.path.join(root, file))
    
    total_images = len(image_files)
    print(f"\n📊 Total {total_images} images found. Starting scan...\n")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_file = {
            executor.submit(process_image, img_path, found_folder, output_csv_writer, processed_count): img_path 
            for img_path in image_files
        }
        
        for future in as_completed(future_to_file):
            processed_count[0] += 1
            result = future.result()
            if result:
                results.append(result)
    
    return results

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program flow."""
    print("=" * 70)
    print("🔍 CVV2NET CARD & CRYPTO WALLET PHOTO SCANNER")
    print("=" * 70)
    print("Detects credit cards, seed phrases, and sensitive info in images.")
    print(f"📌 Loaded tags: {len(TAGS)}")
    print("-" * 70)
    
    target_dir = input("\n📁 Folder path to scan: ").strip().strip('"')
    
    if not os.path.isdir(target_dir):
        print("❌ ERROR: Invalid folder path!")
        sys.exit(1)
    
    default_csv = f"ccfinder_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_file = input(f"💾 CSV filename (default: {default_csv}): ").strip() or default_csv
    
    try:
        threads = int(input("🔢 Thread count (recommended: 4-8): ").strip() or 4)
    except ValueError:
        threads = 4
        print("⚠️ Invalid input, using default 4 threads.")
    
    print("\n" + "=" * 70)
    print(f"🚀 STARTING SCAN...")
    print(f"📂 Target: {target_dir}")
    print(f"💾 Output: {output_file}")
    print(f"⚡ Threads: {threads}")
    print("=" * 70 + "\n")
    
    start_time = datetime.now()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['timestamp', 'original_path', 'saved_path', 'matched_tags', 'tag_count', 'ocr_text']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        results = scan_images(target_dir, threads, writer)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("✅ SCAN COMPLETED!")
    print("=" * 70)
    print(f"🔍 Total found: {len(results)} image(s)")
    print(f"⏱️ Duration: {duration:.2f} seconds")
    print(f"💾 Results: {output_file}")
    print(f"📁 Images: {os.path.join(target_dir, 'found')}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
