
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import smtplib
from email.message import EmailMessage

def ftc_scrape():
    html_text = requests.get('https://www.ftc.gov/enforcement/cases-proceedings/2110015/nvidiaarm-matter').text
    soup = BeautifulSoup(html_text, 'lxml')
    docket = soup.find('div', class_ = 'view-content')
    entry = docket.find('article')
    date = entry.find('span', class_ = 'date date-display-single').text
    datetime_obj = datetime.strptime(date, '%B %d, %Y')

    if datetime_obj.date() == datetime.today().date():
        title = entry.find('a').text
        link = entry.find('a', attrs={'href': re.compile('^https://')})
        link = link.get('href')
        res = f'New Entry\nDate: {date}\nDocument Title: {title}\nLink: {link}'

    else:
        res = 'No new entries'
    
    return res

def send_email(message):
    
    msg = EmailMessage()
    msg['Subject'] = 'FTC v. Nvidia alert'
    msg['From'] = 'EMAIL'
    msg['To'] = 'EMAIL'
    msg.set_content(message)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('EMAIL', 'PASSWORD')
        smtp.send_message(msg)


if __name__ == '__main__':
    res = ftc_scrape()
    send_email(res)
