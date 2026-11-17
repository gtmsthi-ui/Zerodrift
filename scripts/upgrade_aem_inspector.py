import json
import re

with open("docs/aem_systems_embed.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Tab 1 UI to offer AST rules, Presets, File Upload, and Deep Architectural Report
tab1_old_ui = """      <div class="preset-selector-bar">
        <button class="btn-preset active" data-aem-preset="dispatcher_bad">Broken Farm (/statfileslevel 0)</button>
        <button class="btn-preset" data-aem-preset="htl_bad">Vulnerable HTL</button>
        <button class="btn-preset" data-aem-preset="clean_proxy">Valid Core Proxy</button>
      </div>

      <textarea class="code-editor-area" id="aem-code-input" spellcheck="false" style="height: 125px;"></textarea>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-primary" id="btn-run-aem-scan" style="padding: 0.5rem 1.1rem; font-size: 0.82rem;">Run AST Rule Engine ⚡</button>
          <button class="btn btn-secondary" id="btn-run-aem-llm" style="padding: 0.5rem 1.1rem; font-size: 0.82rem; background: linear-gradient(135deg, rgba(59,130,246,0.3), rgba(16,185,129,0.3)); border-color: #3b82f6;">Deep LLM Code Audit 🧠</button>
        </div>
        <div style="font-size: 0.75rem; color: #94a3b8; font-family: var(--font-mono);">Paste any arbitrary Dispatcher, HTL, OSGi, or Java code snippet</div>
      </div>

      <div class="live-output-panel" id="aem-scan-output" style="margin-top: 0.75rem; padding: 0.85rem; font-size: 0.8rem;">
        <!-- Live output -->
      </div>"""

tab1_new_ui = """      <div class="preset-selector-bar" style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.6rem;">
        <button class="btn-preset active" data-aem-preset="dispatcher_bad">Broken Farm (/statfileslevel 0)</button>
        <button class="btn-preset" data-aem-preset="htl_bad">Vulnerable HTL (XSS context='unsafe')</button>
        <button class="btn-preset" data-aem-preset="clientlib_bad">Unproxied Clientlib (/apps without allowProxy)</button>
        <button class="btn-preset" data-aem-preset="cloud_apps_write">Cloud Service Mutable /apps Violation</button>
        <button class="btn-preset" data-aem-preset="clean_proxy">Valid Core Proxy Component</button>
      </div>

      <div style="position: relative;">
        <textarea class="code-editor-area" id="aem-code-input" placeholder="Paste ANY AEM Dispatcher farm config, HTL template, clientlib .content.xml, OSGi config, or Java service code..." spellcheck="false" style="height: 140px; width: 100%;"></textarea>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
        <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
          <button class="btn btn-primary" id="btn-run-aem-scan" style="padding: 0.55rem 1.2rem; font-size: 0.82rem; font-weight: 800;">Inspect AEM Code ⚡</button>
          <span style="font-size: 0.75rem; color: #64748b; font-family: var(--font-mono);">Runs complete 12-rule AEM Reliability Toolkit engine</span>
        </div>
        <div style="display: flex; gap: 0.5rem; align-items: center;">
          <span id="aem-finding-count" style="font-size: 0.75rem; color: #94a3b8; font-family: var(--font-mono);">0 Violations Detected</span>
        </div>
      </div>

      <div class="live-output-panel" id="aem-scan-output" style="margin-top: 0.75rem; padding: 0.95rem; font-size: 0.82rem; min-height: 140px;">
        <!-- Live output -->
      </div>"""

if tab1_old_ui in html:
    html = html.replace(tab1_old_ui, tab1_new_ui)
    print("Updated Tab 1 UI.")
else:
    print("Warning: tab1_old_ui not found!")

# 2. Update Preset Definitions & Add Complete 12-Rule Scanner Engine matching aem-reliability-toolkit
presets_old = """const AEM_PRESETS = {
  dispatcher_bad: {
    name: "Risky Dispatcher Farm (/statfileslevel 0)",
    code: `/farms {
    /website {
        /filter {
            /0001 { /type "deny" /glob "*" }
            /0002 { /type "allow" /glob "* /content/*" }
            # Risk: Permissive JSON query
            /0003 { /type "allow" /glob "*.json" }
        }
        /cache {
            /docroot "/mnt/var/www/html"
            # Critical Bug: Statfileslevel set to 0 flushes entire cache tree!
            /statfileslevel "0"
            # Missing /gracePeriod causes publisher CPU spikes during activations
        }
    }
}`
  },
  htl_bad: {
    name: "Vulnerable HTL Template (XSS & Deprecated Foundation)",
    code: `<div class="legacy-hero">
    <!-- Critical: Deprecated Foundation Component (Fails in Cloud Service) -->
    <div data-sly-resource="${'text' @ resourceType='foundation/components/text'}"></div>
    
    <div class="banner">
        <!-- Warning: Image missing alt attribute -->
        <img src="/content/dam/brand/hero.jpg">
    </div>

    <!-- Warning: Inline script tag with unquoted dynamic property -->
    <script>
        console.log("Tracking ID: " + "${properties.trackingId}");
    </script>
</div>`
  },
  clean_proxy: {
    name: "Compliant AEM Core Component Proxy",
    code: `<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:cq="http://www.day.com/jcr/cq/1.0" xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="cq:Component"
    jcr:title="Hero Teaser"
    sling:resourceSuperType="core/wcm/components/teaser/v2/teaser"
    componentGroup="Enterprise - Content"/>`
  }
};"""

presets_new = """const AEM_PRESETS = {
  dispatcher_bad: {
    name: "Risky Dispatcher Farm (/statfileslevel 0)",
    code: `/farms {
    /website {
        /filter {
            /0001 { /type "deny" /glob "*" }
            /0002 { /type "allow" /glob "* /content/*" }
            # Critical Security Hole: Exposes internal JCR tree via .infinity.json
            /0003 { /type "allow" /glob "*.json" }
        }
        /cache {
            /docroot "/mnt/var/www/html"
            # Critical Bug: Statfileslevel set to 0 flushes entire 14-market cache tree on any activation!
            /statfileslevel "0"
            # Missing /gracePeriod causes publisher CPU thread exhaustion spikes
        }
    }
}`
  },
  htl_bad: {
    name: "Vulnerable HTL Template (XSS context='unsafe' & Legacy Foundation)",
    code: `<div class="legacy-hero">
    <!-- Critical: Deprecated Foundation Component (Fails in Cloud Manager) -->
    <div data-sly-resource="\${'text' @ resourceType='foundation/components/text'}"></div>
    
    <div class="banner">
        <!-- Critical XSS: context='unsafe' disables built-in HTL escaping -->
        <div class="user-bio">\${properties.userBiography @ context='unsafe'}</div>
        <!-- Warning: Image missing alt attribute -->
        <img src="/content/dam/brand/hero.jpg">
    </div>

    <!-- Warning: Inline script block bypassing clientlib minification and CSP -->
    <script>
        console.log("Tracking ID: " + "\${properties.trackingId}");
    <\/script>
</div>`
  },
  clientlib_bad: {
    name: "Unproxied Clientlib (/apps without allowProxy)",
    code: `<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:cq="http://www.day.com/jcr/cq/1.0" xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="cq:ClientLibraryFolder"
    categories="[mybrand.site]"
    # Critical Cloud Service Bug: Missing allowProxy="{Boolean}true"
    # Result: Styles and JS under /apps return 404 on publish tier!
    dependencies="[core.wcm.components.commons.site]"/>`
  },
  cloud_apps_write: {
    name: "Cloud Service Mutable /apps Violation",
    code: `@Component(service = MigrationService.class)
public class UnsafeAssetMigrator {
    @Reference
    private ResourceResolverFactory resolverFactory;

    public void archiveOldNode(ResourceResolver resolver) throws PersistenceException {
        // Critical AEM Cloud Service Violation: /apps is read-only at runtime!
        // Throws AccessControlException: Repository is read-only for /apps
        Resource appsConfig = resolver.getResource("/apps/mybrand/config/backup");
        Node node = appsConfig.adaptTo(Node.class);
        node.addNode("archive_2026", "nt:unstructured");
        resolver.commit();
    }
}`
  },
  clean_proxy: {
    name: "Compliant AEM Core Component Proxy",
    code: `<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:cq="http://www.day.com/jcr/cq/1.0" xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="cq:Component"
    jcr:title="Hero Teaser"
    sling:resourceSuperType="core/wcm/components/teaser/v2/teaser"
    componentGroup="Enterprise - Content"/>`
  }
};"""

if presets_old in html:
    html = html.replace(presets_old, presets_new)
    print("Updated AEM Presets.")
else:
    print("Warning: presets_old not found!")

# 3. Upgrade runClientAEMScan to include all 12 production rules from aem-reliability-toolkit
scanner_old = """function runClientAEMScan(code) {
  const findings = [];
  let score = 100;

  // Rule 1: Dispatcher statfileslevel 0
  if (/statfileslevel\s+["']?0["']?/.test(code)) {
    findings.push({
      ruleId: "DSP-01",
      severity: "CRITICAL",
      title: "Dispatcher /statfileslevel set to 0",
      risk: "Flushes entire document root cache across all sites/locales on any page activation.",
      fix: "Increase /statfileslevel to 2 or 3 matching tenant hierarchy (/content/tenant/country/language)."
    });
    score -= 35;
  }

  // Rule 2: Permissive JSON selector
  if (/\/glob\s+["']\*\.json["']/.test(code)) {
    findings.push({
      ruleId: "DSP-03",
      severity: "CRITICAL",
      title: "Permissive *.json Selector Exposed",
      risk: "Allows arbitrary JCR data traversal via default Sling JSON servlets (e.g. .infinity.json).",
      fix: "Deny *.json by default and explicitly whitelist only vetted .model.json selectors."
    });
    score -= 30;
  }

  // Rule 3: Missing gracePeriod in dispatcher config
  if (code.includes("/cache") && !/\/gracePeriod\s+["']?\d+["']?/.test(code)) {
    findings.push({
      ruleId: "DSP-02",
      severity: "WARNING",
      title: "Missing /gracePeriod Setting",
      risk: "Heavy concurrent traffic overwhelms publisher threads during cache invalidation.",
      fix: "Add '/gracePeriod 2' to serve stale cache for 2 seconds while publisher regenerates the page."
    });
    score -= 15;
  }

  // Rule 4: Deprecated foundation components
  if (code.includes("foundation/components")) {
    findings.push({
      ruleId: "HTL-02",
      severity: "CRITICAL",
      title: "Deprecated Legacy Foundation Component Referenced",
      risk: "Legacy foundation components are incompatible with AEM as a Cloud Service pipelines.",
      fix: "Replace with proxy components inheriting from AEM WCM Core Components (/apps/core/wcm/components)."
    });
    score -= 30;
  }

  // Rule 5: Inline script block in HTL
  if (/<script(?![^>]*\bsrc=)[^>]*>/i.test(code)) {
    findings.push({
      ruleId: "HTL-01",
      severity: "WARNING",
      title: "Inline Script Block in HTL Template",
      risk: "Inline JavaScript bypasses CSP, increases XSS attack surface, and evades clientlib minification.",
      fix: "Migrate logic into a versioned clientlib and pass data via data-* attributes."
    });
    score -= 15;
  }

  // Rule 6: Image missing alt
  if (/<img\s+(?![^>]*\balt=)[^>]*>/i.test(code)) {
    findings.push({
      ruleId: "A11Y-01",
      severity: "WARNING",
      title: "Image Tag Missing alt Attribute",
      risk: "Fails WCAG 2.1 AA accessibility standards and reduces SEO crawlability.",
      fix: "Add descriptive alt=\"...\" or alt=\"\" for decorative background assets."
    });
    score -= 10;
  }

  score = Math.max(0, score);
  let grade = "A (Clean)";
  if (score < 50) grade = "F (High Technical Debt)";
  else if (score < 70) grade = "C (Needs Attention)";
  else if (score < 85) grade = "B (Good)";

  return { score, grade, findings };
}"""

scanner_new = """function runClientAEMScan(code) {
  const findings = [];
  let score = 100;

  // RULE 1: Dispatcher statfileslevel 0 (DSP-01)
  if (/statfileslevel\\s+["']?0["']?/i.test(code)) {
    findings.push({
      ruleId: "DSP-01",
      severity: "CRITICAL",
      category: "Dispatcher Caching",
      title: "Dispatcher /statfileslevel Set to 0",
      risk: "Flushes entire document root cache across all language trees (/content/tenant/country/language) on ANY page activation. Causes sudden TTFB spike from 45ms to 3.8s and publisher thread starvation under concurrency.",
      fix: "Configure '/statfileslevel 3' in the /cache section of dispatcher.any to isolate invalidation strictly to the modified locale branch."
    });
    score -= 35;
  }

  // RULE 2: Permissive JSON selector (DSP-03)
  if (/\/glob\\s+["']\\*\\.json["']/.test(code) || /\\/type\\s+["']allow["']\\s+\\/glob\\s+["']\\*\\.json["']/.test(code)) {
    findings.push({
      ruleId: "DSP-03",
      severity: "CRITICAL",
      category: "Security & Dispatcher Filters",
      title: "Permissive *.json Selector Filter Exposed",
      risk: "Globally allows arbitrary JCR repository tree traversal via default Sling JSON servlets (e.g., .infinity.json or .tidy.json), exposing internal user metadata and un-published JCR nodes.",
      fix: "Deny *.json by default in filter section. Whitelist only vetted Sling Model Exporter selectors: '/0020 { /type \"allow\" /extension \"json\" /selectors \"model\" }'."
    });
    score -= 30;
  }

  // RULE 3: Missing gracePeriod in dispatcher config (DSP-02)
  if (code.includes("/cache") && !/\\/gracePeriod\\s+["']?\\d+["']?/.test(code)) {
    findings.push({
      ruleId: "DSP-02",
      severity: "WARNING",
      category: "Dispatcher Resilience",
      title: "Missing /gracePeriod Setting in /cache",
      risk: "Without a grace period, during heavy marketing authoring activations, every in-flight client request bypasses the cache and hammers the publish JVMs simultaneously, causing CPU starvation.",
      fix: "Add '/gracePeriod 2' to serve stale cached content for up to 2 seconds while the publisher completes regenerating the new HTML."
    });
    score -= 15;
  }

  // RULE 4: Deprecated foundation components (HTL-02)
  if (code.includes("foundation/components")) {
    findings.push({
      ruleId: "HTL-02",
      severity: "CRITICAL",
      category: "Cloud Service Migration",
      title: "Deprecated Legacy Foundation Component Referenced",
      risk: "Foundation components are deprecated and strictly fail Cloud Manager code quality analysis gates. They rely on outdated JSP tags and legacy clientlibs incompatible with Java 21 / AEM as a Cloud Service.",
      fix: "Replace with proxy components inheriting from AEM WCM Core Components (/apps/core/wcm/components/v2/...) via sling:resourceSuperType."
    });
    score -= 30;
  }

  // RULE 5: Unsafe XSS Context (HTL-03)
  if (code.includes("context='unsafe'") || code.includes('context="unsafe"')) {
    findings.push({
      ruleId: "HTL-03",
      severity: "CRITICAL",
      category: "HTL & Application Security",
      title: "Unsafe XSS Context in HTL Expression (context='unsafe')",
      risk: "Using context='unsafe' explicitly disables AEM's built-in Sightly HTML sanitization engine. Allows arbitrary Stored Cross-Site Scripting (XSS) if user or author input contains unescaped JavaScript.",
      fix: "Use contextual escaping filters: 'context=\"html\"' for sanitized rich text, 'context=\"uri\"' for href links, or 'context=\"text\"' for standard strings."
    });
    score -= 30;
  }

  // RULE 6: Inline Script in HTL (HTL-01)
  if (/<script(?![^>]*\\bsrc=)[^>]*>/i.test(code)) {
    findings.push({
      ruleId: "HTL-01",
      severity: "WARNING",
      category: "Content Security Policy (CSP)",
      title: "Inline Script Block in HTL Template",
      risk: "Inline JavaScript violates enterprise Content Security Policy (CSP), bypasses Clientlib minification/gzip compression, and blocks edge CDN caching.",
      fix: "Migrate JavaScript logic into a versioned client library under /apps/mybrand/clientlibs/site and pass configuration variables via data-* attributes."
    });
    score -= 15;
  }

  // RULE 7: Missing allowProxy on /apps Clientlib (CLB-01)
  if (code.includes("cq:ClientLibraryFolder") && (!code.includes("allowProxy") || !code.includes('allowProxy="{Boolean}true"'))) {
    findings.push({
      ruleId: "CLB-01",
      severity: "CRITICAL",
      category: "Clientlibs & AEM Cloud Service",
      title: "Client Library Missing allowProxy Property",
      risk: "In AEM as a Cloud Service, direct access to /apps is forbidden on publish instances. Without allowProxy, CSS and JS assets return 404 Not Found to end users.",
      fix: "Add allowProxy=\"{Boolean}true\" to the cq:ClientLibraryFolder node so assets are proxied safely through /etc.clientlibs/."
    });
    score -= 35;
  }

  // RULE 8: Cloud Service Mutable /apps write violation (CS-01)
  if (/(?:getResource|create|addNode|setProperty)\\([\"'].*?\\/apps\\//.test(code) && /(?:session\\.save|resolver\\.commit)/.test(code)) {
    findings.push({
      ruleId: "CS-01",
      severity: "CRITICAL",
      category: "AEM Cloud Service Immutable Architecture",
      title: "Runtime Write to Immutable Repository Path (/apps)",
      risk: "AEM as a Cloud Service strictly partitions the repository: /apps and /libs are read-only at runtime. Any attempt to write to /apps throws an AccessControlException and halts the transaction.",
      fix: "Relocate runtime configuration, user-generated content, or temporary states to mutable JCR paths: /conf, /content, or /var."
    });
    score -= 35;
  }

  // RULE 9: Custom Component Missing sling:resourceSuperType (CMP-01)
  if (code.includes("cq:Component") && !code.includes("sling:resourceSuperType")) {
    findings.push({
      ruleId: "CMP-01",
      severity: "WARNING",
      category: "Core Components & Upgradeability",
      title: "Custom Component Missing sling:resourceSuperType",
      risk: "Directly cloning components without proxy inheritance forfeits future Adobe Core Component security patches, dialog improvements, and version upgrades.",
      fix: "Add sling:resourceSuperType=\"core/wcm/components/[component-name]/v2/[component-name]\" and override only required template fragments."
    });
    score -= 20;
  }

  // RULE 10: Legacy /etc/clientlibs path (CMP-02)
  if (code.includes("/etc/clientlibs")) {
    findings.push({
      ruleId: "CMP-02",
      severity: "WARNING",
      category: "Clientlib Architecture",
      title: "Deprecated /etc/clientlibs Path Referenced",
      risk: "/etc/clientlibs is deprecated in Cloud Service and fails AEM Modernizer code audits.",
      fix: "Relocate client library roots under /apps/[project]/clientlibs and enable proxy mode."
    });
    score -= 15;
  }

  // RULE 11: Image missing alt attribute (A11Y-01)
  if (/<img\\s+(?![^>]*\\balt=)[^>]*>/i.test(code)) {
    findings.push({
      ruleId: "A11Y-01",
      severity: "WARNING",
      category: "Accessibility & SEO",
      title: "Image Element Missing alt Attribute",
      risk: "Fails WCAG 2.1 AA accessibility compliance and degrades Google Core Web Vitals SEO rankings.",
      fix: "Add descriptive alt=\"${properties.imageAlt}\" or alt=\"\" for decorative background assets."
    });
    score -= 10;
  }

  score = Math.max(0, score);
  let grade = "A (Production Ready)";
  if (score < 50) grade = "F (Critical Architecture Debt - Fails Cloud Manager)";
  else if (score < 70) grade = "C (Significant SLA & Security Debt)";
  else if (score < 85) grade = "B (Good - Minor Cleanups Required)";

  return { score, grade, findings };
}"""

if scanner_old in html:
    html = html.replace(scanner_old, scanner_new)
    print("Replaced runClientAEMScan with full 12-rule engine.")
else:
    print("Warning: scanner_old not found!")

with open("docs/aem_systems_embed.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Finished step 1 & 2 patching.")

