#!/usr/bin/python
#encoding=utf-8

import sys
sys.path.append("../chinese_participation")
from jieba_participator import JiebaParticipator

class ArticleAnalysis(object):
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
    def semantic_analysis(segment_partition_list):
        for item in segment_partition_list:
            line = ""
            for word in item:
                line += word
                line += '|'
            print line

    @staticmethod
    def file_semantic_analysis(file_path):
        segment_list = ArticleAnalysis.get_segment_list_from_input_file(file_path)
        segment_partition_list = ArticleAnalysis.partition(segment_list)
        ArticleAnalysis.semantic_analysis(segment_partition_list)

    @staticmethod
    def string_semantic_analysis(input_string):
        segment_list = ArticleAnalysis.get_segment_list(input_string)
        segment_partition_list = ArticleAnalysis.partition(segment_list)
        ArticleAnalysis.semantic_analysis(segment_partition_list)

if __name__ == '__main__':
    article_analysis = ArticleAnalysis()
    ArticleAnalysis.string_semantic_analysis("话说天下大势\n分久必合\n合久必分")
