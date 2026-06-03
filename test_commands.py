#!/usr/bin/env python3
"""
Resident Orca - Command Test Suite
Tests all major command functionalities
"""

import subprocess
import json
import time
import sys
from typing import Dict, List, Tuple

class OrcaTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def run_test(self, name: str, command: str, expected_success: bool = True, timeout: int = 30) -> bool:
        """Run a single test"""
        print(f"\n{'='*60}")
        print(f"TEST: {name}")
        print(f"Command: {command}")
        print(f"{'='*60}")
        
        try:
            result = subprocess.run(
                f'echo "{command}" | python3 resident_orca.py --test-mode',
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0 if expected_success else result.returncode != 0
            
            if success:
                print(f"✅ PASSED")
                self.passed += 1
            else:
                print(f"❌ FAILED")
                print(f"Output: {result.stdout[:500]}")
                if result.stderr:
                    print(f"Error: {result.stderr[:500]}")
                self.failed += 1
            
            self.results.append({
                'name': name,
                'passed': success,
                'output': result.stdout[:1000]
            })
            return success
            
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT")
            self.failed += 1
            return False
        except Exception as e:
            print(f"💥 ERROR: {e}")
            self.failed += 1
            return False
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*70)
        print("🐋 RESIDENT ORCA - COMPLETE TEST SUITE")
        print("="*70)
        
        # Basic Commands
        tests = [
            ("System Info", "system", True, 10),
            ("Current Time", "time", True, 5),
            ("Current Date", "date", True, 5),
            ("System Status", "status", True, 10),
            
            # Network Tests
            ("Ping Localhost", "ping 127.0.0.1", True, 15),
            ("Ping Google DNS", "ping 8.8.8.8", True, 15),
            ("DNS Lookup", "dns google.com", True, 10),
            ("WHOIS Lookup", "whois google.com", True, 20),
            ("IP Location", "location 8.8.8.8", True, 10),
            
            # IP Management
            ("Add IP", "add_ip 192.168.1.1", True, 5),
            ("List IPs", "list_ips", True, 5),
            ("Remove IP", "remove_ip 192.168.1.1", True, 5),
            
            # Traffic Types
            ("Traffic Types", "traffic_types", True, 5),
            
            # SSH Commands (if SSH available)
            ("SSH List", "ssh_list", True, 5),
            
            # Phishing Commands
            ("Generate Facebook Phish", "generate_phishing_link_for_facebook", True, 5),
            ("Generate Instagram Phish", "generate_phishing_link_for_instagram", True, 5),
            ("Phishing Links", "phishing_links", True, 5),
            
            # Threat Detection
            ("Recent Threats", "threats 5", True, 5),
            
            # Report Generation
            ("Security Report", "report", True, 10),
        ]
        
        for test in tests:
            self.run_test(*test)
            time.sleep(1)  # Small delay between tests
        
        # Traffic Generation Test (if enabled)
        print("\n" + "="*60)
        print("⚠️  TRAFFIC GENERATION TEST (requires permission)")
        print("="*60)
        response = input("Run traffic generation test? (y/n): ").strip().lower()
        if response == 'y':
            self.run_test("ICMP Traffic", "generate_traffic icmp 127.0.0.1 5", True, 10)
        
        # Nikto Test (if installed)
        if subprocess.run(['which', 'nikto'], capture_output=True).returncode == 0:
            print("\n" + "="*60)
            print("⚠️  NIKTO SCAN TEST (requires target permission)")
            print("="*60)
            response = input("Run Nikto test? (y/n): ").strip().lower()
            if response == 'y':
                self.run_test("Nikto Scan", "nikto scanme.nmap.org", True, 120)
        
        # Print Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        
        print(f"\n✅ PASSED: {self.passed}")
        print(f"❌ FAILED: {self.failed}")
        print(f"📈 TOTAL: {self.passed + self.failed}")
        print(f"🏆 SUCCESS RATE: {(self.passed/(self.passed+self.failed)*100):.1f}%")
        
        if self.failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if not result['passed']:
                    print(f"  - {result['name']}")
        
        # Save results
        with open('test_results.json', 'w') as f:
            json.dump({
                'timestamp': time.time(),
                'passed': self.passed,
                'failed': self.failed,
                'results': self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results.json")
        print("="*70)

def main():
    tester = OrcaTester()
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🐋 RESIDENT ORCA - AUTOMATED TEST SUITE v1.0            ║
    ║                                                              ║
    ║  This will test all major functionality of the Orca C2      ║
    ║  framework. Some tests require network access and may       ║
    ║  take several minutes to complete.                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    response = input("Run all tests? (y/n): ").strip().lower()
    if response == 'y':
        tester.run_all_tests()
    else:
        print("Test cancelled.")

if __name__ == "__main__":
    main()