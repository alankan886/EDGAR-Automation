import time
import xml.etree.ElementTree as ET
import functions
import sys
import os

if __name__ == '__main__':

    # Going try to install the modules for the user
    try:
        functions.install('selenium')
        functions.install('BeautifulSoup4')
        functions.install('urllib3')
    except:
        print("Oops, sorry you might have to pip install manually")

    print('\n')


    while 1:
        print("Enter exit to leave...\n")

        cik = input("Please Enter the CIK #: ")


        if cik.lower() == 'exit':
            sys.exit()

        # Prevents invalid input
        try:
            # If input isn't a combination of numbers
            int(cik)
            err = False
        except:
            # Clear the input buffer, so if the previous try is invalid, it doesn't carry over.
            os.system('clear')

            print("Your CIK # is invalid")
            err = True

        # If length of cik is invalid or input isn't numbers, make sure no extra space.
        if len(cik) != 10 or err is True:
            print("CIK # should contain 10 digits \n")

        else:
            break



    while 1:
        ith = input("Please enter the i-th most recent report you want to review, i: ")

        if ith.lower() == 'exit':
            sys.exit()

        # I can only get to 1st to 40th reports right now.


        try:
            int(ith)
            err = False
        except:
            # Clear the input buffer, so if the previous try is invalid, it doesn't carry over.
            os.system('clear')

            print("Invalid input.")
            err = True

        if int(ith) > 40:
            print("Currently don't support i > 40")
            err = True

        if err == False and int(ith) > 0:
            break



    # Callig loadPage with Selenium from functions.py
    driver, compName, filing = functions.load13FRes(cik)



    # Wait for the page to load
    time.sleep(3)


    # Get the URL of the current page
    url = driver.current_url

    # Get the page source AKA html format
    data = driver.page_source

    # The rock is coooooooooooking
    res, links = functions.cookTheSoup(data)

    # We go for the first link since that's the most updated one
    functions.loadDoc(links[0], driver)

    #This time out is a MUST, else xmlUrl would load the previous page url
    time.sleep(3)

    # Since the page is at the xml page now, we get the current url.
    try:
        xmlUrl = functions.loadXml(driver)
    except:
        print("Company document doesn't not contain a information table.")
        driver.quit()
        sys.exit()

    # We read the content on the xml page given the url
    content = functions.readXml(xmlUrl)

    # Creat ElementTree
    root = ET.fromstring(content)

    time.sleep(3)

    # idx is a list that has all the index of previous reports dates in res.
    idx = [i for i in range(2,len(res), 3)]

    # Writing up the file name here. The value for ith is being used here.
    fileName = compName + '--' + filing + '--' + res[idx[int(ith)-1]] + '.txt'
    fNameLs = [compName, filing, res[idx[int(ith)-1]]]

    # Write the tsv file.
    functions.writeTsv(fileName, fNameLs, root)

    # Closer the webpage when finished.
    driver.quit()
