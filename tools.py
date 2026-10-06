"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

    price_comparison(target, candidates)           → dict | None

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()
    
    # Normalize the search description into keywords
    query_keywords = set(description.lower().split())
    
    # Filter by price and size, score by keyword overlap
    candidates = []
    for listing in listings:
        # Filter by max_price
        if max_price is not None and listing.get("price", float("inf")) > max_price:
            continue
        
        # Filter by size (case-insensitive, handle size ranges like "S/M")
        if size is not None:
            listing_size = (listing.get("size") or "").lower()
            query_size = size.lower()
            # Match if the query size appears as a standalone component or full match
            if query_size not in listing_size and listing_size != query_size:
                # Check if it's a component of a range like "S/M" or "XS-M"
                size_parts = listing_size.replace("-", "/").split("/")
                if query_size not in size_parts:
                    continue
        
        # Score by keyword overlap with title and description
        title_text = (listing.get("title") or "").lower()
        desc_text = (listing.get("description") or "").lower()
        style_tags = [tag.lower() for tag in (listing.get("style_tags") or [])]
        
        # Count matching keywords
        overlap = 0
        for keyword in query_keywords:
            if keyword in title_text.split():
                overlap += 2  # weight title matches higher
            elif keyword in desc_text:
                overlap += 1
            elif keyword in style_tags:
                overlap += 1.5
        
        if overlap > 0:
            candidates.append((overlap, listing))
    
    # Sort by score (descending) and return top results
    candidates.sort(key=lambda x: x[0], reverse=True)
    results = [listing for _, listing in candidates[:config.SEARCH_RESULT_LIMIT]]
    
    return results


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    item_title = new_item.get("title", "item")
    item_brand = new_item.get("brand") or "unbranded"
    item_category = new_item.get("category", "piece")
    item_style = ", ".join(new_item.get("style_tags", []))
    item_condition = new_item.get("condition", "good")
    
    wardrobe_items = wardrobe.get("items", [])
    
    if not wardrobe_items:
        # Empty wardrobe: ask for general styling advice
        prompt = f"""I found a {item_condition} {item_brand} {item_title} ({item_category}, style: {item_style}). 
        
I don't have any items in my wardrobe yet. Give me 1-2 general styling ideas for how to wear this piece. Focus on the vibe and what essentials would work well with it."""
    else:
        # Non-empty wardrobe: suggest specific outfit combinations
        wardrobe_desc = "\n".join([
            f"- {w.get('name', 'item')} ({w.get('category', 'clothing')})"
            for w in wardrobe_items[:10]  # limit to first 10 for brevity
        ])
        
        prompt = f"""I found a {item_condition} {item_brand} {item_title} ({item_category}, style: {item_style}).

My current wardrobe includes:
{wardrobe_desc}

Give me 1-2 specific outfit suggestions that combine this new piece with items I already own. Name the pieces you'd pair it with."""
    
    response = generate(prompt)
    return response if response else ""


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # Guard against empty or whitespace-only outfit
    if not outfit or not outfit.strip():
        return "No outfit suggestion available for this item."
    
    item_title = new_item.get("title", "item")
    item_price = new_item.get("price", "unknown")
    item_platform = new_item.get("platform", "unknown platform")
    item_condition = new_item.get("condition", "good")
    item_brand = new_item.get("brand") or "this piece"
    
    prompt = f"""Write a 2-4 sentence social media caption for someone posting about a thrift find.

Item: {item_title}
Price: ${item_price}
Condition: {item_condition}
Platform: {item_platform}
Outfit suggestion: {outfit}

The caption should be casual, mention the price and platform naturally (not as a list), describe the vibe, and sound like a real post someone would make. Be specific about why this find is cool."""
    
    response = generate(prompt)
    return response if response else ""


# ── Tool 4: price_comparison ────────────────────────────────────────────────

def price_comparison(target: dict, candidates: list[dict] | None = None) -> dict | None:
    """
    Compare a target listing's price to similar listings and summarize the market.

    Args:
        target: a listing dict (must include `id` and `price`).
        candidates: optional list of listing dicts to compare against; if
                    None, the function should load listings from the dataset.

    Returns:
        A dict with these keys when comparables exist:
            `target_id` (str), `target_price` (float),
            `median_price` (float), `min_price` (float), `max_price` (float),
            `num_competitors` (int), `competitors` (list of dicts).

        Each competitor dict contains: `id` (str), `price` (float),
        `platform` (str), `url` (str), and `similarity` (float).

    When it has nothing:
        Returns `None` when no comparable listings are found.

    TODO:
        1. If `candidates` is None, call `load_listings()` and use that.
        2. Filter candidates by category/style/size as appropriate to find
           comparable items.
        3. Compute min/median/max and return the summarized dict.

    Test it from a terminal before you move on:
        python -c "from tools import price_comparison; from utils.data_loader import load_listings; print(price_comparison(load_listings()[0]))"
    """
    if not target or "price" not in target:
        return None
    
    if candidates is None:
        candidates = load_listings()
    
    if not candidates:
        return None
    
    # Get target attributes
    target_id = target.get("id")
    target_price = float(target.get("price", 0))
    target_category = target.get("category")
    target_size = (target.get("size") or "").lower()
    target_style_tags = set(tag.lower() for tag in (target.get("style_tags") or []))
    
    # Find comparable items
    comparables = []
    for item in candidates:
        # Skip the target itself
        if item.get("id") == target_id:
            continue
        
        if not item.get("price"):
            continue
        
        # Must be same category
        if item.get("category") != target_category:
            continue
        
        # Calculate similarity score
        similarity = 0.5  # base similarity for same category
        
        # Size match (if both have sizes)
        if target_size and item.get("size"):
            item_size = (item.get("size") or "").lower()
            if target_size == item_size:
                similarity += 0.3
            elif target_size in item_size or item_size in target_size:
                similarity += 0.15
        
        # Style tag overlap
        item_style_tags = set(tag.lower() for tag in (item.get("style_tags") or []))
        tag_overlap = len(target_style_tags & item_style_tags)
        if tag_overlap > 0:
            similarity += min(0.2, tag_overlap * 0.05)
        
        # Build competitor record
        competitor = {
            "id": item.get("id"),
            "price": float(item.get("price", 0)),
            "platform": item.get("platform", "unknown"),
            "url": item.get("url", ""),
            "similarity": round(similarity, 2),
        }
        comparables.append(competitor)
    
    # No comparables found
    if not comparables:
        return None
    
    # Sort by similarity (descending) and collect prices
    comparables.sort(key=lambda x: x["similarity"], reverse=True)
    prices = [c["price"] for c in comparables]
    prices.sort()
    
    # Compute price statistics
    n = len(prices)
    median_price = prices[n // 2] if n % 2 else (prices[n // 2 - 1] + prices[n // 2]) / 2
    
    return {
        "target_id": target_id,
        "target_price": round(target_price, 2),
        "median_price": round(median_price, 2),
        "min_price": round(min(prices), 2),
        "max_price": round(max(prices), 2),
        "num_competitors": n,
        "competitors": comparables,
    }

