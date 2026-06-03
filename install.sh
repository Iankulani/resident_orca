#!/bin/bash

# Resident Orca - Installation Script
# Supports: Ubuntu/Debian, RHEL/CentOS, Fedora, Arch, macOS

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🐋 RESIDENT ORCA - INSTALLATION SCRIPT v1.0              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
            VER=$VERSION_ID
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    echo -e "${GREEN}✓ Detected OS: $OS${NC}"
}

# Install system dependencies
install_deps() {
    echo -e "\n${YELLOW}Installing system dependencies...${NC}"
    
    case $OS in
        ubuntu|debian)
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv \
                nmap whois dnsutils net-tools iputils-ping traceroute \
                curl wget git build-essential libpcap-dev iptables \
                tcpdump nikto
            ;;
        rhel|centos|fedora)
            sudo yum install -y python3 python3-pip nmap whois \
                bind-utils net-tools iputils traceroute curl wget \
                git gcc libpcap-devel iptables tcpdump
            ;;
        arch)
            sudo pacman -S --noconfirm python python-pip nmap \
                bind-tools net-tools iputils traceroute curl wget \
                git base-devel libpcap iptables tcpdump
            ;;
        macos)
            brew install python3 nmap whois bind net-tools \
                traceroute curl wget git libpcap iptables tcpdump
            ;;
        *)
            echo -e "${RED}Unsupported OS. Please install dependencies manually.${NC}"
            ;;
    esac
    
    echo -e "${GREEN}✓ System dependencies installed${NC}"
}

# Setup Python virtual environment
setup_venv() {
    echo -e "\n${YELLOW}Setting up Python virtual environment...${NC}"
    
    python3 -m venv orca_env
    source orca_env/bin/activate
    
    echo -e "${GREEN}✓ Virtual environment created${NC}"
}

# Install Python packages
install_python_packages() {
    echo -e "\n${YELLOW}Installing Python packages...${NC}"
    
    pip install --upgrade pip
    
    # Install with optimizations
    pip install --no-cache-dir \
        requests>=2.31.0 \
        paramiko>=3.3.0 \
        psutil>=5.9.0 \
        Flask>=2.3.0 \
        matplotlib>=3.7.0 \
        seaborn>=0.12.0 \
        numpy>=1.24.0 \
        reportlab>=4.0.0 \
        scapy>=2.5.0 \
        whois>=0.9.0 \
        qrcode>=7.4.0 \
        pyshorteners>=1.0.1 \
        discord.py>=2.3.0 \
        telethon>=1.34.0 \
        slack-sdk>=3.23.0 \
        colorama>=0.4.6
    
    echo -e "${GREEN}✓ Python packages installed${NC}"
}

# Create configuration directories
create_dirs() {
    echo -e "\n${YELLOW}Creating configuration directories...${NC}"
    
    mkdir -p .resident_orca/ssh_keys
    mkdir -p .resident_orca/phishing_pages
    mkdir -p orca_reports/graphics
    mkdir -p temp
    
    echo -e "${GREEN}✓ Directories created${NC}"
}

# Create config file
create_config() {
    echo -e "\n${YELLOW}Creating default configuration...${NC}"
    
    cat > .resident_orca/config.json << EOF
{
    "version": "1.0.0",
    "database": ".resident_orca/orca_data.db",
    "log_file": ".resident_orca/orca.log",
    "web_port": 5000,
    "phishing_port": 8080,
    "auto_start_web": true,
    "max_command_history": 1000,
    "threat_detection": true,
    "auto_block_threats": false
}
EOF
    
    echo -e "${GREEN}✓ Configuration created${NC}"
}

# Create launcher script
create_launcher() {
    echo -e "\n${YELLOW}Creating launcher script...${NC}"
    
    cat > run_orca.sh << 'EOF'
#!/bin/bash
source orca_env/bin/activate
python3 resident_orca.py "$@"
EOF
    
    chmod +x run_orca.sh
    
    echo -e "${GREEN}✓ Launcher created: ./run_orca.sh${NC}"
}

# Create desktop entry (Linux)
create_desktop_entry() {
    if [[ "$OS" != "macos" ]]; then
        cat > ~/.local/share/applications/resident-orca.desktop << EOF
[Desktop Entry]
Name=Resident Orca
Comment=Cybersecurity Command & Control Server
Exec=$(pwd)/run_orca.sh
Icon=$(pwd)/.resident_orca/orca_icon.png
Terminal=true
Type=Application
Categories=Network;Security;
EOF
        echo -e "${GREEN}✓ Desktop entry created${NC}"
    fi
}

# Main installation
main() {
    detect_os
    install_deps
    setup_venv
    install_python_packages
    create_dirs
    create_config
    create_launcher
    
    echo -e "\n${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ RESIDENT ORCA INSTALLATION COMPLETE!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "\n${YELLOW}To start Resident Orca:${NC}"
    echo -e "  ${BLUE}./run_orca.sh${NC}"
    echo -e "\n${YELLOW}To run in background:${NC}"
    echo -e "  ${BLUE}./run_orca.sh &${NC}"
    echo -e "\n${YELLOW}To run tests:${NC}"
    echo -e "  ${BLUE}source orca_env/bin/activate && python3 test_commands.py${NC}"
    echo -e "\n${YELLOW}Web Dashboard:${NC}"
    echo -e "  ${BLUE}http://localhost:5000${NC}"
    echo -e "\n${YELLOW}For help:${NC}"
    echo -e "  ${BLUE}type 'help' at the Orca prompt${NC}"
    echo -e "\n${GREEN}════════════════════════════════════════════════════════════════${NC}"
}

main "$@"