from pytest import mark

from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message
from nursing_llm_server.core.models.payload import Payload
from nursing_llm_server.infrastructure.config.ollama import OllamaConfig
from nursing_llm_server.infrastructure.llm.adapters.payload_builder.ollama_payload_builder import (
    OllamaPayloadBuilder,
)
from tests.mock.mock_loaders import (
    make_memory_message_loader,
    make_memory_prompt_loader,
)


def test_build_chat_payload_matches_config_defaults() -> None:
    # Provide required numeric config values explicitly
    config = OllamaConfig(
        temperature=0.5,
        max_tokens=512,
        top_p=0.95,
        seed=42,
    )
    builder = OllamaPayloadBuilder(
        config,
        prompt_loader=make_memory_prompt_loader(""),
        message_loader=make_memory_message_loader([]),
    )

    messages = [Message(role=Role.USER, content="Hello world")]

    payload = builder.build_chat_payload(messages)

    assert isinstance(payload, Payload)
    assert payload.model == config.model
    assert payload.messages == messages
    assert payload.stream is True

    # options should be present and include the configured numeric parameters
    assert payload.options is not None
    assert payload.options["temperature"] == config.temperature
    assert payload.options["top_p"] == config.top_p
    assert payload.options["max_tokens"] == config.max_tokens
    assert payload.options["seed"] == config.seed


@mark.asyncio
async def test_build_chat_payload_from_user_includes_prompt_and_examples() -> None:
    prompt_content = "This is a system prompt."
    example_messages = [
        Message(role=Role.USER, content="Example user message"),
        Message(role=Role.ASSISTANT, content="Example assistant reply"),
    ]

    config = OllamaConfig(temperature=0.5, max_tokens=256, top_p=0.9, seed=0)
    builder = OllamaPayloadBuilder(
        config,
        prompt_loader=make_memory_prompt_loader(prompt_content),
        message_loader=make_memory_message_loader(example_messages),
    )

    user_input = "Hello, how are you?"
    prompt_id = "test-prompt"
    example_id = "test-examples"

    payload = await builder.build_chat_payload_from_user(
        user_input=user_input,
        prompt_id=prompt_id,
        example_id=example_id,
    )

    assert isinstance(payload, Payload)
    assert payload.model == config.model
    assert payload.stream is True
    assert payload.options is not None
    assert payload.messages is not None
    assert len(payload.messages) == 4
    assert all(isinstance(msg, Message) for msg in payload.messages)

    # Check that the messages include the prompt, examples, and user input in order
    expected_messages = [
        Message(role=Role.SYSTEM, content=prompt_content),
        *example_messages,
        Message(role=Role.USER, content=user_input),
    ]
    assert payload.messages == expected_messages
    assert payload.messages[0].role == Role.SYSTEM
    assert payload.messages[0].content == prompt_content
    assert payload.messages[1] == example_messages[0]
    assert payload.messages[2] == example_messages[1]
