# Text Humanization System

A multi-pass prompt system for rewriting AI-generated text to pass human scrutiny and reduce AI detection markers.

## Quick Start

**Fastest method:** Use `humanize-text.md` as your system prompt and paste your AI-generated text.

**Most thorough method:** Run the two-pass pipeline below.

## The Two-Pass Pipeline

```
AI-Generated Text
       |
       v
+------------------+
| Pass 1:          |
| semantic-lock.md |
+------------------+
       |
       v
+------------------------+
| Pass 2:                |
| controlled-degradation.md |
+------------------------+
       |
       v
Human-Sounding Output
```

### Pass 1: Semantic Lock (`semantic-lock.md`)

Locks meaning before style changes. Produces flat, boring output on purpose.

- Preserves facts, order, and intent exactly
- Plain, literal language
- No stylistic flourishes
- One thought per sentence

**Why this step?** Prevents meaning drift when you humanize. Creates a stable baseline.

### Pass 2: Controlled Degradation (`controlled-degradation.md`)

Destroys the polished, balanced quality that marks AI writing.

- Introduces uneven rhythms and fragments
- Allows cognitive drift (restating ideas imperfectly)
- Ends abruptly without resolution
- Some sentences may feel unnecessary

**Why this step?** Human writing has imperfections. AI writing is too balanced.

## All-in-One Alternative (`humanize-text.md`)

Combines both passes with three modes:

| Mode | Trigger | Use Case |
|------|---------|----------|
| Humanize | (default) | Standard rewrite for credibility |
| AI-Nullification | Start input with `Mode: Nullify` | Aggressive stripping of AI patterns |
| Ultra-Short | Start input with `Mode: Ultra` | Blunt, minimal rewrite |

## What AI Detectors Look For

These prompts systematically remove common AI markers:

**Structural patterns:**
- Balanced sentence structures
- Clean rhetorical contrasts
- Polished transitions
- Symmetrical constructions

**Overused words:**
- just, very, really, actually, basically
- insight, perspective, significant
- leverage, utilize, ensure, foster
- innovative, transformative, cutting-edge

**Punctuation:**
- Em dashes
- Semicolons

## Usage Examples

### Two-Pass (Claude, GPT, etc.)

```
# Step 1
System prompt: [paste semantic-lock.md]
User: [paste your AI-generated text]

# Step 2
System prompt: [paste controlled-degradation.md]
User: [paste output from step 1]
```

### Single-Pass

```
System prompt: [paste humanize-text.md]
User: [paste your AI-generated text]
```

### Aggressive Mode

```
System prompt: [paste humanize-text.md]
User: Mode: Nullify

[paste your AI-generated text]
```

## When to Use Each Approach

| Situation | Recommended |
|-----------|-------------|
| Quick rewrite | `humanize-text.md` (default mode) |
| Important document | Two-pass pipeline |
| Still detecting as AI after one pass | `Mode: Nullify` |
| Very short text | `Mode: Ultra` |

## Files

| File | Purpose |
|------|---------|
| `semantic-lock.md` | Pass 1: Lock meaning |
| `controlled-degradation.md` | Pass 2: Introduce human imperfection |
| `humanize-text.md` | All-in-one with multiple modes |
