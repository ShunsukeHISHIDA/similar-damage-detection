"""
@file Score.py
@brief 類似スコア算出に関わるクラスを管理

@author Shunsuke Hishida / created on 2022/05/23
@copyrights (c) 2022 Global Walkers,inc All rights reserved.
"""
import yaml


def loadYaml(path):
    """
    @return dest dict    yamlファイルを読み込んだ dict
    """
    with open(path, mode="r", encoding="utf-8") as f:
        dest = yaml.full_load(f)
    return dest
