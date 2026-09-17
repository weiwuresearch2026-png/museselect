# Website publishing

The static project page is deployed from this directory by the GitHub Pages
workflow. Before enabling Pages:

1. set `codeUrl`, `dataUrl`, and `websiteUrl` in `config.js`;
2. decide whether the anonymous PDF should remain public during review;
3. update author/citation metadata when anonymity is lifted;
4. run the release audit without `--allow-publication-blockers`;
5. enable **Settings → Pages → Source: GitHub Actions**.

No analytics, cookies, external fonts, or third-party scripts are used.

