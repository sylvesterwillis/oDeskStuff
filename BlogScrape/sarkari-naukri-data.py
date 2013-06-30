# This obtains the 15 most recent blog posts from http://www.sarkari-naukri.in/ into an associated text file.
from bs4 import BeautifulSoup
import urllib2
import datetime
import sys
import re
import time
from datetime import date, timedelta
        
def WriteToFile(currentFile, link, title, publishDate, postSoup):
    currentFile.write("----------------------------------------------------------------------------------------------------------------------\n")
    currentFile.write("Link: " + str(link.encode('utf-8')) + "\n\n")
    currentFile.write("Title: " + str(title.encode('utf-8')) + "\n")
    currentFile.write("Date Posted: " + str(publishDate.encode('utf-8')) + "\n")

    currentFile.write("Content: " + "\n")
    currentFile.write("\t" + str(postSoup.find("h1", class_="schema_title").contents[0].encode('utf-8')) + "\n")
    currentFile.write("\t" + str(postSoup.find("h2", class_="schema_hiringorganization").contents[0].encode('utf-8')) + "\n")

    scHeadings = postSoup.find_all("div", class_="scheading")

    # Begin scHeader output
    for j in range(0, len(scHeadings)):

        currentFile.write( "\t" + str(scHeadings[j].contents[0].encode('utf-8')))
        # Because the last shHeading contains a span within a link, it is considered to be a 
        # special case.
        if j == (len(scHeadings) - 1):
            currentFile.write(str(scHeadings[j].contents[1].contents[0].contents[0].encode('utf-8')) + "\n")
        else:
            currentFile.write(str(scHeadings[j].contents[1].contents[0].encode('utf-8')) + "\n")


    scourHeadings = postSoup.find_all("div", class_="scourheading")

    for j in range(0, len(scourHeadings)):
        # Replacing <br /> with newlines.
        replacedHTML = scourHeadings[j].contents[1]

        for br in replacedHTML.find_all('br'):
            br.replace_with("\n")

        currentFile.write("\t" + str(scourHeadings[j].contents[0].encode('utf-8')) + str(replacedHTML.get_text().encode('utf-8')) + "\n")
# End of WriteToFile

todayDate = date.today()
currentDate = todayDate.strftime('%d%B%y')

yesterday = date.today() - timedelta(days=1)
yesterdayDate = yesterday.strftime('%d%B%y')

currentFile = open(str(currentDate) + '_sarkari-naukri.txt', 'w')
yesterdayFile = None

try:
   yesterdayFile = open(yesterdayDate + '_sarkari-naukri.txt', 'ab+')
except IOError:
   print 'Yesterday\'s file not found, using today only'

# HTML source for homepage.
homePage = urllib2.urlopen('http://www.sarkari-naukri.in/').read()
homePageSoup = BeautifulSoup(homePage)

# Traverse to entry-title h2 which contains link to post.
postsLinkContainer = homePageSoup.find_all("h2", class_="entry-title")

numberOfCollectedPosts = 15

# Iterate through list of post links, scraping information into file as needed. Use of encode() to 
# minimize errors when printing characters.
for i in range(0, numberOfCollectedPosts):
    linkTag = postsLinkContainer[i].a
    link = linkTag['href']
    
    title = linkTag.contents[0]
    
    publishDate = postsLinkContainer[i].find_next_sibling("abbr").contents[0]
    publishDateFormatted = time.strftime('%d%B%y', time.strptime(publishDate, '%B %d, %Y'))    

    postMatchFound = False

    postPage = urllib2.urlopen(link).read()
    postSoup = BeautifulSoup(postPage)

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
            WriteToFile(yesterdayFile, link, title, publishDate, postSoup)

    else:
        WriteToFile(currentFile, link, title, publishDate, postSoup)

currentFile.close()
yesterdayFile.close()
