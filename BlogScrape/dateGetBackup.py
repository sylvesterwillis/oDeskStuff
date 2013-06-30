import time

if len(sys.argv) == 1:
    print "No date entered, using today's date only."
else:
    # Check for input arguments of dd-mm-yyyy format to be used in parsing.
    dateMatch = re.search(r'\d{2}-\d{2}-\d{4}', sys.argv[1])

    if dateMatch != None:
        try:
            pastDate = time.strptime(dateMatch.group(), '%d-%m-%Y')
            parsedTime = time.strftime('%d%B%y', pastDate)
        except ValueError:
            print "Date entered is not valid."
