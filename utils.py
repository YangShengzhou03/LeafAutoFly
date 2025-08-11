import json

# 应用设置 - 存储在内存中
_app_settings = {
    "theme": "light",
    "theme_color": "#409eff",
    "notifications": True,
    "language": "zh-CN",
    "timezone": "Asia/Shanghai"
}

def get_app_settings():
    """获取应用设置"""
    return _app_settings.copy()

def save_app_settings(settings):
    """保存应用设置"""
    global _app_settings
    # 只更新已存在的设置键，防止注入未知设置
    for key in _app_settings:
        if key in settings:
            _app_settings[key] = settings[key]

def cron_to_human_readable(cron_expr):
    """将cron表达式转换为人类可读格式"""
    if not cron_expr:
        return "无效的表达式"
        
    parts = cron_expr.split()
    if len(parts) != 5:
        return "无效的表达式"
        
    minute, hour, day, month, weekday = parts
    
    # 处理分钟
    min_str = "每分钟" if minute == "*" else f"{minute}分"
    
    # 处理小时
    if hour == "*":
        hour_str = "每小时"
    else:
        hour_str = f"{hour}时"
    
    # 处理日期和星期（简单处理）
    if day == "*" and weekday == "*":
        day_str = "每天"
    elif day != "*":
        day_str = f"每月{day}日"
    else:
        weekdays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
        if weekday == "*":
            day_str = "每天"
        else:
            try:
                day_num = int(weekday)
                day_str = f"每周{weekdays[day_num]}"
            except:
                day_str = f"每周{weekday}"
    
    # 处理月份
    if month == "*":
        month_str = ""
    else:
        month_str = f"{month}月"
    
    # 组合结果
    result = f"{min_str} {hour_str} {day_str} {month_str}".strip()
    return result if result else "无效的表达式"
