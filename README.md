# AutoWordle
 Automated Wordle playing bot.  Uses NY Times allowed word list and scrape of previous answers to compile a basic vocabulary, then scores the words based on how frequently individual letters occur in the word dictionary.  The bot opens a Chrome window using Selenium and enters the guesses, then clicks the Share button to send the results in a text message using Twilio.

 Originally this used the 2k solutions list published by the NY Times but due to recent changes where the Wordle editor is now adding new words, we can no longer rely on that list and must use the larger 12k list of allowed words.  As an improvement, I might curate the 12k list to remove obscure words like SOARE.

To run the bot, you will need Python3, BeautifulSoup, Selenium, and Twilio.

https://www.python.org/downloads/

`pip install beautifulsoup4`

`pip install -U selenium`

`pip3 install twilio`
