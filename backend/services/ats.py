from typing import List

DOMAIN_KEYWORDS = {
    "Yazılım": [
        "python", "java", "c#", "javascript", "algoritma", "veritabanı",
        "api", "rest", "mvc", "oop", "veri yapıları", "git", "docker"
    ],
    "Yapay Zeka": [
        "machine learning", "derin öğrenme", "pytorch", "tensorflow",
        "model", "doğal dil işleme", "computer vision", "neural network",
        "veri bilimi", "scikit-learn"
    ],
    "Siber Güvenlik": [
        "penetrasyon", "vulnerability", "firewall", "kripto", "şifreleme",
        "sızma testi", "network security", "IDS", "IPS", "SOC"
    ],
    "Ağ/Network": [
        "tcp/ip", "router", "switch", "vpn", "dns", "dhcp", "ospf",
        "routing", "firewall", "network topology"
    ],
}

def compute_ats_score(text: str, domain: str) -> tuple[int, List[str]]:
    text_lower = text.lower()
    keywords = DOMAIN_KEYWORDS.get(domain, [])
    found = [kw for kw in keywords if kw in text_lower]
    missing = [kw for kw in keywords if kw not in found]
    score = int(len(found) / len(keywords) * 100) if keywords else 0
    return score, missing