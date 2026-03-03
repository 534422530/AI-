#!/usr/bin/env python3
"""
IP扫描工具 - 扫描本地网络中的所有设备
作者: 老四
"""

import socket
import subprocess
import platform
import concurrent.futures
import re
from typing import List, Tuple
import argparse


def get_local_network() -> str:
    """获取本机所在的网段"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    # 获取网段前缀 (如 192.168.1)
    parts = local_ip.split('.')
    network_prefix = '.'.join(parts[:3])
    return network_prefix


def ping_ip(ip: str, timeout: int = 1) -> Tuple[str, bool]:
    """Ping单个IP地址，返回(IP, 是否在线)"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        result = subprocess.run(
            ['ping', param, '1', '-w', str(timeout * 1000), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )
        return (ip, result.returncode == 0)
    except subprocess.TimeoutExpired:
        return (ip, False)
    except Exception:
        return (ip, False)


def arp_scan(ip: str) -> str:
    """通过ARP表获取设备MAC地址"""
    try:
        if platform.system().lower() == 'windows':
            result = subprocess.run(
                ['arp', '-a', ip],
                capture_output=True,
                text=True,
                timeout=2
            )
            # 解析MAC地址
            match = re.search(r'([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})', result.stdout)
            if match:
                return match.group(1)
        else:
            result = subprocess.run(
                ['arp', '-n', ip],
                capture_output=True,
                text=True,
                timeout=2
            )
            match = re.search(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})', result.stdout)
            if match:
                return match.group(1)
    except Exception:
        pass
    return "N/A"


def get_hostname(ip: str) -> str:
    """尝试获取设备主机名"""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return "N/A"
    except Exception:
        return "N/A"


def scan_network(network_prefix: str = None, start: int = 1, end: int = 254, workers: int = 50) -> List[Tuple[str, str, str, str]]:
    """
    扫描指定网段的所有IP
    返回: [(IP, MAC地址, 主机名, 状态), ...]
    """
    if network_prefix is None:
        network_prefix = get_local_network()
    
    print(f"\n正在扫描网段: {network_prefix}.0/24")
    print(f"扫描范围: {network_prefix}.{start} - {network_prefix}.{end}")
    print("-" * 60)
    
    # 生成所有IP地址
    ip_list = [f"{network_prefix}.{i}" for i in range(start, end + 1)]
    
    online_devices = []
    checked = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(ping_ip, ip): ip for ip in ip_list}
        
        for future in concurrent.futures.as_completed(futures):
            ip, is_online = future.result()
            checked += 1
            
            if is_online:
                mac = arp_scan(ip)
                hostname = get_hostname(ip)
                online_devices.append((ip, mac, hostname))
                print(f"[在线] {ip:<15} MAC: {mac:<20} 主机名: {hostname}")
            
            # 进度显示
            if checked % 20 == 0:
                print(f"进度: {checked}/{len(ip_list)}", end='\r')
    
    return online_devices


def scan_all_networks(workers: int = 100, skip_private: bool = False) -> List[Tuple[str, str, str]]:
    """
    扫描所有网段 (慎用！扫描整个互联网IP范围)
    skip_private: 是否跳过私有IP段
    """
    online_devices = []
    total_ips = 256 * 256 * 256 * 256  # 约43亿个IP
    checked = 0
    
    print("\n⚠️  警告: 正在扫描全部IP网段，这将需要很长时间！")
    print("建议使用 Ctrl+C 中断扫描")
    print("=" * 60)
    
    # 私有IP段范围
    private_ranges = [
        (10, 10),           # 10.0.0.0/8
        (172, 172),         # 172.16.0.0/12 (简化处理)
        (192, 192),         # 192.168.0.0/16
    ]
    
    def should_skip(first_octet: int) -> bool:
        if not skip_private:
            return False
        for start, end in private_ranges:
            if start <= first_octet <= end:
                return True
        return False
    
    try:
        for first in range(1, 256):  # 第一段 1-255
            if should_skip(first):
                print(f"跳过私有网段: {first}.x.x.x")
                continue
            
            for second in range(0, 256):  # 第二段 0-255
                for third in range(0, 256):  # 第三段 0-255
                    ip_list = [f"{first}.{second}.{third}.{fourth}" for fourth in range(1, 255)]
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                        futures = {executor.submit(ping_ip, ip, timeout=0.5): ip for ip in ip_list}
                        
                        for future in concurrent.futures.as_completed(futures):
                            ip, is_online = future.result()
                            checked += 1
                            
                            if is_online:
                                mac = arp_scan(ip)
                                hostname = get_hostname(ip)
                                online_devices.append((ip, mac, hostname))
                                print(f"[在线] {ip:<15} MAC: {mac:<20} 主机名: {hostname}")
                            
                            if checked % 100 == 0:
                                percent = (checked / total_ips) * 100
                                print(f"进度: {checked}/{total_ips} ({percent:.6f}%)", end='\r')
                    
                    if checked % 10000 == 0:
                        print(f"\n已扫描: {checked} 个IP, 发现: {len(online_devices)} 台设备")
                        
    except KeyboardInterrupt:
        print(f"\n\n用户中断扫描！已扫描 {checked} 个IP")
    
    return online_devices


def scan_multiple_networks(networks: List[str], workers: int = 50) -> List[Tuple[str, str, str]]:
    """
    扫描多个指定网段
    networks: 网段列表，如 ['192.168.1', '192.168.0', '10.0.0']
    """
    all_devices = []
    
    for network_prefix in networks:
        print(f"\n{'='*60}")
        print(f"正在扫描网段: {network_prefix}.0/24")
        devices = scan_network(network_prefix=network_prefix, workers=workers)
        all_devices.extend(devices)
    
    return all_devices


def save_results(devices: List[Tuple], filename: str = "scan_results.txt"):
    """保存扫描结果到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("IP扫描结果\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'IP地址':<18} {'MAC地址':<22} {'主机名':<20}\n")
        f.write("-" * 60 + "\n")
        for ip, mac, hostname in devices:
            f.write(f"{ip:<18} {mac:<22} {hostname:<20}\n")
        f.write(f"\n共发现 {len(devices)} 台在线设备\n")
    print(f"\n结果已保存到: {filename}")


def main():
    parser = argparse.ArgumentParser(description='IP扫描工具 - 扫描本地网络设备')
    parser.add_argument('-n', '--network', type=str, help='指定网段 (如 192.168.1)')
    parser.add_argument('-s', '--start', type=int, default=1, help='起始IP (默认1)')
    parser.add_argument('-e', '--end', type=int, default=254, help='结束IP (默认254)')
    parser.add_argument('-w', '--workers', type=int, default=50, help='并发线程数 (默认50)')
    parser.add_argument('-o', '--output', type=str, help='保存结果到文件')
    parser.add_argument('--all', action='store_true', help='扫描全部IP网段 (慎用！)')
    parser.add_argument('--skip-private', action='store_true', help='扫描全部网段时跳过私有IP')
    parser.add_argument('--multi', type=str, help='扫描多个网段，用逗号分隔 (如 192.168.1,192.168.0,10.0.0)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("IP扫描工具 - 老四")
    print("=" * 60)
    
    # 根据参数选择扫描模式
    if args.all:
        devices = scan_all_networks(workers=args.workers, skip_private=args.skip_private)
    elif args.multi:
        networks = [n.strip() for n in args.multi.split(',')]
        devices = scan_multiple_networks(networks=networks, workers=args.workers)
    else:
        devices = scan_network(
            network_prefix=args.network,
            start=args.start,
            end=args.end,
            workers=args.workers
        )
    
    print("\n" + "=" * 60)
    print(f"扫描完成! 共发现 {len(devices)} 台在线设备")
    print("=" * 60)
    
    # 显示结果表格
    if devices:
        print(f"\n{'IP地址':<18} {'MAC地址':<22} {'主机名':<20}")
        print("-" * 60)
        for ip, mac, hostname in devices:
            print(f"{ip:<18} {mac:<22} {hostname:<20}")
    
    # 保存结果
    if args.output:
        save_results(devices, args.output)
    elif devices:
        save = input("\n是否保存结果到文件? (y/n): ").lower()
        if save == 'y':
            filename = input("文件名 (默认 scan_results.txt): ").strip()
            filename = filename if filename else "scan_results.txt"
            save_results(devices, filename)


if __name__ == "__main__":
    main()
