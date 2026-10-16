from mcp.server.mcpserver import MCPServer as Server

mcp = Server("snail-poetry")

POEM = """\
The Snail and the Little Blue Boat

A snail once found a boat of blue
Abandoned by a pond at dawn.
"Why crawl," she said, "the whole way through,
When I could simply sail along?"

She hauled her shell up over the side,
Unfurled a leaf to catch the breeze,
And pushed away on the morning tide
Beneath the drooping willow trees.

The dragonflies all stopped to stare,
The frogs looked up from lily pads.
A turtle muttered, "Well, I declare,"
While minnows gossiped in their schools.

She wasn't fast. She wasn't grand.
She drifted slow as drying dew.
But oh, the view from off the land!
The whole wide world was hers to cruise.

And when the evening stars came out,
She dropped her anchor, soft and small,
Tucked in her shell, with no more doubt
That slow is not the same as stalled.
"""


@mcp.resource(
    "poem://snail-with-a-boat",
    name="snail_with_a_boat",
    description="A short poem about a snail who finds a boat.",
    mime_type="text/plain",
)
def snail_poem() -> str:
    return POEM


if __name__ == "__main__":
    mcp.run()