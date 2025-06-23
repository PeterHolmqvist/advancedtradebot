# File: mode_manager.py

import json

class ModeManager:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.mode = self.config.get("mode", "grid")

    def get_mode(self):
        return self.mode

    def set_mode(self, new_mode):
        if new_mode in ["grid", "trend", "volatility"]:
            self.mode = new_mode
            self.config["mode"] = new_mode
            with open("config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        return False

    def get_config(self):
        return self.config


if __name__ == "__main__":
    mm = ModeManager()
    print("Current mode:", mm.get_mode())