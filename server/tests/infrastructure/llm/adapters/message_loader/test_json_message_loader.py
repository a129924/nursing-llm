from pathlib import Path

from pytest import mark, raises

from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.infrastructure.llm.adapters.message_loader.json_message_loader import (
    JSONMessageLoader,
)


@mark.asyncio
async def test_json_message_loader_reads_list(tmp_path: Path) -> None:
    base = tmp_path / "messages"
    base.mkdir()
    msg_file = base / "message_test.json"
    msg_file.write_text(
        '[{"role": "user", "content": "hello"}, {"role": "assistant", "content": "ok"}]'
    )

    loader = JSONMessageLoader(str(base))

    messages = await loader.load_messages("test")

    assert len(messages) == 2
    assert messages[0].role == Role.USER
    assert messages[0].content == "hello"
    assert messages[1].role == Role.ASSISTANT


@mark.asyncio
async def test_json_message_loader_reads_single_dict(tmp_path: Path) -> None:
    base = tmp_path / "messages2"
    base.mkdir()
    msg_file = base / "message_single.json"
    msg_file.write_text('{"role": "assistant", "content": "single"}')

    loader = JSONMessageLoader(str(base))

    messages = await loader.load_messages("single")

    assert isinstance(messages, list)
    assert len(messages) == 1
    assert messages[0].role == Role.ASSISTANT
    assert messages[0].content == "single"


@mark.asyncio
async def test_json_message_loader_invalid_json_raises(tmp_path: Path) -> None:
    base = tmp_path / "messages3"
    base.mkdir()
    msg_file = base / "message_bad.json"
    msg_file.write_text("{this is not: }")

    loader = JSONMessageLoader(str(base))

    from nursing_llm_server.infrastructure.llm.adapters.message_loader.errors import (
        MessageParseError,
    )

    with raises(MessageParseError):
        await loader.load_messages("bad")


@mark.asyncio
async def test_json_message_loader_schema_error_raises(tmp_path: Path) -> None:
    base = tmp_path / "messages4"
    base.mkdir()
    msg_file = base / "message_schema_bad.json"
    # valid JSON but invalid schema
    msg_file.write_text('[{"role": "user"}]')

    loader = JSONMessageLoader(str(base))

    from nursing_llm_server.infrastructure.llm.adapters.message_loader.errors import (
        MessageSchemaError,
    )

    with raises(MessageSchemaError):
        await loader.load_messages("schema_bad")


@mark.asyncio
async def test_json_message_loader_file_not_found_raises(tmp_path: Path) -> None:
    base = tmp_path / "messages_missing"
    base.mkdir()

    loader = JSONMessageLoader(str(base))

    from nursing_llm_server.infrastructure.llm.adapters.message_loader.errors import (
        MessageFileNotFoundError,
    )

    with raises(MessageFileNotFoundError):
        await loader.load_messages("does_not_exist")
