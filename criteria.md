# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
The search is based on plain keyboard and this means the matching sets are are imperfect so some valid phrases will miss. A strict 5/5 target would be harder to guarantee

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — in 5 of 5 tries.

**Why this target:**
the criteria is direct and has a yes or no system. If the query stops before the second tool, it works but if it does not, it isn't working hence the 5/5 target 

---

## 3. The selected item must survive the whole loop

After `search_listings` returns a result and the loop stores it in `session["selected_item"]`, that same item's `id` and price appear in the session and in the output of both `suggest_outfit` and `create_fit_card` — in 5 of 5 tries.

**Why this target:**
The loop can call all three tools and still be wrong if it switches items between steps. Either the item IDs match or they don't so 5 of 5 is the right target. If state is broken, no other criterion can pass



---

## 4. Fit-card fallback and content requirement are both enforced

`create_fit_card` returns a 2-4 sentence caption that mentions the price of the item and platform - 4 out of 5 tries 



**Why this target:**

wording varies between runs and the acceptance criteria is whether the output is caption-shaped and includes the required details not whether it is word for word identical 
---

## 5. Search enforces the Price Cap 

Given a search with a price ceiling like "under $30", every listing returned by `search_listings` has a price at or below the requested maximum in 5 of 5 tries.

**Why this target:**
Either the prices are below the cap or they aren't. If the search ignores the budget, the result is broken, not close. So 5 of 5 is the right setting



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
