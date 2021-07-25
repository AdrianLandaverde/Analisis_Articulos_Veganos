from selenium import webdriver
import time
import datetime
import pandas as pd

def openArticle(driver,i, dataframe):
    link= i.find_element_by_tag_name("a").get_attribute('href')
    driver.execute_script("window.open('');") 
    driver.switch_to.window(driver.window_handles[1]) 
    driver.get(link)
    time.sleep(3)
    
def closeArticle(driver):
    driver.close() 
    driver.switch_to.window(driver.window_handles[0])
    
def scrapArticle(driver):
    content= driver.find_element_by_class_name("entry-content")
    paragraphs= content.find_elements_by_tag_name("p")
    if(len(paragraphs)>3):   
        try:
            title= driver.find_element_by_class_name("entry-title.entry-title--with-subtitle").text
        except:
            title= driver.find_element_by_class_name("entry-title").text
        date= driver.find_element_by_class_name("entry-date.published").get_attribute("datetime")
        link= driver.current_url
        text=""
        for i in paragraphs:
            text= text + i.text + " "
        article=[title,link,date,text]
    else:
        article=[]
    return(article)
            
def loopArticles(driver,dataframe):
    articles= driver.find_elements_by_class_name("entry-title")
    for i in articles:
        try:
            openArticle(driver, i, dataframe)
        except:
            openArticle(driver, i, dataframe)
        try:
            article= scrapArticle(driver)
        except:
            driver.navigate().refresh();
            article= scrapArticle(driver)
        if(len(article)!=0):
            dataframe= dataframe.append({"Title":article[0],"Link":article[1],"Date":article[2],
                                         "Text":article[3]},ignore_index=True)
        closeArticle(driver)
    return(dataframe)
        
def nextPage(driver):
    nextPage= driver.find_element_by_class_name("next.page-numbers")
    nextPage.click()
    
def showProgress(startTime, page, dataframe):
    print(" ")
    print("-----------------------------------")
    timeElapsed= (datetime.datetime.now())-startTime
    print("Pages Completed: " + str(page))
    print("Time elapsed: " +str(timeElapsed))
    print("Number of articles: " + str(len(dataframe)))
    print("Last Article: " + dataframe.iloc[len(dataframe)-1]["Title"])
    print("-----------------------------------")
    
def writeCSV(dataframe):
    dataframe["Date"]= pd.to_datetime(dataframe["Date"],format="%Y-%m-%dT%H:%M")
    dataframe["Date"]= dataframe["Date"].apply(lambda x: x.strftime('%m/%d/%Y'))
    dataframe.to_csv('articles_PlantBasedNews.csv',index=False, encoding="utf-8-sig")
    
def scrapAll():
    PATH= "C:\Program Files (x86)\chromedriver.exe"
    driver= webdriver.Chrome(PATH)
    newsPage="https://plantbasednews.org/all/page/777/"
    
    driver.get(newsPage)
    
    df_Articles= pd.DataFrame(columns=["Title","Link","Date","Text"])
    page=777
    startTime= datetime.datetime.now()
    while True:
        time.sleep(3)
        df_Articles= loopArticles(driver, df_Articles)
        showProgress(startTime, page, df_Articles)
        try:
            nextPage(driver)
            page+=1
        except:
            break
    writeCSV(df_Articles)
            