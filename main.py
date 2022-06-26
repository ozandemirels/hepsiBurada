import requests
from bs4 import BeautifulSoup
import smtplib
import time

url = input("Takibe almak istediğiniz ürünün Hepsiburada'daki url'sini giriniz.")
expectedPrice = input('Alarm koymak istediğniz fiyatı giriniz.')
headers = {'User-Agent': 'my user agent(google)'}


def checkPrice():
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    pname = soup.find('div', class_='hide-title').header
    pname = pname.text.replace('\n', '')
    currentPrice = soup.find('div', class_='product-price price-container big')
    currentPrice = currentPrice.find_all('span')
    if len(currentPrice[5].text) >= 4:
        currentPrice = str(currentPrice[5].text).replace('.', '') + '.' + str(currentPrice[6].text)
    else:
        currentPrice = str(currentPrice[5].text) + '.' + str(currentPrice[6].text)
    if float(currentPrice) <= float(expectedPrice):
        send_mail(pname)
        return False


def send_mail(pname):
    gmailUser = 'ozandemirel.93@gmail.com'
    gmailPassword = '****************'
    to = 'ozandemirel.93@gmail.com'
    try:
        smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmailUser, gmailPassword)
        subject = "Hepsiburada'daki " + pname + " adlı ürünün fiyatı belirlediğiniz fiyatın altına düştü.\n\nHepsiburada'daki " + pname + ' adlı ürünün fiyatı belirlediğiniz fiyatın altına düştü.\n\nİncelemek için linke tıklayınız --> ' + url
        mail_content = f"To:{to}\nFrom:{gmailUser}\nSubject:{subject}"
        mail_content = mail_content.encode('utf-8')
        smtpserver.sendmail(gmailUser, to, mail_content)
    except smtplib.SMTPException as error:
        print(error)
    smtpserver.close()


while True:
    if checkPrice() == False:
        break
    else:
        time.sleep(60 * 60)