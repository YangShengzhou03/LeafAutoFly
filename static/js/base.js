document.addEventListener('DOMContentLoaded', function() {
    // 初始化欢迎动画
    if (typeof initWelcomeAnimation === 'function') {
        initWelcomeAnimation();
    }

    // 任务列表相关初始化
    if (window.location.pathname === '/' && document.getElementById('taskList')) {
        initAutoInfoTaskList();
    }

    // 初始化按钮效果
    initButtonEffects();

    // 初始化执行按钮
    initExecuteButton();

    // 初始化重复选项按钮
    initRepeatButton();
});

// 初始化按钮效果
function initButtonEffects() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        ['mousedown', 'touchstart'].forEach(event => {
            button.addEventListener(event, () => button.classList.add('button-pressed'));
        });
        ['mouseup', 'mouseleave', 'touchend', 'touchcancel'].forEach(event => {
            button.addEventListener(event, () => button.classList.remove('button-pressed'));
        });
    });
}

// 初始化执行按钮
function initExecuteButton() {
    const executeBtn = document.querySelector('.execute-btn');
    if (executeBtn) {
        executeBtn.addEventListener('click', function() {
            if (this.classList.contains('loading')) return;

            this.classList.add('loading');
            this.innerHTML = '<span class="spinner"></span> 执行中...';
            this.disabled = true;

            setTimeout(() => {
                this.classList.remove('loading');
                this.innerHTML = '执行';
                this.disabled = false;
            }, 1500);
        });
    }
}

// 初始化重复选项按钮
function initRepeatButton() {
    const repeatBtn = document.querySelector('.repeat-btn');
    if (repeatBtn) {
        const currentRepeat = repeatBtn.querySelector('.current-repeat');
        const repeatOptions = document.querySelector('.repeat-options');
        if (currentRepeat && repeatOptions) {
            repeatBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                repeatOptions.style.display = repeatOptions.style.display === 'block' ? 'none' : 'block';
            });

            document.addEventListener('click', function() {
                if (repeatOptions.style.display === 'block') {
                    repeatOptions.style.display = 'none';
                }
            });

            repeatOptions.querySelectorAll('.repeat-item').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.stopPropagation();
                    currentRepeat.textContent = this.textContent;
                    repeatOptions.style.display = 'none';
                });
            });
        }
    }
}
function initAutoInfoTaskList() {
    const taskList = document.getElementById('taskList');
    if (!taskList) return;

    // 初始化UI元素引用
    const ui = {
        taskList: taskList,
        addTaskBtn: document.getElementById('add-task-btn'),
        emptyState: document.querySelector('.empty-task-state'),
        toggleAdvancedSettings: document.querySelector('.toggle-advanced-settings'),
        advancedOptions: document.querySelector('.advanced-options'),
        saveBtn: document.getElementById('save-btn'),
        importBtn: document.getElementById('import-btn'),
        exportBtn: document.getElementById('export-btn'),
        executeAllBtn: document.getElementById('execute-all-btn'),
        sortSelect: document.getElementById('sort-select'),
        messageInput: document.querySelector('.message-input'),
        datetimeInput: document.querySelector('.datetime-input'),
        repeatBtn: document.querySelector('.repeat-btn'),
        notificationContainer: document.querySelector('.task-notification-container')
    };

    // 初始化高级设置切换
    initAdvancedSettings(ui);

    // 加载任务
    loadAutoInfoTasks(ui);

    // 设置表单验证
    setupFormValidation(ui);

    // 绑定添加任务事件
    bindAddTaskEvent(ui);

    // 绑定保存任务事件
    bindSaveTaskEvent(ui);

    // 绑定导出任务事件
    bindExportTaskEvent(ui);

    // 绑定导入任务事件
    bindImportTaskEvent(ui);

    // 绑定执行全部任务事件
    bindExecuteAllTasksEvent(ui);

    // 绑定排序任务事件
    bindSortTasksEvent(ui);
}

// 初始化高级设置
function initAdvancedSettings(ui) {
    if (ui.toggleAdvancedSettings && ui.advancedOptions) {
        ui.toggleAdvancedSettings.addEventListener('click', function() {
            const parent = this.closest('.advanced-settings');
            parent.classList.toggle('open');
            ui.advancedOptions.style.maxHeight = ui.advancedOptions.style.maxHeight ? null : ui.advancedOptions.scrollHeight + 'px';
        });
    }
}

// 绑定添加任务事件
function bindAddTaskEvent(ui) {
    if (ui.addTaskBtn) {
        ui.addTaskBtn.addEventListener('click', function() {
            const messageInput = document.querySelector('.message-input');
            const datetimeInput = document.querySelector('.datetime-input');
            const repeatBtn = document.querySelector('.repeat-btn');
            const currentRepeat = repeatBtn ? repeatBtn.querySelector('.current-repeat') : null;

            const taskText = messageInput.value.trim();
            const taskTime = datetimeInput.value;
            const repeatValue = currentRepeat ? currentRepeat.textContent : '仅一次';

            if (!taskText || !taskTime) {
                showNotification('请输入消息内容和时间', 'error');
                return;
            }

            const currentTime = new Date();
            const selectedTime = new Date(taskTime);
            if (selectedTime <= currentTime) {
                showNotification('请选择一个未来的时间', 'error');
                return;
            }

            const task = {
                id: Date.now(),
                text: taskText,
                time: taskTime,
                repeat: repeatValue,
                createdAt: new Date().toISOString(),
                status: 'pending'
            };

            addAutoInfoTask(task, ui);
            saveAutoInfoTasks(ui);

            messageInput.value = '';
            datetimeInput.value = '';
            if (currentRepeat) {
                currentRepeat.textContent = '仅一次';
            }

            showNotification('任务添加成功', 'success');
        });
    }
}

// 绑定保存任务事件
function bindSaveTaskEvent(ui) {
    if (ui.saveBtn) {
        ui.saveBtn.addEventListener('click', function() {
            saveAutoInfoTasks(ui);
            showNotification('任务已保存', 'success');
        });
    }
}

// 绑定导出任务事件
function bindExportTaskEvent(ui) {
    if (ui.exportBtn) {
        ui.exportBtn.addEventListener('click', function() {
            const tasks = JSON.parse(localStorage.getItem('autoInfoTasks') || '[]');
            const blob = new Blob([JSON.stringify(tasks, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'auto_info_tasks_' + new Date().toISOString().slice(0, 10) + '.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            showNotification('任务已导出', 'success');
        });
    }
}

// 绑定导入任务事件
function bindImportTaskEvent(ui) {
    if (ui.importBtn) {
        ui.importBtn.addEventListener('click', function() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(event) {
                        try {
                            const importedTasks = JSON.parse(event.target.result);
                            if (Array.isArray(importedTasks)) {
                                document.querySelectorAll('.task-item').forEach(item => item.remove());

                                importedTasks.forEach(task => {
                                    if (task.text && task.time) {
                                        task.id = Date.now() + Math.floor(Math.random() * 1000);
                                        task.status = task.status || 'pending';
                                        addAutoInfoTask(task, ui);
                                    }
                                });

                                saveAutoInfoTasks(ui);

                                if (ui.emptyState && importedTasks.length > 0) {
                                    ui.emptyState.style.display = 'none';
                                }

                                showNotification('任务已导入', 'success');
                            } else {
                                showNotification('导入文件格式不正确', 'error');
                            }
                        } catch (error) {
                            showNotification('导入失败: ' + error.message, 'error');
                        }
                    };
                    reader.readAsText(file);
                }
            };
            input.click();
        });
    }
}

// 绑定执行全部任务事件
function bindExecuteAllTasksEvent(ui) {
    if (ui.executeAllBtn) {
        ui.executeAllBtn.addEventListener('click', function() {
            if (this.classList.contains('loading')) return;

            this.classList.add('loading');
            this.textContent = '执行中...';
            this.disabled = true;

            const taskItems = document.querySelectorAll('.task-item');
            if (taskItems.length === 0) {
                showNotification('没有任务可执行', 'info');
                this.classList.remove('loading');
                this.textContent = '执行全部';
                this.disabled = false;
                return;
            }

            let completedCount = 0;
            taskItems.forEach((item, index) => {
                setTimeout(() => {
                    item.style.backgroundColor = 'rgba(76, 175, 80, 0.1)';
                    item.style.transition = 'all 0.3s';

                    completedCount++;
                    if (completedCount === taskItems.length) {
                        setTimeout(() => {
                            this.classList.remove('loading');
                            this.textContent = '执行全部';
                            this.disabled = false;
                            showNotification('所有任务已执行完成', 'success');
                        }, 500);
                    }
                }, index * 300);
            });
        });
    }
}

// 绑定排序任务事件
function bindSortTasksEvent(ui) {
    if (ui.sortSelect) {
        ui.sortSelect.addEventListener('change', function() {
            sortTasks(this.value, ui);
        });
    }

    // 添加任务到列表
    function addAutoInfoTask(task, ui) {
        if (ui.emptyState) {
            ui.emptyState.style.display = 'none';
        }

        const taskItem = document.createElement('div');
        taskItem.className = 'task-item animate-fade-in';
        taskItem.dataset.id = task.id;
        taskItem.dataset.time = task.time;
        taskItem.dataset.status = task.status;

        const date = new Date(task.time);
        const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        const formattedTime = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;

        let statusClass = '';
        let statusIcon = '';

        switch (task.status) {
            case 'running':
                statusClass = 'status-running';
                statusIcon = '🔄';
                break;
            case 'completed':
                statusClass = 'status-completed';
                statusIcon = '✅';
                break;
            case 'failed':
                statusClass = 'status-failed';
                statusIcon = '❌';
                break;
            default:
                statusClass = 'status-pending';
                statusIcon = '⏱️';
        }

        taskItem.innerHTML = `
            <div class="task-info">
                <div class="task-title">${task.text}</div>
                <div class="task-time">
                    时间: ${formattedDate} ${formattedTime} | 重复: ${task.repeat}
                </div>
                <div class="task-status ${statusClass}">
                    <span class="status-icon">${statusIcon}</span>
                    <span class="status-text">${getStatusText(task.status)}</span>
                </div>
            </div>
            <div class="task-actions">
                <button class="task-action-btn edit"><i class="edit-icon"></i></button>
                <button class="task-action-btn delete"><i class="delete-icon"></i></button>
                <button class="task-action-btn execute"><i class="execute-icon"></i></button>
            </div>
        `;

        // 绑定删除按钮事件
        taskItem.querySelector('.task-action-btn.delete').addEventListener('click', function() {
            taskItem.style.height = taskItem.offsetHeight + 'px';
            taskItem.style.overflow = 'hidden';
            taskItem.style.transition = 'all 0.3s';
            taskItem.style.opacity = '0';
            taskItem.style.transform = 'translateX(-20px)';

            setTimeout(() => {
                taskItem.remove();
                saveAutoInfoTasks(ui);

                const taskItems = document.querySelectorAll('.task-item');
                if (taskItems.length === 0 && ui.emptyState) {
                    ui.emptyState.style.display = 'flex';
                }

                showNotification('任务已删除', 'info');
            }, 300);
        });

        // 绑定编辑按钮事件
        taskItem.querySelector('.task-action-btn.edit').addEventListener('click', function() {
            const messageInput = document.querySelector('.message-input');
            const datetimeInput = document.querySelector('.datetime-input');
            const repeatBtn = document.querySelector('.repeat-btn');
            const currentRepeat = repeatBtn ? repeatBtn.querySelector('.current-repeat') : null;

            if (messageInput && datetimeInput && currentRepeat) {
                messageInput.value = task.text;
                datetimeInput.value = task.time;
                currentRepeat.textContent = task.repeat;

                taskItem.remove();
                saveAutoInfoTasks(ui);

                const taskItems = document.querySelectorAll('.task-item');
                if (taskItems.length === 0 && ui.emptyState) {
                    ui.emptyState.style.display = 'flex';
                }
            }
        });

        // 绑定执行按钮事件
        taskItem.querySelector('.task-action-btn.execute').addEventListener('click', function() {
            if (task.status === 'running') return;

            task.status = 'running';
            const statusElement = taskItem.querySelector('.task-status');
            const statusIcon = taskItem.querySelector('.status-icon');
            const statusText = taskItem.querySelector('.status-text');

            statusElement.className = 'task-status status-running';
            statusIcon.textContent = '🔄';
            statusIcon.style.animation = 'spin 1s linear infinite';
            statusText.textContent = '执行中';

            setTimeout(() => {
                task.status = 'completed';
                statusElement.className = 'task-status status-completed';
                statusIcon.textContent = '✅';
                statusIcon.style.animation = 'none';
                statusText.textContent = '已完成';
                saveAutoInfoTasks(ui);
                showNotification('任务执行完成', 'success');
            }, 2000);
        });

        ui.taskList.insertBefore(taskItem, ui.emptyState);

        // 添加悬停效果
        taskItem.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.1)';
            this.style.transition = 'all var(--transition-speed)';
        });
        taskItem.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    }

    // 保存任务到本地存储
    function saveAutoInfoTasks(ui) {
        const tasks = [];
        const taskItems = document.querySelectorAll('.task-item');

        taskItems.forEach(item => {
            tasks.push({
                id: parseInt(item.dataset.id),
                text: item.querySelector('.task-title').textContent,
                time: item.dataset.time,
                repeat: item.querySelector('.task-time').textContent.split('重复: ')[1],
                status: item.dataset.status
            });
        });

        localStorage.setItem('autoInfoTasks', JSON.stringify(tasks));
    }

    // 从本地存储加载任务
    function loadAutoInfoTasks(ui) {
        const tasks = JSON.parse(localStorage.getItem('autoInfoTasks') || '[]');

        if (tasks.length > 0) {
            if (ui.emptyState) {
                ui.emptyState.style.display = 'none';
            }

            tasks.forEach(task => {
                addAutoInfoTask(task, ui);
            });
        }
    }

    // 任务排序
    function sortTasks(sortType, ui) {
        const taskItems = Array.from(document.querySelectorAll('.task-item'));

        // 根据不同的排序类型进行排序
        switch (sortType) {
            case 'timeAsc':
                taskItems.sort((a, b) => new Date(a.dataset.time) - new Date(b.dataset.time));
                break;
            case 'timeDesc':
                taskItems.sort((a, b) => new Date(b.dataset.time) - new Date(a.dataset.time));
                break;
            case 'status':
                const statusOrder = { 'pending': 0, 'running': 1, 'completed': 2, 'failed': 3 };
                taskItems.sort((a, b) => statusOrder[a.dataset.status] - statusOrder[b.dataset.status]);
                break;
            default:
                // 默认按创建时间排序
                taskItems.sort((a, b) => parseInt(a.dataset.id) - parseInt(b.dataset.id));
        }

        // 重新排列任务项
        taskItems.forEach(item => {
            ui.taskList.insertBefore(item, ui.emptyState);
        });
    }

    // 设置表单验证
    function setupFormValidation(ui) {
        if (!ui.messageInput || !ui.datetimeInput) return;

        ui.messageInput.addEventListener('input', function() {
            if (this.value.trim().length > 0) {
                this.classList.remove('input-error');
            }
        });

        ui.datetimeInput.addEventListener('change', function() {
            const currentTime = new Date();
            const selectedTime = new Date(this.value);
            if (selectedTime <= currentTime) {
                this.classList.add('input-error');
                showNotification('请选择一个未来的时间', 'error');
            } else {
                this.classList.remove('input-error');
            }
        });
    }

    // 显示通知
    function showNotification(message, type) {
        const notificationContainer = document.querySelector('.task-notification-container');
        if (!notificationContainer) return;

        // 创建通知元素
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} animate-fade-in`;
        alert.textContent = message;

        // 添加到容器
        notificationContainer.appendChild(alert);

        // 3秒后移除通知
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 3000);
    }

    // 获取状态文本
    function getStatusText(status) {
        switch (status) {
            case 'pending':
                return '待执行';
            case 'running':
                return '执行中';
            case 'completed':
                return '已完成';
            case 'failed':
                return '执行失败';
            default:
                return '待执行';
        }
    }
}

// 初始化欢迎区域动画
function initWelcomeAnimation() {
    const welcomeSection = document.querySelector('.welcome-section');
    if (!welcomeSection) return;

    // 添加淡入效果
    welcomeSection.style.opacity = '0';
    welcomeSection.style.transform = 'translateY(20px)';
    welcomeSection.style.transition = 'opacity 0.8s ease, transform 0.8s ease';

    // 当元素进入视口时触发动画
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                welcomeSection.style.opacity = '1';
                welcomeSection.style.transform = 'translateY(0)';

                // 数字动画
                animateNumbers();
                observer.disconnect();
            }
        });
    }, { threshold: 0.1 });

    observer.observe(welcomeSection);
}

// 数字动画 - 优化版
    function animateNumbers() {
        const statNumbers = document.querySelectorAll('.welcome-stat .stat-number');
        if (!statNumbers.length) return;

        // 使用requestAnimationFrame进行统一更新，减少重绘
        const duration = 2000; // 动画持续时间（毫秒）
        const startTime = performance.now();

        // 存储所有数字元素及其目标值
        const numberElements = Array.from(statNumbers).map(number => ({
            element: number,
            target: parseInt(number.textContent)
        }));

        // 统一更新函数
        function updateNumbers(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            numberElements.forEach(item => {
                const currentValue = Math.floor(item.target * progress);
                item.element.textContent = currentValue + '+';
                item.element.classList.add('count-animation');
            });

            if (progress < 1) {
                requestAnimationFrame(updateNumbers);
            }
        }

        requestAnimationFrame(updateNumbers);
    }

// 加载页面内容
function loadPageContent(page, url) {
    // 显示加载状态
    const contentArea = document.getElementById('content-area');
    if (!contentArea) return;

    contentArea.innerHTML = '<div style="display: flex; justify-content: center; align-items: center; height: 100%;"><div class="loader-spinner" style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid var(--primary-color); border-radius: 50%; animation: spin 1s linear infinite;"></div></div>';

    // 模拟异步加载
    setTimeout(() => {
        // 根据不同页面加载不同内容
        fetch(url)
            .then(response => response.text())
            .then(html => {
                // 提取页面主体内容
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                const newContent = tempDiv.querySelector('#content-area').innerHTML;
                contentArea.innerHTML = newContent;

                // 重新初始化页面特定的JavaScript
                initPageScripts(page);
            })
            .catch(error => {
                contentArea.innerHTML = '<div style="padding: 20px; text-align: center; color: #ff4d4f;">加载失败: ' + error.message + '</div>';
            });
    }, 300);
}

// 初始化页面特定的脚本
function initPageScripts(page) {
    // 根据页面类型执行不同的初始化
    if (page === 'auto_info') {
        // 检查auto_info.js是否已经加载
        if (typeof window.initForm !== 'function') {
            // 未加载则动态加载
            loadScript('/static/js/auto_info.js', function() {
                initAutoInfoPage();
            });
        } else {
            // 已加载则直接初始化
            initAutoInfoPage();
        }

        function initAutoInfoPage() {
            // 初始化任务列表
            if (document.getElementById('taskList')) {
                initAutoInfoTaskList();
            }
            
            // 初始化表单
            window.initForm();
            console.log('auto_info.js初始化函数已调用');
        }
    } else if (page === 'ai_takeover') {
        // 这里可以添加AI接管页面的初始化代码
    }

    // 重新绑定按钮点击态
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mousedown', function() {
            this.classList.add('button-pressed');
        });
        button.addEventListener('mouseup', function() {
            this.classList.remove('button-pressed');
        });
        button.addEventListener('mouseleave', function() {
            this.classList.remove('button-pressed');
        });
    });

    // 重新初始化执行按钮加载态
    const executeBtn = document.querySelector('.execute-btn');
    if (executeBtn) {
        executeBtn.addEventListener('click', function() {
            if (this.classList.contains('loading')) return;

            this.classList.add('loading');
            this.innerHTML = '<span class="spinner"></span> 执行中...';
            this.disabled = true;

            // 模拟执行完成
            setTimeout(() => {
                this.classList.remove('loading');
                this.innerHTML = '执行';
                this.disabled = false;
            }, 1500);
        });
    }
}

// 动态加载脚本
function loadScript(url, callback) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    script.onload = callback;
    document.head.appendChild(script);
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* 编辑和删除图标样式 */
.edit-icon::before {
    content: '✏️';
}

.delete-icon::before {
    content: '🗑️';
}
`;
document.head.appendChild(style);