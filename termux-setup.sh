#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing Python and dependencies..."
pkg install -y python python-pip clang ninja make cmake git rust binutils libxml2 libxslt

echo "[*] Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Checking for root access..."
if [ "$(id -u)" = "0" ]; then
    echo "[+] Root detected - Layer4 methods (SYN, ICMP, AMP) will work"
else
    echo "[!] No root access - Layer4 methods (SYN, ICMP, AMP, OVH-UDP) will NOT work"
    echo "    Layer7 methods (GET, POST, CFB, etc.) will work fine"
fi

echo ""
echo "[*] Installation complete!"
echo ""
echo "Usage examples:"
echo "  Layer7: python start.py GET http://example.com 5 100 proxy.txt 10 60"
echo "  Layer4: python start.py UDP 1.2.3.4:80 100 60"
echo "  Tools:  python start.py tools"
echo ""
echo "NOTE: On Android, methods using raw sockets (SYN, ICMP, etc.)"
echo "      require root. Run 'tsu' first if you need these methods."
