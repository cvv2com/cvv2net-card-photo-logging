#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVV2NET Kart Fotoğraf Tarama Aracı
Görsellerdeki kredi kartı, banka kartı ve hassas bilgileri OCR ile tespit eder.
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
# YAPILANDIRMA
# ============================================================================

# Tesseract yolu (Windows için otomatik tespit)
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
        print("⚠️ UYARI: Tesseract OCR bulunamadı. Lütfen Tesseract'ı yükleyin.")
        print("İndirme Linki: https://github.com/tesseract-ocr/tesseract")

# Etiket listesi - Çok dilli kredi kartı ve hassas bilgi tespiti
TAGS = [
    # Kart türleri
    "Credit Card", "Tarjeta de Crédito", "Kreditkarte", "Кредитная Карта", 
    "Carte de Crédit", "クレジットカード", "信用卡", "신용 카드", "Kredi Kartı", 
    "Carta di Credito", "Creditcard", "CC", "Payment Card", "Bank Card", 
    "Plastic Card", "Debit Card", "Banka Kartı", "Ödeme Kartı",
    
    # Kart markaları
    "Visa", "VISA", "Mastercard", "MASTERCARD", "Master Card", "American Express", 
    "AMEX", "Amex", "Discover", "DISCOVER", "Diners Club", "Diners", "JCB", 
    "UnionPay", "Maestro", "Cirrus",
    
    # Kart bilgileri
    "Card Number", "Número de Tarjeta", "Kartennummer", "Номер Карты", 
    "Numéro de Carte", "カード番号", "卡号", "카드 번호", "Kart Numarası", 
    "Card Holder", "Cardholder", "Kart Sahibi", "Titular",
    
    # Geçerlilik tarihi
    "Expiration Date", "Exp Date", "Valid Until", "Valid Thru", "Good Thru",
    "Son Kullanma Tarihi", "Geçerlilik Tarihi", "有効期限", "到期日",
    
    # Güvenlik kodları
    "CVV", "CVC", "CSC", "CVV2", "CID", "Security Code", "Güvenlik Kodu",
    "Código de Seguridad", "Sicherheitscode", "セキュリティコード",
    
    # PIN ve imza
    "PIN", "PIN Code", "Signature", "Firma", "İmza", "Authorized Signature",
    
    # Kripto wallet seed phrases
    "Mnemonic", "Seed Phrase", "Recovery Phrase", "12 word", "24 word",
    "Wallet", "Private Key", "Master Private Key", "BIP39", "BIP44",
    
    # Gift card'lar
    "Gift Card", "Hediye Kartı", "Prepaid Card", "Vanilla", "VanillaGift",
    
    # Ek güvenlik
    "Balance", "Bakiye", "Account", "Hesap", "Transaction", "İşlem"
]

# Desteklenen görsel formatları
SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')

# ============================================================================
# YARDIMCI FONKSİYONLAR
# ============================================================================

def create_folder(folder_path):
    """Klasör yoksa oluşturur."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"✅ Klasör oluşturuldu: {folder_path}")

def get_unique_filename(folder, filename):
    """Aynı isimde dosya varsa benzersiz isim oluşturur."""
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1
    
    return new_filename

def format_ocr_text(text):
    """OCR metnini temizler ve formatlar."""
    return ' '.join(text.split()).replace('\n', ' ')[:500]  # İlk 500 karakter

# ============================================================================
# ANA FONKSİYONLAR
# ============================================================================

def process_image(image_path, found_folder, output_csv_writer, processed_count):
    """
    Görseli işler, OCR analizi yapar ve eşleşen sonuçları kaydeder.
    
    Args:
        image_path: İşlenecek görsel dosyası yolu
        found_folder: Bulunan görsellerin kaydedileceği klasör
        output_csv_writer: CSV yazıcı nesnesi
        processed_count: İşlenen görsel sayacı
    
    Returns:
        dict veya None: Eşleşme varsa sonuç dictionary'si
    """
    try:
        # OCR işlemi
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng')
        
        # Etiket eşleştirme (büyük/küçük harf duyarsız)
        text_lower = text.lower()
        matched_tags = [tag for tag in TAGS if tag.lower() in text_lower]
        
        # Eşleşme varsa kaydet
        if matched_tags:
            # Benzersiz dosya adı oluştur
            original_filename = os.path.basename(image_path)
            unique_filename = get_unique_filename(found_folder, original_filename)
            save_path = os.path.join(found_folder, unique_filename)
            
            # Görseli kaydet
            image.save(save_path)
            
            # Zaman damgası ekle
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Sonuç oluştur
            result = {
                'timestamp': timestamp,
                'original_path': image_path,
                'saved_path': save_path,
                'matched_tags': ", ".join(matched_tags),
                'ocr_text': format_ocr_text(text)
            }
            
            # CSV'ye anında yaz
            output_csv_writer.writerow(result)
            
            print(f"✅ [#{processed_count[0]}] BULUNDU: {original_filename} → {len(matched_tags)} etiket eşleşti")
            
            return result
        else:
            print(f"⚪ [#{processed_count[0]}] Tarandı: {os.path.basename(image_path)}")
            
    except Exception as e:
        print(f"⚠️ HATA [{os.path.basename(image_path)}]: {str(e)}")
    
    return None

def scan_images(directory, threads=4, output_csv_writer=None):
    """
    Klasördeki tüm görselleri tarar ve OCR analizi yapar.
    
    Args:
        directory: Taranacak ana klasör
        threads: Paralel işlem sayısı
        output_csv_writer: CSV yazıcı nesnesi
    
    Returns:
        list: Bulunan sonuçların listesi
    """
    found_folder = os.path.join(directory, 'found')
    create_folder(found_folder)
    
    results = []
    processed_count = [0]  # Liste içinde sayaç (mutable)
    
    # Tüm görsel dosyalarını topla
    image_files = []
    for root, _, files in os.walk(directory):
        # 'found' klasörünü atla
        if 'found' in root:
            continue
        for file in files:
            if file.lower().endswith(SUPPORTED_IMAGE_FORMATS):
                image_files.append(os.path.join(root, file))
    
    total_images = len(image_files)
    print(f"\n📊 Toplam {total_images} görsel bulundu. Tarama başlıyor...\n")
    
    # Paralel işleme
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_file = {
            executor.submit(process_image, img_path, found_folder, output_csv_writer, processed_count): img_path 
            for img_path in image_files
        }
        
        # Sonuçları topla
        for future in as_completed(future_to_file):
            processed_count[0] += 1
            result = future.result()
            if result:
                results.append(result)
    
    return results

# ============================================================================
# ANA PROGRAM
# ============================================================================

def main():
    """Ana program akışı."""
    print("=" * 70)
    print("🔍 CVV2NET KART FOTOĞRAF TARAMA ARACI")
    print("=" * 70)
    print("Bu araç, görsellerdeki kredi kartı, seed phrase ve hassas bilgileri tespit eder.")
    print("-" * 70)
    
    # Kullanıcı girdileri
    target_dir = input("\n📁 Taranacak klasör yolu: ").strip().strip('"')
    
    if not os.path.isdir(target_dir):
        print("❌ HATA: Geçersiz klasör yolu!")
        sys.exit(1)
    
    # CSV dosya adı
    default_csv = f"ccfinder_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_file = input(f"💾 CSV dosya adı (varsayılan: {default_csv}): ").strip() or default_csv
    
    # Thread sayısı
    try:
        threads = int(input("🔢 Thread sayısı (önerilen: 4-8): ").strip() or 4)
    except ValueError:
        threads = 4
        print("⚠️ Geçersiz giriş, varsayılan 4 thread kullanılıyor.")
    
    print("\n" + "=" * 70)
    print(f"🚀 TARAMA BAŞLATILIYOR...")
    print(f"📂 Hedef: {target_dir}")
    print(f"💾 Çıktı: {output_file}")
    print(f"⚡ Thread: {threads}")
    print("=" * 70 + "\n")
    
    start_time = datetime.now()
    
    # CSV dosyasını aç ve yazma işlemini başlat
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['timestamp', 'original_path', 'saved_path', 'matched_tags', 'ocr_text']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        # Tarama işlemi
        results = scan_images(target_dir, threads, writer)
    
    # Sonuç özeti
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("✅ TARAMA TAMAMLANDI!")
    print("=" * 70)
    print(f"🔍 Toplam bulunan: {len(results)} görsel")
    print(f"⏱️ Süre: {duration:.2f} saniye")
    print(f"💾 Sonuçlar: {output_file}")
    print(f"📁 Görseller: {os.path.join(target_dir, 'found')}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {str(e)}")
        sys.exit(1)