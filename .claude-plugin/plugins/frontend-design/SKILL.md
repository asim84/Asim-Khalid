---
name: frontend-design
description: Use for frontend tasks in the Asim-Khalid Next.js/Tailwind project. Trigger phrases: "create a component", "new page", "add styling", "review UI", "new React component", "style this", "scaffold a page", "design a layout".
---

# frontend-design

A skill for building and maintaining the Next.js + Tailwind CSS frontend in the Asim-Khalid project (`frontend/src`).

## Stack
- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **Language**: TypeScript

## Tasks

### Create a new component
1. Create file at `frontend/src/components/<ComponentName>.tsx`
2. Use functional component with typed props interface
3. Apply Tailwind classes for styling
4. Export as default

### Create a new page
1. Create file at `frontend/src/app/<route>/page.tsx`
2. Follow Next.js App Router conventions
3. Use `'use client'` directive only if the page needs interactivity

### Review UI / styling
1. Read the component file
2. Check for consistent Tailwind usage, spacing, responsiveness
3. Suggest improvements inline

### Add or update styling
1. Use Tailwind utility classes — avoid custom CSS unless necessary
2. Follow mobile-first responsive design (`sm:`, `md:`, `lg:`)
3. Keep class lists readable — split long className strings across lines

## Conventions
- Component filenames: PascalCase (`MyButton.tsx`)
- Keep components small and single-purpose
- Co-locate styles with components using Tailwind (no separate CSS files)
