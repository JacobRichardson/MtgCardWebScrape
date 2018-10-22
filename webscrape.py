import smtplib
import requests
from bs4 import BeautifulSoup

#Links for all the cards
links = ["https://www.mtggoldfish.com/price/Modern+Masters+2015/Mox+Opal#paper",
         "https://www.mtggoldfish.com/price/Zendikar+Expeditions:Foil/Hallowed+Fountain#paper",
         "https://www.mtggoldfish.com/price/Kaladesh+Inventions:Foil/Platinum+Angel#online"
         ]
#Array to store all the card objects created from the links
cardList = []
#Is the array of numbers you want the card's price to be checked against. So if the first card in cardList
#has a price above 100 it will be added to the email message saying the price is above 100 dollars
watchPrices = [100, 200, 100]
#class to store the information of each card
class card:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    #function used to see if a given price is higher than the card price
    def higherPrice(self, givenPrice):
        if self.price > givenPrice:
            return True
#Function to access a given url
def makeSoup(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.text,"html.parser")
    return soupdata
#Function to process all the urls in a list
def processLinks():
    for x in links:
        #calls makeSoup function to process each indiviual link
        soup = makeSoup(x)
        #card price is stored in the second div with class name "price-box-price. Used .text to get the actual value."
        price = float(soup.find_all("div", class_="price-box-price")[1].text)
        #same thing for the name of the card except it had its own class name.
        name = soup.find("div", class_="price-card-name-header-name").text
        #create a new card object based on the data taken off the website
        card1 = card(name, price)
        #add it to the list of card objects
        cardList.append(card1)

#function used to send an email
def sendEmail(subject, msg):
    try:
        server =smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        #change this line to send an email to any email
        server.login("SteathlyShadowSniper@gmail.com", "%Password%")
        message = 'Subject: {} \n \n{}'.format(subject, msg)
        server.sendmail("SteathlyShadowSniper@gmail.com", "SteathlyShadowSniper@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send")
#function that will take a url and a alert price and send an email about whether or not the alert price has been reached
def checkPrice(url, alertPrice):
    soup = makeSoup(url)
    price = float(soup.find_all("div", class_="price-box-price")[1].text)
    name = soup.find("div", class_="price-card-name-header-name").text
    if(float(price) > float(alertPrice)):
        message = str(name) + "Price threshold was "  \
                  + str(alertPrice) + ". The current price is " + str(price)
        sendEmail("Magic Card Price Alert", message)
    if(float(alertPrice) > float(price)):
        message = str(name) + "Alert price has not been reached yet. The current price is " + str(price)+ \
                              ". The alert price is set to " + str(alertPrice) + "."
        sendEmail("Magic Card Price Update", message)
#function to compare the card prices with the watch prices and create a string to be sent to the email
def cardListWatchPrices(prices):
    index = 0
    message = ""
    for cards in cardList:
        #first check to see if the watch price is higher than the card price
        if (cards.higherPrice(prices[index])):
            #if it is add the desired infromation to a string and do keeping added onto itself
            message = message + cardList[index].name +"Price threshold was "  \
                      + str(prices[index]) + ". The current price is " + str(cardList[index].price) + "\n" + \
                      "----------------------------------------------------------------------------------------"
        index = index + 1
    #call the send email function with the large string of all the desired information
    sendEmail("Magic Card Price Alert", message)
#function to test all the other functions
def main():
    processLinks()
    cardListWatchPrices(watchPrices)
    #checkPrice("https://www.mtggoldfish.com/price/Modern+Masters+2015/Mox+Opal#paper", 200)

main()
