import json

# Load settings when the module is imported
try:
    with open("settings.json", "r") as f:
        settings = json.load(f)
except FileNotFoundError:
    print("Settings file not found. Creating a new one with default settings.")
    
    # Define default settings
    default_settings = {
        "webhooks": "",
        "prefix": ""
    }
    
    # Create or overwrite settings.json with default settings
    with open("settings.json", "w") as f:
        json.dump(default_settings, f, indent=4)
    settings = default_settings

# Function to access settings
def get_webhooks_url():
    return settings.get("webhooks", "")

def get_prefix():
    return settings.get("prefix", "")
