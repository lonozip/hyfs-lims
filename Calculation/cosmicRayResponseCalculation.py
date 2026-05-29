# -*- coding: utf-8 -*-
"""
宇宙射线响应值计算模块

该模块实现环境γ辐射剂量率测量中宇宙射线响应值的计算方法。
基于红碱淖湖基准点的宇宙射线响应值，通过地理位置（经纬度、高程）
对测量点的宇宙射线响应值进行修正计算。

计算公式：
    Xc(测量点) = (Xc_基准 / cosmic_ray_基准) × cosmic_ray(测量点)

参数说明：
    SinlanmudaM: 太阳赤纬角的正弦值
    lanmudaM: 太阳赤纬角（度）
    cosmic_ray_0: 海平面宇宙射线剂量率
    cosmic_ray: 测量点宇宙射线剂量率
    xc_response_1: 计算得到的测量点宇宙射线响应值
"""

import math


def cosmicRayResponseCalculation(longitude, latitude, elevation, k3, xc_response):
    """
    计算测量点的宇宙射线响应值

    基于红碱淖湖基准点数据，通过地理位置参数修正得到测量点的宇宙射线响应值。

    :param longitude: 测量点经度（度）
    :param latitude: 测量点纬度（度）
    :param elevation: 测量点高程（米）
    :param k3: 屏蔽修正因子
    :param xc_response: 基准点宇宙射线响应值
    :return: 测量点宇宙射线响应值
    """
    # 红碱淖湖基准点参数（固定常量）
    COSMIC_RAY_HONG = 42.31795062 # 红碱淖湖基准点宇宙射线剂量率（nGy/h）
    # xc_response 由调用方传入，不再在此处覆盖
    # 计算太阳赤纬角正弦值
    # 公式基于地理坐标和太阳位置关系，用于修正宇宙射线随纬度的变化
    SinlanmudaM = math.sin(math.radians(latitude)) * math.cos(math.radians(11.7)) + \
                  math.cos(math.radians(latitude)) * math.sin(math.radians(11.7)) * math.cos(math.radians(longitude - 291))

    # 计算太阳赤纬角（弧度转角度）
    lanmudaM = math.degrees(math.asin(SinlanmudaM))

    # 根据太阳赤纬角确定海平面宇宙射线剂量率
    # 当赤纬角大于30度时，采用修正值32 nGy/h
    if lanmudaM > 30:
        cosmic_ray_0 = 32
    else:
        cosmic_ray_0 = 30

    # 将高程从米转换为公里（公式要求单位为km）
    H_km = elevation / 1000.0

    # 根据高程计算测量点的宇宙射线剂量率
    # 公式：cosmic_ray = cosmic_ray_0 × (0.21 × e^(-1.649×H) + 0.79 × e^(0.4528×H))
    cosmic_ray = cosmic_ray_0 * (0.21 * math.exp(-1.649 * H_km) + 0.79 * math.exp(0.4528 * H_km))

    # 根据基准点响应值计算测量点的宇宙射线响应值
    # 公式：Xc(测量点) = (cosmic_ray / cosmic_ray_Hong) × xc_response
    xc_response_1 = (cosmic_ray / COSMIC_RAY_HONG) * xc_response

    return xc_response_1


def calculate_r_gamma_avg_std(r_gamma_1, r_gamma_2, r_gamma_3, r_gamma_4, r_gamma_5, r_gamma_6, r_gamma_7, r_gamma_8, r_gamma_9, r_gamma_10):
    """
    计算10次γ射线仪器示值的平均值和样本标准差

    :param r_gamma_1: 第1次仪器示值（nGy/h）
    :param r_gamma_2: 第2次仪器示值（nGy/h）
    :param r_gamma_3: 第3次仪器示值（nGy/h）
    :param r_gamma_4: 第4次仪器示值（nGy/h）
    :param r_gamma_5: 第5次仪器示值（nGy/h）
    :param r_gamma_6: 第6次仪器示值（nGy/h）
    :param r_gamma_7: 第7次仪器示值（nGy/h）
    :param r_gamma_8: 第8次仪器示值（nGy/h）
    :param r_gamma_9: 第9次仪器示值（nGy/h）
    :param r_gamma_10: 第10次仪器示值（nGy/h）
    :return: (平均值, 样本标准差)
    """
    # 计算算术平均值
    avg = (r_gamma_1 + r_gamma_2 + r_gamma_3 + r_gamma_4 + r_gamma_5 + r_gamma_6 + r_gamma_7 + r_gamma_8 + r_gamma_9 + r_gamma_10) / 10

    # 计算样本标准差（除以n-1=9，反映样本波动程度）
    std = math.sqrt(
        ((r_gamma_1 - avg) ** 2 +
         (r_gamma_2 - avg) ** 2 +
         (r_gamma_3 - avg) ** 2 +
         (r_gamma_4 - avg) ** 2 +
         (r_gamma_5 - avg) ** 2 +
         (r_gamma_6 - avg) ** 2 +
         (r_gamma_7 - avg) ** 2 +
         (r_gamma_8 - avg) ** 2 +
         (r_gamma_9 - avg) ** 2 +
         (r_gamma_10 - avg) ** 2) / 9
    )

    return avg, std


# 环境γ辐射剂量率测量结果计算
def calculate_env_gamma(env_gamma, xc_response_1, k3, k1, k2, avg):
    """
    计算环境γ辐射剂量率

    核心计算公式：D = (Rγ × k1 / k2) - (Xc × k3)

    参数说明：
        k1: 仪器校准/检定因子
        k2: 仪器检验源效率因子（无检验源时取1）
        k3: 建筑物屏蔽修正因子（楼房=0.8，平房=0.9，原野=1.0）
        Xc: 宇宙射线响应值
        Rγ: 仪器示值平均值

    :param env_gamma: 环境γ辐射剂量率（输出参数）
    :param xc_response_1: 宇宙射线响应值 Xc
    :param k3: 屏蔽修正因子
    :param k1: 校准/检定因子
    :param k2: 效率因子
    :param avg: 仪器示值平均值 Rγ
    :return: 环境γ辐射剂量率值
    """
    # 计算公式：环境γ辐射剂量率 = k1 × k2 × 平均值 - k3 × 宇宙射线响应值
    env_gamma = k1 * k2 * avg - k3 * xc_response_1

    return env_gamma


if __name__ == '__main__':
    """
    模块自测入口
    """
    # 设置测试数据（根据图片数据）
    r_gamma_1, r_gamma_2, r_gamma_3, r_gamma_4, r_gamma_5, r_gamma_6, r_gamma_7, r_gamma_8, r_gamma_9, r_gamma_10 = 125.0, 123.0, 124.0, 125.0, 126.0, 124.0, 125.0, 124.0, 122.0, 123.0

    k3, k1, k2 = 0.8, 1.23, 1.2

    # 计算宇宙射线响应值
    # 参数：经度, 纬度, 高程(米), k3屏蔽修正因子, xc_response基准点响应值
    xc = cosmicRayResponseCalculation(
        longitude=108.702694,
        latitude=34.337444,
        elevation=385,  # 高程：385米
        k3=0.8,             # 屏蔽修正因子
        xc_response=13      # 基准点宇宙射线响应值
    )

    # 计算平均值和标准差
    av, std = calculate_r_gamma_avg_std(r_gamma_1, r_gamma_2, r_gamma_3, r_gamma_4, r_gamma_5, r_gamma_6, r_gamma_7, r_gamma_8, r_gamma_9, r_gamma_10)

    print(f"测量点的宇宙射线响应值：{xc}")
    print(f"仪器示值平均值：{av}")
    print(f"仪器示值标准差：{std}")

    print("\n宇宙射线响应值计算模块已加载")
    print("使用示例：")
    print("  from cosmicRayResponseCalculation import calculate_env_gamma")
    print("  dose = calculate_env_gamma(None, xc_response, k3, k1, k2, avg_value)")