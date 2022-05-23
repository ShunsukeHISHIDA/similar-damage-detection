"""
@file Score.py
@brief 類似スコア算出に関わるクラスを管理

@author Shunsuke Hishida / created on 2022/05/23
@copyrights (c) 2022 Global Walkers,inc All rights reserved.
"""
import itertools
from collections import defaultdict

import pandas as pd
from Utility.Checker import checkTotalWeights
from Utility.Loader import loadYaml


class UnitScore(object):
    __SCORE_WEIGHTS_PATH = "./Weights/Score.yaml"

    @property
    def score(self) -> int:
        """
        @brief compositionScoreとorderScoreの合計値を返す
        """
        return self.__compositionScore + self.__orderScore

    def __init__(self, target: list, correct: list):
        self.__compositionScore = None
        self.__orderScore = None
        scoreWeights = loadYaml(self.__SCORE_WEIGHTS_PATH)
        checkTotalWeights(scoreWeights)
        self.__calculateCompositionScore(target, correct, scoreWeights["composition"])
        self.__calculateOrderScore(target, correct, scoreWeights["order"])

    def __calculateCompositionScore(self, target: list, correct: list, weight: int):
        """
        @brief  文字の構成要素に着目して点数化する
                なお、重みをかける前のスコアの最大を100とし、最後に重みを掛けた値を
                本関数内のスコアとする
        """
        commonWordNum = self.countCommonWordNumber(target, correct)
        # 構成数があっている文字数の割合を求めて、満点である100点を掛ける
        tmpScore = 100 * commonWordNum / len(correct)
        # weightは 0 から 100 の値なので、100を割った値をtempScoreに掛ける
        self.__compositionScore = int((weight / 100) * tmpScore)
        # print("compositionScore: ", self.__compositionScore)

    def __calculateOrderScore(self, target, correct, weight):
        """
        @brief  文字の構成順序に着目して点数化する
                なお、重みをかける前のスコアの最大を100とし、最後に重みを掛けた値を
                本関数内のスコアとする
        """
        commonWordNum = 0
        for targetWord, correctWord in itertools.zip_longest(target, correct):
            if targetWord == correctWord:
                commonWordNum += 1
        # 順番があっている文字数の割合を求めて、満点である100点を掛ける
        tmpScore = 100 * commonWordNum / len(correct)
        # weightは 0 から 100 の値なので、100を割った値をtempScoreに掛ける
        self.__orderScore = int((weight / 100) * tmpScore)
        # print("orderScore: ", self.__orderScore)

    def countCommonWordNumber(self, target: list, correct: list) -> int:
        """
        @brief target と correct の文字列の中で共通の文字数を数える
        """
        commonWordNum = 0
        targetCounter = self.countWord(target)
        correctCounter = self.countWord(correct)
        for word, num in targetCounter.items():
            if word in correctCounter:
                commonWordNum += num
        return commonWordNum

    def countWord(self, wordList) -> dict:
        counter = defaultdict(int)
        for word in wordList:
            counter[word] += 1
        return dict(counter)


class TotalScore(object):
    __ATTRIBUTE_WEIGHTS_PATH = "./Weights/Attribute.yaml"

    @property
    def index(self):
        return self.__index

    @property
    def totalScore(self):
        return self.__totalScore

    def __init__(self, index: int, targetData: pd.Series, correctData: pd.DataFrame):
        self.__index = index
        self.__totalScore = None
        weights: dict = loadYaml(self.__ATTRIBUTE_WEIGHTS_PATH)
        checkTotalWeights(weights)
        self.__calculate(weights, targetData, correctData)

    def __calculate(
        self, weights: dict, targetData: pd.Series, correctData: pd.DataFrame
    ):
        """
        @brief 当該indexのデータの類似度を計算
        """
        scoreList = []
        for attrName, weightValue in weights.items():
            # print("target: ", targetData[attrName])
            # print("correct: ", correctData.at[0, attrName])
            target = str(targetData[attrName])
            correct = str(correctData.at[0, attrName])
            unitScore = UnitScore(list(target), list(correct))
            # print("unitScore: ", unitScore.score)
            scoreList.append(int(weightValue / 100 * unitScore.score))
        self.__totalScore = sum(scoreList)
