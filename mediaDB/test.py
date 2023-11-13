from mediaDB.extension.Parsers.tv import ParserVideo
import re

def main():
    t_name = "T3KASHi"

    dic = {
     "patterns": {
          "episode": [
               "^(?P<title>.+?)[\\. _]S(?P<season>\\d{1,2})E(?P<episode>\\d{1,4})"
          ],
          "batch": [
               "^(?P<title>.+?)[\\. _]S(?P<season>\\d{1,2})(?!(\\d{1,2})?E\\d{1,4})",
               "(?i)^(?P<title>.*?)\.((S\d{1,2}E\d{1,4})|(S\d{1,2})|(MULTI|SUBFRENCH|CUSTOM|UNCENSORED|REMASTERED))"
          ],
          "movie": []
                }
        }
    ep= "Kill.la.Kill.MULTi.1080p.BluRay.x264-T3KASHi"
    ep="Code.Geass.Lelouch.of.the.Rebellion.S01.FRENCH.720p.BluRay.x264-T3KASHi"
    '^(?i)(?P<title>.*?)\.(MULTI|SUBFRENCH|CUSTOM|UNCENSORED|REMASTERED).+?'
    # print(re.match(r'(?i)^(?P<title>.*?)\.((S\d{1,2}E\d{1,4})|(S\d{1,2})|(MULTI|SUBFRENCH|CUSTOM|UNCENSORED|REMASTERED))', ep).groupdict())
    # ParserVideo(t_name).addSource(dic["patterns"]["episode"],dic["patterns"]["batch"],dic["patterns"]["movie"])
    print(ParserVideo(t_name).getTVAttribute(ep, is_batch=True))

    # with open("/home/strange/dev/mediaDB/mediaDB/exemples/tsundere-raws-test-shows", "r", encoding="utf-8") as f:
    #     for ep in f:
    #         print(ep)
    #         print(ParserVideo(t_name).getTVAttribute(ep, is_batch=True))
    
    # ParserTV("T3KASHi").addSource(js["patterns"]["episode"], js["patterns"]["batch"], js["patterns"]["movie"])