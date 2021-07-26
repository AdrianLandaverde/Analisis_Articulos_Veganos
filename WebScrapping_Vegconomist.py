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
    
def fixDate(dataframe):
    dataframe["Date"]=pd.to_datetime(dataframe["Date"])
    dataframe["Date"]= dataframe["Date"].apply(lambda x: x.strftime('%m/%d/%Y'))
    return(dataframe)

def writeCSV(dataframe):
    dataframe.to_csv('articles_Vegconomist.csv',index=False, encoding="utf-8-sig")
    
def srcapAll():
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
    df_Articles= fixDate(df_Articles)
    writeCSV(df_Articles)
    
    
def lastArticleReached(dataframe, lastLink):
    df_link=dataframe.loc[dataframe["Link"]==lastLink]
    if(len(df_link)!=0):
        return([True,list(df_link.index)[0]])
    else:
        return([False])
    
        
def updateArticles(): 
    df_OldArticles= pd.read_csv("articles_Vegconomist.csv")
    lastLink= df_OldArticles.iloc[0]["Link"]
    PATH= "C:\Program Files (x86)\chromedriver.exe"
    driver= webdriver.Chrome(PATH)
    newsPage="https://vegconomist.com/all-news/"
    
    driver.get(newsPage)
    
    df_NewArticles= pd.DataFrame(columns=["Title","Link","Date","Text"])
    page=1
    startTime= datetime.datetime.now()
    while True:
        time.sleep(3)
        df_NewArticles= loopArticles(driver, df_NewArticles)
        showProgress(startTime, page, df_NewArticles)
        checkLink= lastArticleReached(df_NewArticles, lastLink)
        if(checkLink[0]==True):
            nLink= checkLink[1]
            if(nLink==0):
                print("-----------------------------------")
                print("There aren't new articles")
                print("-----------------------------------")
                df_NewArticles= df_NewArticles.iloc[0:0]
                df_Articles= df_OldArticles
            else:
                df_NewArticles= df_NewArticles.iloc[:nLink]
                df_NewArticles= fixDate(df_NewArticles)
                df_Articles= pd.concat(df_NewArticles,df_OldArticles)
                print("-----------------------------------")
                print("Articles uptaded")
                writeCSV(df_Articles)
                print("CSV file updated")
                print("-----------------------------------")
            break
        else:
            nextPage(driver)
            page+=1




    

            