(() => {
  const config = window.MUSESELECT_RELEASE || {};
  const links = { code: config.codeUrl, data: config.dataUrl };

  document.querySelectorAll("[data-release-link]").forEach((node) => {
    const url = links[node.dataset.releaseLink];
    if (url) {
      node.href = url;
      node.removeAttribute("aria-disabled");
      node.textContent = node.dataset.releaseLink === "code" ? "GitHub Code" : "Hugging Face Data";
    }
  });

  const copyButton = document.querySelector("[data-copy-citation]");
  const citation = document.querySelector("#citation code");
  if (copyButton && citation) {
    copyButton.addEventListener("click", async () => {
      await navigator.clipboard.writeText(citation.textContent);
      copyButton.textContent = "Copied";
      window.setTimeout(() => { copyButton.textContent = "Copy BibTeX"; }, 1600);
    });
  }
})();

