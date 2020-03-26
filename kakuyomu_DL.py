# coding:utf-8

import requests
import pathlib
import re
from bs4 import BeautifulSoup


class kakuyomu_DL():
    mainSoup = None

    # constructor : get mainpage html
    def __init__(self, url):
        res = requests.get(url)

        if res.status_code == requests.codes.ok:
            self.mainSoup = BeautifulSoup(res.text, "html.parser")

            if not self.isWorks_main():
                print("not works main page")
                quit()

            print("Title  : " + self.get_title())
            print("Author : " + self.get_author())

        else:
            print("not exist")
            quit()

    # Determine if it is the main page or not
    def isWorks_main(self):
        if self.mainSoup.find(attrs={"data-route": "public:works:work"}) is not None:
            return True
        else:
            return False

    # get novel title
    def get_title(self):
        return self.mainSoup.find("h1", id="workTitle").getText()

    # get novel author
    def get_author(self):
        return self.mainSoup.find("span", id="workAuthor-activityName").getText()

    # get episode link hrefs list
    def get_episodeLinks(self):
        episodes_hrefs = []
        links = [link for link in self.mainSoup.find_all(
            "a", {"class", "widget-toc-episode-episodeTitle"})]

        for href in links:
            episodes_hrefs.append("https://kakuyomu.jp" + href["href"])

        return episodes_hrefs

    def get_episode(self, link):
        contents_dict = {"chapter": "",
                         "section": "", "title": "", "episode": ""}
        soup = BeautifulSoup(requests.get(link).text, "html.parser")

        chapter = soup.find(
            "p", {"class", "chapterTitle level1 js-vertical-composition-item"})
        section = soup.find(
            "p", {"class", "chapterTitle level2 js-vertical-composition-item"})
        if chapter is not None:
            contents_dict["chapter"] = chapter.string
        if section is not None:
            contents_dict["section"] = section.string

        contents_dict["title"] = soup.find(
            "p", {"class", "widget-episodeTitle js-vertical-composition-item"}).string
        contents_dict["episode"] = "\n".join([str(html.text) for html in soup.find_all(
            "p", id=re.compile("\d+"))])

        return contents_dict

    # create a pdf file by creating and compiling a .tex file.

    def set_novel(self):
        default_pass = "./kakuyomu/" + self.get_title()
        links = self.get_episodeLinks()
        chapter = ""
        section = ""

        pathlib.Path(default_pass).mkdir(parents=True)
        with open(default_pass + "/" + "output.log", "w") as f:
            f.write("--- OUT PUT LOG ---\n")

        for link in links:
            episode_dict = self.get_episode(link)
            save_pass = default_pass

            if episode_dict["chapter"] != "":
                chapter = "/" + episode_dict["chapter"]
                section = ""
                print("chapter : " + episode_dict["chapter"])
                with open(default_pass + "/" + "output.log", "a") as f:
                    f.write("chapter : " + episode_dict["chapter"] + "\n")
            if episode_dict["section"] != "":
                section = "/" + episode_dict["section"]
                print("\tsection : " + episode_dict["section"])
                with open(default_pass + "/" + "output.log", "a") as f:
                    f.write("\tsection : " + episode_dict["section"] + "\n")

            save_pass += chapter + section
            path = pathlib.Path(save_pass)

            if not path.exists():
                path.mkdir(parents=True)

            with open(save_pass + "/" + episode_dict["title"] + ".txt", "w") as f:
                f.write(episode_dict["episode"])
                print("\t\tepisode saved : " + episode_dict["title"])
            with open(default_pass + "/" + "output.log", "a") as f:
                f.write("\t\tepisode saved : " + episode_dict["title"] + "\n")


if __name__ == "__main__":
    # """
    print("■■■■                                     ■                               ")
    print("■                          ■■           ■■                               ")
    print("■                          ■■           ■■■■■■    ■■■■■■■■        ■■     ")
    print("■            ■             ■■■■■■      ■■   ■            ■        ■      ")
    print("■            ■          ■■■■    ■     ■■    ■            ■        ■      ")
    print("■            ■             ■    ■    ■■    ■■            ■       ■■  ■   ")
    print("■            ■             ■   ■■          ■       ■■■■■■■       ■   ■   ")
    print("■            ■             ■   ■■         ■■             ■       ■    ■  ")
    print("■            ■            ■    ■■        ■■              ■      ■    ■■■ ")
    print("             ■           ■■    ■        ■■        ■■■■■■■■    ■■■■■■■■ ■■")
    print("             ■          ■■   ■■■       ■                                 ")
    print("          ■■■■                                         ")
    # """
    print("Enter the URL of the main page of the work posted on kakuyomu.")
    download_url = input()
    novelData = kakuyomu_DL(download_url)
    novelData.set_novel()
