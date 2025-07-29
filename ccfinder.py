import os
import csv
import pytesseract
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Tesseract yolu (Windows için gerekebilir)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Etiket listesi (kredi kartı vb. içeren filtreleme)
TAGS = [
    "Credit Card", "Tarjeta de Crédito", "Kreditkarte", "Кредитная Карта", "Carte de Crédit", "クレジットカード", 
    "信用卡", "신용 카드", "Kredi Kartı", "Carta di Credito", "Creditcard", "CC", "Payment Card", "Bank Card", 
    "Plastic Card", "Tarjeta Bancaria", "Tarjeta de Pago", "Plástico", "Bankkarte", "Zahlungskarte", "Plastikgeld", 
    "Банковская Карта", "Платежная Карта", "Carte Bancaire", "Carte de Paiement", "信用カード", "決済カード", "カード", 
    "贷记卡", "银行卡", "支付卡", "결제 카드", "은행 카드", "Banka Kartı", "Ödeme Kartı", "Carta Bancaria", 
    "Carta di Pagamento", "Card Number", "Número de Tarjeta", "Kartennummer", "Номер Карты", "Numéro de Carte", 
    "カード番号", "卡号", "카드 번호", "Kart Numarası", "Numero della Carta", "CC Number", "Credit Card Number", 
    "Account Number", "Número de Cuenta", "Número de Tarjeta de Crédito", "Kreditkartennummer", "Kontonummer", 
    "Номер Кредитной Карты", "Номер Счета", "Numéro de Compte", "Numéro de Carte de Crédit", "クレジットカード番号", 
    "口座番号", "信用卡号码", "账号", "신용 카드 번호", "계좌 번호", "Kredi Kartı Numarası", "Hesap Numarası", 
    "Numero di Conto", "Numero della Carta di Credito", "Card Holder", "Titular de la Tarjeta", "Karteninhaber", 
    "Держатель Карты", "Titulaire de la Carte", "カード所有者", "持卡人", "카드 소지자", "Kart Sahibi", 
    "Titolare della Carta", "Cardholder", "Card Owner", "Primary Account Holder", "Propietario de la Tarjeta", 
    "Titular Principal", "Kartenbesitzer", "Kontoinhaber", "Владелец Карты", "Владелец Счета", "Détenteur de la Carte", 
    "Titulaire du Compte", "カード名義人", "口座名義人", "卡主", "账户持有人", "카드 명의자", "계좌 소유자", "Kart Hamili", 
    "Hesap Sahibi", "Possessore della Carta", "Intestatario", "Expiration Date", "Fecha de Vencimiento", "Ablaufdatum", 
    "Срок Действия", "Date d'Expiration", "有効期限", "有效期", "만료일", "Son Kullanma Tarihi", "Data di Scadenza", 
    "Exp. Date", "Exp Date", "Valid Until", "Valid Thru", "Good Thru", "Fecha de Caducidad", "Fecha de Expiración", 
    "Válido Hasta", "Gültig Bis", "Verfallsdatum", "Gültigkeitsdatum", "Действительно До", "Годен До", "Истекает", 
    "Date de Validité", "Valable Jusqu'à", "Date d'Échéance", "使用期限", "期限切れ", "有効期間", "到期日", "有效日期", 
    "有效期至", "유효기간", "유효 날짜", "만기일", "Geçerlilik Tarihi", "Geçerli Olduğu Tarih", "Valido Fino A", "Scade il", 
    "Termine di Validità", "Valid From", "Válido Desde", "Gültig Von", "Действительно С", "Valable à Partir De", 
    "有効開始日", "有效期从", "유효 시작일", "Geçerlilik Başlangıcı", "Valido Dal", "Valid Through", "Validity Period", 
    "Periodo de Validez", "Vigencia", "Gültigkeitszeitraum", "Nutzungszeitraum", "Период Действия", "Срок Годности", 
    "Période de Validité", "Durée de Validité", "有効期間", "使用可能期間", "有效期间", "使用期限", "유효 기간", 
    "사용 기간", "Geçerlilik Süresi", "Kullanım Dönemi", "Periodo di Validità", "Intervallo di Validità", "Security Code", 
    "Código de Seguridad", "Sicherheitscode", "Код Безопасности", "Code de Sécurité", "セキュリティコード", "安全码", 
    "보안 코드", "Güvenlik Kodu", "Codice di Sicurezza", "CVV", "CVC", "CSC", "Card Verification Value", "CVV2", "CID", 
    "CVV", "CVC", "Código de Verificación", "Código de Validación", "Prüfnummer", "Kartenprüfnummer", "Sicherheitsnummer", 
    "Защитный Код", "Проверочный Код", "CVV-код", "Cryptogramme Visuel", "Code de Vérification", "CVV", "認証コード", 
    "確認コード", "セキュリティ番号", "验证码", "安全代码", "卡验证码", "검증 코드", "인증 코드", "카드 검증 값", "Doğrulama Kodu", 
    "CVV", "Kart Güvenlik Kodu", "Codice di Verifica", "CVV", "Codice di Controllo", "PIN Code", "Código PIN", "PIN-Code", 
    "ПИН-код", "Code PIN", "暗証番号", "密码", "비밀번호", "PIN Kodu", "Codice PIN", "Personal Identification Number", 
    "PIN", "Secret Code", "Número de Identificación Personal", "Clave", "Código Secreto", "Persönliche Identifikationsnummer", 
    "Geheimzahl", "PIN", "Персональный Идентификационный Номер", "Секретный Код", "Numéro d'Identification Personnel", 
    "Code Secret", "PIN番号", "個人識別番号", "秘密の番号", "个人识别码", "PIN码", "私人密码", "PIN код", "개인 식별 번호", 
    "비밀 코드", "Kişisel Kimlik Numarası", "Şifre", "Gizli Kod", "Numero di Identificazione Personale", "Codice Segreto", 
    "Signature", "Firma", "Unterschrift", "Подпись", "Signature", "署名", "签名", "서명", "İmza", "Firma", "Authorized Signature", 
    "Signature Strip", "Sign Here", "Firma Autorizada", "Banda de Firma", "Firme Aquí", "Autorisierte Unterschrift", 
    "Unterschriftsfeld", "Hier Unterschreiben", "Авторизованная Подпись", "Полоса Для Подписи", "Распишитесь Здесь", 
    "Signature Autorisée", "Bande de Signature", "Signez Ici", "承認された署名", "署名欄", "ここに署名", "授权签名", "签名条", 
    "在此签名", "승인된 서명", "서명란", "여기에 서명", "Yetkili İmza", "İmza Bandı", "Buraya İmzalayın", "Firma Autorizzata", 
    "Striscia per la Firma", "Firmare Qui", "Visa", "VISA", "VISA INT", "Mastercard", "MASTERCARD", "Master Card", 
    "American Express", "AMEX", "Amex", "AMERICAN EXPRESS", "Discover", "DISCOVER", "Diners Club", "Diners", "Dinners Club", 
    "JCB", "Japan Credit Bureau", "UnionPay", "China UnionPay", "Maestro", "Cirrus", "Debit Card", "Tarjeta de Débito", 
    "Debitkarte", "Дебетовая Карта", "Carte de Débit", "デビットカード", "借记卡", "직불 카드", "Banka Kartı", "Carta di Debito", 
    "Credit Card", "Tarjeta de Crédito", "Kreditkarte", "Кредитная Карта", "Carte de Crédit", "クレジットカード", "信用卡", 
    "신용 카드", "Kredi Kartı", "Carta di Credito", "Prepaid Card", "Tarjeta Prepago", "Prepaid-Karte", "Предоплаченная Карта", 
    "Carte Prépayée", "プリペイドカード", "预付卡", "선불 카드", "Ön Ödemeli Kart", "Carta Prepagata", "Charge Card", 
    "Gift Card", "Virtual Card", "Tarjeta de Cargo", "Tarjeta de Regalo", "Charge-Karte", "Geschenkkarte", "Подарочная Карта", 
    "Carte Cadeau", "ギフトカード", "礼品卡", "기프트 카드", "Hediye Kartı", "Carta Regalo", "Basic", "Básica", "Basis", 
    "Базовая", "Basique", "ベーシック", "基础卡", "기본", "Temel", "Base", "Standard", "Estándar", "Standard", "Стандарт", 
    "Standard", "スタンダード", "标准卡", "표준", "Standart", "Standard", "Gold", "Oro", "Gold", "Золотая",
]

# Desteklenen görsel formatları
SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

def process_image(image_path, found_folder, output_csv_writer):
    """Verilen görseli işleyip OCR analizini yapacak ve sonucu /found altına kaydedecek fonksiyon."""
    print(f"[📷] OCR yapılıyor: {image_path}")
    try:
        # Görseli aç ve OCR işlemi yap
        text = pytesseract.image_to_string(Image.open(image_path))
        matched_tags = [tag for tag in TAGS if tag.lower() in text.lower()]
        
        # Etiket eşleşmesi varsa görseli kaydet
        if matched_tags:
            # /found klasörüne kaydet
            if not os.path.exists(found_folder):
                os.makedirs(found_folder)  # /found dizini yoksa oluştur

            # Yeni dosya yolu oluştur
            base_name = os.path.basename(image_path)
            save_path = os.path.join(found_folder, base_name)

            # Görseli /found klasörüne kaydet
            image = Image.open(image_path)
            image.save(save_path)

            # CSV'ye anında yazma işlemi
            result = {
                'file': save_path,
                'matched_tags': ", ".join(matched_tags),
                'ocr_text': text.replace('\n', ' ')
            }
            output_csv_writer.writerow(result)  # Anında yazma işlemi

            return result
    except Exception as e:
        print(f"[⚠️] Hata ({image_path}): {e}")
    return None

def scan_images(directory, threads=4, output_csv_writer=None):
    """Verilen klasördeki tüm görselleri tarar ve OCR sonuçlarını döndürür."""
    found_folder = os.path.join(directory, 'found')
    results = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Tüm dosyaları işle
        future_to_file = {executor.submit(process_image, os.path.join(root, file), found_folder, output_csv_writer): os.path.join(root, file)
                          for root, _, files in os.walk(directory)
                          for file in files if file.lower().endswith(SUPPORTED_IMAGE_FORMATS)}
        
        # Her bir işin sonucunu kontrol et
        for future in future_to_file:
            result = future.result()
            if result:
                results.append(result)
    
    return results

def save_to_csv(results, output_path):
    """OCR sonuçlarını bir CSV dosyasına kaydeder."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['file', 'matched_tags', 'ocr_text']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    target_dir = input("🔍 Tarama yapılacak klasör: ").strip()
    
    # Geçerli dosya adı kontrolü
    while True:
        output_file = input("💾 Çıktı CSV dosyası (örn: ocr_output.csv): ").strip()
        if not output_file:
            print("❌ Geçersiz dosya adı. Lütfen geçerli bir dosya adı girin.")
        else:
            break

    threads = int(input("🔢 Kaç iş parçacığı (thread) kullanılacak? (Önerilen: 4): ").strip() or 4)

    if not os.path.isdir(target_dir):
        print("❌ Geçersiz klasör yolu.")
        exit(1)

    print(f"\n[🚀] Taramaya başlandı: {target_dir}")

    # Dosyayı hemen açıp yazma başlat
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['file', 'matched_tags', 'ocr_text']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # OCR işlemi
        scan_images(target_dir, threads, writer)

    print(f"\n[✅] Tarama tamamlandı. Sonuçlar yazıldı → {output_file}")
