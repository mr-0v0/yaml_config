import yaml
import os


def recursive_replace_with_value(data):
    if isinstance(data, dict):
        for key in list(data.keys()):
            data[key] = recursive_replace_with_value(data[key])
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            data[idx] = recursive_replace_with_value(item)
    elif isinstance(data, str) and data.startswith("$"):
        var = os.environ.get(data[1:])
        if var:
            data = var
        else:
            print(f"{data[1:]} not found in env")
    return data


def recursive_replace_with_variable(data, existing_data):
    if isinstance(data, dict):
        for key in list(data.keys()):
            if key in existing_data.keys():
                data[key] = recursive_replace_with_variable(data[key], existing_data[key])
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            data[idx] = recursive_replace_with_variable(item, item)
    elif isinstance(data, str) and existing_data.startswith("$"):
        data = existing_data
    return data


def read_config(file_name: str) -> dict:

    # Check File Exists
    if not os.path.exists(file_name):
        raise Exception(f"Config File {file_name} not found")

    # Load File
    with open(file_name, "r") as config_file:
        config = yaml.safe_load(config_file)

    config = recursive_replace_with_value(config)

    return config


def save_config(file_name: str, config: dict):
    # Save if it is new file
    if not os.path.exists(file_name):
        with open(file_name, "w") as config_file:
            yaml.safe_dump(config, config_file)
            return

    # Load existing file and replace with env
    with open(file_name, "r") as existing_config_file:
        existing_config = yaml.safe_load(existing_config_file)

    replaced_config = recursive_replace_with_variable(config, existing_config)

    with open(file_name, "w") as config_file:
        yaml.safe_dump(replaced_config, config_file)

    return


if __name__ == "__main__":
    # Test Case
    config = read_config("config.yaml")
    print(config)
    config["New_Test"] = "New Item"
    config["Test"]["key"] = "wonderful"
    save_config("config.yaml", config)
