document.addEventListener('DOMContentLoaded', function() {
    initWelcomeAnimation();

    if (window.location.pathname === '/' && document.getElementById('taskList')) {
        loadAutoInfoTasks();
        setupFormValidation();
    }

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

    const repeatBtn = document.querySelector('.repeat-btn');
    const currentRepeat = repeatBtn ? repeatBtn.querySelector('.current-repeat') : null;
    const repeatOptions = document.querySelector('.repeat-options');
    const repeatItems = repeatOptions ? repeatOptions.querySelectorAll('.repeat-item') : [];

    if (repeatBtn && currentRepeat && repeatOptions) {
        repeatBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            repeatOptions.style.display = repeatOptions.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', function() {
            if (repeatOptions.style.display === 'block') {
                repeatOptions.style.display = 'none';
            }
        });

        repeatItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.stopPropagation();
                currentRepeat.textContent = this.textContent;
                repeatOptions.style.display = 'none';
            });
        });
    }
});

function initAutoInfoTaskList() {
    const taskList = document.getElementById('taskList');
    const addTaskBtn = document.getElementById('add-task-btn');
    const emptyState = document.querySelector('.empty-task-state');
    const toggleAdvancedSettings = document.querySelector('.toggle-advanced-settings');
    const advancedOptions = document.querySelector('.advanced-options');
    const saveBtn = document.getElementById('save-btn');
    const importBtn = document.getElementById('import-btn');
    const exportBtn = document.getElementById('export-btn');
    const executeAllBtn = document.getElementById('execute-all-btn');
    const sortSelect = document.getElementById('sort-select');

    if (!taskList) return;

    if (toggleAdvancedSettings && advancedOptions) {
        toggleAdvancedSettings.addEventListener('click', function() {
            const parent = this.closest('.advanced-settings');
            parent.classList.toggle('open');
            advancedOptions.style.maxHeight = advancedOptions.style.maxHeight ? null : advancedOptions.scrollHeight + 'px';
        });
    }

    loadAutoInfoTasks();
    setupFormValidation();

    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', function() {
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

            addAutoInfoTask(task);
            saveAutoInfoTasks();

            messageInput.value = '';
            datetimeInput.value = '';
            if (currentRepeat) {
                currentRepeat.textContent = '仅一次';
            }

            showNotification('任务添加成功', 'success');
        });
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            saveAutoInfoTasks();
            showNotification('任务已保存', 'success');
        });
    }

    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
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

    if (importBtn) {
        importBtn.addEventListener('click', function() {
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
                                const taskItems = document.querySelectorAll('.task-item');
                                taskItems.forEach(item => item.remove());

                                importedTasks.forEach(task => {
                                    if (task.text && task.time) {
                                        task.id = Date.now() + Math.floor(Math.random() * 1000);
                                        task.status = task.status || 'pending';
                                        addAutoInfoTask(task);
                                    }
                                });

                                saveAutoInfoTasks();

                                if (emptyState && importedTasks.length > 0) {
                                    emptyState.style.display = 'none';
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

    if (executeAllBtn) {
        executeAllBtn.addEventListener('click', function() {
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

    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            sortTasks(this.value);
        });
    }

    function addAutoInfoTask(task) {
        if (emptyState) {
            emptyState.style.display = 'none';
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

        const deleteBtn = taskItem.querySelector('.task-action-btn.delete');
        deleteBtn.addEventListener('click', function() {
            taskItem.style.height = taskItem.offsetHeight + 'px';
            taskItem.style.overflow = 'hidden';
            taskItem.style.transition = 'all 0.3s';
            taskItem.style.opacity = '0';
            taskItem.style.transform = 'translateX(-20px)';

            setTimeout(() => {
                taskItem.remove();
                saveAutoInfoTasks();

                const taskItems = document.querySelectorAll('.task-item');
                if (taskItems.length === 0 && emptyState) {
                    emptyState.style.display = 'flex';
                }

                showNotification('任务已删除', 'info');
            }, 300);
        });

        const editBtn = taskItem.querySelector('.task-action-btn.edit');
        editBtn.addEventListener('click', function() {
            const messageInput = document.querySelector('.message-input');
            const datetimeInput = document.querySelector('.datetime-input');
            const repeatBtn = document.querySelector('.repeat-btn');
            const currentRepeat = repeatBtn ? repeatBtn.querySelector('.current-repeat') : null;

            if (messageInput && datetimeInput && currentRepeat) {
                messageInput.value = task.text;
                datetimeInput.value = task.time;
                currentRepeat.textContent = task.repeat;

                taskItem.remove();
                saveAutoInfoTasks();

                const taskItems = document.querySelectorAll('.task-item');
                if (taskItems.length === 0 && emptyState) {
                    emptyState.style.display = 'flex';
                }
            }
        });

        const executeBtn = taskItem.querySelector('.task-action-btn.execute');
        executeBtn.addEventListener('click', function() {
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
                saveAutoInfoTasks();
                showNotification('任务执行完成', 'success');
            }, 2000);
        });

        taskList.insertBefore(taskItem, emptyState);

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

    function saveAutoInfoTasks() {
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

    function loadAutoInfoTasks() {
        const tasks = JSON.parse(localStorage.getItem('autoInfoTasks') || '[]');

        if (tasks.length > 0) {
            if (emptyState) {
                emptyState.style.display = 'none';
            }

            tasks.forEach(task => {
                addAutoInfoTask(task);
            });
        }
    }

    // 任务排序
    function sortTasks(sortType) {
        const taskItems = Array.from(document.querySelectorAll('.task-item'));
        const emptyState = document.querySelector('.empty-task-state');

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
            taskList.insertBefore(item, emptyState);
        });
    }

    // 设置表单验证
    function setupFormValidation() {
        const messageInput = document.querySelector('.message-input');
        const datetimeInput = document.querySelector('.datetime-input');

        if (messageInput) {
            messageInput.addEventListener('input', function() {
                if (this.value.trim().length > 0) {
                    this.classList.remove('input-error');
                }
            });
        }

        if (datetimeInput) {
            datetimeInput.addEventListener('change', function() {
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
        const statusMap = {
            'pending': '待执行',
            'running': '执行中',
            'completed': '已完成',
            'failed': '执行失败'
        };
        return statusMap[status] || '待执行';
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

// 数字动画
function animateNumbers() {
    const statNumbers = document.querySelectorAll('.welcome-stat .stat-number');
    if (!statNumbers.length) return;

    statNumbers.forEach(number => {
        const target = parseInt(number.textContent);
        let count = 0;
        const duration = 2000; // 动画持续时间（毫秒）
        const step = target / (duration / 16); // 每16ms更新一次

        number.classList.add('count-animation');

        const updateCount = () => {
            count += step;
            if (count < target) {
                number.textContent = Math.floor(count) + '+';
                requestAnimationFrame(updateCount);
            } else {
                number.textContent = target + '+';
            }
        };

        updateCount();
    });
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
        // 强制加载auto_info.js文件，确保初始化函数可用
        loadScript('/static/js/auto_info.js', function() {
            // 初始化任务列表
            if (document.getElementById('taskList')) {
                initAutoInfoTaskList();
            }
            
            // 初始化表单
            if (typeof window.initForm === 'function') {
                window.initForm();
                console.log('auto_info.js初始化函数已调用');
            } else {
                console.error('无法找到initForm函数');
            }
        });
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