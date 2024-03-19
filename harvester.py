import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
url = input("Başında https olacak şekilde urlyi giriniz: ")
def find_emails(url):
    # Ziyaret edilen URL'leri depolamak için bir set oluştur
    visited_urls = set()
    
    # E-posta adreslerini bulmak için düzenli ifade (regular expression) tanımla
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Verilen URL'yi ziyaret etmek için yardımcı bir fonksiyon tanımla
    def visit_page(url):
        # URL'yi ziyaret edildi olarak işaretle
        visited_urls.add(url)
        
        # Web sitesinden HTML içeriğini indir
        response = requests.get(url)
        html_content = response.text
        
        # E-posta adreslerini bul
        emails = re.findall(email_pattern, html_content)
        
        # Bulunan e-posta adreslerini ekrana yazdır
        if emails:
            print(f"{url} adresinde bulunan e-posta adresleri:")
            for email in emails:
                print(email)
        
        # HTML içeriğini BeautifulSoup kullanarak ayrıştır
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Tüm bağlantıları bul
        links = soup.find_all('a', href=True)
        
        # Her bir bağlantıya git ve e-posta adreslerini ara
        for link in links:
            href = link['href']
            absolute_url = urljoin(url, href)
            if absolute_url not in visited_urls:
                visit_page(absolute_url)
    
    # Verilen URL'yi ziyaret et
    visit_page(url)

# Test etmek için bir web sitesi URL'si
website_url = url

# E-posta adreslerini bul
find_emails(website_url)
