# Contributing

Contributions should keep the skill reusable across repositories, frameworks, hosting providers, and analytics systems.

## Before opening a pull request

1. Keep operational guidance evidence-based and provider-neutral.
2. Put shared routing and safety rules in `SKILL.md`; put detailed phase or adapter guidance in `references/`.
3. Do not add credentials, customer data, private infrastructure details, private repository URLs, organization-specific analytics IDs, or absolute local paths.
4. Preserve the explicit authorization boundary for production mutations.
5. Run:

   ```bash
   python3 scripts/validate.py
   ```

6. Describe the user scenario that motivated the change and the observable decision it improves.

Avoid adding universal rules for a single project's convention. Project-specific commands belong in a downstream adapter, not this repository.
