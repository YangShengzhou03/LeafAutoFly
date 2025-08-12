import os


def create_directory(path):
    """创建目录，已存在则跳过"""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"✅ 目录: {path}")
    except Exception as e:
        print(f"❌ 目录创建失败 {path}: {e}")


def create_file(path):
    """创建空文件，已存在则跳过"""
    if os.path.exists(path):
        print(f"ℹ️ 文件已存在: {path}")
        return

    try:
        with open(path, 'w', encoding='utf-8') as f:
            pass  # 创建空文件
        print(f"✅ 文件: {path}")
    except Exception as e:
        print(f"❌ 文件创建失败 {path}: {e}")


def main():
    # 项目根目录
    root = os.path.abspath("WeChatAutomation")
    create_directory(root)

    # 根目录文件
    create_file(os.path.join(root, "README.md"))
    create_file(os.path.join(root, "LICENSE"))
    create_file(os.path.join(root, ".gitignore"))
    create_file(os.path.join(root, "start.bat"))
    create_file(os.path.join(root, "docker-compose.yml"))

    # 后端目录结构
    backend = os.path.join(root, "backend")
    create_directory(backend)

    # 后端根文件
    create_file(os.path.join(backend, "run.py"))
    create_file(os.path.join(backend, "manage.py"))
    create_file(os.path.join(backend, "requirements.txt"))
    create_file(os.path.join(backend, "requirements-dev.txt"))
    create_file(os.path.join(backend, ".env"))
    create_file(os.path.join(backend, ".env.example"))
    create_file(os.path.join(backend, ".gitignore"))
    create_file(os.path.join(backend, "Dockerfile"))

    # 后端应用目录
    backend_app = os.path.join(backend, "app")
    create_directory(backend_app)
    create_file(os.path.join(backend_app, "__init__.py"))
    create_file(os.path.join(backend_app, "config.py"))

    # 后端核心模块
    backend_core = os.path.join(backend_app, "core")
    create_directory(backend_core)
    create_file(os.path.join(backend_core, "__init__.py"))
    create_file(os.path.join(backend_core, "wechat.py"))
    create_file(os.path.join(backend_core, "scheduler.py"))
    create_file(os.path.join(backend_core, "ai.py"))

    # 后端路由
    backend_routes = os.path.join(backend_app, "routes")
    create_directory(backend_routes)
    create_file(os.path.join(backend_routes, "__init__.py"))
    create_file(os.path.join(backend_routes, "api.py"))
    create_file(os.path.join(backend_routes, "auth.py"))
    create_file(os.path.join(backend_routes, "main.py"))

    # 后端服务层
    backend_services = os.path.join(backend_app, "services")
    create_directory(backend_services)
    create_file(os.path.join(backend_services, "__init__.py"))
    create_file(os.path.join(backend_services, "task_service.py"))
    create_file(os.path.join(backend_services, "ai_service.py"))

    # 后端工具类
    backend_utils = os.path.join(backend_app, "utils")
    create_directory(backend_utils)
    create_file(os.path.join(backend_utils, "__init__.py"))
    create_file(os.path.join(backend_utils, "helpers.py"))
    create_file(os.path.join(backend_utils, "validators.py"))

    # 后端数据存储
    backend_data = os.path.join(backend, "data")
    create_directory(backend_data)
    create_file(os.path.join(backend_data, ".gitkeep"))
    create_file(os.path.join(backend_data, "tasks.json"))
    create_file(os.path.join(backend_data, "contacts.json"))
    create_file(os.path.join(backend_data, "users.json"))

    # 后端日志
    backend_logs = os.path.join(backend, "logs")
    create_directory(backend_logs)
    create_file(os.path.join(backend_logs, ".gitkeep"))

    # 后端测试
    backend_tests = os.path.join(backend, "tests")
    create_directory(backend_tests)
    create_file(os.path.join(backend_tests, "__init__.py"))
    create_file(os.path.join(backend_tests, "test_api.py"))
    create_file(os.path.join(backend_tests, "test_tasks.py"))

    # 前端目录结构
    frontend = os.path.join(root, "frontend")
    create_directory(frontend)

    # 前端根文件
    create_file(os.path.join(frontend, "package.json"))
    create_file(os.path.join(frontend, "package-lock.json"))
    create_file(os.path.join(frontend, "vue.config.js"))
    create_file(os.path.join(frontend, "babel.config.js"))
    create_file(os.path.join(frontend, ".env"))
    create_file(os.path.join(frontend, ".env.development"))
    create_file(os.path.join(frontend, ".env.production"))
    create_file(os.path.join(frontend, ".gitignore"))
    create_file(os.path.join(frontend, "Dockerfile"))

    # 前端public目录
    frontend_public = os.path.join(frontend, "public")
    create_directory(frontend_public)
    create_file(os.path.join(frontend_public, "index.html"))
    create_file(os.path.join(frontend_public, "favicon.ico"))
    create_file(os.path.join(frontend_public, "robots.txt"))

    # 前端src目录
    frontend_src = os.path.join(frontend, "src")
    create_directory(frontend_src)
    create_file(os.path.join(frontend_src, "main.js"))
    create_file(os.path.join(frontend_src, "App.vue"))

    # 前端API
    frontend_api = os.path.join(frontend_src, "api")
    create_directory(frontend_api)
    create_file(os.path.join(frontend_api, "__init__.py"))
    create_file(os.path.join(frontend_api, "client.js"))
    create_file(os.path.join(frontend_api, "auth.js"))
    create_file(os.path.join(frontend_api, "tasks.js"))
    create_file(os.path.join(frontend_api, "ai.js"))
    create_file(os.path.join(frontend_api, "user.js"))

    # 前端组件
    frontend_components = os.path.join(frontend_src, "components")
    create_directory(frontend_components)

    # 布局组件
    frontend_layout = os.path.join(frontend_components, "layout")
    create_directory(frontend_layout)
    create_file(os.path.join(frontend_layout, "Layout.vue"))
    create_file(os.path.join(frontend_layout, "Navbar.vue"))
    create_file(os.path.join(frontend_layout, "Sidebar.vue"))
    create_file(os.path.join(frontend_layout, "Footer.vue"))

    # 通用组件
    frontend_common = os.path.join(frontend_components, "common")
    create_directory(frontend_common)
    create_file(os.path.join(frontend_common, "BaseButton.vue"))
    create_file(os.path.join(frontend_common, "Card.vue"))
    create_file(os.path.join(frontend_common, "Modal.vue"))
    create_file(os.path.join(frontend_common, "Table.vue"))
    create_file(os.path.join(frontend_common, "Form.vue"))
    create_file(os.path.join(frontend_common, "Loading.vue"))

    # 任务相关组件
    frontend_task = os.path.join(frontend_components, "task")
    create_directory(frontend_task)
    create_file(os.path.join(frontend_task, "TaskForm.vue"))
    create_file(os.path.join(frontend_task, "TaskList.vue"))
    create_file(os.path.join(frontend_task, "TaskCalendar.vue"))
    create_file(os.path.join(frontend_task, "TaskDetail.vue"))

    # AI相关组件
    frontend_ai = os.path.join(frontend_components, "ai")
    create_directory(frontend_ai)
    create_file(os.path.join(frontend_ai, "AiSetting.vue"))
    create_file(os.path.join(frontend_ai, "ReplyTemplate.vue"))
    create_file(os.path.join(frontend_ai, "ChatHistory.vue"))

    # 前端视图
    frontend_views = os.path.join(frontend_src, "views")
    create_directory(frontend_views)

    # 仪表盘
    frontend_dashboard = os.path.join(frontend_views, "dashboard")
    create_directory(frontend_dashboard)
    create_file(os.path.join(frontend_dashboard, "Dashboard.vue"))
    create_file(os.path.join(frontend_dashboard, "Statistics.vue"))
    create_file(os.path.join(frontend_dashboard, "RecentActivity.vue"))

    # 任务调度
    frontend_task_view = os.path.join(frontend_views, "task")
    create_directory(frontend_task_view)
    create_file(os.path.join(frontend_task_view, "TaskScheduler.vue"))
    create_file(os.path.join(frontend_task_view, "CreateTask.vue"))
    create_file(os.path.join(frontend_task_view, "EditTask.vue"))
    create_file(os.path.join(frontend_task_view, "TaskLog.vue"))

    # AI接管
    frontend_ai_view = os.path.join(frontend_views, "ai")
    create_directory(frontend_ai_view)
    create_file(os.path.join(frontend_ai_view, "AiTakeover.vue"))
    create_file(os.path.join(frontend_ai_view, "AiSettings.vue"))
    create_file(os.path.join(frontend_ai_view, "TemplateManager.vue"))

    # 个人中心
    frontend_profile = os.path.join(frontend_views, "profile")
    create_directory(frontend_profile)
    create_file(os.path.join(frontend_profile, "Profile.vue"))
    create_file(os.path.join(frontend_profile, "AccountSettings.vue"))
    create_file(os.path.join(frontend_profile, "SecuritySettings.vue"))

    # 认证页面
    frontend_auth = os.path.join(frontend_views, "auth")
    create_directory(frontend_auth)
    create_file(os.path.join(frontend_auth, "Login.vue"))
    create_file(os.path.join(frontend_auth, "Register.vue"))
    create_file(os.path.join(frontend_auth, "ForgotPassword.vue"))

    # 错误页面
    frontend_errors = os.path.join(frontend_views, "errors")
    create_directory(frontend_errors)
    create_file(os.path.join(frontend_errors, "404.vue"))
    create_file(os.path.join(frontend_errors, "403.vue"))
    create_file(os.path.join(frontend_errors, "500.vue"))

    # 前端路由
    frontend_router = os.path.join(frontend_src, "router")
    create_directory(frontend_router)
    create_file(os.path.join(frontend_router, "index.js"))
    create_file(os.path.join(frontend_router, "routes.js"))

    # 前端状态管理
    frontend_store = os.path.join(frontend_src, "store")
    create_directory(frontend_store)
    create_file(os.path.join(frontend_store, "index.js"))

    # Vuex模块
    frontend_store_modules = os.path.join(frontend_store, "modules")
    create_directory(frontend_store_modules)
    create_file(os.path.join(frontend_store_modules, "auth.js"))
    create_file(os.path.join(frontend_store_modules, "tasks.js"))
    create_file(os.path.join(frontend_store_modules, "ai.js"))
    create_file(os.path.join(frontend_store_modules, "user.js"))
    create_file(os.path.join(frontend_store_modules, "dashboard.js"))

    # 前端工具
    frontend_utils = os.path.join(frontend_src, "utils")
    create_directory(frontend_utils)
    create_file(os.path.join(frontend_utils, "auth.js"))
    create_file(os.path.join(frontend_utils, "date.js"))
    create_file(os.path.join(frontend_utils, "format.js"))
    create_file(os.path.join(frontend_utils, "validation.js"))

    # 前端资产
    frontend_assets = os.path.join(frontend_src, "assets")
    create_directory(frontend_assets)

    # 图片
    frontend_images = os.path.join(frontend_assets, "images")
    create_directory(frontend_images)
    create_file(os.path.join(frontend_images, ".gitkeep"))

    # 样式
    frontend_styles = os.path.join(frontend_assets, "styles")
    create_directory(frontend_styles)
    create_file(os.path.join(frontend_styles, "index.scss"))
    create_file(os.path.join(frontend_styles, "variables.scss"))
    create_file(os.path.join(frontend_styles, "mixins.scss"))
    create_file(os.path.join(frontend_styles, "common.scss"))

    print("\n🎉 项目结构创建完成！")
    print(f"项目路径: {root}")


if __name__ == "__main__":
    main()
