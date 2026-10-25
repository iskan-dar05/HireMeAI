# HireMeAI Frontend

The frontend is a Next.js dashboard for authenticated CV creation and management, design selection, profile settings, and ATS scoring workflows. It uses Clerk for authentication and calls the HireMeAI backend API.

## Requirements

- Node.js 22 or later
- pnpm 12.3.4 (the version declared by the project)

## Configure

Set these variables in the frontend process environment (or in `frontend/.env.local`):

```dotenv
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-publishable-key
CLERK_SECRET_KEY=your-clerk-secret-key
```

Configure Clerk redirect and authorized-party settings to match `http://localhost:3000` during local development.

## Run Locally

```bash
pnpm install
pnpm dev
```

Open `http://localhost:3000`. For a production build, run `pnpm build` and then `pnpm start`.

## Notes

The repository uses `pnpm-lock.yaml`. The current frontend Dockerfile expects `package-lock.json`, so its container build needs to be aligned with pnpm before it can be used as-is.
