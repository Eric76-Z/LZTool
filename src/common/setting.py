# 获取根目录
from os.path import dirname, abspath

base_dir = dirname(dirname(abspath(__file__)))
main_ui_path = 'ui/lztMain.ui'
start_ui_path = 'ui/start.ui'