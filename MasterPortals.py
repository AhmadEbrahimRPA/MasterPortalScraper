'''
Navigate to URL
scrape data
save table to CSV file
'''

import time
start_time = time.time()

from config import logging, endPopUp, driver
from components import scrapeScholars, saveScholars
import traceback
from tkinter import Tk

try:
    # scrape data
    logging.info('Start Process')
    scholars = scrapeScholars()
    logging.info('total number of scholarships is' + str(len(scholars.keys())))
    #save data
    saveScholars(scholars)
    # get excution time
    execution_Time = time.time() - start_time
    logging.info("--- "+str(int(execution_Time/60))+" Minutes ---")
    driver.close()
    # end notification popup
    root = Tk()
    app = endPopUp(root, len(scholars.keys()))
    root.mainloop()
    logging.info('Process End')
except Exception as error:
    logging.error(traceback.format_exc())
    driver.close()
    logging.info('Excution couldn\'t be finished properly')