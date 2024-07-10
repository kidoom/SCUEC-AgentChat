import os

def generate_directory_tree(start_path, indent=""):
    for item in os.listdir(start_path):
        path = os.path.join(start_path, item)
        if os.path.isdir(path) and item not in ["__pycache__", "ERNIE-SDK"]:
            print(indent + "|-- " + item)
            generate_directory_tree(path, indent + "    ")

if __name__ == "__main__":
    start_path = "D:/SCUEC-AgentChat/Agent"  # 请修改为你的项目路径
    generate_directory_tree(start_path)
