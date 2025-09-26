# Changelog
# [server-0.2.0] - 2025-09-26
 v0.2.0 - feat: 配置與護理紀錄解析器改進

- 更新版本至 0.2.0（server）
- 新增護理紀錄結構化解析資源（prompts 與 few-shot 範例）
- 新增配置系統與 Loader：
  - BaseConfig（pydantic）
  - Loader 抽象類別、EnvLoader（.env stream 支援）、ConfigParserError
  - OllamaConfig（host/port/model/timeout/api_key）
- 新增測試與測試資源（helpers、conftest、unit tests、mock .env 檔）
- 調整專案設定：
  - .gitignore 新增 pyrightconfig.json
  - 調整 client/server pyproject.toml 的 pytest 設定

  
