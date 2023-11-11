from mediaDB.extension.Parsers.tv import ParserTV
import re

def main():

    print(ParserTV("Tsundere-Raws").getTVAttribute("Butareba -The Story of a Man Who Turned into a Pig- S01E06 VOSTFR 720p WEB x264 AAC -Tsundere-Raws (CR) (Buta no Liver wa Kanetsu Shiro)", is_batch=True))
    js = {
        "pattern_episode": "^(?P<title>.+?)\.S(?P<season>\d{1,2})E(?P<episode>\d{1,4})",
        "pattern_batch": "^(?P<title>.+?)\.S(?P<season>\d{1,2})" 
    }