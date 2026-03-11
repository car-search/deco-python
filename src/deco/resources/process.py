# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["ProcessResource", "AsyncProcessResource"]


class ProcessResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProcessResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/car-search/deco-python#accessing-raw-response-data-eg-headers
        """
        return ProcessResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProcessResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/car-search/deco-python#with_streaming_response
        """
        return ProcessResourceWithStreamingResponse(self)

    def retrieve(
        self,
        user_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Handle User Request

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/process/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncProcessResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProcessResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/car-search/deco-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProcessResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProcessResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/car-search/deco-python#with_streaming_response
        """
        return AsyncProcessResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        user_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Handle User Request

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/process/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ProcessResourceWithRawResponse:
    def __init__(self, process: ProcessResource) -> None:
        self._process = process

        self.retrieve = to_raw_response_wrapper(
            process.retrieve,
        )


class AsyncProcessResourceWithRawResponse:
    def __init__(self, process: AsyncProcessResource) -> None:
        self._process = process

        self.retrieve = async_to_raw_response_wrapper(
            process.retrieve,
        )


class ProcessResourceWithStreamingResponse:
    def __init__(self, process: ProcessResource) -> None:
        self._process = process

        self.retrieve = to_streamed_response_wrapper(
            process.retrieve,
        )


class AsyncProcessResourceWithStreamingResponse:
    def __init__(self, process: AsyncProcessResource) -> None:
        self._process = process

        self.retrieve = async_to_streamed_response_wrapper(
            process.retrieve,
        )
