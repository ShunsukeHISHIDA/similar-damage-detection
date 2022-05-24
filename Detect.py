"""
@file Detect.py
@brief 類似損傷を抽出するプログラム

@author Shunsuke Hishida / created on 2022/05/23
@copyrights (c) 2022 Global Walkers,inc All rights reserved.
"""
import os

import pandas as pd

from Calculator.Score import TotalScore
from Utility.Checker import checkAttribute


def main(
    targetData: pd.DataFrame,
    correctData: pd.DataFrame,
    threshold: int,
    outputDir: str,
    outputFileName: str,
):
    """
    @brief メイン関数
    @param targetData       類似検索をかけるテーブルデータ
    @param correctData      対象データ（このデータの類似データを検索する）
    @param threshold        抽出するスコアの閾値
                            閾値以上のデータを抽出する
    @param outputDir        抽出したデータの出力ディレクトリ
    @param outputFileName   出力するファイル名
    """
    extractingIndexList = []
    for index, data in targetData.iterrows():
        score = TotalScore(index, data, correctData)
        print(f"[index: {index}] score: {score.totalScore}")
        if score.totalScore >= threshold:
            extractingIndexList.append(index)
    extractedData = targetData.loc[extractingIndexList]
    os.makedirs(outputDir, exist_ok=True)
    extractedData.to_csv(os.path.join(outputDir, outputFileName))


if __name__ == "__main__":
    ### 設定 ###
    targetDataPath = "./Example/DamageList.csv"
    correctDataPath = "./Example/DamageList.csv"
    outputDir = "./Output"
    outputFileName = "ExtractedDamageList.csv"
    scoreThreshold = 90  # 0 <= scoreThreshold <= 100 の範囲で選択
    ############
    targetData = pd.read_csv(targetDataPath)
    correctData = pd.read_csv(correctDataPath)
    checkAttribute(targetData, correctData)
    main(targetData, correctData, scoreThreshold, outputDir, outputFileName)
