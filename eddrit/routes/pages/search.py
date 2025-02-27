from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from eddrit.reddit.fetch import search_posts, search_subreddits
from eddrit.routes.common.context import (
    get_canonical_url_context,
    get_templates_common_context,
)
from eddrit.templates import templates


async def search(request: Request) -> Response:
    input_text = request.query_params.get("q", "")
    subreddit_search_results = await search_subreddits(input_text)
    posts_search_results = await search_posts(input_text)

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "subreddits": subreddit_search_results[:3],
            "posts": posts_search_results,
            **get_templates_common_context(request),
            **get_canonical_url_context(request),
        },
    )


routes = [
    Route("/search", endpoint=search, methods=["GET"]),
]
