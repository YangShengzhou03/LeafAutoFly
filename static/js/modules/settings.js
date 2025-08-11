// 设置管理模块
const settingsModule = {
    // 默认设置
    defaultSettings() {
        return {
            appName: "LeafAuto 智能管理系统",
            language: "zh-CN",
            timezone: "Asia/Shanghai",
            notifications: true,
            theme: "light",
            theme_color: "#409eff",
            layoutDensity: "comfortable"
        };
    },
    
    // 保存设置到本地存储
    saveSettings(settings) {
        localStorage.setItem('appSettings', JSON.stringify(settings));
    },
    
    // 加载设置（优先从API获取，其次从本地存储，最后使用默认）
    async loadSettings() {
        try {
            // 尝试从API获取
            const response = await fetch('/api/settings');
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.log('无法从API获取设置，使用本地存储或默认值');
        }
        
        // 尝试从本地存储获取
        const localSettings = localStorage.getItem('appSettings');
        if (localSettings) {
            return JSON.parse(localSettings);
        }
        
        // 返回默认设置
        return this.defaultSettings();
    },
    
    // 应用主题设置
    applyThemeSettings(theme, themeColor) {
        // 应用主题颜色
        document.documentElement.style.setProperty('--el-color-primary', themeColor);
        
        // 应用主题模式
        const darkStylesheet = document.getElementById('dark-mode-stylesheet');
        let isDark = false;
        
        if (theme === 'dark') {
            isDark = true;
        } else if (theme === 'auto') {
            isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
        
        darkStylesheet.disabled = !isDark;
        document.documentElement.classList.toggle('dark-mode', isDark);
        
        return isDark;
    },
    
    // 应用布局密度
    applyLayoutDensity(density) {
        document.documentElement.classList.toggle('layout-compact', density === 'compact');
    }
};

// 初始化时应用保存的设置
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const settings = await settingsModule.loadSettings();
        settingsModule.applyThemeSettings(settings.theme, settings.theme_color);
        settingsModule.applyLayoutDensity(settings.layoutDensity);
    } catch (error) {
        console.error('初始化设置失败:', error);
    }
});
