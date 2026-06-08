# Advisory Source Checks

Load this reference when the user provides an unstructured source such as a blog post, news article, social post, screenshot, or vague advisory description.

## Source Priority

1. Primary maintainer or project advisory.
2. Registry or ecosystem advisory: GitHub Security Advisory, npm advisory/audit data, PyPI vulnerability metadata, OSV, CVE/NVD, distro security tracker, or vendor bulletin.
3. Source evidence: release tags, commits, diffs, package tarballs, provenance, signatures, or removed versions.
4. Secondary reporting: blogs, newsletters, social posts, scanners, or vendor write-ups.

Use secondary reporting to find leads, not as final proof. Preserve the difference between "reported by article" and "confirmed by primary source".

## Open Structured Sources

- OSV: query by package ecosystem/name/version or vulnerability ID when package details are known.
- GitHub Security Advisories: check GHSA/CVE aliases, affected package ecosystem, vulnerable version range, patched version, and references.
- GitHub Dependency Review or dependency graph APIs: useful for repository dependency evidence when available.
- npm: use lockfiles first for local evidence; `npm audit --json` and registry advisory data can add vulnerability context but may lag active compromise reports.
- PyPI: project JSON metadata can expose vulnerability entries and release files; pair it with lockfile or environment evidence before deciding exposure.
- Vendor and distro trackers: use for OS packages, base images, and language runtime images.

## Web Fetching And Web Pages

A web-fetch or browser tool is appropriate for reading a provided article or advisory page, but it is not the best primary way to check affectedness. Prefer structured data or primary sources when available because they expose aliases, affected ranges, patched versions, and references more reliably than prose.

Use web fetching when:

- The user supplied a specific article and wants its claims assessed.
- The primary source is only available as a web page.
- Structured APIs do not yet contain a new incident and the article has concrete indicators to verify locally.

## Do Not

- Do not collapse aliases too early; one issue may appear as GHSA, CVE, OSV, npm, PyPI, or vendor IDs.
- Do not assume advisory databases are complete for active malicious-package incidents.
- Do not treat a scanner result as affectedness without checking local version/path/execution evidence.
- Do not quote long article passages; summarise the claim and link the source when web access is used.
