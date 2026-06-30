'use client';

/* =============================================================================
 * Connected Platform — Research Primer card ("research primer" work card)
 * Single React/TSX component built to the Orbit Design Brain.
 *
 * BRAIN RULES / CONTRACTS / DEFAULTS APPLIED
 * -----------------------------------------------------------------------------
 * Platform (AGENTS.md §2.2, platforms/connected-platform.md)
 *   - Platform identified FIRST as Connected Platform (internal Efficio users:
 *     Delivery Consultant / Category Analyst). This is the CP workspace
 *     research-primer card from the discovery pack (CP-led, no standalone client
 *     release). CP copy is concise/operational ("Download", "Re-run", "Re-run
 *     research"); no client-facing explanatory framing.
 *
 * Tokens only (AGENTS.md §2.1, defaults.md)
 *   - Zero hardcoded colours/spacing/radius/shadow/z-index/font sizes. Every
 *     visual value resolves through --orbit-* tokens. Theme-agnostic: renders in
 *     both `efficio`/CP (:root) and `orbit` ([data-theme="orbit"]) because all
 *     values come from tokens, never theme-conditional component logic.
 *
 * work-card pattern (patterns/work-card.md)
 *   - Card has no header/action slots, so the titled content card is composed via
 *     the work-card anatomy: Header (eyebrow + title + status) -> Metadata
 *     (timestamp + who-generated) -> Actions row. Scan order title -> status ->
 *     metadata -> actions. NO summarised body prose (discovery pack: remove
 *     summarised text + remove GPT name; 250-char primer label cap).
 *
 * card-panel contract (components/card-panel.md + defaults.md "Cards")
 *   - <Card type="Dynamic" padding="Base"> (Small when compact). Never nested.
 *     Status states (Information/Success) tint the surface + show the rail via the
 *     `indicator` rail to mirror the ClauseIQ completed-card treatment.
 *
 * button contract (components/button.md + defaults.md "Buttons & actions")
 *   - Exactly ONE Primary per view = "Re-run research" (the modal confirm) / the
 *     "Re-run" action that opens it. Download = Secondary. Share = IconButton
 *     (icon-only action) with ariaLabel (paper-plane). Verb-led sentence-case
 *     labels. Button has no loading state (gap report) -> the running state
 *     disables the action row instead of faking a spinner-button.
 *
 * dialog contract (components/dialog.md + defaults.md "Dialogs & overlays")
 *   - Re-run modal = <Overlay size="Default" height="Content"> mirroring the
 *     "add initiative" modal (InitiativeSelectionModal): titled via
 *     ariaLabelledBy, focus-trapped, Escape/backdrop close, focus returns to the
 *     triggering Re-run control. Category = Dropdown (single, "Please Select..."),
 *     Countries = MultiSelectDropdown. Field gaps use form defaults
 *     (--orbit-space-base between fields, --orbit-space-xs label->input).
 *
 * badge-status / status-indicator contracts (approved workflow mappings)
 *   - Tool-coverage rows use StatusIndicator (dot + label) — the compact inline
 *     row primitive. Card-level "Shared by client" uses Badge (filled chip).
 *     APPROVED MAPPINGS USED:
 *       Completed         -> "Success"     [SOURCED]
 *       Running           -> "Information"  [SOURCED]   (discovery "In Progress")
 *       Shared by client  -> "Information"  (settled, badge-status.md)
 *       Failed            -> "Error"        (settled, badge-status.md)
 *     Colour is NEVER alone — every status pairs with text.
 *
 * Accessibility (AGENTS.md §2.4, accessibility.md)
 *   - All actions are Orbit controls (native buttons, visible focus ring via
 *     tokens), keyboard-operable. Icons are decorative (FaIcon ariaHidden); the
 *     accessible name lives on the control. Tool-coverage list is a described
 *     region; timestamp/owner are label/value metadata, not prose.
 *
 * State + role (AGENTS.md §2.7, work-card.md page-level states)
 *   - States present: default/completed, running (auto-trigger), loading skeleton
 *     (same card shape/density), EMPTY (no category -> no pack created), error
 *     (recovery action), disabled/permission-limited (re-run only for
 *     Efficio-led / Jointly-led per discovery Journey B), plus the modal's
 *     submitting state. Tool-coverage = exactly 2 states (Completed, Running) +
 *     empty, per discovery ("auto-triggered, so no incomplete state").
 *
 * ICON LIBRARY / COMPONENT USED — and why
 * -----------------------------------------------------------------------------
 *   USED: Orbit's `FaIcon` primitive (Font Awesome 6 Pro, local OTF via
 *   @font-face) driven by the exported `FA` unicode constants, plus a few
 *   prototype-style local unicode constants (download , rotate ,
 *   paper-plane ) for glyphs not yet in `FA` — exactly the pattern the
 *   ClauseIQ prototype uses (ICON_DOWNLOAD/ICON_ROTATE).
 *   WHY: defaults.md "Icons" is explicit — FaIcon is THE icon component (61 uses
 *   in source); Orbit has NO other icon library installed and importing
 *   lucide-react / react-icons / @fortawesome/* is a forbidden defect (0 uses,
 *   not a dependency). Icons are decorative (ariaHidden) by default.
 *
 * GOLDEN EXAMPLE — canonical `work-card` reference. Cleaned from the 2026-06-23
 * stress test (scored 17/18, visually confirmed in efficio + orbit themes); the
 * hardcoded border width was replaced with `--orbit-space-px`.
 * Settled decisions (owner-approved 2026-06-24): "Shared by client" -> Information;
 * "Failed" -> Error. (CP personas remain [CONFIRM] and CP shell/density biases
 * [SCREENSHOT] in-review — see the platform profile; they don't affect this card.)
 * ========================================================================== */

import React, { useId, useRef, useState } from 'react';
import {
  Card,
  Button,
  IconButton,
  Overlay,
  Badge,
  StatusIndicator,
  Dropdown,
  MultiSelectDropdown,
  Headings,
  Text,
  FaIcon,
  FA,
} from '@efficio/orbit';

/* Icon unicode not yet exported on `FA` — defined locally exactly as the
 * ClauseIQ prototype does (ICON_DOWNLOAD/ICON_ROTATE). Still rendered through
 * the canonical FaIcon primitive; no external icon library is imported. */
const ICON_DOWNLOAD = ''; // fa-arrow-down-to-line
const ICON_ROTATE = ''; // fa-arrows-rotate (re-run)
const ICON_PAPER_PLANE = ''; // fa-paper-plane (share to CP)
const ICON_FOLDER_OPEN = ''; // empty-state glyph

const PRIMER_CHAR_LIMIT = 250;

/* ----------------------------------------------------------------------------
 * Types
 * ------------------------------------------------------------------------- */

/** Discovery: Key Tool Coverage Card = exactly 2 states + empty. */
export type ToolCoverageState = 'Completed' | 'Running';

export interface ToolCoverageItem {
  id: string;
  name: string;
  state: ToolCoverageState;
}

/** Card-level lifecycle states (work-card page-level states). */
export type PrimerCardState =
  | 'completed' // default: a generated primer exists
  | 'running' // auto-triggered generation in flight
  | 'loading' // initial fetch skeleton
  | 'empty' // no category selected -> no pack created
  | 'error'; // generation/fetch failed -> recovery

export interface ResearchPrimerCardProps {
  /** Initiative this primer belongs to. */
  initiativeName: string;
  /** Generated primer title/identifier (NOT summarised body prose). */
  primerTitle: string;
  /** When it was generated, pre-formatted (metadata, not prose). */
  generatedAt?: string;
  /**
   * Who generated it. Auto-generation defaults to the initiative owner
   * (discovery Journey: "auto -> default to initiative owner").
   */
  generatedBy?: string;
  /** True when the primer was auto-generated (drives the who-generated icon). */
  wasAutoGenerated?: boolean;
  /** Tool-coverage rows (ClauseIQ Key Tool Coverage). */
  toolCoverage?: ToolCoverageItem[];
  /** Card lifecycle state. */
  state?: PrimerCardState;
  /**
   * Re-run is permitted only for Efficio-led / Jointly-led initiatives
   * (discovery Journey B). Disables the action row with a visible reason.
   */
  canReRun?: boolean;
  /** Shared to the CP share modal -> "Shared by client" status (Orbit->CP). */
  sharedByClient?: boolean;
  /** Compact density for dense CP workspaces. */
  density?: 'Default' | 'Compact';
  /** Category options for the re-run modal. */
  categoryOptions?: { label: string; value: string }[];
  /** Country options for the re-run modal. */
  countryOptions?: { label: string; value: string }[];

  onDownload?: () => void;
  /** Fires on re-run confirm; sends a notification (discovery: notify on re-run). */
  onReRun?: (params: { category: string; countries: string[] }) => void;
  onShare?: () => void;
  /** Empty-state CTA: select a category to create the pack. */
  onSelectCategory?: () => void;
  /** Error-state recovery. */
  onRetry?: () => void;
}

/* ----------------------------------------------------------------------------
 * Status mapping (approved workflow mappings — badge-status.md)
 * ------------------------------------------------------------------------- */

const TOOL_STATUS: Record<
  ToolCoverageState,
  { indicator: 'Success' | 'Information'; label: string }
> = {
  Completed: { indicator: 'Success', label: 'Completed' },
  Running: { indicator: 'Information', label: 'Running' },
};

/* ----------------------------------------------------------------------------
 * Re-run modal — mirrors the "add initiative" modal (Overlay + Dropdown +
 * MultiSelectDropdown). Category required; Countries optional/multi.
 * ------------------------------------------------------------------------- */

interface ReRunModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: (params: { category: string; countries: string[] }) => void;
  categoryOptions: { label: string; value: string }[];
  countryOptions: { label: string; value: string }[];
}

function ReRunModal({
  open,
  onClose,
  onConfirm,
  categoryOptions,
  countryOptions,
}: ReRunModalProps) {
  const titleId = useId();
  const [category, setCategory] = useState('');
  const [countries, setCountries] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [attempted, setAttempted] = useState(false);

  // Discovery decision: no category selected -> no pack created. Category required.
  const categoryMissing = attempted && category === '';

  const handleConfirm = () => {
    if (category === '') {
      setAttempted(true);
      return;
    }
    setSubmitting(true);
    onConfirm({ category, countries });
  };

  const handleClose = () => {
    if (submitting) return;
    setCategory('');
    setCountries([]);
    setAttempted(false);
    onClose();
  };

  return (
    <Overlay
      visible={open}
      onClose={handleClose}
      ariaLabelledBy={titleId}
      size="Default"
      height="Content"
    >
      {/* Overlay has no header/footer slots (dialog gap report) — composed here. */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--orbit-space-l)',
          padding: 'var(--orbit-space-l)',
        }}
      >
        {/* Header: visible title + close control (dialog contract) */}
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            gap: 'var(--orbit-space-base)',
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-xs)' }}>
            <Headings size="Heading 4">
              <span id={titleId}>Re-run research</span>
            </Headings>
            <Text variant="Secondary" size="Paragraph">
              Choose the category and countries to regenerate this research primer.
            </Text>
          </div>
          <IconButton
            variant="Tertiary"
            size="Medium"
            ariaLabel="Close re-run dialog"
            onClick={handleClose}
            icon={<FaIcon icon={FA.xmark} size={14} color="var(--orbit-color-text-primary)" />}
          />
        </div>

        {/* Fields — gap = --orbit-space-base (form defaults) */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-base)' }}>
          <Dropdown
            label="Category"
            placeholder="Please Select..."
            required
            options={categoryOptions}
            value={category}
            onChange={(next) => {
              setCategory(next);
              setAttempted(false);
            }}
            invalid={categoryMissing}
            message={categoryMissing ? 'Select a category to create the pack.' : undefined}
          />
          <MultiSelectDropdown
            label="Countries"
            placeholder="Please Select..."
            options={countryOptions}
            value={countries}
            onChange={setCountries}
          />
        </div>

        {/* Footer actions — Tertiary cancel + single Primary confirm */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            gap: 'var(--orbit-space-s)',
            paddingTop: 'var(--orbit-space-base)',
            borderTop: 'var(--orbit-space-px) solid var(--orbit-color-border-default)',
          }}
        >
          <Button variant="Tertiary" onClick={handleClose} disabled={submitting}>
            Cancel
          </Button>
          <Button
            variant="Primary"
            onClick={handleConfirm}
            disabled={submitting}
            icon={
              <FaIcon
                icon={ICON_ROTATE}
                size={14}
                color="var(--orbit-color-btn-primary-icon)"
              />
            }
          >
            {submitting ? 'Re-running…' : 'Re-run research'}
          </Button>
        </div>
      </div>
    </Overlay>
  );
}

/* ----------------------------------------------------------------------------
 * Tool-coverage list — StatusIndicator rows (2 states + empty)
 * ------------------------------------------------------------------------- */

function ToolCoverage({
  items,
  density,
}: {
  items: ToolCoverageItem[];
  density: 'Default' | 'Compact';
}) {
  const indicatorSize = density === 'Compact' ? 'Small' : 'Default';

  if (items.length === 0) {
    // Empty: no category selected -> no pack created (so no tool coverage).
    return (
      <Text variant="Secondary" size="Small">
        No tool coverage yet — generate a primer to populate it.
      </Text>
    );
  }

  return (
    <ul
      style={{
        listStyle: 'none',
        margin: 'var(--orbit-space-0)',
        padding: 'var(--orbit-space-0)',
        display: 'flex',
        flexDirection: 'column',
        gap: density === 'Compact' ? 'var(--orbit-space-xs)' : 'var(--orbit-space-s)',
      }}
    >
      {items.map((item) => {
        const mapped = TOOL_STATUS[item.state];
        return (
          <li
            key={item.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 'var(--orbit-space-base)',
            }}
          >
            <Text variant="Primary" size="Paragraph">
              {item.name}
            </Text>
            <StatusIndicator
              status={mapped.indicator}
              size={indicatorSize}
              label={mapped.label}
              ariaLabel={`${item.name}: ${mapped.label}`}
            />
          </li>
        );
      })}
    </ul>
  );
}

/* ----------------------------------------------------------------------------
 * Loading skeleton — same card shape/density (work-card: no spinner reflow)
 * ------------------------------------------------------------------------- */

function SkeletonBar({ width }: { width: string }) {
  return (
    <span
      aria-hidden="true"
      style={{
        display: 'block',
        width,
        height: 'var(--orbit-space-m)',
        borderRadius: 'var(--orbit-radius-sm)',
        background: 'var(--orbit-color-bg-hover)',
      }}
    />
  );
}

/* ----------------------------------------------------------------------------
 * Main card
 * ------------------------------------------------------------------------- */

export function ResearchPrimerCard({
  initiativeName,
  primerTitle,
  generatedAt,
  generatedBy,
  wasAutoGenerated = false,
  toolCoverage = [],
  state = 'completed',
  canReRun = true,
  sharedByClient = false,
  density = 'Default',
  categoryOptions = [],
  countryOptions = [],
  onDownload,
  onReRun,
  onShare,
  onSelectCategory,
  onRetry,
}: ResearchPrimerCardProps) {
  const [modalOpen, setModalOpen] = useState(false);
  const reRunTriggerRef = useRef<HTMLButtonElement>(null);

  const padding = density === 'Compact' ? 'Small' : 'Base';
  const sectionGap =
    density === 'Compact' ? 'var(--orbit-space-base)' : 'var(--orbit-space-m)';

  // Card surface state -> token-tinted surface + rail (card-panel contract).
  const cardState =
    state === 'error' ? 'Error' : state === 'running' ? 'Information' : 'Default';
  const showRail = cardState !== 'Default';

  // Re-run disabled while running, while loading, or without permission.
  const reRunDisabled = !canReRun || state === 'running' || state === 'loading';

  const openReRun = () => setModalOpen(true);
  const closeReRun = () => {
    setModalOpen(false);
    reRunTriggerRef.current?.focus(); // return focus to trigger (work-card)
  };
  const confirmReRun = (params: { category: string; countries: string[] }) => {
    onReRun?.(params); // sends notification on re-run (discovery)
    setModalOpen(false);
    reRunTriggerRef.current?.focus();
  };

  /* ---- EMPTY: no category selected -> no pack created --------------------- */
  if (state === 'empty') {
    return (
      <Card type="Dynamic" padding={padding}>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            gap: 'var(--orbit-space-base)',
          }}
        >
          <FaIcon
            icon={ICON_FOLDER_OPEN}
            size={24}
            color="var(--orbit-color-text-secondary)"
          />
          <Headings size="Heading 5">No research primer yet</Headings>
          <Text variant="Secondary" size="Paragraph">
            No category is selected for {initiativeName}, so no pack was created.
            Select a category to generate the primer.
          </Text>
          <Button variant="Primary" onClick={onSelectCategory}>
            Select category
          </Button>
        </div>
      </Card>
    );
  }

  /* ---- LOADING: skeleton in the same card shape/density ------------------- */
  if (state === 'loading') {
    return (
      <Card type="Dynamic" padding={padding}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: sectionGap }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-s)' }}>
            <SkeletonBar width="40%" />
            <SkeletonBar width="70%" />
          </div>
          <SkeletonBar width="55%" />
          <div style={{ display: 'flex', gap: 'var(--orbit-space-s)' }}>
            <SkeletonBar width="var(--orbit-space-xxl)" />
            <SkeletonBar width="var(--orbit-space-xxl)" />
          </div>
        </div>
      </Card>
    );
  }

  /* ---- COMPLETED / RUNNING / ERROR --------------------------------------- */
  const ownerName = generatedBy ?? initiativeName + ' owner';

  return (
    <>
      <Card type="Dynamic" padding={padding} state={cardState} indicator={showRail}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: sectionGap }}>
          {/* HEADER: eyebrow + title + status (scan order: title -> status) */}
          <div
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              justifyContent: 'space-between',
              gap: 'var(--orbit-space-base)',
            }}
          >
            <div
              style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-xs)' }}
            >
              <Text variant="Secondary" size="Small">
                {initiativeName}
              </Text>
              {/* Title only — NO summarised body prose; capped to the primer limit */}
              <Headings size="Heading 5">
                {primerTitle.length > PRIMER_CHAR_LIMIT
                  ? `${primerTitle.slice(0, PRIMER_CHAR_LIMIT - 1)}…`
                  : primerTitle}
              </Headings>
            </div>

            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--orbit-space-s)',
                flexShrink: 0,
              }}
            >
              {state === 'running' && (
                <StatusIndicator
                  status="Information"
                  size={density === 'Compact' ? 'Small' : 'Default'}
                  label="Running"
                  ariaLabel={`${primerTitle}: research running`}
                />
              )}
              {state === 'error' && (
                <StatusIndicator
                  status="Error"
                  size={density === 'Compact' ? 'Small' : 'Default'}
                  label="Failed"
                  ariaLabel={`${primerTitle}: generation failed`}
                />
              )}
              {/* "Shared by client" chip — Information (settled per badge-status.md) */}
              {sharedByClient && state !== 'error' && (
                <Badge label="Shared by client" status="Information" />
              )}
            </div>
          </div>

          {/* METADATA: timestamp + who-generated (label/value, not prose) */}
          {state !== 'error' && (
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                alignItems: 'center',
                gap: 'var(--orbit-space-base)',
              }}
            >
              {generatedAt && (
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--orbit-space-xs)' }}>
                  <FaIcon icon={FA.file} size={12} color="var(--orbit-color-text-secondary)" />
                  <Text variant="Secondary" size="Small">
                    {state === 'running' ? 'Generating…' : `Generated ${generatedAt}`}
                  </Text>
                </span>
              )}
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--orbit-space-xs)' }}>
                {/* Who-generated icon: auto -> initiative owner */}
                <FaIcon
                  icon={wasAutoGenerated ? FA.smile : FA.user}
                  size={12}
                  color="var(--orbit-color-text-secondary)"
                />
                <Text variant="Secondary" size="Small">
                  {wasAutoGenerated ? `Auto-generated · ${ownerName}` : ownerName}
                </Text>
              </span>
            </div>
          )}

          {/* ERROR body + recovery action */}
          {state === 'error' && (
            <Text variant="Error" size="Paragraph">
              We couldn’t generate the research primer for {initiativeName}. Try again,
              or re-run with different parameters.
            </Text>
          )}

          {/* TOOL COVERAGE (Key Tool Coverage) — 2 states + empty */}
          {state !== 'error' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-s)' }}>
              <Text variant="Secondary" size="Small">
                Key tool coverage
              </Text>
              <ToolCoverage items={toolCoverage} density={density} />
            </div>
          )}

          {/* ACTIONS: one Primary (Re-run) + Download Secondary + Share IconButton.
              Permission/running disables the row with a visible reason. */}
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              alignItems: 'center',
              gap: 'var(--orbit-space-s)',
            }}
          >
            {state === 'error' ? (
              <Button variant="Primary" onClick={onRetry}>
                Try again
              </Button>
            ) : (
              <>
                <Button
                  ref={reRunTriggerRef}
                  variant="Primary"
                  onClick={openReRun}
                  disabled={reRunDisabled}
                  icon={
                    <FaIcon
                      icon={ICON_ROTATE}
                      size={14}
                      color="var(--orbit-color-btn-primary-icon)"
                    />
                  }
                >
                  Re-run
                </Button>
                <Button
                  variant="Secondary"
                  onClick={onDownload}
                  disabled={state === 'running'}
                  icon={<FaIcon icon={ICON_DOWNLOAD} size={14} />}
                >
                  Download
                </Button>
                {/* Paper-plane Share -> CP share modal (Orbit->CP) */}
                <IconButton
                  variant="Tertiary"
                  size="Medium"
                  ariaLabel="Share research to Connected Platform"
                  onClick={onShare}
                  disabled={state === 'running'}
                  icon={<FaIcon icon={ICON_PAPER_PLANE} size={14} />}
                />
              </>
            )}
          </div>

          {/* Visible disabled reason (permission-limited, work-card) */}
          {!canReRun && state !== 'error' && (
            <Text variant="Secondary" size="Small">
              Re-run is available on Efficio-led and Jointly-led initiatives only.
            </Text>
          )}
        </div>
      </Card>

      <ReRunModal
        open={modalOpen}
        onClose={closeReRun}
        onConfirm={confirmReRun}
        categoryOptions={categoryOptions}
        countryOptions={countryOptions}
      />
    </>
  );
}

export default ResearchPrimerCard;
