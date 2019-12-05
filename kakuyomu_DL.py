#coding:utf-8
import requests
import copy
import pathlib


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
            tmp_title = tmp[1].split("</p>")
            title = tmp_title[0]
            data = string.split("<p id=\"p")
            data.pop(0)
            for str_data in data:
                s = str_data.split("\">")
                t = s[1].split("</p>")

                #テキストファイルにするとき削除する文字列
                t[0] = t[0].replace("<br />","\n")
                t[0] = t[0].replace("<em class=\"emphasisDots","")
                t[0] = t[0].replace("<span>","")
                t[0] = t[0].replace("</span>","")
                t[0] = t[0].replace("</em>","")
                t[0] = t[0].replace("<ruby><rb>","")
                t[0] = t[0].replace("</rb><rp>","")
                t[0] = t[0].replace("</rp><rt>","")
                t[0] = t[0].replace("</rt><rp>","")
                t[0] = t[0].replace("</rp></ruby>","")
                text.append(t[0])
            result_text = copy.deepcopy("\n".join(text))
            result_text = result_text.replace("\u3000","")
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