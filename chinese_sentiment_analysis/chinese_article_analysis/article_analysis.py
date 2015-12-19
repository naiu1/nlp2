#!/usr/bin/python
#encoding=utf-8

import sys
sys.path.append("../chinese_participation")
sys.path.append("../dut_lib/")
sys.path.append("../algorithms/")
from jieba_participator import JiebaParticipator
from dut_extractor import DutExtractor
from dut_extractor_factory import DutExtractorFactory
from bsa_algorithm import BsaAlgorithm

class ArticleAnalysis(object):
    setence_separator_set = set(["。", "？", "！"])
    @staticmethod
    def get_segment_list_from_input_file(file_path):
        input_file = file(file_path, "r")
        segment_list = list()
        segment_partition_list = list()
        line = input_file.readline()
        while line:
            segment_list.append(line.strip())
            line = input_file.readline()
        input_file.close()
        return segment_list

    @staticmethod
    def get_segment_list(input_string):
        segment_list = input_string.split("\n")
        return segment_list

    @staticmethod
    def partition(segment_list):
        segment_partition_list = list()
        for seg in segment_list:
             partition_list = JiebaParticipator.participate(seg)
             segment_partition_list.append(partition_list)
        return segment_partition_list

    @staticmethod
    def semantic_analysis(segment_partition_list, library, algorithm):
        segment_semantic_result = list()
        if library == "dut":
            article_semantic_result = ArticleAnalysis.dut_semantic_analysis(segment_partition_list)
        if algorithm == "bsa_algorithm":
            article_semantic_value = ArticleAnalysis.bsa_algorithm_cal(article_semantic_result)
        return article_semantic_value

    @staticmethod
    def dut_semantic_analysis(segment_partition_list):
        dut_extractor = DutExtractorFactory.get_dut_extractor("../dut_lib/dut_sentiment_words.csv")
        total_semantic_value = 0
        article_semantic_result = list()
        for segment in segment_partition_list:
            input_setence_list = list()
            setence = list()
            for word in segment:
                word = word.encode("UTF-8").strip()
                setence.append(word)
                if word in ArticleAnalysis.setence_separator_set:
                    input_setence_list.append(setence)
                    setence = list()
            if len(setence) != 0:
                input_setence_list.append(setence)
            segment_semantic_result = list()
            for setence in input_setence_list:
                result = dut_extractor.get_word_semantic(setence)
                segment_semantic_result.append(result)
            article_semantic_result.append(segment_semantic_result)
        return article_semantic_result

    @staticmethod
    def bsa_algorithm_cal(article_semantic_result):
        bsa_algorithm = BsaAlgorithm("../common_lib/negative_words.txt")
        article_semantic_result = bsa_algorithm.cal_semantic_value(article_semantic_result)
        return article_semantic_result

#    @staticmethod
#    def dut_semantic_analysis(segment_partition_list):
#        dut_extractor = DutExtractorFactory.get_dut_extractor("../dut_lib/dut_sentiment_words.csv", "../common_lib/negative_words.txt")
#        total_semantic_value = 0
#        article_semantic_result = list()
#        for segment in segment_partition_list:
#            input_setence_list = list()
#            setence = list()
#            for word in segment:
#                word = word.encode("UTF-8").strip()
#                setence.append(word)
#                if word in ArticleAnalysis.setence_separator_set:
#                    input_setence_list.append(setence)
#                    setence = list()
#            if len(setence) != 0:
#                input_setence_list.append(setence)
#            segment_semantic_result = list()
#            for setence in input_setence_list:
#                result = dut_extractor.get_word_semantic(setence)
#                segment_semantic_result.append(result)
#            article_semantic_result.append(segment_semantic_result)
#        segment_value_list = list()
#        for seg_result in article_semantic_result:
#             seg_value = list()
#             for setence_result in seg_result:
#                 setence_value = 0
#                 for word_result in setence_result:
#                     if word_result.has_key("meaning") is False:
#                         continue
#                     value = int(word_result["semantic_strength"])
#                     if word_result["semantic_polagiry"] == "2":
#                         value = value * (-1)
#                     setence_value += value
#                 seg_value.append(setence_value)
#             segment_value_list.append(seg_value)
#        segment_value = list()
#        for item in segment_value_list:
#            sum = 0
#            counter = 0
#            for value in item:
#                sum += value
#                counter += 1
#            if counter == 0:
#                average = 0
#            else:
#                average = sum /counter
#            segment_value.append(average)
#        article_sum = 0
#        seg_counter = 0
#        for seg in segment_value:
#            article_sum += seg
#            seg_counter += 1
#        if seg_counter == 0:
#            article_average = 0
#        else:
#            article_average = float(article_sum) / seg_counter
#        return article_average

    @staticmethod
    def file_semantic_analysis(file_path, library, algorithm):
        segment_list = ArticleAnalysis.get_segment_list_from_input_file(file_path)
        segment_partition_list = ArticleAnalysis.partition(segment_list)
        article_result = ArticleAnalysis.semantic_analysis(segment_partition_list, library, algorithm)
        return article_result

    @staticmethod
    def string_semantic_analysis(input_string, library, algorithm):
        segment_list = ArticleAnalysis.get_segment_list(input_string)
        segment_partition_list = ArticleAnalysis.partition(segment_list)
        article_result = ArticleAnalysis.semantic_analysis(segment_partition_list, library, algorithm)
        return article_result

if __name__ == '__main__':
    article_analysis = ArticleAnalysis()
    result = ArticleAnalysis.string_semantic_analysis("烛花这个电影不很恶心，让人讨厌\n我不讨厌这个电影\n不血腥，不恶心，吃不下饭去\n我不喜欢那种浪漫的电影\n", "dut", "bsa_algorithm")
    print "The semantic result:", result
