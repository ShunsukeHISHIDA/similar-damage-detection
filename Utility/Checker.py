"""
@file Checker.py
@brief データの確認を行う関数を管理

@author Shunsuke Hishida / created on 2022/05/23
@copyrights (c) 2022 Global Walkers,inc All rights reserved.
"""
import numpy as np
import pandas as pd


def checkAttribute(data_1: pd.DataFrame, data_2: pd.DataFrame):
    """
    @brief 2つのデータの属性が一致するか確認する
    @Error AttributeError   属性が一致しない場合に発出
    """
    if not (np.array_equal(data_1.columns, data_2.columns)):
        raise AttributeError("allData と targetData の属性値が異なります")


def checkTotalWeights(weights: dict):
    """
    @brief 各属性のweightsの合計が100になることを確認する
    @Error ValueError   各属性のweightsの合計が100にならない場合に発出
    """
    totalWeights = sum(list(weights.values()))
    if totalWeights != 100:
        raise ValueError("AttributeのWeightsの合計が100でない")
