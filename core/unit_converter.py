# -*- coding: utf-8 -*-
"""
单位数量级换算模块

支持以下数量级前缀：
- 尧 (Y): 10^24
- 泽 (Z): 10^21
- 艾 (E): 10^18
- 拍 (P): 10^15
- 太 (T): 10^12
- 吉 (G): 10^9
- 兆 (M): 10^6
- 千 (k): 10^3
- 百 (h): 10^2
- 十 (da): 10^1
- 分 (d): 10^-1
- 厘 (c): 10^-2
- 毫 (m): 10^-3
- 微 (μ): 10^-6
- 纳 (n): 10^-9
- 皮 (p): 10^-12
- 飞 (f): 10^-15
- 阿 (a): 10^-18
- 仄 (z): 10^-21
- 幺 (y): 10^-24
"""

# 数量级前缀与对应的指数
PREFIXES = {
    # 中文前缀
    '尧': 24,
    '泽': 21,
    '艾': 18,
    '拍': 15,
    '太': 12,
    '吉': 9,
    '兆': 6,
    '千': 3,
    '百': 2,
    '十': 1,
    '分': -1,
    '厘': -2,
    '毫': -3,
    '微': -6,
    '纳': -9,
    '皮': -12,
    '飞': -15,
    '阿': -18,
    '仄': -21,
    '幺': -24,
    # 符号前缀
    'Y': 24,
    'Z': 21,
    'E': 18,
    'P': 15,
    'T': 12,
    'G': 9,
    'M': 6,
    'k': 3,
    'h': 2,
    'da': 1,
    'd': -1,
    'c': -2,
    'm': -3,
    'μ': -6,
    'n': -9,
    'p': -12,
    'f': -15,
    'a': -18,
    'z': -21,
    'y': -24,
}

# 基础单位列表
BASE_UNITS = [
    'm', 'kg', 's', 'A', 'K', 'mol', 'cd',  # SI基本单位
    'Bq', 'Gy', 'Sv', 'Hz', 'N', 'Pa', 'J', 'W', 'V', 'Ω', 'F', 'H',  # 导出单位
    'm/s', 'm/s²', 'm³', 'kg/m³', 'mol/m³',  # 组合单位
    '%', '°C',  # 其他常用单位
]

def get_prefix_factor(prefix):
    """
    获取数量级前缀对应的换算因子
    :param prefix: 数量级前缀（如 '千', '毫', 'k', 'm'）
    :return: 换算因子（10的幂次方）
    """
    if prefix in PREFIXES:
        return 10 ** PREFIXES[prefix]
    return 1.0

def convert_value(value, from_prefix, to_prefix):
    """
    在不同数量级之间转换值
    :param value: 原始值
    :param from_prefix: 原始数量级前缀
    :param to_prefix: 目标数量级前缀
    :return: 转换后的值
    """
    try:
        value = float(value)
        from_factor = get_prefix_factor(from_prefix)
        to_factor = get_prefix_factor(to_prefix)
        return value * (from_factor / to_factor)
    except (ValueError, TypeError):
        return None

def parse_unit(unit_str):
    """
    解析单位字符串，分离数量级前缀和基础单位
    :param unit_str: 单位字符串（如 'kBq', '毫Gy', 'μSv/h'）
    :return: (前缀, 基础单位)
    """
    if not unit_str:
        return ('', '')
    
    # 尝试匹配最长的前缀
    for prefix in sorted(PREFIXES.keys(), key=len, reverse=True):
        if unit_str.startswith(prefix):
            return (prefix, unit_str[len(prefix):])
    
    return ('', unit_str)

def format_unit(prefix, base_unit):
    """
    格式化单位字符串
    :param prefix: 数量级前缀
    :param base_unit: 基础单位
    :return: 格式化后的单位字符串
    """
    return f"{prefix}{base_unit}" if prefix else base_unit

def get_all_prefixes():
    """
    获取所有可用的数量级前缀列表
    :return: 前缀列表（中文在前，符号在后）
    """
    chinese_prefixes = [p for p in PREFIXES.keys() if p.isalpha() and p == p.encode('utf-8').decode('utf-8') and len(p) == 1 and '\u4e00' <= p <= '\u9fff']
    symbol_prefixes = [p for p in PREFIXES.keys() if p not in chinese_prefixes]
    return chinese_prefixes + symbol_prefixes

def get_prefix_display(prefix):
    """
    获取前缀的显示名称（包含中文和符号）
    :param prefix: 前缀
    :return: 显示名称
    """
    # 中文前缀和符号前缀的映射
    display_map = {
        '尧': '尧 (Y)',
        '泽': '泽 (Z)',
        '艾': '艾 (E)',
        '拍': '拍 (P)',
        '太': '太 (T)',
        '吉': '吉 (G)',
        '兆': '兆 (M)',
        '千': '千 (k)',
        '百': '百 (h)',
        '十': '十 (da)',
        '分': '分 (d)',
        '厘': '厘 (c)',
        '毫': '毫 (m)',
        '微': '微 (μ)',
        '纳': '纳 (n)',
        '皮': '皮 (p)',
        '飞': '飞 (f)',
        '阿': '阿 (a)',
        '仄': '仄 (z)',
        '幺': '幺 (y)',
        'Y': 'Y (尧)',
        'Z': 'Z (泽)',
        'E': 'E (艾)',
        'P': 'P (拍)',
        'T': 'T (太)',
        'G': 'G (吉)',
        'M': 'M (兆)',
        'k': 'k (千)',
        'h': 'h (百)',
        'da': 'da (十)',
        'd': 'd (分)',
        'c': 'c (厘)',
        'm': 'm (毫)',
        'μ': 'μ (微)',
        'n': 'n (纳)',
        'p': 'p (皮)',
        'f': 'f (飞)',
        'a': 'a (阿)',
        'z': 'z (仄)',
        'y': 'y (幺)',
    }
    return display_map.get(prefix, prefix)

def convert_to_base_unit(value, unit_str):
    """
    将带单位的值转换为基础单位值
    :param value: 数值
    :param unit_str: 单位字符串
    :return: 基础单位下的数值
    """
    try:
        value = float(value)
        prefix, base_unit = parse_unit(unit_str)
        factor = get_prefix_factor(prefix)
        return value * factor, base_unit
    except (ValueError, TypeError):
        return None, unit_str

def convert_from_base_unit(base_value, target_unit):
    """
    将基础单位值转换为目标单位值
    :param base_value: 基础单位下的数值
    :param target_unit: 目标单位字符串
    :return: 目标单位下的数值
    """
    try:
        base_value = float(base_value)
        prefix, base_unit = parse_unit(target_unit)
        factor = get_prefix_factor(prefix)
        return base_value / factor
    except (ValueError, TypeError):
        return None


def auto_best_unit(base_value, base_unit, min_val=0.1, max_val=999):
    """
    给定基础值和基础单位，自动选择使数值在可读范围内的最佳数量级前缀

    算法：遍历所有可用前缀，找到使转换后的绝对值在 [min_val, max_val) 范围内的前缀。
    对于 0 值，直接返回基础单位。
    如果没有前缀能使值落入范围，选择使值最接近 1 的前缀。

    :param base_value: 基础单位下的数值
    :param base_unit: 基础单位字符串（如 'Gy/h'）
    :param min_val: 可读范围下限（默认 0.1）
    :param max_val: 可读范围上限（默认 999）
    :return: (最佳前缀, 转换后的值, 完整单位字符串)
             例如: ('n', 123.4, 'nGy/h')
    """
    try:
        base_value = float(base_value)
    except (ValueError, TypeError):
        return ('', base_value, base_unit)

    if base_value == 0:
        return ('', 0.0, base_unit)

    abs_val = abs(base_value)

    best_prefix = ''
    best_display_value = base_value
    best_distance = float('inf')

    prefixes_to_try = [
        ('T', 12), ('G', 9), ('M', 6), ('k', 3),
        ('', 0),
        ('m', -3), ('μ', -6), ('n', -9), ('p', -12),
    ]

    for prefix, exponent in prefixes_to_try:
        factor = 10 ** exponent
        display_value = abs_val / factor

        if min_val <= display_value < max_val:
            return (prefix, base_value / factor, f'{prefix}{base_unit}' if prefix else base_unit)

        distance = abs(display_value - 1)
        if distance < best_distance:
            best_distance = distance
            best_prefix = prefix
            best_display_value = base_value / factor

    return (best_prefix, best_display_value, f'{best_prefix}{base_unit}' if best_prefix else base_unit)
