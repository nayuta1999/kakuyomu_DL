#coding:utf-8
import requests
import copy
import pathlib
import re


class kakuyomu_DL():
    url = ""
    def __init__(self,url):
        self.url = url

    def getURL(self):
        return self.url

    def getContents(self):
        response = requests.get(self.url)
        if(response.status_code != requests.codes.ok):
            print("無効なURLです")
            quit()
        return response.text

    def getTitle(self):
        text = self.getContents()
        tmp = text.split("<title>")
        tmp = tmp[1].split("</title>")
        return tmp[0]

    def host_url(self):
        url = self.url
        tmp = url.split("https://kakuyomu.jp/")
        url = tmp[1]
        return url

    def scraiping_url(self):
        result_url = []
        text = self.getContents()
        result = text.split(self.host_url()+"/episodes/")
        for i in range(1,len(result)):
            tmp_url = result[i].split("\"")
            result_url.append(tmp_url[0])
        result_url.pop(0)
        return result_url

    def save_Contents(self):
        result = []
        number = self.scraiping_url()
        for i in number:
            response = requests.get(self.url+"/episodes/"+i)
            result.append(response.text)
        return result

    def scraiping_Contents(self):

        response = self.save_Contents()
        text = []
        text_data = []

        for string in response:
            
            tmp = string.split("<p class=\"widget-episodeTitle js-vertical-composition-item\">")
            column = 0

            tmp_title = tmp[1].split("</p>")
            title = tmp_title[0]
            
            data = re.split("(<p id=\"p\d*\">)",string)
            data.pop(0)

            for str in data:

                if(column % 2 == 1):

                    s = str.split("</div>")
                    replace_text = s[0]

                    #ルビ用の置き換え
                    replace_text = replace_text.replace("<ruby><rb>","")
                    replace_text = replace_text.replace("</rb><rp>","")
                    replace_text = replace_text.replace("</rp><rt>","")
                    replace_text = replace_text.replace("</rt><rp>","")
                    replace_text = replace_text.replace("</rp></ruby>","")

                    #傍点用の置き換え
                    replace_text = replace_text.replace("<em class=\"emphasisDots\">","")
                    replace_text = replace_text.replace("<span>","")
                    replace_text = replace_text.replace("</span>","")
                    replace_text = replace_text.replace("</em>","")
                    
                    #改行用の置き換え
                    replace_text = replace_text.replace("</p>","")
                    replace_text = replace_text.replace("<br />","")
                    replace_text = re.sub("(<p id=\"p\d*\" class=\"blank\">)","",replace_text)
                    
                    text.append(replace_text)

                column+=1
                
            column = 0
            result_text = copy.deepcopy(" ".join(text))
            #いるかどうかわからんから現状コメントアウト中
            #result_text = result_text.replace("\u3000","")            
            text_data.append({title:result_text})
            text = []
            
        return text_data

    def save_text(self):
        text = self.scraiping_Contents()
        book = self.getTitle()
        p = pathlib.Path("./kakuyomu/"+book)
        if(p.exists() == False):
            p.mkdir(parents=True)
        for i in text:
            for title in i.keys():
                with open("./kakuyomu/"+book+"/"+title+".txt",'w') as f:
                    f.write(i[title])