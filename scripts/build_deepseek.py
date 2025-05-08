import os
import shutil
import sys

def validate_and_copy_files(root_dir='.', build_dir='build'):
    # 确保build目录存在
    build_path = os.path.join(root_dir, build_dir)
    os.makedirs(build_path, exist_ok=True)

    error_occurred = False

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 排除build目录本身
        if dirpath.startswith(build_path):
            continue

        # 计算当前目录深度
        rel_path = os.path.relpath(dirpath, root_dir)
        depth = len(rel_path.split(os.path.sep)) if rel_path != '.' else 0

        # 只处理深度为3的目录（语言/地区/语音目录）
        if depth == 3:
            dir_name = os.path.basename(dirpath)
            required_files = [
                f"{dir_name}.bank",
                f"{dir_name}.bank.guids",
                f"{dir_name}.sii"
            ]

            # 检查文件是否存在
            missing_files = []
            for f in required_files:
                if f not in filenames:
                    missing_files.append(f)

            if missing_files:
                print(f"错误：目录 {dirpath} 缺少文件: {', '.join(missing_files)}")
                error_occurred = True
            else:
                # 创建目标目录并复制文件
                dest_dir = os.path.join(build_path, rel_path)
                os.makedirs(dest_dir, exist_ok=True)
                
                for f in required_files:
                    src = os.path.join(dirpath, f)
                    dest = os.path.join(dest_dir, f)
                    shutil.copy2(src, dest)
                    print(f"已复制: {src} -> {dest}")

    if error_occurred:
        print("\n错误: 存在文件缺失，请检查上述错误信息")
        sys.exit(1)
    else:
        print("\n所有文件已成功复制到build目录")

if __name__ == "__main__":
    validate_and_copy_files()