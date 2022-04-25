from config import bs4, url, logging, requests, driver, WebDriverWait, EC, By
import glob
import os
import pandas as pd
from time import strftime
import re





def getPageSource(in_URL):
    '''
    Navigate to desired URL then return page source
    '''
    try:
        logging.info('Navigate to desired '+in_URL)
        print('Navigate to desired '+in_URL)
        driver.get(in_URL)
        logging.info('navigated to URL')
        return driver.page_source
    except:
        try:
            logging.info('Navigate to desired '+in_URL)
            print('Navigate to desired '+in_URL)
            driver.get(in_URL)
            logging.info('navigated to URL')
            return driver.page_source
        except:
            logging.info('Navigate to desired '+in_URL)
            print('Navigate to desired '+in_URL)
            driver.get(in_URL)
            logging.info('navigated to URL')
            return driver.page_source




def GetScholarshipInfo(URL):
    logging.info('get Scholarship needed information')
    content = getPageSource(URL)
    soup = bs4.BeautifulSoup(content,'html.parser')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[@class='Name']")))
    universityName = soup.find("a", {"class": "Name"}).getText().strip()
    checkFeautred = soup.findAll("a", {"class": 'StudyLink TrackingExternalLink ProgrammeWebsiteLink'})
    if checkFeautred:
        feautredBy = checkFeautred[0].getText().strip()
        feautredByLink = soup.find("a", {"class": 'StudyLink TrackingExternalLink ProgrammeWebsiteLink'}).get('href')
    else:
        feautredBy = None
        feautredByLink = None
    logging.info('Scholarship needed information got')
    return universityName, feautredBy, feautredByLink



def scrapeScholars():
    '''
    open URL, scrape the website, add data to the dictionary of needed data then go to next page and so on.
    '''
    
    logging.info('scraping scholarships...')
    sch = dict()
    
    pageNumber = 0
    while(pageNumber <= 9990):
        content = getPageSource(url+str(pageNumber))
        soup = bs4.BeautifulSoup(content,'html.parser') #
        regex = re.compile('.*ClickThrough premium js-Study StudyCard') # get class regex
        scholarships = soup.findAll("a", {"class": regex})
        for scholarship in scholarships:
            feautred = scholarship.findAll("div", {"class": "Promoted js-Promoted"})
            # universityName = (scholarship.findAll("span", {"class": "Fact LocationFact"})[0]).getText().strip() not sch.get(universityName.strip())
            if feautred:
                universityLocation = (scholarship.findAll("span", {"class": "Fact LocationFact"})[1]).getText().strip()
                name = (scholarship.find("div")).get('data-description') #scholarship name
                link = scholarship.get('href')
                universityName, feautredBy, feautredByLink = GetScholarshipInfo(link)
                if feautredBy:
                    logging.info(universityName + ' with link '+link+' will be added to the sheet')
                    Duration = (scholarship.find("span", {"class": "js-duration Fact KeyFact"})).getText().strip()
                    fees = (scholarship.find("span", {"class": "Fact KeyFact"})).getText().strip()
                    description = (scholarship.find("p", {"class": "Description"})).getText().strip()
                    sch.setdefault(universityName.strip(), [universityLocation, name, link, feautredBy, feautredByLink, Duration, fees, description])
                else:
                    logging.info(universityName + ' with link '+link+' will not be added to the sheet')
            
        pageNumber = pageNumber + 10

    logging.info('scholarships scraped successfully')
    return sch



def writeRange(scholarships, excel_file_name=None):
    '''
    save data to excel file
    '''
    logging.info('write data to excel file')
    universityName = list(scholarships.keys())
    universityLocation = list(list(zip(*scholarships.values()))[0])
    name = list(list(zip(*scholarships.values()))[1])
    link = list(list(zip(*scholarships.values()))[2])
    feautredBy = list(list(zip(*scholarships.values()))[3])
    feautredByLink = list(list(zip(*scholarships.values()))[4])
    Duration = list(list(zip(*scholarships.values()))[5])
    fees = list(list(zip(*scholarships.values()))[6])
    description = list(list(zip(*scholarships.values()))[7])
    scholarsExcel = pd.DataFrame(list(zip(universityName, universityLocation, name, 
                                   link, feautredBy, feautredByLink, Duration, fees, description)),
                                  columns= ['University Name', 'University Location', 
                                            'Name', 'Link', 'Feautred By', 'Feautred By Link', 'Duration', 'Fees', 'Description']
                                  )
    # scholarsExcel = pd.DataFrame(list(zip(universityName, universityLocation, name, 
    #                                link, officialLink, Duration, fees, description)),
    #                               columns= ['University Name', 'University Location', 
    #                                         'Name', 'Link', 'Official Link', 'Duration', 'Fees', 'Description']
    #                               )
    if not excel_file_name:
        excel_file_name = strftime("%a-%d-%m-%H-%M")+'.xlsx'
    scholarsExcel.to_excel(excel_file_name, index=False, encoding='utf-8')
    logging.info('data written to excel file')



def getNewScholars(oldNames, scholarships):
    '''
    compare two lists then save excel file with new data
    '''
    logging.info('get new scholarships')
    newScholars = dict()
    currentNames = list(scholarships.keys())
    newNames = [i for i in currentNames if i not in oldNames and i]
    if newNames:
        for name in newNames:
            if name.strip():
                newScholars.setdefault(name, scholarships[name])
    
        writeRange(newScholars, strftime("%a-%d-%m")+'new.xlsx')
        logging.info('new scholarships successfully got')


def getdeletedScholars(oldNames, oldScholars, currentNames):
    '''
    compare two lists then save excel file with deleted data
    '''
    logging.info('get deleted scholarships')
    deletedScholars = dict()
    delNames = [i for i in oldNames if i not in currentNames and i]
    if delNames:
        for name in delNames:
            if name.strip():
                deletedScholars.setdefault(name, oldScholars[name])
    
        writeRange(deletedScholars, strftime("%a-%d-%m")+'del.xlsx')
        logging.info('deleted scholarships successfully got')


def saveScholars(scholars):
    '''
    1.get last excel files and read name column from it
    2.get new scholarships
    3.get deleted scholarships
    4.get All scholarships
    '''
    # 1.get last excel files and read name column from it
    excelFiles = glob.glob('*.xlsx')
    if excelFiles:
        '''
        only in case there is an old file(not first run)
        '''
        oldScholars = dict()
        excelFiles.sort(key=lambda f: os.path.getctime(f)) # arrange them by last modified date (accending)
        recentExcel = excelFiles[len(excelFiles)-1] # last excel file
        lastData = pd.read_excel(recentExcel) # get last data from last excel shhet
        lastuniversityName = list(lastData['University Name']) # get name column

        #2.get new scholarships
        getNewScholars(lastuniversityName, scholars)
        #3.get deleted scholarships
        universityLocation = list(lastData['University Location'])
        name = list(lastData['Name'])
        link = list(lastData['Link'])
        feautredBy = list(lastData['Feautred By'])
        feautredByLink = link = list(lastData['Feautred By Link'])
        Duration = list(lastData['Duration'])
        fees = list(lastData['Fees'])
        description = list(lastData['Description'])
        # create dictionary of old values
        for i in range(len(lastuniversityName)):
            oldScholars.setdefault(lastuniversityName[i], [universityLocation[i], name[i], link[i], feautredBy, 
                                                            feautredByLink, Duration[i], fees[i], description[i]])
        newuniversityName = list(scholars.keys())
        getdeletedScholars(lastuniversityName, oldScholars, newuniversityName)
        #4.get All scholarships
        writeRange(scholars)
    else:
        '''
        only in case there is no old file(first run)
        '''
        #4.get All scholarships
        writeRange(scholars)