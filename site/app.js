(function () {
  "use strict";

  var DATA = window.PREMIUM_TASTE_DATA || {
    counts: { principles: 62, antiPatterns: 25, references: 18, directions: 4 },
    directions: [],
    references: [],
    antiPatterns: [],
    tokens: {},
  };
  var Audit = window.PremiumTasteAudit;

  function escapeHtml(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function wireTablist(tablistEl, onChange) {
    if (!tablistEl) return;
    var tabs = Array.prototype.slice.call(tablistEl.querySelectorAll('[role="tab"]'));
    function activate(tab) {
      tabs.forEach(function (t) {
        var active = t === tab;
        t.setAttribute("aria-selected", active ? "true" : "false");
        t.tabIndex = active ? 0 : -1;
        var panelId = t.getAttribute("aria-controls");
        if (panelId) {
          var panel = document.getElementById(panelId);
          if (panel && !panel.classList.contains("stage-sheet")) {
            panel.hidden = !active;
          }
        }
      });
      if (onChange) onChange(tab);
    }
    tabs.forEach(function (tab, idx) {
      tab.tabIndex = tab.getAttribute("aria-selected") === "true" ? 0 : -1;
      tab.addEventListener("click", function () { activate(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = -1;
        if (e.key === "ArrowRight") next = (idx + 1) % tabs.length;
        else if (e.key === "ArrowLeft") next = (idx - 1 + tabs.length) % tabs.length;
        else if (e.key === "Home") next = 0;
        else if (e.key === "End") next = tabs.length - 1;
        if (next !== -1) {
          e.preventDefault();
          tabs[next].focus();
          activate(tabs[next]);
        }
      });
    });
  }

  function wireCopyButton(btn, getText) {
    if (!btn) return;
    var orig = btn.textContent;
    btn.addEventListener("click", function () {
      var text = typeof getText === "function" ? getText() : "";
      if (!text) return;
      function done() {
        btn.textContent = "Copied";
        window.setTimeout(function () { btn.textContent = orig; }, 1500);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(done);
      } else {
        done();
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* 01. SPLIT WORKBENCH SCENARIOS                                       */
  /* ------------------------------------------------------------------ */
  var ROWAN_BOWL_SVG =
    '<svg viewBox="0 0 120 96" width="120" height="96" role="img" aria-label="Wheel-thrown stoneware bowl illustration" style="background:#e5ddcc;border-radius:4px;display:block;width:100%;height:auto;">' +
    '<ellipse cx="60" cy="79" rx="34" ry="5" fill="#d3c8b2"/>' +
    '<path d="M18 32 C18 61, 36 74, 60 74 C84 74, 102 61, 102 32 Z" fill="#efe9dc" stroke="#1c1915" stroke-width="1.4"/>' +
    '<ellipse cx="60" cy="32" rx="42" ry="8" fill="#f7f4ee" stroke="#1c1915" stroke-width="1.4"/>' +
    '<path d="M29 33 C42 40, 78 40, 91 33" fill="none" stroke="#7a3e2e" stroke-width="1.3"/>' +
    '<rect x="44" y="73" width="32" height="5" fill="#e6decb" stroke="#1c1915" stroke-width="1.2"/>' +
    "</svg>";

  var METRICS_BARS_SVG =
    '<svg viewBox="0 0 280 56" width="280" height="56" role="img" aria-label="p99 endpoint latency distribution showing 412 ms auth-edge spike" style="display:block;width:100%;height:auto;">' +
    '<line x1="0" y1="50" x2="280" y2="50" stroke="#e2e2da" stroke-width="1"/>' +
    '<rect x="4" y="38" width="18" height="12" fill="#c7cbc5"/><rect x="26" y="40" width="18" height="10" fill="#c7cbc5"/>' +
    '<rect x="48" y="35" width="18" height="15" fill="#c7cbc5"/><rect x="70" y="39" width="18" height="11" fill="#c7cbc5"/>' +
    '<rect x="92" y="36" width="18" height="14" fill="#c7cbc5"/><rect x="114" y="32" width="18" height="18" fill="#8a5a12"/>' +
    '<rect x="136" y="24" width="18" height="26" fill="#8a5a12"/><rect x="158" y="8" width="18" height="42" fill="#8f2d1f"/>' +
    '<rect x="180" y="12" width="18" height="38" fill="#8f2d1f"/><rect x="202" y="29" width="18" height="21" fill="#8a5a12"/>' +
    '<rect x="224" y="38" width="18" height="12" fill="#185a3f"/><rect x="246" y="41" width="18" height="9" fill="#185a3f"/>' +
    "</svg>";

  var SCENARIOS = {
    ai: {
      beforeLabel: "Without rules · FAIL (17 violations)",
      afterLabel: "precise-technical · ia-writer + figma · PASS",
      notes: [
        { rule: "product.first-screen", text: "Replaces 4 vanity stat boxes and an upgrade banner with context files + diff output immediately." },
        { rule: "chrome.sparkle + type.avoid-tells", text: "Drops sparkles, purple glows, and Inter gradient text for quiet plain action verbs." },
        { rule: "hierarchy.one-primary-action", text: "Keeps Run revision as the single primary action instead of three competing indigo buttons." },
      ],
      beforeHtml: function () {
        return (
          '<div class="mock-before-dark">' +
          '<div class="mock-before-center">' +
          '<div style="font-size:0.7rem;color:#a5b4fc;">✨ Powered by next-gen AI agents</div>' +
          '<p class="mock-before-h1">Supercharge your workflow</p>' +
          '<p class="mock-before-sub">Trusted by 10,000+ AI teams worldwide</p>' +
          "</div>" +
          '<div class="mock-before-grid">' +
          '<div class="mock-before-box">Speed<br/><strong>4.8x</strong></div>' +
          '<div class="mock-before-box">CSAT<br/><strong>99.4%</strong></div>' +
          '<div class="mock-before-box">Saved<br/><strong>420h</strong></div>' +
          "</div>" +
          '<div class="mock-before-ctas">' +
          '<span class="mock-before-pill">✨ Generate Magic</span>' +
          '<span class="mock-before-pill">Upgrade Pro</span>' +
          "</div>" +
          "</div>"
        );
      },
      afterHtml: function () {
        return (
          '<div class="mini-app">' +
          '<div class="mini-app-bar"><span>draftbench / release-notes-v2.4</span><span>1,420 tokens · 38 ms</span></div>' +
          '<div class="mini-ws-grid">' +
          '<div class="mini-ws-rail">' +
          '<strong style="color:var(--ink);">Context</strong>' +
          '<span>changelog.md</span><span>api-diff.json</span><span>webhooks.ts</span>' +
          "</div>" +
          '<div class="mini-ws-main">' +
          '<div style="font-weight:500;font-size:0.875rem;">Tighten webhook header migration copy</div>' +
          '<div class="mini-diff-line">+ Verify signature via X-Event-Sig-256 header.<br/>- Remove deprecated X-Hook-Sig examples.</div>' +
          '<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.75rem;">' +
          '<span style="color:var(--muted);font-family:var(--font-mono);">temperature 0 · diff verified</span>' +
          '<span style="color:var(--accent);font-weight:500;">Run revision →</span>' +
          "</div>" +
          "</div>" +
          "</div>" +
          "</div>"
        );
      },
    },
    rowan: {
      beforeLabel: "Without rules · FAIL (12 violations)",
      afterLabel: "quiet-luxury · aesop + cos · PASS",
      notes: [
        { rule: "uniqueness.material", text: "Swaps cold purple SaaS chrome for Warm Paper (#f3efe6), terracotta ink (#7a3e2e), and quiet clay proportions." },
        { rule: "content.abstract-verbs", text: "Replaces 'Elevate your everyday rituals' with firing temperature, weight, diameter, and price." },
        { rule: "material.gray-card-shadow", text: "Drops rounded drop-shadow cards for one asymmetrical two-column shelf." },
      ],
      beforeHtml: function () {
        return (
          '<div class="mock-before-dark">' +
          '<div class="mock-before-center">' +
          '<p class="mock-before-h1">Elevate your rituals</p>' +
          '<p class="mock-before-sub">Trusted by 10,000+ homes · Seamless craft</p>' +
          "</div>" +
          '<div class="mock-before-grid">' +
          '<div class="mock-before-box">✦ Glow</div>' +
          '<div class="mock-before-box">✦ Next-gen</div>' +
          '<div class="mock-before-box">✦ Unlock Calm</div>' +
          "</div>" +
          '<div class="mock-before-ctas"><span class="mock-before-pill">Shop Now</span><span class="mock-before-pill">Learn More</span></div>' +
          "</div>"
        );
      },
      afterHtml: function () {
        return (
          '<div class="mini-rowan">' +
          '<div>' + ROWAN_BOWL_SVG + "</div>" +
          '<div style="display:grid;gap:0.375rem;">' +
          '<div style="font-family:var(--font-mono);font-size:0.7rem;color:#5c564c;">ROWAN CLAY · BATCH 14</div>' +
          '<div style="font-size:1rem;font-weight:600;">Ash glaze bowl, 185 mm</div>' +
          '<div style="font-size:0.8125rem;color:#5c564c;">Reduction-fired to 1,240°C over speckled stoneware. 490&nbsp;g.</div>' +
          '<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:0.25rem;">' +
          '<strong style="font-family:var(--font-mono);color:#7a3e2e;">$68</strong>' +
          '<span style="font-size:0.8125rem;text-decoration:underline;color:#1c1915;">Reserve firing</span>' +
          "</div>" +
          "</div>" +
          "</div>"
        );
      },
    },
    pricing: {
      beforeLabel: "Without rules · FAIL (13 violations)",
      afterLabel: "precise-technical · stripe-docs · PASS",
      notes: [
        { rule: "skeleton.saas-landing", text: "Turns 3 shadowed 'MOST POPULAR' feature boxes into a scannable specification table." },
        { rule: "content.fake-proof", text: "Deletes 'Trusted by 5,000+ startups' and leads directly with the real metered unit rate." },
        { rule: "type.tabular-numbers", text: "Aligns gigabyte volumes, overage cents, and retention days in tabular columns." },
      ],
      beforeHtml: function () {
        return (
          '<div class="mock-before-dark">' +
          '<div class="mock-before-center">' +
          '<p class="mock-before-h1">Unlock seamless scale</p>' +
          '<p class="mock-before-sub">Trusted by 5,000+ startups</p>' +
          "</div>" +
          '<div class="mock-before-grid">' +
          '<div class="mock-before-box">Starter<br/><strong>$0</strong></div>' +
          '<div class="mock-before-box" style="border-color:#818cf8;">POPULAR<br/><strong>$49</strong></div>' +
          '<div class="mock-before-box">Enterprise<br/><strong>Custom</strong></div>' +
          "</div>" +
          '<div class="mock-before-ctas"><span class="mock-before-pill">Get Started</span><span class="mock-before-pill">Get Started</span></div>' +
          "</div>"
        );
      },
      afterHtml: function () {
        return (
          '<div class="mini-app">' +
          '<div class="mini-app-bar"><span>MetricPort Plans</span><span>$0.18 / extra GB · 0 seat fees</span></div>' +
          '<table class="clean-table">' +
          "<thead><tr><th>Metric</th><th>Starter</th><th>Team ($49)</th><th>Dedicated</th></tr></thead>" +
          "<tbody>" +
          "<tr><td>Ingest</td><td>5 GB</td><td>250 GB</td><td>2 TB</td></tr>" +
          "<tr><td>Overage</td><td>Hard cap</td><td>$0.18 / GB</td><td>$0.12 / GB</td></tr>" +
          "<tr><td>Retention</td><td>7 days</td><td>30 days</td><td>365 days</td></tr>" +
          "</tbody>" +
          "</table>" +
          "</div>"
        );
      },
    },
    metrics: {
      beforeLabel: "Without rules · FAIL (dashboard-costume)",
      afterLabel: "precise-technical · things-3 · PASS",
      notes: [
        { rule: "layout.dashboard-costume", text: "Cuts decorative '99.99% Uptime' KPI boxes and puts live failed endpoints on row one." },
        { rule: "color.meaningful-semantics", text: "Uses red (#8f2d1f) and amber (#8a5a12) strictly on real degraded latency bars and queue rows." },
        { rule: "product.first-screen", text: "Gives on-call engineers route, p99 latency, error percentage, and time started above the fold." },
      ],
      beforeHtml: function () {
        return (
          '<div class="mock-before-dark">' +
          '<div class="mock-before-center"><p class="mock-before-h1">Seamless Observability</p></div>' +
          '<div class="mock-before-grid">' +
          '<div class="mock-before-box">Uptime<br/><strong>99.99%</strong></div>' +
          '<div class="mock-before-box">Velocity<br/><strong>3.1x</strong></div>' +
          '<div class="mock-before-box">Score<br/><strong>98/100</strong></div>' +
          "</div>" +
          '<div class="mock-before-ctas"><span class="mock-before-pill">✨ Boost Insights</span><span class="mock-before-pill">Export</span></div>' +
          "</div>"
        );
      },
      afterHtml: function () {
        return (
          '<div class="mini-app">' +
          '<div class="mini-app-bar"><span>northbeam-eu-west · 14:18 UTC</span><span class="status-fail">2 active incidents</span></div>' +
          '<div style="padding:0.75rem;display:grid;gap:0.625rem;">' +
          METRICS_BARS_SVG +
          '<table class="clean-table">' +
          "<thead><tr><th>ID</th><th>Route</th><th>State</th><th>p99</th></tr></thead>" +
          "<tbody>" +
          '<tr><td><code>INC-402</code></td><td>auth-edge /token</td><td class="status-fail">502 spike</td><td>412 ms</td></tr>' +
          '<tr><td><code>INC-399</code></td><td>billing-worker</td><td style="color:var(--warning);font-weight:500;">Queue lag</td><td>18.2 s</td></tr>' +
          "</tbody>" +
          "</table>" +
          "</div>" +
          "</div>"
        );
      },
    },
    cli: {
      beforeLabel: "Without rules · FAIL (14 violations)",
      afterLabel: "precise-technical · teenage-engineering · PASS",
      notes: [
        { rule: "product.first-screen", text: "Puts real curl install line + schema validation error message immediately on the first fold." },
        { rule: "content.abstract-verbs", text: "Replaces 'Blazing Fast' & 'Enterprise Safe' cards with 1.8 MB static musl binary and 4.2 ms parse metrics." },
        { rule: "hierarchy.one-primary-action", text: "Eliminates side-by-side 'Get Started Free' and 'Book a Demo' SaaS buttons." },
      ],
      beforeHtml: function () {
        return (
          '<div class="mock-before-dark">' +
          '<div class="mock-before-center">' +
          '<p class="mock-before-h1">Transform YAML configs</p>' +
          '<p class="mock-before-sub">Trusted by 10,000+ developers</p>' +
          "</div>" +
          '<div class="mock-before-grid">' +
          '<div class="mock-before-box">✨ Smart</div>' +
          '<div class="mock-before-box">🚀 Fast</div>' +
          '<div class="mock-before-box">🛡️ Safe</div>' +
          "</div>" +
          '<div class="mock-before-ctas"><span class="mock-before-pill">Get Started</span><span class="mock-before-pill">Book Demo</span></div>' +
          "</div>"
        );
      },
      afterHtml: function () {
        return (
          '<div style="display:grid;gap:0.625rem;">' +
          '<div class="mini-terminal">' +
          '<div style="color:#a6aca7;"># static binary · 1.8 MB · zero runtime deps</div>' +
          '<div>$ curl -fsSL https://get.kestrel.dev/install.sh | sh<br/>$ kestrel check deploy/*.yaml --schema service.json<br/><span style="color:#f4a298;">deploy/api.yaml:14:9 error [port] expected integer, got "8080"</span></div>' +
          "</div>" +
          '<div style="display:flex;justify-content:space-between;font-family:var(--font-mono);font-size:0.72rem;color:var(--muted);">' +
          "<span>Cold parse: 4.2 ms</span><span>Exit 0 pass · 1 fail · 2 I/O</span>" +
          "</div>" +
          "</div>"
        );
      },
    },
    harbor: {
      beforeLabel: "Without rules · FAIL (generic rounded cards)",
      afterLabel: "editorial-print · financial-times + monocle · PASS",
      notes: [
        { rule: "density.measure", text: "Sets readable 56–66ch editorial measure paired with issue dateline and crisp masthead rule." },
        { rule: "material.ink-hairlines", text: "Replaces glowing rounded teaser tiles with warm paper #fbf7f1 and ruled ink hairlines." },
        { rule: "content.concrete-nouns", text: "Opens with real energy capacity numbers from Helsinki & Gothenburg rather than generic buzzwords." },
      ],
      beforeHtml: function () {
        return (
          '<div class="mock-before-dark">' +
          '<div class="mock-before-center"><p class="mock-before-h1">Revolutionize reading</p></div>' +
          '<div class="mock-before-grid">' +
          '<div class="mock-before-box">Next-Gen Feed</div>' +
          '<div class="mock-before-box">AI Magic Digest</div>' +
          '<div class="mock-before-box">Unlock Pro</div>' +
          "</div>" +
          "</div>"
        );
      },
      afterHtml: function () {
        return (
          '<div class="mini-editorial">' +
          '<div style="display:flex;justify-content:space-between;font-family:var(--font-mono);font-size:0.7rem;color:#4e4944;border-bottom:1px solid #d8d0c4;padding-bottom:0.35rem;">' +
          "<span>HARBOR DISPATCH · ISSUE 48</span><span>6 MIN READ</span>" +
          "</div>" +
          '<div style="font-size:1.05rem;font-weight:600;line-height:1.25;max-width:34ch;">Why Nordic grid operators are adding 4-hour thermal brick storage next to substations</div>' +
          '<div style="font-size:0.8125rem;color:#4e4944;max-width:54ch;">Direct curtailment figures from municipal heat networks in Helsinki and Gothenburg, compared per MWh stored.</div>' +
          "</div>"
        );
      },
    },
  };

  var wb = { scenario: "ai", view: "split" };
  var stageSplitEl = document.getElementById("stage-split");
  var diffStripEl = document.getElementById("diff-strip");
  var viewSplitBtn = document.getElementById("view-split");
  var viewAfterBtn = document.getElementById("view-after");
  var viewBeforeBtn = document.getElementById("view-before");

  function renderWorkbench() {
    var sc = SCENARIOS[wb.scenario] || SCENARIOS.ai;
    if (viewSplitBtn) viewSplitBtn.setAttribute("aria-pressed", wb.view === "split" ? "true" : "false");
    if (viewAfterBtn) viewAfterBtn.setAttribute("aria-pressed", wb.view === "after" ? "true" : "false");
    if (viewBeforeBtn) viewBeforeBtn.setAttribute("aria-pressed", wb.view === "before" ? "true" : "false");

    if (stageSplitEl) {
      stageSplitEl.className = "stage-split" + (wb.view === "split" ? "" : " single-col");
      var html = "";
      if (wb.view === "split" || wb.view === "before") {
        html +=
          '<div class="stage-pane stage-pane-before" data-taste-specimen="negative">' +
          '<div class="stage-pane-head"><span>WITHOUT PREMIUM TASTE</span><span class="status-fail">' + escapeHtml(sc.beforeLabel) + "</span></div>" +
          '<div>' + sc.beforeHtml() + "</div>" +
          "</div>";
      }
      if (wb.view === "split" || wb.view === "after") {
        html +=
          '<div class="stage-pane">' +
          '<div class="stage-pane-head"><span>WITH PREMIUM TASTE</span><span class="status-pass">' + escapeHtml(sc.afterLabel) + "</span></div>" +
          '<div>' + sc.afterHtml() + "</div>" +
          "</div>";
      }
      stageSplitEl.innerHTML = html;
    }

    if (diffStripEl) {
      diffStripEl.innerHTML = sc.notes
        .map(function (n) {
          return (
            '<div class="diff-note">' +
            '<span class="diff-rule">' + escapeHtml(n.rule) + "</span>" +
            '<p class="diff-text">' + escapeHtml(n.text) + "</p>" +
            "</div>"
          );
        })
        .join("");
    }
  }

  wireTablist(document.getElementById("scenario-tabs"), function (tab) {
    wb.scenario = tab.getAttribute("data-scenario") || "ai";
    renderWorkbench();
  });

  [viewSplitBtn, viewAfterBtn, viewBeforeBtn].forEach(function (btn) {
    if (!btn) return;
    btn.addEventListener("click", function () {
      wb.view = btn.getAttribute("data-view") || "split";
      renderWorkbench();
    });
  });

  renderWorkbench();

  /* ------------------------------------------------------------------ */
  /* 02. LIVE STATIC AUDITOR                                             */
  /* ------------------------------------------------------------------ */
  var AUDIT_PRESETS = {
    saas: {
      file: "hero.html",
      code:
        '<style>\n' +
        '  body { font-family: "Inter", sans-serif; color: #0f172a; }\n' +
        '  h1 { background: linear-gradient(90deg, #fff, #818cf8); -webkit-background-clip: text; }\n' +
        '  .card { border-radius: 18px; box-shadow: 0 20px 40px rgba(0,0,0,0.12); color: #94a3b8; background: #ffffff; }\n' +
        '  button:focus { outline: none; }\n' +
        '</style>\n' +
        '<section class="hero">\n' +
        '  <h1>Elevate your workflow seamlessly</h1>\n' +
        '  <p>Trusted by 10,000+ teams to unlock next-gen velocity.</p>\n' +
        '  <div class="actions">\n' +
        '    <button class="btn-primary">Get Started</button>\n' +
        '    <button class="btn-primary" style="background:#4f46e5">Book Demo</button>\n' +
        '  </div>\n' +
        '</section>',
    },
    ai: {
      file: "prompt.html",
      code:
        '<style>\n' +
        '  body { font-family: "Space Grotesk", sans-serif; }\n' +
        '  textarea { outline: none; }\n' +
        '</style>\n' +
        '<div class="card" style="background:#16192b;border-radius:16px">\n' +
        '  <h2>✨ Supercharge AI Writing</h2>\n' +
        '  <textarea placeholder="Ask AI magic anything..."></textarea>\n' +
        '  <div class="cta"><button class="bg-indigo-600">✨ Generate</button><button class="bg-indigo-600">Upgrade</button></div>\n' +
        '</div>',
    },
    "pricing-ok": {
      file: "pricing.html",
      code:
        '<style>\n' +
        '  body { font-family: "IBM Plex Sans", sans-serif; background: #f5f5f2; color: #1b1d1c; }\n' +
        '  :focus-visible { outline: 2px solid #1e5c40; outline-offset: 2px; }\n' +
        '  .btn-primary { background: #1e5c40; color: #ffffff; }\n' +
        '</style>\n' +
        '<main>\n' +
        '  <h1>Metered ingestion billed per gigabyte ($0.18 / GB)</h1>\n' +
        '  <div class="actions">\n' +
        '    <a class="btn-primary" href="#team">Start Team plan ($49 / mo)</a>\n' +
        '    <a class="btn-secondary" href="#starter">Use Starter ($0)</a>\n' +
        '  </div>\n' +
        '</main>',
    },
    "rowan-ok": {
      file: "rowan.html",
      code:
        '<style>\n' +
        '  body { font-family: "IBM Plex Sans", system-ui, sans-serif; background: #f3efe6; color: #1c1915; }\n' +
        '  :focus-visible { outline: 2px solid #7a3e2e; outline-offset: 2px; }\n' +
        '  .btn-primary { background: #7a3e2e; color: #f6f1e8; }\n' +
        '</style>\n' +
        '<main>\n' +
        '  <h1>Wheel-thrown stoneware bowl · 185 mm · $68</h1>\n' +
        '  <button class="btn-primary" type="button">Add to bag ($68)</button>\n' +
        '</main>',
    },
  };

  var auditFileInput = document.getElementById("audit-file-name");
  var auditCodeInput = document.getElementById("audit-code-input");
  var auditVerdict = document.getElementById("audit-verdict");
  var auditScoresEl = document.getElementById("audit-scores");
  var auditFindingsEl = document.getElementById("audit-findings");
  var copyAuditBtn = document.getElementById("copy-audit-report");
  var latestAuditResult = null;

  var SCORE_LABELS = [
    ["hierarchy", "Hierarchy"],
    ["spacing", "Spacing"],
    ["uniqueness", "Uniqueness"],
    ["restraint", "Restraint"],
    ["accessibility", "Accessibility"],
    ["product_fit", "Product fit"],
  ];

  function runLiveAudit() {
    if (!Audit || !auditCodeInput) return;
    var fname = (auditFileInput && auditFileInput.value.trim()) || "snippet.html";
    var res = Audit.auditCode(auditCodeInput.value, fname);
    latestAuditResult = res;

    if (auditVerdict) {
      if (!res.findings.length) {
        auditVerdict.textContent = "PASS · 0 rule violations";
        auditVerdict.className = "audit-verdict status-pass";
      } else {
        auditVerdict.textContent = (res.passed ? "WARN · " : "FAIL · ") + res.findings.length + " violation(s)";
        auditVerdict.className = "audit-verdict " + (res.passed ? "" : "status-fail");
      }
    }

    if (auditScoresEl) {
      auditScoresEl.innerHTML = SCORE_LABELS.map(function (pair) {
        var val = res.scores[pair[0]];
        var pct = Math.max(12, val * 20);
        var lowCls = val <= 2 ? " is-low" : "";
        return (
          '<div class="score-meter">' +
          '<div class="score-meter-row">' +
          '<span class="score-meter-name">' + pair[1] + "</span>" +
          '<span class="score-meter-num">' + val + "/5</span>" +
          "</div>" +
          '<div class="meter-track"><div class="meter-fill' + lowCls + '" style="width:' + pct + '%;"></div></div>' +
          "</div>"
        );
      }).join("");
    }

    if (auditFindingsEl) {
      if (!res.findings.length) {
        auditFindingsEl.innerHTML =
          '<div class="finding-row" style="border-inline-start-color:var(--accent);">' +
          '<div class="finding-row-id status-pass">No automated anti-patterns found</div>' +
          "<p>Verify visual measure (60–72ch) and first-screen job fit manually.</p>" +
          "</div>";
      } else {
        auditFindingsEl.innerHTML = res.findings
          .map(function (f) {
            return (
              '<div class="finding-row' + (f.severity === "warn" ? " is-warn" : "") + '">' +
              '<div class="finding-row-id">[' + escapeHtml(f.severity.toUpperCase()) + "] L" + f.line + " · " + escapeHtml(f.rule) + "</div>" +
              "<p>" + escapeHtml(f.message) + " Fix: " + escapeHtml(f.fix) + "</p>" +
              "</div>"
            );
          })
          .join("");
      }
    }
  }

  if (auditCodeInput) {
    auditCodeInput.value = AUDIT_PRESETS.saas.code;
    auditCodeInput.addEventListener("input", runLiveAudit);
  }
  if (auditFileInput) auditFileInput.addEventListener("input", runLiveAudit);

  var presetBtns = Array.prototype.slice.call(document.querySelectorAll("[data-preset]"));
  presetBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var p = AUDIT_PRESETS[btn.getAttribute("data-preset")];
      if (!p) return;
      presetBtns.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      if (auditFileInput) auditFileInput.value = p.file;
      if (auditCodeInput) auditCodeInput.value = p.code;
      runLiveAudit();
    });
  });

  wireCopyButton(copyAuditBtn, function () {
    return latestAuditResult && Audit ? Audit.formatReport(latestAuditResult) : "";
  });
  runLiveAudit();

  /* ------------------------------------------------------------------ */
  /* 03. SETUP TABS & PROMPT BUILDER                                     */
  /* ------------------------------------------------------------------ */
  wireTablist(document.getElementById("setup-tabs"));
  Array.prototype.forEach.call(document.querySelectorAll(".copy-btn[data-copy-target]"), function (btn) {
    wireCopyButton(btn, function () {
      var el = document.getElementById(btn.getAttribute("data-copy-target"));
      return el ? el.textContent : "";
    });
  });

  var pbJob = document.getElementById("pb-job");
  var pbDir = document.getElementById("pb-direction");
  var cmdPrompt = document.getElementById("cmd-prompt");

  function renderPromptBuilder() {
    if (!cmdPrompt) return;
    var job = (pbJob && pbJob.value.trim()) || "Name what the user comes to this screen to do.";
    var dir = (pbDir && pbDir.value) || "auto";
    var dirLine =
      dir === "auto"
        ? "Pick the closest direction in taste/directions.yaml and one reference in taste/references/index.yaml."
        : "Use direction `" + dir + "` in taste/directions.yaml and load one matching reference from taste/references/index.yaml.";
    cmdPrompt.textContent =
      "Read AGENTS.md in .premium-taste/ (or https://github.com/02-OS/premium-taste) and follow its load order.\n" +
      dirLine + "\n" +
      "Refuse all generic SaaS anti-patterns in taste/anti-patterns.yaml, then run skills/critique-ui.md and `python3 scripts/audit.py` on changed files.\n\n" +
      "Job of this screen: " + job;
  }

  if (pbJob) pbJob.addEventListener("input", renderPromptBuilder);
  if (pbDir) pbDir.addEventListener("change", renderPromptBuilder);
  renderPromptBuilder();

  /* ------------------------------------------------------------------ */
  /* 04. TOKEN & CONTRAST STUDIO                                         */
  /* ------------------------------------------------------------------ */
  var TOKEN_KEYS = [
    { key: "surface", label: "Surface", fallback: "#f5f5f2" },
    { key: "surface-raised", label: "Surface Raised", fallback: "#ffffff" },
    { key: "ink", label: "Ink", fallback: "#1b1d1c" },
    { key: "ink-muted", label: "Ink Muted", fallback: "#4e5450" },
    { key: "accent", label: "Accent", fallback: "#1e5c40" },
    { key: "on-accent", label: "On Accent", fallback: "#f3f6f4" },
  ];

  var tokenState = {
    packId: "precise-technical",
    packName: "Instrument",
    exportMode: "css",
    colors: {
      surface: "#f5f5f2",
      "surface-raised": "#ffffff",
      ink: "#1b1d1c",
      "ink-muted": "#4e5450",
      accent: "#1e5c40",
      "on-accent": "#f3f6f4",
    },
  };

  var tokenControlsEl = document.getElementById("token-controls");
  var contrastTbody = document.getElementById("contrast-tbody");
  var tokenPreviewOuter = document.getElementById("token-preview-outer");
  var tokenPreview = document.getElementById("token-preview");
  var tokenExportCode = document.getElementById("token-export-code");

  function loadTokenPack(dirId) {
    var pack = DATA.tokens && DATA.tokens[dirId];
    if (!pack) return;
    tokenState.packId = dirId;
    tokenState.packName = pack.name || dirId;
    TOKEN_KEYS.forEach(function (item) {
      var val = pack.colors && pack.colors[item.key];
      tokenState.colors[item.key] = val || (dirId === "editorial-print" && item.key === "on-accent" ? "#f6f1e8" : item.fallback);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-token-pack]"), function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-token-pack") === dirId ? "true" : "false");
    });
    renderTokenStudio();
  }

  function buildTokenControls() {
    if (!tokenControlsEl) return;
    tokenControlsEl.innerHTML = TOKEN_KEYS.map(function (item) {
      var hexId = "tok-" + item.key + "-hex";
      var val = tokenState.colors[item.key];
      return (
        '<div class="swatch-item">' +
        '<label for="' + hexId + '">' + escapeHtml(item.label) + "</label>" +
        '<div class="swatch-control">' +
        '<input type="color" id="tok-' + item.key + '-pick" aria-label="' + escapeHtml(item.label) + ' color picker" value="' + escapeHtml(val) + '" data-token-pick="' + item.key + '" />' +
        '<input type="text" id="' + hexId + '" value="' + escapeHtml(val) + '" data-token-hex="' + item.key + '" spellcheck="false" />' +
        "</div>" +
        "</div>"
      );
    }).join("");

    Array.prototype.forEach.call(tokenControlsEl.querySelectorAll("[data-token-pick]"), function (picker) {
      picker.addEventListener("input", function () {
        var key = picker.getAttribute("data-token-pick");
        tokenState.colors[key] = picker.value.toLowerCase();
        var hexEl = document.getElementById("tok-" + key + "-hex");
        if (hexEl) hexEl.value = tokenState.colors[key];
        renderTokenReadouts();
      });
    });

    Array.prototype.forEach.call(tokenControlsEl.querySelectorAll("[data-token-hex]"), function (hexEl) {
      hexEl.addEventListener("input", function () {
        var key = hexEl.getAttribute("data-token-hex");
        var v = hexEl.value.trim();
        if (Audit && Audit.hexToRgb(v)) {
          tokenState.colors[key] = v.toLowerCase();
          var pick = document.getElementById("tok-" + key + "-pick");
          if (pick && /^#[0-9a-f]{6}$/i.test(v)) pick.value = v;
          renderTokenReadouts();
        }
      });
    });
  }

  function renderTokenReadouts() {
    var c = tokenState.colors;
    if (contrastTbody && Audit) {
      var pairs = [
        { name: "ink / surface", fg: c.ink, bg: c.surface },
        { name: "ink / surface-raised", fg: c.ink, bg: c["surface-raised"] },
        { name: "ink-muted / surface", fg: c["ink-muted"], bg: c.surface },
        { name: "on-accent / accent", fg: c["on-accent"], bg: c.accent },
      ];
      contrastTbody.innerHTML = pairs
        .map(function (p) {
          var r = Audit.contrastRatio(p.fg, p.bg) || 0;
          var status = r >= 7 ? "AAA Pass" : r >= 4.5 ? "AA Pass" : "Fail (< 4.5:1)";
          return (
            "<tr>" +
            "<td><code>" + p.name + "</code></td>" +
            "<td><code>" + r.toFixed(2) + ":1</code></td>" +
            '<td class="' + (r >= 4.5 ? "ratio-pass" : "ratio-fail") + '">' + status + "</td>" +
            "</tr>"
          );
        })
        .join("");
    }

    if (tokenPreviewOuter && tokenPreview) {
      tokenPreviewOuter.style.background = c.surface;
      tokenPreview.style.background = c["surface-raised"];
      tokenPreview.style.color = c.ink;
      var eyebrowEl = document.getElementById("tp-eyebrow");
      var bodyEl = document.getElementById("tp-body");
      var ctaEl = document.getElementById("tp-cta");
      if (eyebrowEl) {
        eyebrowEl.textContent = "LIVE SURFACE CHECK · " + tokenState.packName.toUpperCase();
        eyebrowEl.style.color = c["ink-muted"];
      }
      if (bodyEl) bodyEl.style.color = c["ink-muted"];
      if (ctaEl) {
        ctaEl.style.background = c.accent;
        ctaEl.style.color = c["on-accent"];
      }
    }

    if (tokenExportCode) {
      var lines = [];
      if (tokenState.exportMode === "tailwind") {
        lines.push("/* Premium Taste — " + tokenState.packName + " (" + tokenState.packId + ") */");
        lines.push("@theme {");
        TOKEN_KEYS.forEach(function (k) { lines.push("  --color-pt-" + k.key + ": " + c[k.key] + ";"); });
        lines.push("}");
      } else if (tokenState.exportMode === "design") {
        lines.push("---");
        lines.push("name: " + tokenState.packName);
        lines.push("direction: " + tokenState.packId);
        lines.push("colors:");
        TOKEN_KEYS.forEach(function (k) { lines.push("  " + k.key + ': "' + c[k.key] + '"'); });
        lines.push("---");
      } else {
        lines.push("/* Premium Taste — " + tokenState.packName + " (" + tokenState.packId + ") */");
        lines.push(":root {");
        TOKEN_KEYS.forEach(function (k) { lines.push("  --pt-" + k.key + ": " + c[k.key] + ";"); });
        lines.push("}");
      }
      tokenExportCode.textContent = lines.join("\n");
    }
  }

  function renderTokenStudio() {
    buildTokenControls();
    renderTokenReadouts();
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-token-pack]"), function (btn) {
    btn.addEventListener("click", function () { loadTokenPack(btn.getAttribute("data-token-pack")); });
  });
  wireTablist(document.getElementById("export-tabs"), function (tab) {
    tokenState.exportMode = tab.getAttribute("data-export") || "css";
    renderTokenReadouts();
  });
  loadTokenPack("precise-technical");

  /* ------------------------------------------------------------------ */
  /* 05. DIRECTIONS RENDERED IN THEIR ACTUAL TOKEN IDENTITIES            */
  /* ------------------------------------------------------------------ */
  var dirGrid = document.getElementById("directions-grid");
  if (dirGrid && DATA.directions.length) {
    dirGrid.innerHTML = DATA.directions
      .map(function (d) {
        var pack = (DATA.tokens && DATA.tokens[d.id]) || {};
        var cols = pack.colors || {};
        var bg = cols.surface || "#f5f5f2";
        var ink = cols.ink || "#1b1d1c";
        var accent = cols.accent || "#1e5c40";
        var onAccent = cols["on-accent"] || (d.id === "editorial-print" ? "#f6f1e8" : "#ffffff");
        var borderStyle = d.id === "cinematic-dark" ? "#2a2825" : (cols.hairline || "#e2e2da");
        return (
          '<article class="dir-tile" style="background:' + escapeHtml(bg) + ";color:" + escapeHtml(ink) + ";border-color:" + escapeHtml(borderStyle) + ';">' +
          '<div class="dir-tile-top">' +
          "<h3>" + escapeHtml(d.id) + "</h3>" +
          '<span class="dir-tile-tag">' + escapeHtml(pack.name || "") + " · " + escapeHtml(d.density || "") + "</span>" +
          "</div>" +
          '<p class="dir-tile-desc">' + escapeHtml(d.summary || "") + "</p>" +
          '<p class="dir-tile-rule"><strong>First screen:</strong> ' + escapeHtml(d.first_screen || "") + "</p>" +
          '<button type="button" class="dir-tile-btn" data-use-tokens="' + escapeHtml(d.id) + '" style="background:' + escapeHtml(accent) + ";color:" + escapeHtml(onAccent) + ';">Load palette in Token Studio →</button>' +
          "</article>"
        );
      })
      .join("");

    Array.prototype.forEach.call(dirGrid.querySelectorAll("[data-use-tokens]"), function (btn) {
      btn.addEventListener("click", function () {
        loadTokenPack(btn.getAttribute("data-use-tokens"));
        var target = document.getElementById("tokens");
        if (target) target.scrollIntoView({ behavior: "smooth" });
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 06. REFERENCES & 07. ANTI-PATTERNS                                  */
  /* ------------------------------------------------------------------ */
  var refState = { dir: "all", query: "" };
  var refListEl = document.getElementById("ref-list");
  var refSearchEl = document.getElementById("ref-search");
  var refFiltersEl = document.getElementById("ref-filters");

  function renderReferences() {
    if (!refListEl) return;
    var q = refState.query.toLowerCase();
    var items = DATA.references.filter(function (r) {
      if (refState.dir !== "all" && r.direction !== refState.dir) return false;
      if (!q) return true;
      return [r.id, r.title, r.job, r.summary, (r.tags || []).join(" ")].join(" ").toLowerCase().indexOf(q) !== -1;
    });

    if (!items.length) {
      refListEl.innerHTML = '<div style="padding:1rem;color:var(--muted);">No references match that search.</div>';
      return;
    }

    refListEl.innerHTML = items
      .map(function (r) {
        var steal = (r.steal || []).map(function (s) { return "<li>" + escapeHtml(s) + "</li>"; }).join("");
        var avoid = (r.avoid || []).map(function (a) { return "<li>" + escapeHtml(a) + "</li>"; }).join("");
        return (
          '<div class="ref-row">' +
          '<button type="button" class="ref-btn" aria-expanded="false" aria-controls="ref-drawer-' + escapeHtml(r.id) + '">' +
          '<span class="ref-name">' + escapeHtml(r.title) + "</span>" +
          '<span class="ref-job">' + escapeHtml(r.job) + "</span>" +
          '<span class="ref-dir">' + escapeHtml(r.direction) + "</span>" +
          "</button>" +
          '<div class="ref-drawer" id="ref-drawer-' + escapeHtml(r.id) + '" hidden>' +
          '<p style="margin:0;color:var(--muted);">' + escapeHtml(r.summary || "") + "</p>" +
          '<div class="ref-drawer-cols">' +
          "<div><strong>What to steal</strong><ul>" + steal + "</ul></div>" +
          "<div><strong>What not to copy</strong><ul>" + avoid + "</ul></div>" +
          "</div>" +
          "</div>" +
          "</div>"
        );
      })
      .join("");

    Array.prototype.forEach.call(refListEl.querySelectorAll(".ref-btn"), function (btn) {
      btn.addEventListener("click", function () {
        var open = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", open ? "false" : "true");
        var drawer = document.getElementById(btn.getAttribute("aria-controls"));
        if (drawer) drawer.hidden = open;
      });
    });
  }

  if (refFiltersEl) {
    Array.prototype.forEach.call(refFiltersEl.querySelectorAll("[data-dir]"), function (btn) {
      btn.addEventListener("click", function () {
        refState.dir = btn.getAttribute("data-dir") || "all";
        Array.prototype.forEach.call(refFiltersEl.querySelectorAll("[data-dir]"), function (b) {
          b.setAttribute("aria-pressed", b === btn ? "true" : "false");
        });
        renderReferences();
      });
    });
  }
  if (refSearchEl) {
    refSearchEl.addEventListener("input", function () {
      refState.query = refSearchEl.value.trim();
      renderReferences();
    });
  }
  renderReferences();

  var apState = { cat: "all" };
  var apFiltersEl = document.getElementById("ap-filters");
  var apTbody = document.getElementById("ap-tbody");

  function renderAntiPatterns() {
    if (!apTbody) return;
    var rows = DATA.antiPatterns.filter(function (ap) {
      return apState.cat === "all" || String(ap.id || "").split(".")[0] === apState.cat;
    });
    apTbody.innerHTML = rows
      .map(function (ap) {
        return (
          "<tr>" +
          "<td><code>" + escapeHtml(ap.id) + "</code></td>" +
          "<td>" + escapeHtml(ap.description || "") + "</td>" +
          "<td>" + escapeHtml((ap.signals || []).slice(0, 2).join("; ")) + "</td>" +
          "<td>" + escapeHtml(ap.instead || "") + "</td>" +
          "</tr>"
        );
      })
      .join("");
  }

  if (apFiltersEl && DATA.antiPatterns.length) {
    var cats = ["all"];
    DATA.antiPatterns.forEach(function (ap) {
      var prefix = String(ap.id || "").split(".")[0];
      if (prefix && cats.indexOf(prefix) === -1) cats.push(prefix);
    });
    apFiltersEl.innerHTML = cats
      .map(function (c) {
        return '<button type="button" class="chip-btn" aria-pressed="' + (c === "all" ? "true" : "false") + '" data-ap-cat="' + escapeHtml(c) + '">' + escapeHtml(c === "all" ? "All (" + DATA.antiPatterns.length + ")" : c) + "</button>";
      })
      .join("");
    Array.prototype.forEach.call(apFiltersEl.querySelectorAll("[data-ap-cat]"), function (btn) {
      btn.addEventListener("click", function () {
        apState.cat = btn.getAttribute("data-ap-cat") || "all";
        Array.prototype.forEach.call(apFiltersEl.querySelectorAll("[data-ap-cat]"), function (b) {
          b.setAttribute("aria-pressed", b === btn ? "true" : "false");
        });
        renderAntiPatterns();
      });
    });
  }
  renderAntiPatterns();

  var countsEl = document.getElementById("header-counts");
  if (countsEl && DATA.counts) {
    countsEl.textContent =
      (DATA.counts.principles || 62) + " rules · " +
      (DATA.counts.antiPatterns || 25) + " anti-patterns · " +
      (DATA.counts.references || 18) + " refs";
  }
})();
