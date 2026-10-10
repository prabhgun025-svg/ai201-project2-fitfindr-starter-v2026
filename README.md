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
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

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

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

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

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



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


