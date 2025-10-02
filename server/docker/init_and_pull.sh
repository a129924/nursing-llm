#!/bin/sh
# ...existing code...
set -eu

PORT=${PORT:-11434}
MODEL_NAME=${MODEL_NAME:-ggml-llama2-7b}
LOGFILE=/var/log/ollama-serve.log

# 啟動 ollama server 背景執行，將輸出寫入 log
ollama serve > "${LOGFILE}" 2>&1 &
SERV_PID=$!

# 等待 /v1/health 最長 120 秒
i=0
MAX_WAIT=120
until [ "$i" -ge "$MAX_WAIT" ]; do
  if command -v curl >/dev/null 2>&1; then
    if curl -sSf "http://localhost:${PORT}/v1/health" >/dev/null 2>&1; then
      break
    fi
  fi
  i=$((i+1))
  sleep 1
done

if [ "$i" -ge "$MAX_WAIT" ]; then
  echo "ollama server did not become healthy" >&2
  echo "===== last 200 lines of server log ====="
  tail -n 200 "${LOGFILE}" || true
  echo "== keeping container alive for debugging (tail -f) =="
  # 保持容器運行以便查看 logs
  exec tail -f "${LOGFILE}"
fi

# 服務已就緒，拉 model（若已存在也會回傳成功）
ollama pull "${MODEL_NAME}" || true

# 停掉背景 server，並以 exec 啟動 foreground server（PID 1）
kill "${SERV_PID}" 2>/dev/null || true
exec ollama serve
# ...existing code...