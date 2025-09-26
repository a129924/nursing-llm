# ...existing code...
from io import TextIOBase
from typing import IO, cast

from typing_extensions import override

from nursing_llm_server.infrastructure.config.loader.base import Loader
from nursing_llm_server.infrastructure.config.loader.errors import ConfigParserError


class EnvLoader(Loader):
    """Load environment-style files (.env) from a text stream or file path."""

    def __init__(self, reader: TextIOBase, raise_on_error: bool = False) -> None:
        self._reader = reader
        self._raise_on_error = raise_on_error

    @override
    def load(self) -> dict[str, str | None]:
        """
        Use python-dotenv to parse the provided text stream.
        Ensure the stream is positioned at the start before parsing.
        """
        from dotenv import dotenv_values

        try:
            # 如果支援 seek，就回到檔案開頭
            try:
                self._reader.seek(0)
            except Exception:
                pass
            # dotenv_values 支援 stream=，不要只讀一行
            result = dotenv_values(stream=cast(IO[str], self._reader))
            return dict(result or {})
        except Exception:
            # 不在 loader 層丟出應用層錯誤，回傳空 dict 以利呼叫端處理或測試判斷
            if self._raise_on_error:
                raise ConfigParserError("Failed to parse .env file") from Exception
            return {}
