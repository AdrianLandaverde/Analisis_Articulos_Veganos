from selenium import webdriver
import time
import datetime
import pandas as pd

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
    
def scrapArticle(driver):
    title= driver.find_element_by_class_name("post-title").text
    date= driver.find_element_by_class_name("post-date").text
    link= driver.current_url
    content= driver.find_element_by_class_name("post-content")
    paragraphs= content.find_elements_by_tag_name("p")
    text=""
    for i in paragraphs:
        text= text + i.text + " "
    article=[title,link,date,text]
    return(article)
            
def loopArticles(driver,dataframe):
    while True:
        articles= driver.find_elements_by_class_name("archive-post-permalink")
        if(len(articles)!=0):
            break
        else:
            print(" ")
            print("-----------------------------------")
            print("Error while opening page")
            print("Trying to refresh page")
            print("-----------------------------------")
            driver.refresh()
            time.sleep(10)            
    for i in articles:
        while True:
            try:
                openArticle(driver, i)
                break
            except:
                print(" ")
                print("-----------------------------------")
                print("Error while opening article")
                print("Trying to open article again")
                print("-----------------------------------")
                driver.close() 
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(10)
        while True:
            try:
                article= scrapArticle(driver)
                break
            except:
                print(" ")
                print("-----------------------------------")
                print("Error while scrapping article")
                print("Trying to refresh article")
                print("-----------------------------------")
                driver.refresh()
                time.sleep(10)
        dataframe= dataframe.append({"Title":article[0],"Link":article[1],"Date":article[2]
                                     ,"Text":article[3]},ignore_index=True)
        print(" ")
        print("-----------------------------------")
        print("Article: " + article[0])
        print("-----------------------------------")
        closeArticle(driver)
    return(dataframe)
        
def nextPage(driver):
    nextPage= driver.find_element_by_class_name("next.page-numbers")
    driver.get(nextPage.get_attribute('href'))
    
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
newsPage="https://vegconomist.com/all-news/"

driver.get(newsPage)

df_Articles= pd.DataFrame(columns=["Title","Link","Date","Text"])
page=1
startTime= datetime.datetime.now()
while True:
    time.sleep(3)
    df_Articles= loopArticles(driver, df_Articles)
    showProgress(startTime, page, df_Articles)
    try:
        nextPage(driver)
        page+=1
    except:
        print(" ")
        print("-----------------------------------")
        print("Last Page Readed")
        print("Pages Readed:" + str(page))
        print("Time Elapsed: " + str((datetime.datetime.now())-startTime))
        print("-----------------------------------")
        break
            