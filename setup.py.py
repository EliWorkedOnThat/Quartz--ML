import os
import json
import platform

def create_dataset_folder():
    project_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(project_path, "Car_Preference_dataset")
    os.makedirs(dataset_path, exist_ok=True)
    return dataset_path

def write_config(dataset_path):
    config = {
        "dataset_path": dataset_path
    }
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    return config_path

def main():
    print(f"Detected OS: {platform.system()}")

    dataset_path = create_dataset_folder()
    print(f"Dataset folder ready at: {dataset_path}")

    config_path = write_config(dataset_path)
    print(f"Config written to: {config_path}")

    print("\nSetup complete. You can now run CarGUI.py to start collecting data.")

if __name__ == "__main__":
    main()