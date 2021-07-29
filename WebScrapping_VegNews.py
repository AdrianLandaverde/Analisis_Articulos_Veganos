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

def loopPage(driver,dataframe,startTime):
    articles= driver.find_elements_by_class_name("story-card.story-card-white")
    for i in articles:
        while True:
            try:
                openArticle(driver,i)
                break
            except:
                print(" ")
                print("-----------------------------------")
                print("Error while oppening article")
                print("Trying to reopen article")
                print("-----------------------------------")
                closeArticle(driver)
        
        try:
            article= scrapArticle(driver, startTime)
        except:
            print(" ")
            print("-----------------------------------")
            print("Error while scrapping article")
            print("Trying to refresh article")
            print("-----------------------------------")
            driver.refresh()
            time.sleep(10)
            try:
                article= scrapArticle(driver, startTime)
            except:
                print(" ")
                print("-----------------------------------")
                print("Error while scrapping article again")
                print("article skipped")
                print("-----------------------------------")
                article=[]
                    
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

df_Articles= pd.DataFrame(columns=["Title","Link","Date","Text"])
page=412
startTime= datetime.datetime.now()

while True:
    newsPage="https://vegnews.com/news/page/" + str(page) 
    driver.get(newsPage)
    try:
        articles= driver.find_element_by_class_name("story-card.story-card-white")
    except:
        print(" ")
        print("-----------------------------------")
        timeElapsed= (datetime.datetime.now())-startTime
        print("Last Paged readed")
        print("Time elapsed: " +str(timeElapsed))
        print("Number of articles: " + str(len(df_Articles)))
        print("Last Article: " + df_Articles.iloc[len(df_Articles)-1]["Title"])
        print("-----------------------------------")
        break
    else:
        time.sleep(3)
        df_Articles= loopPage(driver, df_Articles, startTime)   
        showProgress(startTime, page, df_Articles)
        page+=1


    




