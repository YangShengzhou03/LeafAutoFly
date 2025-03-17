import subprocess
from pyinjector import inject


def inject_dll():
    process_name = "WeChat.exe"
    dll_path = r"dll_file/Dll.dll"

    def get_process_pid(process_name):
        try:
            result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {process_name}', '/FO', 'CSV'],
                                    capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                pid = lines[1].split(',')[1].strip('"')
                return int(pid)
            else:
                print(f"未找到进程: {process_name}")
                return None
        except Exception as e:
            print(f"获取进程PID失败: {e}")
            return None

    pid = get_process_pid(process_name)
    if pid is None:
        return
    try:
        inject(pid, dll_path)
        print(f"成功将DLL注入到进程 {pid}")
    except Exception as e:
        print(f"注入DLL失败：{e}")


if __name__ == '__main__':
    inject_dll()
