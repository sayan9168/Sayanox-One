from .crawler import run as crawl
from .sqli_scan import test_sqli
from .xss_scan import run as scan_xss
from .fuzzer import run as fuzz_paths
from .waf_detector import run as detect_waf

def run_web_scan(targets, config, runner):
    out = {}
    for url in targets:
        out[url] = {
            "waf": detect_waf(url, config),
            "crawled": crawl(url, config),
            "sqli": test_sqli(url, {}, None),
            "xss": scan_xss(url, config),
            "dirs": fuzz_paths(url, config)
        }
    return out
