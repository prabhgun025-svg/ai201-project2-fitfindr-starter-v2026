# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## Stretch Features I am adding to the project 
1. a Fourth Tool which is price comparison 
2. Style Memory in which the agent remembers a wardrobe between runs 


## What This Does

This is a fitfindr application in which the user asks questions such as pricing, or fit models or reccomendations, etc. and the AI will output the answers. It would search the projects listing to match to match the text query and optional fiters for candidates, suggets outfits for the candidates 
---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- What it does: Searches the project's listings data for items whose title, description, or style tags match the keywords. It can also filter by size and a price ceiling. Results are ranked by keyword overlap, and title matches count most.
- Inputs: `description` (str, required), `size` (str, optional, matched case-insensitively), `max_price` (float, optional, US dollars, inclusive)
- Returns: Up to 10 listing dicts, best match first. Each has keys: `id` (str), `title` (str), `description` (str), `category` (str), `style_tags` (list of str), `size` (str), `condition` (str), `price` (float), `colors` (list of str), `brand` (str or null), and `platform` (str).
- When it has nothing: Returns an empty list (`[]`).

### `suggest_outfit`

- What it does: Generates outfit suggestions by combining one or more listings into cohesive looks based on style rules and optional user/context inputs.
- Inputs: `listings` (list of listing dicts), `weather` (str, optional), `occasion` (str, optional), `user_profile` (dict, optional)
- Returns: A list of outfit dicts, each with `items` (list of listing `id` strings), `description` (str), `style_tags` (list of str), and `confidence` (float 0.0-1.0).
- When it has nothing: Returns an empty list (`[]`).

### `create_fit_card`

- What it does: Renders a single, shareable fit card summarizing an outfit or listing, suitable for display or sending to a UI or API consumer.
- Inputs: `outfit` (dict describing the outfit; required), `image_url` (str, optional), `brand_info` (dict, optional)
- Returns: A dict with `title` (str), `bullet_points` (list of str), `price` (float), `image` (str URL or null), `call_to_action` (str), and `metadata` (dict with source ids and timestamps).
- When it has nothing: Returns `None` when it cannot produce a valid card (e.g., missing required `outfit` information).

### `price_comparison`

- What it does: Compares a target listing's price against similar listings to show how it sits in the market.
- Inputs: `target` (listing dict with `id` and `price`), `candidates` (list of listing dicts, optional)
- Returns: A dict with `target_id` (str), `target_price` (float), `median_price` (float), `min_price` (float), `max_price` (float), `num_competitors` (int), and `competitors` (list of dicts with `id`, `price`, `platform`, `url`, `similarity`).
- When it has nothing: Returns `None` when no comparable listings can be found.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** "If `search_listings` returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to `suggest_outfit`. If `suggest_outfit` returns an empty string or the wardrobe is empty, put a message in the session and stop; otherwise continue to `create_fit_card`." — `agent.py::run_agent`

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex — extracts price with pattern `(?:under\s+)?(?:\$)?(\d+(?:\.\d+)?)`, size with `(?:size\s+)?([XS]+|M|L|XL|XXL|\d+)`, and the remaining text becomes the description.

**What moves through the session:** `query` (input) → `parsed` (description, size, max_price extracted) → `search_results` (list of listings) → `selected_item` (first listing, or None if empty search) → `outfit_suggestion` (model text) → `fit_card` (model caption, or None if stopped early) → `error` (message if branch stops).

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python3 app.py ask 'silk slip dress in midi length under $40'

```

  Found:    Leather Belt — Brown, Braided — $12.0 on thredUp

  Outfit:   Here are two distinct outfit suggestions that incorporate your new brown braided leather belt with your current wardrobe, leaning into its vintage, western, and earth-tone qualities:

### Outfit 1: The Laid-Back Earth-Tone Neutral
*This look plays on relaxed proportions and mixes shades of brown, khaki, and white for an effortless, vintage-casual everyday vibe.*

*   **Bottoms:** Wide-leg khaki trousers
*   **Tops:** White ribbed tank top
*   **Outerwear:** Oversized grey crewneck sweatshirt (worn over the shoulders or layered on top)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt + Black crossbody bag

**Why it works:** Threading the brown braided belt through the wide-leg khakis anchors the high-waisted fit and breaks up the light earth tones. Pairing it with the crisp white ribbed tank keeps the top half light and summery, while the chunky white sneakers tie the whole casual silhouette together. 

---

### Outfit 2: Western-Edge Denim on Denim
*This look utilizes the belt as a bridge between classic western styling and your darker streetwear pieces.*

*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Tops:** Black cropped zip hoodie
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

**Why it works:** The dark wash straight-leg jeans provide a great canvas for the rich texture of the brown braided belt, leaning heavily into a rugged, vintage aesthetic. Layering the black cropped zip hoodie under the vintage black denim jacket creates a sleek, monochromatic dark base that lets the brown leather belt stand out as a stylish, contrasting focal point. Finished with the black combat boots, the look gets a tough, grounded edge.

  Fit card: Scored this gorgeous vintage brown braided leather belt on thredUp for just $12 in literal mint condition! Obsessed with how the rich texture adds the *best* earthy, western touch to both lazy-day denim looks and tailored trousers. Can't wait to wear this piece on repeat. 🤎✨

2 model calls this session, 642 prompt + 450 output tokens

**The three tools, tested one at a time**

```
$ python3 -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, '
```
$ python3 -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

```
Here are two specific outfit suggestions that integrate the medium-wash Levi's 501s with your current wardrobe, leaning into different vibes you can create:

### Outfit 1: Effortless Streetwear Casual
*This look plays with proportions by pairing the straight-leg 501s with an oversized top, grounded by chunky sneakers for an easy, everyday aesthetic.*

* **Bottoms:** Vintage Levi's 501 Jeans (Medium Wash)
* **Top:** Oversized grey crewneck sweatshirt
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag + Brown leather belt 

### Outfit 2: Edgy Contrast
*This look creates a cool-girl textural contrast by pairing the vintage medium-wash denim with darker, cropped layers and utilitarian footwear.*

* **Bottoms:** Vintage Levi's 501 Jeans (Medium Wash)
* **Top:** White ribbed tank top
* **Outerwear:** Black cropped zip hoodie (layered over the tank)
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt
```
$ python3 -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```
Nothing beats the broken-in feel of a true vintage pair of Levi's 501s, especially in this classic medium wash. Just dropped these beauties on my Depop for $38 and they are dying for a simple weekend uniform of crisp white sneakers and an oversized tee. Grab them before I change my mind and keep them for myself!
'''
python3 -c "from tools import price_comparison; from utils.data_loader import load_listings; print(price_comparison(load_listings()[0]))"

'''
{'target_id': 'lst_001', 'target_price': 38.0, 'median_price': 30.0, 'min_price': 14.0, 'max_price': 36.0, 'num_competitors': 9, 'competitors': [{'id': 'lst_021', 'price': 29.0, 'platform': 'poshmark', 'url': '', 'similarity': 0.75}, {'id': 'lst_016', 'price': 24.0, 'platform': 'poshmark', 'url': '', 'similarity': 0.65}, {'id': 'lst_037', 'price': 30.0, 'platform': 'thredUp', 'url': '', 'similarity': 0.65}, {'id': 'lst_031', 'price': 36.0, 'platform': 'depop', 'url': '', 'similarity': 0.6}, {'id': 'lst_005', 'price': 32.0, 'platform': 'depop', 'url': '', 'similarity': 0.55}, {'id': 'lst_011', 'price': 27.0, 'platform': 'poshmark', 'url': '', 'similarity': 0.55}, {'id': 'lst_013', 'price': 30.0, 'platform': 'depop', 'url': '', 'similarity': 0.55}, {'id': 'lst_026', 'price': 14.0, 'platform': 'depop', 'url': '', 'similarity': 0.55}, {'id': 'lst_025', 'price': 34.0, 'platform': 'poshmark', 'url': '', 'similarity': 0.5}]}
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- I told the AI to check my criteria from 3-5 to see if they are good enough for in which I am able to answer and do with no context and give reccomendations for the the targets set 
- The criteria for 3 was not able to be followed with little context so it was unable to decipher and the targets were too lenient (3/5 + 4/5)
- I changed the criteria for number three to better reflect and tested it again until the criteria can be done with no context and I did not follow the AI reccomendation for the targets set so I made the targets 5/5 as I think that would better fit the criterion 


**Moment 2**

- I asked it to tell me what to try next after reading the empty result message and to tell me what would it do if the search returns nothing, knowing nothing about the app. 
- it said it would know to loosen the filters or rephrase, so it isn't a dead end. But It would be guessing which lever matters, and the description would make it suspect the problem was something It couldn't see.
- I made it more descriptive so the AI knows exactly where the search went wrong as well as give it tips on what to try in their next search 

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->



| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A Matching Query completes all three tools  | 4/5 | PASS | PASS |PASS| PASS | PASS | MET (5/5)|
| 2. An Impossible Query stops before the second tool | 5/5 | PASS |PASS  | PASS | PASS | PASS | MET (5/5) |
| 3. The selected item must survive the whole loop | 5/5 | FAIL | FAIL | FAIL |FAIL| FAIL | MISSED 0/5 |
| 4. fit card fllback and content requirement are both enforced |  4/5| PASS | PASS |PASS  | PASS | PASS | MET (5/5) |
| 5. search enforces the Price Cap | 5/5 |  PASS| PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

matching query completes  (example wardrobe)
  query: vintage graphic tee under $30
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
      out: 1 items: Straight Leg Khaki Trousers — Olive
      →    branch: results, continuing
[3] select_item
      in:  1 results
      out: Straight Leg Khaki Trousers — Olive ($29.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='Straight Leg Khaki Trousers — Olive', wardrobe=10 items
      out: Here are two specific outfit suggestions that incorporate your new olive straight-leg trousers, blending that …
[5] create_fit_card
      in:  new_item='Straight Leg Khaki Trousers — Olive', outfit=<suggest_outfit text>
      out: Scored these gorgeous olive straight-leg trousers in pristine condition on Poshmark for just $29, and I am off…
  try 1: completed — fit card 366 chars
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
      out: 1 items: Straight Leg Khaki Trousers — Olive
      →    branch: results, continuing
[3] select_item
      in:  1 results
      out: Straight Leg Khaki Trousers — Olive ($29.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='Straight Leg Khaki Trousers — Olive', wardrobe=10 items
      out: Here are two specific outfit suggestions that incorporate your new olive straight-leg khaki trousers while pla…
[5] create_fit_card
      in:  new_item='Straight Leg Khaki Trousers — Olive', outfit=<suggest_outfit text>
      out: Found my new favorite pair of trousers on Poshmark for just $29 and the condition is honestly unreal! These ol…
  try 2: completed — fit card 322 chars
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
      out: 1 items: Straight Leg Khaki Trousers — Olive
      →    branch: results, continuing
[3] select_item
      in:  1 results
      out: Straight Leg Khaki Trousers — Olive ($29.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='Straight Leg Khaki Trousers — Olive', wardrobe=10 items
      out: Here are two specific outfit suggestions that blend your new olive straight-leg trousers with your current war…
[5] create_fit_card
      in:  new_item='Straight Leg Khaki Trousers — Olive', outfit=<suggest_outfit text>
      out: Scored these straight-leg olive trousers in excellent condition on Poshmark for just $29, and they are officia…
  try 3: completed — fit card 358 chars
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
      out: 1 items: Straight Leg Khaki Trousers — Olive
      →    branch: results, continuing
[3] select_item
      in:  1 results
      out: Straight Leg Khaki Trousers — Olive ($29.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='Straight Leg Khaki Trousers — Olive', wardrobe=10 items
      out: Here are 2 specific outfit suggestions that seamlessly integrate your new olive straight-leg trousers into you…
[5] create_fit_card
      in:  new_item='Straight Leg Khaki Trousers — Olive', outfit=<suggest_outfit text>
      out: Scored these olive straight-leg trousers in pristine condition for just $29 on Poshmark, and they are official…
  try 4: completed — fit card 371 chars
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
      out: 1 items: Straight Leg Khaki Trousers — Olive
      →    branch: results, continuing
[3] select_item
      in:  1 results
      out: Straight Leg Khaki Trousers — Olive ($29.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='Straight Leg Khaki Trousers — Olive', wardrobe=10 items
      out: Here are two specific outfit suggestions that incorporate your new olive straight-leg trousers with pieces fro…
[5] create_fit_card
      in:  new_item='Straight Leg Khaki Trousers — Olive', outfit=<suggest_outfit text>
      out: Scored these gorgeous olive straight-leg trousers in pristine condition for just $29 on Poshmark, and I am off…
  try 5: completed — fit card 336 chars

impossible query stops early  (example wardrobe)
  query: designer ballgown size XXS under $5
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
  try 1: stopped early — No items found matching 'deigner bagown' under $5.0 in size 
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
  try 2: stopped early — No items found matching 'deigner bagown' under $5.0 in size 
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
  try 3: stopped early — No items found matching 'deigner bagown' under $5.0 in size 
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
  try 4: stopped early — No items found matching 'deigner bagown' under $5.0 in size 
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
  try 5: stopped early — No items found matching 'deigner bagown' under $5.0 in size 

empty wardrobe  (empty wardrobe)
  query: denim jacket under $50
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
[2] search_listings (via MCP)
      in:  {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
      out: 3 items: 90s Track Jacket — Navy/White Stripe, Shacket — Olive Canvas, Denim Vest — Medium Wash, Studded
      →    branch: results, continuing
[3] select_item
      in:  3 results
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe', wardrobe=0 items
      out: That’s an incredible find. A 90s Champion track jacket in navy with white stripes is the ultimate heritage str…
[5] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe', outfit=<suggest_outfit text>
      out: Scored this absolute vintage treasure on Poshmark for just $45! This 90s navy and white striped track jacket h…
  try 1: completed — fit card 291 chars
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
[2] search_listings (via MCP)
      in:  {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
      out: 3 items: 90s Track Jacket — Navy/White Stripe, Shacket — Olive Canvas, Denim Vest — Medium Wash, Studded
      →    branch: results, continuing
[3] select_item
      in:  3 results
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe', wardrobe=0 items
      out: That is an absolute classic find. A 90s Champion navy and white track jacket is the holy grail of vintage athl…
[5] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe', outfit=<suggest_outfit text>
      out: Absolute holy grail find secured! ⚡️ Scoring this vintage 90s navy and white track jacket in pristine conditio…
  try 2: completed — fit card 385 chars
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
[2] search_listings (via MCP)
      in:  {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
      out: 3 items: 90s Track Jacket — Navy/White Stripe, Shacket — Olive Canvas, Denim Vest — Medium Wash, Studded
      →    branch: results, continuing
[3] select_item
      in:  3 results
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe', wardrobe=0 items
      out: That is an absolute classic find! A 90s Champion navy and white stripe track jacket is one of the most versati…
  [rate limit] 15 requests used this minute. Waiting 32s. This is normal.
[5] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe', outfit=<suggest_outfit text>
      out: Scored the ultimate 90s vintage track jacket in pristine condition for just $45! ⚡️ Obsessed with the navy and…
  try 3: completed — fit card 361 chars
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
[2] search_listings (via MCP)
      in:  {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
      out: 3 items: 90s Track Jacket — Navy/White Stripe, Shacket — Olive Canvas, Denim Vest — Medium Wash, Studded
      →    branch: results, continuing
[3] select_item
      in:  3 results
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe', wardrobe=0 items
      out: That is a classic find! A 90s Champion track jacket is the ultimate versatile piece because it bridges the gap…
[5] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe', outfit=<suggest_outfit text>
      out: Scored this vintage 90s navy and white track jacket in mint condition for just $45 on Poshmark! It’s the ultim…
  try 4: completed — fit card 281 chars
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
[2] search_listings (via MCP)
      in:  {'description': 'deni jacket', 'size': 'M', 'max_price': 50.0}
      out: 3 items: 90s Track Jacket — Navy/White Stripe, Shacket — Olive Canvas, Denim Vest — Medium Wash, Studded
      →    branch: results, continuing
[3] select_item
      in:  3 results
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe', wardrobe=0 items
      out: That is a classic find! A 90s Champion track jacket in navy with white stripes is the ultimate heritage street…
[5] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe', outfit=<suggest_outfit text>
      out: Scored this pristine 90s navy and white track jacket for just $45, and honestly, it’s the ultimate heritage st…
  try 5: completed — fit card 385 chars

Wrote results/run_2026-10-11_1347_before.md
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| Criterion | Target | Verdict | How I decided |
|---|---|---|---|
| 1. A Matching Query completes all three tools  | 4/5 | 5/5 | In all five tries, the three tools worked as intended and each try ends with a fit card  |  
| 2. An Impossible Query stops before the second tool | 5/5 | 5/5 | All impossible queries in all 5 tries stopped early and the message said what to change in the search |  
| 3. The selected item must survive the whole loop | 5/5 |  |  0/5| While it survived the loop, no id appears in the log and that is what the criterion asks for, the id |
| 4. fit card fllback and content requirement are both enforced| 5/5 | 5/5 | every item has 3-4 sentences and mentions both price and platform|
| 5. search enforces the Price Cap| 5/5 | 5/5 | every try returned under the price capped at $30 so they all passed |  

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path** (`python app.py ask 'vintage graphic tee under $30' --trace`)

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': '30', 'max_price': 30.0}
      out: 1 items: Straight Leg Khaki Trousers — Olive
      →    branch: results, continuing
[3] select_item
      in:  1 results
      out: Straight Leg Khaki Trousers — Olive ($29.0, poshmark)
      →    first result
[4] suggest_outfit
      in:  new_item='Straight Leg Khaki Trousers — Olive', wardrobe=10 items
      out: Here are two specific outfit suggestions that incorporate your new olive straight-leg khaki trousers while pla…
[5] create_fit_card
      in:  new_item='Straight Leg Khaki Trousers — Olive', outfit=<suggest_outfit text>
      out: Scored these olive straight-leg trousers in excellent condition on Poshmark for just $29, and I am officially …
```

The loop works, but step [1] shows the query parser reading the price "30" as `size='30'`, so the search's only match is a pair of W30 trousers, not a tee.

**Empty search** (`python app.py ask 'designer ballgown size XXS under $5' --trace`)

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'deigner bagown', 'size': 'S', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
```

Two steps instead of five: the branch stops before `suggest_outfit`.

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## Failure Modes

Each one triggered on its own, with `search_listings` running over MCP.

**1. Empty search.** `python app.py ask 'designer ballgown size XXS under $5'`

```
  No items found matching 'deigner bagown' under $5.0 in size S. Try different keywords, a higher price, or removing size filters.

0 model calls this session
```

Handled: the loop stopped before `suggest_outfit` and named three things to change. The message also exposes a parser bug in `agent.py::run_agent`: the size regex has no word boundaries, so it took the "s" in "designer" as size S (not XXS) and stripped letters out of the description.

**2. Empty wardrobe.** `python app.py ask 'denim jacket under $50' --empty-wardrobe`

```
(running with an empty wardrobe)

  Found:    90s Track Jacket — Navy/White Stripe — $45.0 on poshmark

  Outfit:   That is an absolute classic find. ... Since you are starting your
            wardrobe from scratch, this jacket is a fantastic anchor piece.
            Here are two distinct ways to style it ...
            [two looks built from essentials to buy, plus a starter checklist]

  Fit card: Scored the ultimate 90s heritage piece today ...

2 model calls this session, 786 prompt + 691 output tokens
```

Handled: `suggest_outfit` returned real advice, not a crash and not an empty string, and the fit card still rendered. Same parser bug: "denim" contains an "m", so it searched with size M and a mangled description, which is why it found a track jacket instead of a denim one.

**3. Model unavailable.** Changed the last character of `GEMINI_API_KEY`, then ran a query I hadn't asked before: `python app.py ask 'corduroy overshirt in olive under $35'`

```
ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

1 model calls this session
```

Not handled by the agent. That clean message came from the catch-all in `app.py::main`, not from my loop: `run_agent` raised, the session (and the listing it had already found) was lost, and the run exited with code 1. Calling `run_agent` directly would have shown a stack trace.

Fix: `agent.py::run_agent` now catches `ModelUnavailable` around `suggest_outfit` and `create_fit_card`, keeps the search result, and puts a message in `session["error"]`. Re-run with a broken key and a new query (`python app.py ask 'faded black denim jacket under $60' --trace`):

```
[3] select_item
      in:  6 results
      out: Vintage Graphic Hoodie — Faded Black ($26.0, depop)
      →    first result
[4] model call failed
      out: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.goo…
      →    ModelUnavailable, stopping

  Found Vintage Graphic Hoodie — Faded Black ($26.0 on depop), but couldn't reach the model to style it: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Fix that and ask again.
```

Now it names what broke and what to do, exits 0, and doesn't hang (about 1 second). I put the key back afterwards.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

