// DOM 元素加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化日期和时间显示
    updateDateTime();
    setInterval(updateDateTime, 1000);

    // 初始化图表
    initCharts();

    // 初始化导航功能
    initNavigation();

    // 初始化模态框功能
    initModal();

    // 初始化主题切换功能
    initThemeSwitcher();

    // 初始化侧边栏切换功能
    initSidebarToggle();

    // 初始化AI聊天功能
    initAiChat();

    // 初始化任务筛选功能
    initTaskFilters();

    // 初始化表单提交处理
    initFormSubmissions();

    // 初始化主题色彩选择
    initThemeColors();
});

// 更新日期和时间
function updateDateTime() {
    const now = new Date();

    // 格式化日期
    const dateOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('current-date').textContent = now.toLocaleDateString('zh-CN', dateOptions);

    // 格式化时间
    const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
    document.getElementById('current-time').textContent = now.toLocaleTimeString('zh-CN', timeOptions);
}

// 初始化图表
function initCharts() {
    // 检查是否为深色模式
    const isDarkMode = document.documentElement.classList.contains('dark');
    const textColor = isDarkMode ? '#C9CDD4' : '#4E5969';

    // 任务执行趋势图表
    const taskTrendCtx = document.getElementById('task-trend-chart').getContext('2d');
    const taskTrendChart = new Chart(taskTrendCtx, {
        type: 'line',
        data: {
            labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
            datasets: [{
                label: '已执行任务',
                data: [18, 24, 21, 32, 26, 15, 24],
                borderColor: '#165DFF',
                backgroundColor: 'rgba(22, 93, 255, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: '失败任务',
                data: [2, 1, 3, 0, 2, 1, 0],
                borderColor: '#F53F3F',
                backgroundColor: 'rgba(245, 63, 63, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: textColor
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        color: textColor
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: textColor
                    }
                }
            }
        }
    });

    // AI 交互统计图表
    const aiInteractionCtx = document.getElementById('ai-interaction-chart').getContext('2d');
    const aiInteractionChart = new Chart(aiInteractionCtx, {
        type: 'bar',
        data: {
            labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
            datasets: [{
                label: 'AI 交互次数',
                data: [12, 19, 15, 28, 22, 10, 89],
                backgroundColor: '#4080FF',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: textColor
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        color: textColor
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: textColor
                    }
                }
            }
        }
    });

    // 监听主题变化，更新图表颜色
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                const isDark = document.documentElement.classList.contains('dark');
                const textColor = isDark ? '#C9CDD4' : '#4E5969';

                // 更新任务趋势图表
                taskTrendChart.options.scales.y.grid.color = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
                taskTrendChart.options.scales.x.grid.color = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
                taskTrendChart.options.scales.y.ticks.color = textColor;
                taskTrendChart.options.scales.x.ticks.color = textColor;
                taskTrendChart.options.plugins.legend.labels.color = textColor;
                taskTrendChart.update();

                // 更新AI交互图表
                aiInteractionChart.options.scales.y.grid.color = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
                aiInteractionChart.options.scales.x.grid.color = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
                aiInteractionChart.options.scales.y.ticks.color = textColor;
                aiInteractionChart.options.scales.x.ticks.color = textColor;
                aiInteractionChart.options.plugins.legend.labels.color = textColor;
                aiInteractionChart.update();
            }
        });
    });

    observer.observe(document.documentElement, { attributes: true });
}

// 初始化导航功能
function initNavigation() {
    const sidebarItems = document.querySelectorAll('.sidebar-item[data-section]');
    const sections = document.querySelectorAll('section[id$="-section"]');
    const pageTitle = document.getElementById('page-title');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');

    // 移动端菜单按钮点击事件
    mobileMenuBtn.addEventListener('click', function() {
        sidebar.classList.toggle('translate-x-0');
        sidebar.classList.toggle('-translate-x-full');
    });

    // 侧边栏项点击事件
    sidebarItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();

            // 获取目标区域
            const targetSection = this.getAttribute('data-section');

            // 更新活跃状态
            sidebarItems.forEach(i => i.classList.remove('sidebar-item-active'));
            this.classList.add('sidebar-item-active');

            // 隐藏所有区域，显示目标区域
            sections.forEach(section => {
                section.classList.add('hidden');
            });

            const activeSection = document.getElementById(`${targetSection}-section`);
            activeSection.classList.remove('hidden');
            activeSection.classList.add('fade-in');

            // 更新页面标题
            pageTitle.textContent = this.querySelector('span').textContent;

            // 在移动设备上点击后收起侧边栏
            if (window.innerWidth < 1024) {
                sidebar.classList.add('-translate-x-full');
                sidebar.classList.remove('translate-x-0');
            }
        });
    });
}

// 初始化模态框功能
function initModal() {
    const addTaskBtn = document.getElementById('add-task-btn');
    const addTaskModal = document.getElementById('add-task-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const cancelTaskBtn = document.getElementById('cancel-task-btn');
    const addTaskForm = document.getElementById('add-task-form');
    const modalContent = addTaskModal.querySelector('.max-w-md');

    // 打开模态框
    function openModal() {
        addTaskModal.classList.remove('hidden');
        // 触发动画
        setTimeout(() => {
            addTaskModal.classList.add('opacity-100');
            modalContent.classList.add('scale-100');
            modalContent.classList.remove('scale-95');
        }, 10);
        document.body.style.overflow = 'hidden';
    }

    // 关闭模态框
    function closeModal() {
        addTaskModal.classList.remove('opacity-100');
        modalContent.classList.remove('scale-100');
        modalContent.classList.add('scale-95');
        setTimeout(() => {
            addTaskModal.classList.add('hidden');
            document.body.style.overflow = '';
        }, 300);
    }

    // 事件监听
    addTaskBtn.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    cancelTaskBtn.addEventListener('click', closeModal);

    // 点击模态框外部关闭
    addTaskModal.addEventListener('click', function(e) {
        if (e.target === addTaskModal) {
            closeModal();
        }
    });

    // 表单提交
    addTaskForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // 获取表单数据
        const taskName = document.getElementById('task-name').value;
        const taskDesc = document.getElementById('task-desc').value;
        const taskType = document.getElementById('task-type').value;
        const taskTime = document.getElementById('task-time').value;

        // 简单验证
        if (!taskName || !taskTime) {
            alert('请填写任务名称和执行时间');
            return;
        }

        // 模拟提交成功
        alert(`任务 "${taskName}" 创建成功！`);
        closeModal();
        addTaskForm.reset();
    });
}

// 初始化主题切换功能
function initThemeSwitcher() {
    const themeRadios = document.querySelectorAll('input[name="theme-mode"]');

    // 检查本地存储中的主题设置
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        document.querySelector('input[name="theme-mode"][value="dark"]').checked = true;
    } else if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark');
        document.querySelector('input[name="theme-mode"][value="light"]').checked = true;
    } else {
        // 跟随系统
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        }
        document.querySelector('input[name="theme-mode"][value="auto"]').checked = true;
    }

    // 主题切换事件
    themeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const theme = this.value;

            if (theme === 'dark') {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            } else if (theme === 'light') {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            } else {
                // 跟随系统
                localStorage.removeItem('theme');
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
            }
        });
    });
}

// 初始化侧边栏切换功能
function initSidebarToggle() {
    const toggleBtn = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');
    const sidebarTexts = document.querySelectorAll('#sidebar span:not(.badge)');
    const logoText = document.querySelector('#sidebar h1 span');

    // 检查本地存储中的侧边栏状态
    const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (sidebarCollapsed) {
        toggleSidebar();
    }

    // 侧边栏切换事件
    toggleBtn.addEventListener('click', toggleSidebar);

    function toggleSidebar() {
        // 切换图标
        const icon = toggleBtn.querySelector('i');
        if (icon.classList.contains('fa-angle-double-left')) {
            icon.classList.replace('fa-angle-double-left', 'fa-angle-double-right');
        } else {
            icon.classList.replace('fa-angle-double-right', 'fa-angle-double-left');
        }

        // 切换侧边栏宽度
        if (window.innerWidth >= 1024) {
            if (sidebar.classList.contains('w-64')) {
                sidebar.classList.remove('w-64');
                sidebar.classList.add('w-20');
                // 隐藏文字
                sidebarTexts.forEach(text => text.classList.add('hidden'));
                logoText.classList.add('hidden');
                localStorage.setItem('sidebarCollapsed', 'true');
            } else {
                sidebar.classList.remove('w-20');
                sidebar.classList.add('w-64');
                // 显示文字
                sidebarTexts.forEach(text => text.classList.remove('hidden'));
                logoText.classList.remove('hidden');
                localStorage.setItem('sidebarCollapsed', 'false');
            }
        }
    }

    // 响应窗口大小变化
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024) {
            sidebar.classList.remove('-translate-x-full', 'translate-x-0');
        } else {
            sidebar.classList.add('-translate-x-full');
            sidebar.classList.remove('translate-x-0');
        }
    });
}

// 初始化AI聊天功能
function initAiChat() {
    const aiInput = document.getElementById('ai-input');
    const aiSendBtn = document.getElementById('ai-send-btn');
    const chatMessages = document.getElementById('ai-chat-messages');

    // 发送消息
    function sendMessage() {
        const message = aiInput.value.trim();
        if (!message) return;

        // 添加用户消息
        const userMessageHTML = `
            <div class="flex gap-3 justify-end slide-in">
                <div class="bg-primary text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-[80%]">
                    <p>${message}</p>
                </div>
                <div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0">
                    <img src="https://picsum.photos/id/1005/40/40" alt="用户头像" class="w-full h-full object-cover">
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', userMessageHTML);

        // 清空输入框
        aiInput.value = '';

        // 滚动到底部
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // 模拟AI回复
        setTimeout(() => {
            const aiResponses = [
                "感谢您的提问。我正在处理您的请求，请稍候...",
                "您的问题很有价值。根据我的分析，建议您...",
                "我理解您的需求了。这是相关的信息和解决方案...",
                "这个问题需要进一步确认一些细节。请问您可以提供更多信息吗？",
                "已收到您的请求，我会尽快处理并给您回复。"
            ];
            const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];

            const aiMessageHTML = `
                <div class="flex gap-3 slide-in">
                    <div class="w-10 h-10 rounded-full bg-primary flex-shrink-0 flex items-center justify-center text-white">
                        <i class="fa fa-robot"></i>
                    </div>
                    <div class="bg-light-bg dark:bg-dark-bg rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%]">
                        <p>${randomResponse}</p>
                    </div>
                </div>
            `;
            chatMessages.insertAdjacentHTML('beforeend', aiMessageHTML);

            // 滚动到底部
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }

    // 发送按钮点击事件
    aiSendBtn.addEventListener('click', sendMessage);

    // 回车键发送消息
    aiInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

// 初始化任务筛选功能
function initTaskFilters() {
    const filterBtns = document.querySelectorAll('.task-filter-btn');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 更新按钮状态
            filterBtns.forEach(b => {
                b.classList.remove('bg-primary', 'text-white');
                b.classList.add('text-light-textSecondary', 'dark:text-dark-textSecondary', 'hover:bg-light-bg', 'dark:hover:bg-dark-bg');
            });

            this.classList.add('bg-primary', 'text-white');
            this.classList.remove('text-light-textSecondary', 'dark:text-dark-textSecondary', 'hover:bg-light-bg', 'dark:hover
            this.classList.remove('text-light-textSecondary', 'dark:text-dark-textSecondary', 'hover:bg-light-bg', 'dark:hover:bg-dark-bg');

            // 这里可以添加实际筛选逻辑
            const filter = this.textContent.trim();
            console.log(`筛选任务: ${filter}`);
        });
    });
}

// 初始化表单提交处理
function initFormSubmissions() {
    const settingsForm = document.getElementById('settings-form');

    settingsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('设置已保存！');
    });
}

// 初始化主题色彩选择
function initThemeColors() {
    const colorBtns = document.querySelectorAll('[data-color]');

    colorBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();

            // 更新按钮状态
            colorBtns.forEach(b => {
                b.classList.remove('ring-2', 'ring-offset-2');
                b.classList.add('hover:ring-2', 'hover:ring-offset-2');
            });

            this.classList.add('ring-2', 'ring-offset-2');
            this.classList.remove('hover:ring-2', 'hover:ring-offset-2');

            // 获取选中的颜色
            const color = this.getAttribute('data-color');
            console.log(`选择主题色彩: ${color}`);

            // 这里可以添加实际切换主题色彩的逻辑
        });
    });
}
