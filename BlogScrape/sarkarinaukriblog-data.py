# This obtains the 15 most recent blog posts from http://www.sarkarinaukriblog.com/ into an associated text file.

from bs4 import BeautifulSoup
import urllib2
import datetime
import re
import time
from datetime import date, timedelta

def WriteToFile(currentFile, info):
    currentFile.write("----------------------------------------------------------------------------------------------------------------------\n")

    info = info.find('a')
    link = info['href']
    title = info.get_text().encode('utf-8')

    currentFile.write("Link: " + str(link.encode('utf-8')) + "\n\n")
    currentFile.write("Title: " + str(title.encode('utf-8')) + "\n")
    currentFile.write("Date Posted: " + str(currentDate.encode('utf-8')) + "\n")

    postPage = urllib2.urlopen(link).read()

    postSoup = BeautifulSoup(postPage)

    postContent = postSoup.find("div", class_="post-body entry-content")

    # Regex to remove the remaining HTML comments and posted by after removeing all HTML tags and leading newlines.
    removedHTML = re.sub('[\s\S]*?\/\/-->', '', postContent.get_text()).lstrip()
    removedHTML = re.sub('Published[\s\S]*?\)', '', removedHTML)

    currentFile.write("Content: \n\t" + removedHTML.strip().encode('utf-8') + "\n")    
# End of WriteToFile

todayDate = date.today()
currentDate = todayDate.strftime('%d%B%y')

yesterday = date.today() - timedelta(days=1)
yesterdayDate = yesterday.strftime('%d%B%y')

currentFile = open(str(currentDate) + '_sarkarinaukriblog.txt', 'w')
yesterdayFile = None

try:
   yesterdayFile = open(yesterdayDate + '_sarkari-naukri.txt', 'ab+')
except IOError:
   print 'Yesterday\'s file not found, using today only'

# HTML source for homepage.
homePage = urllib2.urlopen('http://www.sarkarinaukriblog.com/').read()
homePageSoup = BeautifulSoup(homePage)

# Traverse to blog-posts hfeed div which contains link to posts and dates of posting.
postsLinkContainer = homePageSoup.find("div", class_="blog-posts hfeed")

dateTags = postsLinkContainer.find_all("h2", class_="date-header")

# Iterate through list of post links, scraping information into file as needed. Use of encode() to 
# minimize errors when printing characters.
for child in postsLinkContainer.findChildren():
    if child != None:
        if child.name == 'h2':
            currentDate = child.get_text().encode('utf-8')
        elif child.name == 'div':
            info = child.find("h3")
            if info != None:
                
                publishDateFormatted = time.strftime('%d%B%y', time.strptime(currentDate, '%d %B, %Y'))

                postMatchFound = False

                # If the date of post matches yesterday, then check yesterday's file for duplicates and append 
                # to yesterday's file if the current posts' title does not match file contents.
                if publishDateFormatted == yesterdayDate and yesterdayFile != None:
                    for line in yesterdayFile:
                        if re.match('Title: .*', line) and line == "Title: " + str(title.encode('utf-8')):
                            postMatchFound = True

                            # Break out of line pattern search.
                            break

                    # Since there is a match in yesterday's file, continue to next post.
                    if postMatchFound == True:
                        continue
                    else:
                        WriteToFile(yesterdayFile, info)

                else:
                    WriteToFile(currentFile, info)

yesterdayFile.close()
currentFile.close()
