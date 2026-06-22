class DecisionEngine:
    def __init__(self, config):
        self.cfg = config
        self.context = {}

    def update_context(self, results):
        self.context.update(results)

    def select_network_targets(self):
        return self.context.get("recon", {}).get("network_targets", [])

    def select_web_targets(self):
        subs = self.context.get("recon", {}).get("subdomains", {}).get("subdomains", [])
        return [f"https://{s}" for s in subs]

    def get_auth_candidates(self):
        return []

    def get_vuln_candidates(self):
        return []
      
