# Changelog
# [server-0.3.0] - 2025-09-30
v0.3.0 - feat: 增強配置、Ollama 支援與護理領域模型

- 更新 server 版本至 0.3.0，並在套件中設定 __version__。
- 新增 OllamaConfig（含 ollama_base_url）、Docker 支援與模型拉取腳本（docker-compose.yml、docker/pull_model.sh）、models 目錄與說明。
- 新增配置載入機制與錯誤類別：BaseConfig、Loader 抽象類、EnvLoader、ConfigParserError。
- 新增 LLM 層級物件與例外：LLMResponse DTO、LLMClientABC、相關 LLM 例外類別。
- 新增型別/協定與驗證基礎：PydanticModelMapperABC、PydanticModelValidatorABC、PydanticValidator。
- 建立護理領域 dataclass（BloodPressure、VitalSigns、PatientStatus、Intervention 等），及更新解析 prompt/few-shot 範例。
- 新增測試輔助與 fixtures，並調整 pyproject.toml 與 .gitignore。

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

