# Hugging Face publishing checklist

1. Replace anonymous author and citation placeholders if anonymity has ended.
2. Confirm the dataset card and `LICENSE-DATA` still declare CC BY 4.0.
3. Confirm every `redistributed_here` value remains false.
4. Run `python tools/release_audit.py` from the GitHub package root.
5. Create an empty dataset repository under the approved owner.
6. Upload this directory's `README.md` and `data/` contents only.
7. Verify all three configurations render in Dataset Viewer.
8. Confirm no raw media, transcript, labels, embeddings, credentials, or local
   filesystem paths appear in the Files tab.
