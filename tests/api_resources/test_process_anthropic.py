# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from deco import Deco, AsyncDeco
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProcessAnthropic:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Deco) -> None:
        process_anthropic = client.process_anthropic.retrieve(
            0,
        )
        assert_matches_type(object, process_anthropic, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Deco) -> None:
        response = client.process_anthropic.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        process_anthropic = response.parse()
        assert_matches_type(object, process_anthropic, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Deco) -> None:
        with client.process_anthropic.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            process_anthropic = response.parse()
            assert_matches_type(object, process_anthropic, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncProcessAnthropic:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncDeco) -> None:
        process_anthropic = await async_client.process_anthropic.retrieve(
            0,
        )
        assert_matches_type(object, process_anthropic, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncDeco) -> None:
        response = await async_client.process_anthropic.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        process_anthropic = await response.parse()
        assert_matches_type(object, process_anthropic, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncDeco) -> None:
        async with async_client.process_anthropic.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            process_anthropic = await response.parse()
            assert_matches_type(object, process_anthropic, path=["response"])

        assert cast(Any, response.is_closed) is True
