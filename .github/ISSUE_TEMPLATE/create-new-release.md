---
name: Create new release
about: Tasks required to cut a new release

---

- [ ] Ensure all issues in the release milestone are closed or moved to another milestone
- [ ] Ensure the Python versions used in the GitHub workflow are up to date
- [ ] Ensure the README is up to date
- [ ] Update the app version in config.py and wherever else it appears
- [ ] Create the release using a tag with the same name as the release
- [ ] Open a PR updating config.py in the main branch with the new version + "dev", closing this issue
