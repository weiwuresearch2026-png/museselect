# Website publishing

The static project page is deployed from this directory by the GitHub Pages
workflow. The live release uses the URLs in `config.js` and intentionally leaves
`dataUrl` empty because the standalone Hugging Face release is deferred.

Before each deployment, synchronize both paper PDFs, update the author/citation
metadata, run the release audit, and verify the Pages workflow.

No analytics, cookies, external fonts, or third-party scripts are used.
