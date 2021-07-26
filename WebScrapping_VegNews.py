from selenium import webdriver
import time
import datetime
import pandas as pd

def closeModalDialog(driver):
    modalContent= driver.find_element_by_class_name("modal-content")
    button= modalContent.find_element_by_class_name("close")
    button.click()
    print(" ")
    print("--------------------------------------------------")
    print("Modal dialog closed")
    print("--------------------------------------------------")

def loadMore(driver):
    loadMore= driver.find_element_by_class_name("btn.btn-primary.btn-outline")
    loadMore.click()

def openArticle(driver,article):
    link= article.get_attribute('href')
    driver.execute_script("window.open('');") 
    driver.switch_to.window(driver.window_handles[1]) 
    time.sleep(3)
    driver.get(link)
    time.sleep(3)

def closeArticle(driver):
    driver.close() 
    driver.switch_to.window(driver.window_handles[0])
    
def scrapArticle(driver, startTime):
    try:
        recipe= driver.find_element_by_class_name("recipe-meta")
        article=[]
    except:    
        title= driver.find_element_by_class_name("article-title").text
        date= driver.find_element_by_class_name("article-date").text
        link = driver.current_url
        content= driver.find_element_by_class_name("article-content.drop-cap")
        paragraphs= content.find_elements_by_tag_name("p")
        paragraphs= paragraphs[:-2]
        text=""
        for i in paragraphs:
            text= text + i.text + " "
        print(" ")
        print("--------------------------------------------------")
        print("Article " + title)
        print("Time Elapsed: " + str((datetime.datetime.now())-startTime))
        print("--------------------------------------------------")
        article=[title,link,date,text]
    return(article)
    

def loopSection(driver, section, dataframe, startTime):
    articles= section.find_elements_by_class_name("story-card  ")
    for i in articles:
        openArticle(driver, i)
        while True:
            try:
                article= scrapArticle(driver, startTime)
                break
            except:
                print(" ")
                print("-----------------------------------")
                print("Error while scrapping article")
                print("Trying to refresh article")
                print("-----------------------------------")
                driver.refresh()
                time.sleep(10)
        if(len(article)!=0):
            dataframe= dataframe.append({"Title":article[0],"Link":article[1],"Date":article[2]
                                         ,"Text":article[3]},ignore_index=True)
        closeArticle(driver)
    return(dataframe)        

def showProgress(startTime, page, dataframe):
    print(" ")
    print("-----------------------------------")
    timeElapsed= (datetime.datetime.now())-startTime
    print("Pages Completed: " + str(page))
    print("Time elapsed: " +str(timeElapsed))
    print("Number of articles: " + str(len(dataframe)))
    print("Last Article: " + dataframe.iloc[len(dataframe)-1]["Title"])
    print("-----------------------------------")

PATH= "C:\Program Files (x86)\chromedriver.exe"
driver= webdriver.Chrome(PATH)
newsPage="https://vegnews.com/news" 

driver.get(newsPage)

df_Articles= pd.DataFrame(columns=["Title","Link","Date","Text"])
page=1
startTime= datetime.datetime.now()

time.sleep(3)
loadMore(driver)

initialSections= driver.find_elements_by_class_name("story-cards-container")
section=1
for i in initialSections:
    df_Articles= loopSection(driver, i,df_Articles, startTime)
    print(" ")
    print("--------------------------------------------------")
    print("Initial Section " + str(section)+ " completed")
    print("Time Elapsed: " + str((datetime.datetime.now())-startTime))
    print("--------------------------------------------------")
    section+=1
    try:
        closeModalDialog(driver)
    except:
        pass
    
page=1
while True:
    loadMore(driver)
    time.sleep(5)
    page+=1
    print(" ")
    print("--------------------------------------------------")
    print("Page " + str(page)+ " loaded")
    print("Time Elapsed: " + str((datetime.datetime.now())-startTime))
    print("--------------------------------------------------")
    section= (driver.find_elements_by_class_name("story-cards-container"))[-1]
    df_Articles= loopSection(driver, section, df_Articles, startTime)
    showProgress(startTime, page, df_Articles)
    




