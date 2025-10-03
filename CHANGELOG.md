# Changelog
# [server-0.4.0] - 2025-10-03
v0.4.0 - feat: 強化 Ollama 支援、LLM 處理器、Mapper/Validator 與 Docker 部署

- 新增/重構 LLM 處理器介面與實作
  - 新增 `LLMProcessorABC`、`OllamaGenerateProcessor`、`OllamaChatProcessor`
  - 調整處理器驗證流程以接受字串或已解析的 dict

- 增強 Pydantic 驗證與錯誤處理
  - PydanticValidator 改為使用 model_validate_json，並拋出應用層 ValidationError
  - 新增多種解析/驗證例外 (ParserError, NursingPayloadParserError, OllamaResponseParserError)

- 型別、Mapper 與 Domain 模型
  - 新增 MapperInterface / PydanticModelMapperABC 與通用型別 (ResponseSchema, PayloadSchema)
  - 新增 Nursing domain dataclasses 與對應 Pydantic schema
  - 實作 NursingMapper、LLMResponse 映射器等

- LLM 客戶端錯誤類別
  - 新增 LLMClientError 與子類 (RateLimit, NotFound, Timeout)

- Docker / Ollama 部署支援
  - 新增 `server/docker/Dockerfile`、`docker/init_and_pull.sh`、`docker-compose.yml` (包含 healthcheck、entrypoint)
  - 新增模型目錄 placeholder `server/data/models`
  - 新增 init/pull 腳本以在容器內確保 Ollama 就緒並拉取模型

- Prompt / 範例與輸出格式調整
  - 更新 few-shot 範例（移除 record_id/patient_id、統一 temperature 格式、保留 vital_signs 欄位）
  - 更新測試以配合回應內容與空流錯誤處理

- 測試與 CI 相關
  - 新增/更新多個 fixture、unit tests（validator、mapper、processor）
  - 更新 conftest 與測試行為以反映實作變更

- 專案設定
  - 調整 .gitignore（排除 outputs、pyrightconfig.json 等）
  - 其他測試與配置修正

Signed-off-by: andrew <a129924@gmail.com>

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

