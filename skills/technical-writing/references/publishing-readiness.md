# Publishing Readiness

Use this reference when a public post or documentation page is moving from draft/review into preview, scheduling, or publication. It complements `public-safety.md`; it does not replace legal, security, product, or communications approval.

## Publishing Gate

Do not call a piece ready to publish until these checks are either verified or explicitly listed as residual risk:

1. **Front matter and metadata**: title, description, date, slug, tags, canonical URL, author, draft flag, scheduled date, and social preview fields match the intended publication state.
2. **Preview versus production**: preview routes, generated pages, RSS/sitemap entries, OpenGraph cards, and scheduled visibility match the site’s actual build behaviour, not just the local Markdown.
3. **Disclosure safety**: run the public-safety checks against body text, headings, code, screenshots, alt text, links, captions, filenames, and metadata. Metadata leaks are still leaks.
4. **Source grounding**: every concrete architecture, performance, cost, reliability, security, or product claim traces to public sources, approved notes, or safe repo facts.
5. **Operational caveats**: analytics, CSP, cookie consent, embedded media, syntax highlighting, and third-party scripts still work in the production build path.

## High-Risk Publication Traps

- A post can be safe in body copy but unsafe in metadata: slugs, tags, image names, and social descriptions often preserve internal project names after the article text is cleaned.
- A scheduled post can be visible through generated indexes, RSS, sitemap, JSON search data, or preview deployments even when the page route is hidden.
- Analytics or embedded scripts may pass local preview and fail under production CSP, cookie consent, or static-hosting headers.
- Screenshots often leak more than prose: browser tabs, URLs, tenant names, branch names, timestamps, internal UI labels, and user avatars.
- Numbers without nearby caveats become marketing claims when quoted out of context.

## Output Shape

For publishing checks, report:

```text
Ready state
- ready | blocked | ready with residual approval risk

Blocking issues
- Location: issue and required fix.

Pre-publication checks
- Verified: ...
- Not verified: ...

Residual approval risk
- Security/legal/product/comms checks still needed, if any.
```
