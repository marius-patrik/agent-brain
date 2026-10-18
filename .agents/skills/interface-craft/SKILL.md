---
name: interface-craft
description: Use to design or implement a product interface, flow, or component from real user tasks, product references, and interaction requirements. Do not redesign unrelated screens or apply generic visual trends to an already approved UI.
---

# Interface Craft

Own the **creation** of usable, coherent interfaces. `quality-without-slop` owns independent critique of an existing artifact; `behavioral-testing` owns behavioral test cases.

## Procedure

1. **Orient:** identify the actual user, primary task, current product surface, brand/design tokens, platform, accessibility constraints and established components. Inspect screenshots or the running application where permitted. If the task is narrow, preserve surrounding identity.
2. **Select a direction:** for a genuinely new surface, collect relevant product-specific references and choose a clear type hierarchy, spacing system, color/contrast usage and interaction model. State how each decision supports the task; do not mimic a reference blindly.
3. **Model real states:** map navigation, keyboard and pointer actions, focus order, loading/empty/error/success states, validation, long content, small viewports and touch. Keep data and state ownership explicit.
4. **Implement cohesively:** reuse existing UI primitives, styles and libraries before introducing a dependency. Avoid placeholder content masquerading as completed UX, inconsistent status bars, accidental z-index stacks and components that disappear when a sidebar collapses.
5. **Inspect actual behavior:** run the interface in an available browser or host UI tool when authorized; exercise the primary journey, resizing, forms, keyboard, focus and failure states. Do not claim visual quality from compilation alone.
6. **Review:** invite `quality-without-slop` to identify measurable usability, fidelity and maintainability failures. Fix blocking outcomes, not arbitrary aesthetic preferences.

## No-slop decision rule

A common component pattern or style is acceptable when the product needs it. Reject generic treatment **only** when it weakens information hierarchy, identity, navigation or an explicit requirement. Prefer evidence from real user tasks and comparison with existing screens over color/font bans.

## Evidence and boundaries

Provide implemented screens/states, screenshots or links when available, tested interactions, incomplete states and known constraints. For a one-line styling fix, skip a full design exercise. Do not silently change approved branding, accessibility expectations or backend contracts.
