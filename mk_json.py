import json
import os

def make_json(filename="config.json"):
    if not os.path.exists(os.path.join(os.getcwd(), filename)):
        data_config = {'config': []}
        data_config['config'].append({
                'root-dir': False,
                'show-images': True
            })

        with open(filename, 'w', encoding='utf-8') as f_source:
            json.dump(data_config, f_source, indent=2)

        if os.path.exists(os.path.join(os.getcwd(), filename)):
            print('Successfully created json config file.')
    else:
        print(f"'{filename}' already exists!")

if __name__ == "__main__":
    make_json()
