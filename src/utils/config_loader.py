
import yaml
import os

def load_config(config_path="config/analysis_config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"File not found")
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config
