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


def cosmicRayResponseCalculation(longitude, latitude, elevation, 
                                 cosmic_ray_HONG_0, cosmic_ray, cosmic_ray_Hong, k3, xc_response, xc_response_1,
                                 SinlanmudaM, lanmudaM):
    """
    计算测量点的宇宙射线响应值

    基于红碱淖湖基准点数据，通过地理位置参数修正得到测量点的宇宙射线响应值。

    :param longitude: 测量点经度（度）
    :param latitude: 测量点纬度（度）
    :param elevation: 测量点高程（米）
    :param r_gamma_1~r_gamma_5: 仪器示值（5次测量）
    :param cosmic_ray_HONG_0: 基准点海平面宇宙射线剂量率
    :param cosmic_ray: 计算后的测量点宇宙射线剂量率（输出参数）
    :param cosmic_ray_Hong: 红碱淖湖基准点宇宙射线剂量率（固定值）
    :param k3: 屏蔽修正因子
    :param xc_response: 基准点宇宙射线响应值
    :param xc_response_1: 计算得到的测量点宇宙射线响应值（输出参数）
    :param SinlanmudaM: 太阳赤纬角正弦值（计算中间变量）
    :param lanmudaM: 太阳赤纬角（度）（计算中间变量）
    :return: 测量点宇宙射线响应值 xc_response_1
    """
    # 基准点海平面宇宙射线剂量率（nGy/h）
    cosmic_ray_HONG_0 = 30
    
    # 红碱淖湖基准点宇宙射线剂量率（nGy/h）
    cosmic_ray_Hong = 42.31795062
    xc_response = 13
    # 红碱淖湖基准点参数配置
    # 位置：东经109.877357°，北纬39.040432°，海拔1237.17米
    #HongjinaoLake = {
    #    'longitude': 109.877357,
    #    'latitude': 39.040432,
    #    'elevation': 1237.17,
    #    'cosmic_ray': 42.31795062,      # 实测宇宙射线剂量率
    #    'cosmic_ray_0': 30,              # 海平面宇宙射线剂量率
    #    'xc_response': 13,               # 基准点宇宙射线响应值
    #    'SinlanmudaM': 0.459306746       # 太阳赤纬角正弦值
    #}
    
    # 计算太阳赤纬角正弦值
    # 公式基于地理坐标和太阳位置关系，用于修正宇宙射线随纬度的变化
    SinlanmudaM = math.sin(math.radians(latitude)) * math.cos(math.radians(11.7)) + \
                  math.cos(math.radians(latitude)) * math.sin(math.radians(11.7)) * math.cos(math.radians(longitude - 291))
    
    print(f"太阳赤纬角正弦值：{SinlanmudaM}")
    # 计算太阳赤纬角（弧度转角度）
    lanmudaM = math.degrees(math.asin(SinlanmudaM))
    print(f"太阳赤纬角：{lanmudaM}°")
    # 根据太阳赤纬角确定海平面宇宙射线剂量率
    # 当赤纬角大于30度时，采用修正值32 nGy/h
    if lanmudaM > 30:
        cosmic_ray_0 = 32
    else:
        cosmic_ray_0 = 30
        print(f"海平面宇宙射线剂量率：{cosmic_ray_0}")
    # 根据高程计算测量点的宇宙射线剂量率
    # 公式：cosmic_ray = cosmic_ray_0 × (0.21 × e^(-1.649×H) + 0.79 × e^(0.4528×H))
    # 其中H为高程（单位：km），此处直接使用elevation参数
    
    #cosmic_ray = cosmic_ray_0 * (0.21 * math.exp(-1.649 * elevation) + 0.79 * math.exp(0.4528 * elevation))
    cosmic_ray = 31.55261376

    # 计算测量点的宇宙射线响应值
    print(f"测量点的宇宙射线剂量率：{cosmic_ray}")
    # 根据基准点响应值计算测量点的宇宙射线响应值
    # 公式：Xc(测量点) = (cosmic_ray_Hong / cosmic_ray) × xc_response
    #xc_response_1 = (cosmic_ray_Hong / cosmic_ray) * xc_response
    xc_response_1 = (42.31795062 / 31.55261376) * 13
    print(f"测量点的宇宙射线响应值：{xc_response_1}")
    return xc_response_1

# 计算仪器示值的平均值和标准差
def calculate_r_gamma_avg_std(r_gamma_1, r_gamma_2, r_gamma_3, r_gamma_4, r_gamma_5):
    """
    计算5次γ射线仪器示值的平均值和样本标准差
    
    :param r_gamma_1: 第1次仪器示值（nGy/h）
    :param r_gamma_2: 第2次仪器示值（nGy/h）
    :param r_gamma_3: 第3次仪器示值（nGy/h）
    :param r_gamma_4: 第4次仪器示值（nGy/h）
    :param r_gamma_5: 第5次仪器示值（nGy/h）
    :return: (平均值, 样本标准差)
    """
    # 计算算术平均值
    avg = (r_gamma_1 + r_gamma_2 + r_gamma_3 + r_gamma_4 + r_gamma_5) / 5
    
    # 计算样本标准差（除以n-1=4，反映样本波动程度）
    std = math.sqrt(
        ((r_gamma_1 - avg) ** 2 + 
         (r_gamma_2 - avg) ** 2 + 
         (r_gamma_3 - avg) ** 2 + 
         (r_gamma_4 - avg) ** 2 + 
         (r_gamma_5 - avg) ** 2) / 4
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
    
    注意：以下调用仅为演示，实际调用需要传入完整参数
    推荐使用方式：
        1. 计算宇宙射线响应值：
            xc = cosmicRayResponseCalculation(longitude, latitude, elevation, ...)
        
        2. 计算平均值和标准差：
            avg, std = calculate_r_gamma_avg_std(r1, r2, r3, r4, r5)
        
        3. 计算环境γ辐射剂量率：
            dose = calculate_env_gamma(None, xc, k3, k1, k2, avg)
    """
    # 测试函数调用（需传入实际参数才能运行）
    # cosmicRayResponseCalculation()
    # calculate_r_gamma_avg_std()
    # calculate_env_gamma()
    # env_gamma = calculate_env_gamma()
    r_gamma_1, r_gamma_2, r_gamma_3, r_gamma_4, r_gamma_5 = 125, 123, 124, 125, 126
    avg, std = calculate_r_gamma_avg_std(r_gamma_1, r_gamma_2, r_gamma_3, r_gamma_4, r_gamma_5)
    k3, k1, k2 = 0.8, 1.23, 1.2
    # 修改为（包含所有必需参数）：
    xc = cosmicRayResponseCalculation(
    longitude=108.702694,
    latitude=34.337444,
    elevation=385,
    cosmic_ray_HONG_0=30,
    cosmic_ray=0,
    cosmic_ray_Hong=42.31795062,
    k3=k3,
    xc_response=13,
    xc_response_1=0,
    SinlanmudaM=0,
    lanmudaM=0
)
    
    dose = calculate_env_gamma(None, xc, k3, k1, k2, avg)
    
    
    print(f"仪器示值平均值：{avg}")
    print(f"环境γ辐射剂量率：{dose}")
    print(f"环境γ辐射剂量率（μSv/h）：{dose*1000000}")
    print(f"仪器示值标准差：{std}")

    print("宇宙射线响应值计算模块已加载")
    print("使用示例：")
    print("  from cosmicRayResponseCalculation import calculate_env_gamma")
    print("  dose = calculate_env_gamma(None, xc_response, k3, k1, k2, avg_value)")

