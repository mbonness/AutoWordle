# AutoWordle
 Automated Wordle playing bot.  Uses NY Times allowed word list and scrape of previous answers to compile a basic vocabulary, then scores the words based on how frequently individual letters occur in the word dictionary.  The bot opens a Chrome window using Selenium and enters the guesses, then clicks the Share button to send the results in a text message using Twilio.
 
 Video: https://www.youtube.com/shorts/QdjO_Y_JXmE

 Originally this used the 2k solutions list published by the NY Times but due to recent changes where the Wordle editor is now adding new words, we can no longer rely on that list.  In fact, the solutions.txt file hosted on the NY Times' website has been gutted so there is no longer an "official" list of possible solutions.  WordleBot 1.0 used to link to solutions.txt and sometimes dinged players for using words that were not a possible solution.

 So I removed about 9,000 obscure words (SOARE) from the 12k "allowed" word list to come up with a more manageable 3k list that includes GUANO (Wordle #646) and hopefully other words the editor is adding to the game in the near future.  Hackers are predicting more new "unknown" words in upcoming puzzles as the editor makes more and more changes to the solutions list which appears to be a scheduled set of words the editor is constantly tweaking and rearranging.

 Thanks to Joanna Peterson for assisting with the dictionary curation effort.

To run the bot, you will need to install Python3, BeautifulSoup, Selenium, and Twilio.  If you want the script to text you the results, edit the textMyself.py file and put your Twilio API keys, phone number, email etc. in the appropriate string literals.

https://www.python.org/downloads/

`pip install beautifulsoup4`

`pip install -U selenium`

`pip3 install twilio`
