#!/bin/bash

# 1. 确保在 frp 解压目录中（当前目录应该有 frpc 文件）
echo "当前目录：$(pwd)"
ls -lh frpc

# 2. 复制 frpc 到系统路径
sudo cp frpc /usr/local/bin/
echo "✓ frpc 已复制到 /usr/local/bin/"

# 3. 创建配置目录
sudo mkdir -p /etc/frp
echo "✓ 配置目录已创建"

# 4. 创建 frpc 配置文件
sudo tee /etc/frp/frpc.toml << 'EOF'
serverAddr = "154.201.94.86"
serverPort = 7000

[[proxies]]
name = "lingshi-api"
type = "http"
localIP = "127.0.0.1"
localPort = 5050
customDomains = ["154.201.94.86"]
EOF
echo "✓ 配置文件已创建"

# 5. 创建 systemd 服务文件
sudo tee /etc/systemd/system/frpc.service << 'EOF'
[Unit]
Description=FRP Client Service
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/frpc -c /etc/frp/frpc.toml
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
EOF
echo "✓ systemd 服务文件已创建"

# 6. 测试配置文件语法
echo "测试配置文件..."
/usr/local/bin/frpc verify -c /etc/frp/frpc.toml
if [ $? -eq 0 ]; then
    echo "✓ 配置文件验证通过"
else
    echo "✗ 配置文件有误，请检查"
    exit 1
fi

# 7. 重载 systemd 并启动服务
sudo systemctl daemon-reload
sudo systemctl enable frpc
sudo systemctl start frpc

# 8. 查看服务状态
echo ""
echo "=== 服务状态 ==="
sudo systemctl status frpc --no-pager

# 9. 查看最近日志
echo ""
echo "=== 最近日志 ==="
sudo journalctl -u frpc -n 20 --no-pager

# 10. 提示后续操作
echo ""
echo "=== 安装完成 ==="
echo "启动命令: sudo systemctl start frpc"
echo "停止命令: sudo systemctl stop frpc"
echo "重启命令: sudo systemctl restart frpc"
echo "查看状态: sudo systemctl status frpc"
echo "查看日志: sudo journalctl -u frpc -f"
