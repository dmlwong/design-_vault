'use client';

/* =============================================================================
 * Orbit / Client Connected Platform — MarketIQ Research Output (TOOL-RUN FLOW)
 * GOLDEN FLOW DRAFT — embodies design-brain/interaction-defaults.md (the 8 heuristics).
 *
 * This is the "what the Contract Analysis prototype SHOULD have been" — same shape
 * (an AI tool that produces a deliverable), DIFFERENT tool (MarketIQ research, not
 * contract analysis) so it teaches the shape without being the test's answer key.
 *
 * INTERACTION-DEFAULTS APPLIED  (and how this inverts the contract-analysis anti-example)
 * -----------------------------------------------------------------------------
 *  #1 Flow shape — form, not wizard
 *     ONE surface. No 4-step Scope→Documents→Focus→Output stepper. The handful of
 *     parameters live in a compact bar; generation is a single action.
 *     (anti-example: a 4-step wizard for ~8 fields.)
 *
 *  #2 The deliverable is the hero (content-first IA)
 *     The research OUTPUT owns the surface. Configuration is a slim top bar, not the
 *     whole screen. Before any run, the output area itself holds the empty-state CTA —
 *     you are never sent through pages of config with the result hidden behind a button.
 *     (anti-example: an all-configuration screen ending in a list of slide titles.)
 *
 *  #3 Restraint in status color
 *     Status = StatusIndicator / Badge / a single error rail. NO whole cards tinted
 *     Information/Success/Highlight for decoration. The generating state is an inline
 *     status + skeleton, not a coloured container.
 *     (anti-example: Card state="Information"/"Success"/"Error" used as decoration.)
 *
 *  #4 Don't proceduralise a selection that can be inline
 *     Category/regions are inline controls in the params bar. The ONE selection big
 *     enough to earn its own surface — choosing the initiative — uses a focused modal
 *     (the sanctioned escape; mirrors the MarketIQ select-initiative precedent), not a
 *     wizard step. (anti-example: a whole "Documents" step that was just a table.)
 *
 *  #5 Minimise steps-to-goal; cut ceremony
 *     No "Launch MarketIQ" intro card, no "Review setup" step, no generic "Next, you
 *     can…" card. Actions are concrete and tied to the output (Save, Download, Re-run).
 *     The common path is one click: Generate.
 *
 *  #6 Match the platform's interaction model (Jakob's law)
 *     OrbitAppShell + PageHeader(type="tool") with the initiative pill, preserving the
 *     selected-initiative context in the shell — the MarketIQ precedent's guidance.
 *
 *  #7 Progressive disclosure + smart defaults
 *     Category + initiative are the essentials; regions/scope are pre-filled sensible
 *     defaults tucked behind an "Adjust parameters" disclosure so the first view is
 *     one decision, not twelve.
 *
 *  #8 Demo affordances are dev-only
 *     No Ready/Loading/Empty/Error toggler shipped in the UI. State is driven by the
 *     `state` prop (a real data state), exactly the way work-card-research-primer does.
 *     (anti-example: a Ready/Loading/Empty/Error button group baked into the screen.)
 *
 * TOKENS ONLY (AGENTS.md §2.1): every visual value is an --orbit-* token; theme-agnostic
 * (renders in efficio :root and orbit [data-theme="orbit"]). No chart component exists in
 * Orbit (data-viz tokens are a known gap) — so the output is numeric metric tiles + a
 * Table, never an invented chart.
 *
 * COMPONENT API NOTE: uses Card WITHOUT the deprecated `type` prop (Card.tsx marks
 * `type` @deprecated — prefer `hasShadow`); flat surfaces omit shadow by default.
 * ========================================================================== */

import React, { useId, useRef, useState } from 'react';
import {
  Badge,
  Button,
  Card,
  Dropdown,
  FA,
  FaIcon,
  HeaderPresets,
  Headings,
  IconButton,
  MultiSelectDropdown,
  Overlay,
  PageHeader,
  Spinner,
  StatusIndicator,
  Table,
  Text,
  type TableColumn,
} from '@efficio/orbit';
import { OrbitAppShell } from '@/components/feature/orbit-shell';

/* Glyphs not yet on `FA` — declared locally but still rendered through the canonical
 * FaIcon primitive (the ClauseIQ/work-card pattern). No external icon library. */
const ICON_DOWNLOAD = ''; // fa-arrow-down-to-line
const ICON_ROTATE = ''; // fa-arrows-rotate (re-run)
const ICON_CHART = ''; // fa-chart-column (output empty-state glyph)

/* ----------------------------------------------------------------------------
 * Data model
 * ------------------------------------------------------------------------- */

export type ResearchState = 'empty' | 'generating' | 'ready' | 'error';

export interface ResearchMetric {
  id: string;
  label: string;
  value: string;
  /** Direction of the delta drives a non-colour-only StatusIndicator. */
  trend?: 'up' | 'down' | 'flat';
  delta?: string;
}

export interface SupplierRow {
  id: string;
  supplier: string;
  region: string;
  marketShare: string;
  priceIndex: string;
  movement: 'Rising' | 'Stable' | 'Declining';
}

export interface ResearchFinding {
  id: string;
  title: string;
  body: string;
}

export interface ResearchParams {
  initiativeCode: string;
  initiativeName: string;
  category: string;
  regions: string[];
}

export interface MarketIqResearchOutputProps {
  state?: ResearchState;
  params: ResearchParams;
  categoryOptions?: { label: string; value: string }[];
  regionOptions?: { label: string; value: string }[];
  generatedAt?: string;
  savedToInitiative?: boolean;
  metrics?: ResearchMetric[];
  findings?: ResearchFinding[];
  suppliers?: SupplierRow[];
  density?: 'Default' | 'Compact';

  onGenerate?: (params: { category: string; regions: string[] }) => void;
  onReRun?: (params: { category: string; regions: string[] }) => void;
  onSave?: () => void;
  onDownload?: () => void;
  onChooseInitiative?: () => void;
  onRetry?: () => void;
}

/* ----------------------------------------------------------------------------
 * Movement → approved status mapping (badge-status.md style; colour never alone)
 * ------------------------------------------------------------------------- */

const MOVEMENT_STATUS: Record<
  SupplierRow['movement'],
  { status: 'Success' | 'Warning' | 'Information'; label: string }
> = {
  Rising: { status: 'Warning', label: 'Rising' },
  Stable: { status: 'Information', label: 'Stable' },
  Declining: { status: 'Success', label: 'Declining' },
};

const TREND_STATUS: Record<
  NonNullable<ResearchMetric['trend']>,
  'Warning' | 'Success' | 'No Status'
> = {
  up: 'Warning',
  down: 'Success',
  flat: 'No Status',
};

/* ----------------------------------------------------------------------------
 * Parameters bar — slim, inline, smart-defaulted. The config is NEVER the screen.
 * Essentials inline; the rest behind an "Adjust parameters" disclosure (#7).
 * ------------------------------------------------------------------------- */

function ParamsBar({
  params,
  categoryOptions,
  regionOptions,
  busy,
  hasOutput,
  onCategory,
  onRegions,
  onChooseInitiative,
  onRun,
}: {
  params: ResearchParams;
  categoryOptions: { label: string; value: string }[];
  regionOptions: { label: string; value: string }[];
  busy: boolean;
  hasOutput: boolean;
  onCategory: (v: string) => void;
  onRegions: (v: string[]) => void;
  onChooseInitiative: () => void;
  onRun: () => void;
}) {
  const [open, setOpen] = useState(false);

  return (
    <Card padding="Small">
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 'var(--orbit-space-base)',
        }}
      >
        {/* Selected-initiative context, persisted (#6) — opens a focused picker (#4 escape) */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--orbit-space-s)' }}>
          <Text variant="Secondary" size="Small">
            Initiative
          </Text>
          <Text variant="Bold" size="Paragraph">
            {params.initiativeCode} · {params.initiativeName}
          </Text>
          <Button variant="Tertiary" size="Small" onClick={onChooseInitiative} disabled={busy}>
            Change
          </Button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--orbit-space-s)' }}>
          <Button variant="Tertiary" size="Small" onClick={() => setOpen((o) => !o)} disabled={busy}>
            {open ? 'Hide parameters' : 'Adjust parameters'}
          </Button>
          {/* The ONE primary action on the surface (#5). Re-run if output exists. */}
          <Button
            variant="Primary"
            onClick={onRun}
            disabled={busy || params.category === ''}
            icon={hasOutput ? <FaIcon icon={ICON_ROTATE} size={14} color="var(--orbit-color-btn-primary-icon)" /> : undefined}
          >
            {busy ? 'Generating…' : hasOutput ? 'Re-run research' : 'Generate research'}
          </Button>
        </div>
      </div>

      {/* Advanced parameters: disclosed, not a wizard step (#7). Smart defaults already set. */}
      {open && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, calc(var(--orbit-space-mega) * 7)), 1fr))',
            gap: 'var(--orbit-space-base)',
            marginTop: 'var(--orbit-space-base)',
            paddingTop: 'var(--orbit-space-base)',
            borderTop: 'var(--orbit-space-px) solid var(--orbit-color-border-default)',
          }}
        >
          <Dropdown
            label="Category"
            placeholder="Please Select..."
            required
            options={categoryOptions}
            value={params.category}
            onChange={onCategory}
          />
          <MultiSelectDropdown
            label="Regions"
            placeholder="All regions"
            options={regionOptions}
            value={params.regions}
            onChange={onRegions}
          />
        </div>
      )}
    </Card>
  );
}

/* ----------------------------------------------------------------------------
 * Metric tiles — numeric (no chart component exists; data-viz tokens are a gap).
 * Composed from Card + Text + StatusIndicator; restraint, not coloured cards (#3).
 * ------------------------------------------------------------------------- */

function MetricTiles({ metrics, density }: { metrics: ResearchMetric[]; density: 'Default' | 'Compact' }) {
  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, calc(var(--orbit-space-mega) * 4)), 1fr))',
        gap: 'var(--orbit-space-base)',
      }}
    >
      {metrics.map((m) => (
        <Card key={m.id} padding={density === 'Compact' ? 'Small' : 'Base'}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-xs)' }}>
            <Text variant="Secondary" size="Small">
              {m.label}
            </Text>
            <Headings size="Heading 4">{m.value}</Headings>
            {m.delta && m.trend && (
              <StatusIndicator status={TREND_STATUS[m.trend]} size="Small" label={m.delta} ariaLabel={`${m.label} ${m.delta}`} />
            )}
          </div>
        </Card>
      ))}
    </div>
  );
}

/* ----------------------------------------------------------------------------
 * The OUTPUT surface — the hero (#2). Switches on real `state` (#8), never a toggler.
 * ------------------------------------------------------------------------- */

const SUPPLIER_COLUMNS = (): TableColumn<SupplierRow>[] => [
  { id: 'supplier', header: 'Supplier', render: (r) => r.supplier },
  { id: 'region', header: 'Region', render: (r) => r.region },
  { id: 'share', header: 'Market share', render: (r) => r.marketShare },
  { id: 'price', header: 'Price index', render: (r) => r.priceIndex },
  {
    id: 'movement',
    header: 'Movement',
    render: (r) => {
      const m = MOVEMENT_STATUS[r.movement];
      return <StatusIndicator status={m.status} size="Small" label={m.label} ariaLabel={`${r.supplier}: ${m.label}`} />;
    },
  },
];

function OutputSurface({
  state,
  params,
  generatedAt,
  savedToInitiative,
  metrics,
  findings,
  suppliers,
  density,
  onSave,
  onDownload,
  onRetry,
  onRun,
}: {
  state: ResearchState;
  params: ResearchParams;
  generatedAt?: string;
  savedToInitiative?: boolean;
  metrics: ResearchMetric[];
  findings: ResearchFinding[];
  suppliers: SupplierRow[];
  density: 'Default' | 'Compact';
  onSave?: () => void;
  onDownload?: () => void;
  onRetry?: () => void;
  onRun: () => void;
}) {
  const gap = density === 'Compact' ? 'var(--orbit-space-base)' : 'var(--orbit-space-l)';

  /* EMPTY — the CTA lives in the output area itself, not behind pages of config (#2). */
  if (state === 'empty') {
    return (
      <Card padding="Base">
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            gap: 'var(--orbit-space-base)',
            padding: 'var(--orbit-space-xl) var(--orbit-space-base)',
          }}
        >
          <FaIcon icon={ICON_CHART} size={28} color="var(--orbit-color-text-secondary)" />
          <Headings size="Heading 4">No research generated yet</Headings>
          <Text variant="Secondary" size="Paragraph">
            Generate a MarketIQ research output for {params.initiativeName}. You can adjust the
            category and regions in the bar above first.
          </Text>
          <Button variant="Primary" onClick={onRun} disabled={params.category === ''}>
            Generate research
          </Button>
        </div>
      </Card>
    );
  }

  /* GENERATING — inline status + skeleton, NOT a coloured container (#3). */
  if (state === 'generating') {
    return (
      <Card padding="Base">
        <div style={{ display: 'flex', flexDirection: 'column', gap }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--orbit-space-s)' }} role="status">
            <Spinner size="Inline" decorative />
            <Text variant="Bold" size="Paragraph">
              Generating market research for {params.category || params.initiativeName}…
            </Text>
          </div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, calc(var(--orbit-space-mega) * 4)), 1fr))',
              gap: 'var(--orbit-space-base)',
            }}
          >
            {[0, 1, 2, 3].map((i) => (
              <SkeletonBar key={i} width="100%" height="var(--orbit-space-xxl)" />
            ))}
          </div>
          <SkeletonBar width="60%" />
          <SkeletonBar width="85%" />
        </div>
      </Card>
    );
  }

  /* ERROR — the single place a container may carry a status rail (#3 escape). Params preserved. */
  if (state === 'error') {
    return (
      <Card padding="Base" state="Error" indicator>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-base)' }}>
          <StatusIndicator status="Error" label="Generation failed" />
          <Headings size="Heading 4">We couldn’t generate this research</Headings>
          <Text variant="Secondary" size="Paragraph">
            Your parameters are still set, so you can retry without starting over.
          </Text>
          <div>
            <Button variant="Primary" onClick={onRetry}>
              Try again
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  /* READY — the deliverable. Output header (status + save/download NEAR the output),
     metric tiles, findings, market table. This is what owns the screen. */
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap }}>
      <Card padding="Base">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-base)' }}>
          {/* Output header: title + status + actions tied to the output (#5) */}
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              alignItems: 'flex-start',
              justifyContent: 'space-between',
              gap: 'var(--orbit-space-base)',
            }}
          >
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-xs)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--orbit-space-s)' }}>
                <Headings size="Heading 3">Market research — {params.category}</Headings>
                {savedToInitiative ? (
                  <Badge label="Saved to initiative" status="Success" />
                ) : (
                  <Badge label="Not saved" status="No Status" />
                )}
              </div>
              <Text variant="Secondary" size="Small">
                {params.initiativeCode} · {params.initiativeName}
                {generatedAt ? ` · Generated ${generatedAt}` : ''}
                {params.regions.length ? ` · ${params.regions.length} region(s)` : ' · All regions'}
              </Text>
            </div>

            {/* Save/Download placed NEXT TO the output they affect (MarketIQ precedent) */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--orbit-space-s)' }}>
              <Button variant="Secondary" onClick={onSave}>
                {savedToInitiative ? 'Saved' : 'Save to initiative'}
              </Button>
              <Button
                variant="Secondary"
                onClick={onDownload}
                icon={<FaIcon icon={ICON_DOWNLOAD} size={14} />}
              >
                Download
              </Button>
            </div>
          </div>

          {/* Metric tiles — the at-a-glance numbers */}
          <MetricTiles metrics={metrics} density={density} />
        </div>
      </Card>

      {/* Findings — the analytical substance, not config (anti-pattern this inverts) */}
      <Card padding="Base">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-base)' }}>
          <Headings size="Heading 4">Key findings</Headings>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-base)' }}>
            {findings.map((f) => (
              <div key={f.id} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-xs)' }}>
                <Text variant="Bold" size="Paragraph">
                  {f.title}
                </Text>
                <Text variant="Secondary" size="Paragraph">
                  {f.body}
                </Text>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Supplier / market table — dense, compact, real Orbit Table */}
      <Card padding="Base">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-base)' }}>
          <Headings size="Heading 4">Supplier landscape</Headings>
          <Table
            ariaLabel="Supplier market landscape"
            columns={SUPPLIER_COLUMNS()}
            rows={suppliers}
            getRowKey={(r) => r.id}
            density="Compact"
            variant="SeparatedRows"
            emptyState={<Text variant="Secondary">No suppliers matched these parameters.</Text>}
          />
        </div>
      </Card>
    </div>
  );
}

/* Skeleton primitive — same idea as work-card-research-primer (no layout reflow). */
function SkeletonBar({ width, height = 'var(--orbit-space-m)' }: { width: string; height?: string }) {
  return (
    <span
      aria-hidden="true"
      style={{
        display: 'block',
        width,
        height,
        borderRadius: 'var(--orbit-radius-sm)',
        background: 'var(--orbit-color-bg-hover)',
      }}
    />
  );
}

/* ----------------------------------------------------------------------------
 * Initiative picker — the ONE selection big enough for a focused surface (#4 escape).
 * A searchable modal table, mirroring the MarketIQ select-initiative precedent — NOT
 * a wizard step.
 * ------------------------------------------------------------------------- */

interface Initiative {
  id: string;
  code: string;
  name: string;
  category: string;
}

function InitiativePicker({
  open,
  initiatives,
  onClose,
  onSelect,
}: {
  open: boolean;
  initiatives: Initiative[];
  onClose: () => void;
  onSelect: (i: Initiative) => void;
}) {
  const titleId = useId();
  const columns: TableColumn<Initiative>[] = [
    { id: 'code', header: 'Code', render: (i) => i.code },
    { id: 'name', header: 'Initiative', render: (i) => i.name },
    { id: 'category', header: 'Category', render: (i) => i.category },
    {
      id: 'pick',
      header: '',
      render: (i) => (
        <Button variant="Tertiary" size="Small" onClick={() => onSelect(i)}>
          Select
        </Button>
      ),
    },
  ];

  return (
    <Overlay visible={open} onClose={onClose} ariaLabelledBy={titleId} size="Default" height="Content">
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--orbit-space-l)', padding: 'var(--orbit-space-l)' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 'var(--orbit-space-base)' }}>
          <Headings size="Heading 4">
            <span id={titleId}>Choose an initiative</span>
          </Headings>
          <IconButton
            variant="Tertiary"
            size="Medium"
            ariaLabel="Close initiative picker"
            onClick={onClose}
            icon={<FaIcon icon={FA.xmark} size={14} color="var(--orbit-color-text-primary)" />}
          />
        </div>
        <Table
          ariaLabel="Initiatives"
          columns={columns}
          rows={initiatives}
          getRowKey={(i) => i.id}
          density="Compact"
          variant="SeparatedRows"
        />
      </div>
    </Overlay>
  );
}

/* ----------------------------------------------------------------------------
 * The flow — a SINGLE surface: params bar + output hero. No stepper, no intro card.
 * ------------------------------------------------------------------------- */

export function MarketIqResearchOutput({
  state = 'empty',
  params,
  categoryOptions = [],
  regionOptions = [],
  generatedAt,
  savedToInitiative = false,
  metrics = [],
  findings = [],
  suppliers = [],
  density = 'Default',
  onGenerate,
  onReRun,
  onSave,
  onDownload,
  onChooseInitiative,
  onRetry,
}: MarketIqResearchOutputProps) {
  const [category, setCategory] = useState(params.category);
  const [regions, setRegions] = useState<string[]>(params.regions);
  const [pickerOpen, setPickerOpen] = useState(false);

  const busy = state === 'generating';
  const hasOutput = state === 'ready';
  const liveParams: ResearchParams = { ...params, category, regions };

  const run = () => {
    const payload = { category, regions };
    if (hasOutput) onReRun?.(payload);
    else onGenerate?.(payload);
  };

  return (
    <OrbitAppShell activeItem="Home">
      {/* PageHeader: tool header + initiative pill (platform convention, #6).
          MarketIQ is an Identify-phase tool → HeaderPresets.identify. */}
      <PageHeader
        type="tool"
        title="MarketIQ"
        subtitle="Market research for your initiative"
        icon={ICON_CHART}
        pill={{ code: params.initiativeCode, label: params.initiativeName }}
        {...HeaderPresets.identify}
      />

      <main
        style={{
          padding: 'var(--orbit-space-l)',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <div
          style={{
            width: 'min(100%, calc(var(--orbit-space-mega) * 24))',
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--orbit-space-l)',
          }}
        >
          <ParamsBar
            params={liveParams}
            categoryOptions={categoryOptions}
            regionOptions={regionOptions}
            busy={busy}
            hasOutput={hasOutput}
            onCategory={setCategory}
            onRegions={setRegions}
            onChooseInitiative={() => {
              onChooseInitiative?.();
              setPickerOpen(true);
            }}
            onRun={run}
          />

          <OutputSurface
            state={state}
            params={liveParams}
            generatedAt={generatedAt}
            savedToInitiative={savedToInitiative}
            metrics={metrics}
            findings={findings}
            suppliers={suppliers}
            density={density}
            onSave={onSave}
            onDownload={onDownload}
            onRetry={onRetry}
            onRun={run}
          />
        </div>
      </main>

      <InitiativePicker
        open={pickerOpen}
        initiatives={[]}
        onClose={() => setPickerOpen(false)}
        onSelect={() => setPickerOpen(false)}
      />
    </OrbitAppShell>
  );
}

export default MarketIqResearchOutput;
