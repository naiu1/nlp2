#!/usr/bin/python
# coding: utf-8

import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("../")
from common import log_tool

logger = log_tool.Logging.get_logger()

class DutExtractor(object):
    def __init__(self):
        self.word_dict = dict()
        with open('dut_sentiment_words.csv','r') as f:
            reader = csv.reader(f)
            for item in reader:
                word = item[0].encode("UTF-8")
                other = item[1:10]
                self.word_dict[word] = other

    def get_word_meaning(self, word_list):
        print "想要表达的情感:"
        for word in word_list:
            if self.word_dict.has_key(word):
                meaning = self.word_dict[word]
                kind = meaning[3]
                sentiment_strength = meaning[4]
                sentiment_polarity = meaning[5]
                print self.get_kind_meaning(kind), "强烈程度:", sentiment_strength

    def get_kind_meaning(self, kind):
        if kind == "PA":
            return "快乐"
        if kind == "PE":
            return "安心"
        if kind == "PD":
            return "尊敬"
        if kind == "PH":
            return "赞扬"
        if kind == "PG":
            return "相信"
        if kind == "PB":
            return "喜爱"
        if kind == "PK":
            return "祝愿"
        if kind == "NA":
            return "愤怒"
        if kind == "NB":
            return "悲伤"
        if kind == "NJ":
            return "失望"
        if kind == "NH":
            return "内疚"
        if kind == "PF":
            return "思念"
        if kind == "NI":
            return "慌张"
        if kind == "NC":
            return "恐惧"
        if kind == "NG":
            return "羞愧"
        if kind == "NE":
            return "烦闷"
        if kind == "ND":
            return "憎恶"
        if kind == "NN":
            return "贬责"
        if kind == "NK":
            return "妒忌"
        if kind == "NL":
            return "怀疑"
        if kind == "PC":
            return "惊奇"

if __name__ == '__main__':
    logger.debug("a")
    dut_extractor = DutExtractor()
    word_list = list()
    final_word_list = list()
    sentence = sys.argv[1]
    length = len(sentence)
    bit_length = length / 3
    counter = 0
    while counter <= bit_length:
        word_list.append(str(sentence[(counter*3):(counter*3)+3]))
        if (counter + 1) * 3 < length:
            word_list.append(str(sentence[(counter*3):((counter+1)*3)+3]))
        if (counter + 2) * 3 < length:
            word_list.append(str(sentence[(counter*3):((counter+2)*3)+3]))
        if (counter + 3) * 3 < length:
            word_list.append(str(sentence[(counter*3):((counter+3)*3)+3]))
        counter += 1
    for item in word_list:
        item = item.encode("UTF-8")
        final_word_list.append(item)
    dut_extractor.get_word_meaning(final_word_list)
