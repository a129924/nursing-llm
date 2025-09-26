import os
import pathlib


def get_abs_path(rel_path: str, from_server: bool = True) -> str:
    """
    取得相對路徑的絕對路徑。

    Args:
        rel_path: 相對路徑。
        from_server: 若為 True，路徑相對於 server 目錄；否則相對於本文件。

    Returns:
        轉換後的絕對路徑。
    """
    if os.path.isabs(rel_path):
        return rel_path

    # 找到 helpers.py（本檔案）所在目錄
    current_dir = pathlib.Path(__file__).parent.absolute()

    if from_server:
        # 從 tests/ 回溯一層到 server/
        base_dir = current_dir.parent
    else:
        # 使用 tests/ 作為基礎目錄
        base_dir = current_dir

    # 連接基礎目錄和相對路徑
    return os.path.join(base_dir, rel_path)


def get_test_file_path(filename: str, category: str | None = None) -> str:
    """
    取得測試檔案路徑，自動查找 tests/mock/files/ 目錄。

    Args:
        filename: 測試檔案名稱。
        category: 可選的子目錄名稱，用於組織不同類型的測試檔案。

    Returns:
        測試檔案的絕對路徑。
    """
    base_path = "tests/mock/files"
    if category:
        base_path = f"{base_path}/{category}"

    return get_abs_path(f"{base_path}/{filename}", from_server=True)
