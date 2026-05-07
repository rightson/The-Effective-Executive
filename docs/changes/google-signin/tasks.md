# Tasks

## 1. Make Google sign-in real

- [ ] 1.1 Add `GET /api/config` returning `{google_client_id: string | null}` from the `GOOGLE_CLIENT_ID` env var.
- [ ] 1.2 Load `https://accounts.google.com/gsi/client` from the SPA `index.html`.
- [ ] 1.3 Replace the `prompt()`-based Google handler in `static/app.js` with `google.accounts.id.initialize` + `google.accounts.id.renderButton`.
- [ ] 1.4 On callback, POST the `credential` to `/api/auth/google`, then `auth.loadMe()` and navigate to dashboard.
- [ ] 1.5 Hide the Google button when `/api/config` returns `null`.

**Acceptance evidence:** clicking the Google button opens the Google chooser; choosing an account lands signed in.

## 2. Update spec and docs

- [ ] 2.1 Update `docs/specs/accounts/spec.md` per the change delta (drop SSO non-goal; add Google sign-in requirements).
- [ ] 2.2 Document `GOOGLE_CLIENT_ID` setup in `README.md` (Google Cloud Console, authorized JavaScript origin).

## 3. End-to-end acceptance

- [ ] 3.1 With `GOOGLE_CLIENT_ID` set, sign in as a brand-new Google email creates an account and lands on dashboard.
- [ ] 3.2 With the same Google email, signing in again resumes the existing user.
- [ ] 3.3 With `GOOGLE_CLIENT_ID` unset, the Google button is hidden and password auth still works.
- [ ] 3.4 No code path asks the user to paste a token.
