
Installation scenario
******************************
sudo apt update
sudo apt install python3 python3-pip tesseract-ocr -y
pip install --upgrade certifi --break-system-packages
pip install --user pytesseract pillow

python -m pip install --upgrade pip

pip install --user certifi

1. Tesseract'ı Yüklemek:
Öncelikle Tesseract'ı bilgisayarınıza yüklemeniz gerekmektedir:

Tesseract'ı Yükleme:

Tesseract İndir https://github.com/tesseract-ocr/tesseract
Windows için Tesseract'ı indirip yükledikten sonra, tesseract.exe'nin yolunu belirlemeniz gerekecek.
Python Kütüphanesini Yükleme:

1. Tesseract OCR Yükleme
Windows için Tesseract OCR'yi yüklemek için aşağıdaki adımları takip edebilirsiniz:

a) Tesseract'ı İndirme
Tesseract OCR Windows Kurulum Sayfası adresine gidin ve en son Windows Installer'ı (örneğin tesseract-ocr-w32-setup-v5.0.0-alpha.20201203.exe) indirin.
b) Yükleme
İndirilen .exe dosyasını çalıştırarak Tesseract OCR'yi kurun. Kurulum sırasında dikkat etmeniz gereken noktalar:
Tesseract'ı varsayılan olarak C:\Program Files\Tesseract-OCR klasörüne kurun.
Tesseract'ın kurulu olduğu dizini not edin, çünkü Python kodunda bu dizini belirtmeniz gerekecek.
c) Sisteme Tesseract Yolunu Ekleyin
Tesseract'ı kurduktan sonra, Python'dan bu yolu kullanabilmesi için yolu belirtmeniz gerekecek.

Örneğin, eğer Tesseract şu dizine kuruluysa:

C:\Program Files\Tesseract-OCR\tesseract.exe

Python kodunda, pytesseract kütüphanesini kullanmadan önce aşağıdaki satırı ekleyin:

python
Copy code
import pytesseract

# Windows için Tesseract yolunu belirtin
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
2. OCR Testi Yapma
Kurulumları tamamladıktan sonra, basit bir OCR testi yapmak için aşağıdaki Python kodunu kullanabilirsiniz:

python
Copy code
from PIL import Image
import pytesseract

# Tesseract yolunu belirtin
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Test görseli (resmin yolunu belirtin)
image_path = "test_image.png"  # Test için bir resim dosyasını belirleyin
img = Image.open(image_path)

# OCR işlemi
text = pytesseract.image_to_string(img)

# Sonucu yazdır
print("OCR Sonucu:")
print(text)
Bu kod, belirtilen resim dosyasındaki metni okur ve terminalde ekrana yazdırır.

3. PATH Değişkenine Tesseract Ekleme (Opsiyonel)
Eğer pytesseract'ı kullanırken herhangi bir sorunla karşılaşırsanız, Tesseract'ın kurulu olduğu dizini PATH ortam değişkenine eklemeyi deneyebilirsiniz.

a) PATH'e Tesseract Yolu Eklemek
Başlat Menüsüne sağ tıklayın ve Sistem → Gelişmiş sistem ayarları → Ortam Değişkenleri'ni seçin.
Sistem değişkenleri kısmında Path'i bulun ve Düzenle'ye tıklayın.
Yeni butonuna basarak şu yolu ekleyin:
txt
Copy code
C:\Program Files\Tesseract-OCR
b) Değişiklikleri Kaydetmek
Tüm pencereyi Tamam diyerek kapatın.
Bu adım, tesseract komutunun her yerden çalışmasını sağlar.


Python kütüphaneleri (pytesseract, pillow, certifi) başarıyla yüklendi.
Tesseract OCR yazılımını indirin, yükleyin ve Python'da doğru yolda kullanıldığından emin olun.
Tesseract'ın yolunu belirtin ve OCR testi yaparak her şeyin düzgün çalıştığından emin olun.

The process_image function performs each image processing:
OCR analysis is performed.
If the tags match, the image is saved in the found folder.
The OCR result and matching tags are instantly written to the CSV file.
Writing Each Processing Results to the CSV File:

***********************

When each image is processed, it is instantly written to the CSV file. This means that previous operations are not lost, even if there are any errors during processing.
Regular Saving of the CSV File and Images:

Images are saved in the found folder, and their file names are saved with their original file names.
The path, tags, and OCR output of each processed image are saved in the CSV file.
Advantages of This Updated Script:
No data loss: If the script closes before the process is complete, the last processed data is not lost because it is instantly written to the CSV upon completion of each process.
Instant results are obtained during processing: As the image is processed, the results are immediately recorded and stored in the found folder, as well as in the files.
This script makes the script more reliable at every stage.

Main changes:
File writing is now continuous: After each image is processed, the process_image function immediately writes the result to a CSV file.
CSV writing has been moved to the scan_images function: As images are processed, the results for each job are immediately written.
This way, as the script processes all images, the results are written to the CSV file, and even if the script is interrupted, the data processed up to that point will not be lost.

[??] Scanning started: C:\
[??] OCR in progress: C:\path\to\image1.jpg
[??] OCR in progress: C:\path\to\image2.png
[?] 10 matches found. Results written ? ocr_output.csv


With the new functionality you added to your code, you OCR the images and save them in the found folder. This is a great step! You've ensured that the images are saved under their respective directories.

Code Summary:
The process_image() function OCRs each image and, if it finds a tag match, saves the image in the found folder.
The scan_images() function processes all the images in the given directory and returns the results as a list.
The save_to_csv() function saves the OCR results to a CSV file.
Additional Notes:
A "found" folder is automatically created (if it doesn't exist), and images are saved in this directory. This prevents any images from being lost or corrupted.

Within the process_image() function, if a text match is found, the image is saved along with its file name.

Potential Improvements:
File Name Conflicts: If multiple images have the same name, conflicts may occur during saving. Adding a timestamp to the file name can be helpful to prevent this.

For example:

python
Copy code
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join(found_folder, f"{timestamp}_{base_name}")
Less Complex Error Messages: If you provide more descriptive error messages during the OCR process, you can more easily resolve issues encountered by users.

Performance Improvements: You can dynamically adjust the number of threads using the ThreadPoolExecutor in the scan_images() function. This allows you to increase the number of threads when more processing power is needed.

Usage:
When running the code, you select the folder you want to scan.
You specify a CSV file name to save the results.
Images are saved under /found, and information about matching tags is written to CSV.
Output Example:
plaintext
Copy code
[??] Scanning started: C:\
[??] OCR is running: C:\path\to\image1.jpg
[??] OCR is running: C:\path\to\image2.png
[?] 10 matches found. Results are written to ? ocr_output.csv


<img width="1920" height="1080" alt="ccphotofinder" src="https://github.com/user-attachments/assets/ca8ec933-7191-46b9-9747-378d4afa213d" />

CSV Kaydı ve Güvenlik: OCR çıktısı içerisinde hassas bilgiler (kart numaraları, son kullanma tarihleri, vb.) varsa, bu verilerin güvenli bir şekilde saklanması ve işlenmesi gerekir. Eğer bir proje için bu tür verileri saklıyorsanız, belirli güvenlik protokollerine dikkat etmeniz gerekmektedir.

Veri Formatı: Kayıt edilen veri şu şekilde görünüyor:

C:\found\20316302.png,"CC, Visa, VISA",aa yw  010010 4050710141969928 |09|2027|209  4050710141969928 |09|2027|209 Country: AR  Brand: visa Type: credit  Check type: pre-authorization Status: succeeded  $ Your balance 196 check


