/* Browser port of scripts/audit.py for the live Premium Taste auditor. */
(function (global) {
  "use strict";

  var COSTUME_FONTS = [
    "Inter",
    "Geist",
    "Space Grotesk",
    "Satoshi",
    "Cabinet Grotesk",
    "Clash Display",
    "Plus Jakarta Sans",
    "DM Sans",
    "Instrument Serif",
    "Instrument Sans",
    "Playfair Display",
    "Cormorant Garamond",
  ];

  var GENERIC_FONTS = new Set([
    "system-ui",
    "-apple-system",
    "blinkmacsystemfont",
    "segoe ui",
    "roboto",
    "helvetica",
    "helvetica neue",
    "arial",
    "sans-serif",
    "serif",
    "monospace",
    "ui-sans-serif",
    "ui-serif",
    "ui-monospace",
    "georgia",
    "palatino",
    "iowan old style",
    "menlo",
    "consolas",
    "sf mono",
    "inherit",
    "initial",
    "unset",
  ]);

  var ABSTRACT_CLICHES = [
    /\belevate your\b/i,
    /\bunlock\b/i,
    /\bseamless(?:ly)?\b/i,
    /\bnext[- ]gen(?:eration)?\b/i,
    /\bempower(?:ing)?\b/i,
    /\bsupercharge\b/i,
    /\brevolutionize\b/i,
    /\bdelightful experience\b/i,
    /\byour workflow\b/i,
  ];

  var FAKE_PROOF_RE = /(?:trusted by\s+\d[\d,+]*|10,000\+\s+\w+|logos?\s*cloud)/i;
  var SPARKLE_RE = /(?:[✦✨🪄]|<Sparkles\b|sparkle-icon)/i;
  var IGNORE_RE = /taste-ignore:\s*([a-z0-9.,\s-]+)/;

  function ignoredRulesOnLine(lines, lineNo) {
    var ignored = new Set();
    var indices = [lineNo - 1, lineNo - 2];
    for (var i = 0; i < indices.length; i++) {
      var idx = indices[i];
      if (idx >= 0 && idx < lines.length) {
        var m = IGNORE_RE.exec(lines[idx]);
        if (m) {
          var parts = m[1].split(",");
          for (var j = 0; j < parts.length; j++) {
            var tok = parts[j].trim().replace(/[*\/>\- ]+$/g, "");
            if (tok) ignored.add(tok);
          }
        }
      }
    }
    return ignored;
  }

  function hexToRgb(hexColor) {
    var h = String(hexColor || "").trim().replace(/^#/, "");
    if (h.length === 3) {
      h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    } else if (h.length === 4) {
      h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    } else if (h.length === 8) {
      h = h.slice(0, 6);
    }
    if (!/^[0-9a-fA-F]{6}$/.test(h)) return null;
    return [
      parseInt(h.slice(0, 2), 16),
      parseInt(h.slice(2, 4), 16),
      parseInt(h.slice(4, 6), 16),
    ];
  }

  function hslToRgb(hue, sat, light) {
    var chroma = (1 - Math.abs(2 * light - 1)) * sat;
    var sector = ((hue % 360) + 360) % 360 / 60;
    var x = chroma * (1 - Math.abs(sector % 2 - 1));
    var red = 0, green = 0, blue = 0;
    if (sector < 1) { red = chroma; green = x; }
    else if (sector < 2) { red = x; green = chroma; }
    else if (sector < 3) { green = chroma; blue = x; }
    else if (sector < 4) { green = x; blue = chroma; }
    else if (sector < 5) { red = x; blue = chroma; }
    else { red = chroma; blue = x; }
    var match = light - chroma / 2;
    return [Math.round((red + match) * 255), Math.round((green + match) * 255), Math.round((blue + match) * 255)];
  }

  function parseColor(token, rootVars, depth) {
    var value = String(token || "").trim().replace(/;$/, "");
    var varMatch = /^var\(\s*(--[A-Za-z0-9_-]+)/i.exec(value);
    if (varMatch) {
      if ((depth || 0) >= 1 || !rootVars) return null;
      if (!Object.prototype.hasOwnProperty.call(rootVars, varMatch[1])) return null;
      return parseColor(rootVars[varMatch[1]], rootVars, (depth || 0) + 1);
    }
    if (value.charAt(0) === "#") return hexToRgb(value);
    var rgb = /^rgba?\(\s*([0-9.]+%?)\s*[, ]\s*([0-9.]+%?)\s*[, ]\s*([0-9.]+%?)/i.exec(value);
    if (rgb) {
      function channel(part) {
        if (/%$/.test(part)) return Math.max(0, Math.min(255, Math.round(parseFloat(part) * 2.55)));
        return Math.max(0, Math.min(255, Math.round(parseFloat(part))));
      }
      return [channel(rgb[1]), channel(rgb[2]), channel(rgb[3])];
    }
    var hsl = /^hsla?\(\s*([0-9.]+)\s*[, ]\s*([0-9.]+)%\s*[, ]\s*([0-9.]+)%/i.exec(value);
    if (hsl) return hslToRgb(parseFloat(hsl[1]), parseFloat(hsl[2]) / 100, parseFloat(hsl[3]) / 100);
    return null;
  }

  function contrastRatio(hexA, hexB) {
    var a = parseColor(hexA);
    var b = parseColor(hexB);
    if (!a || !b) return null;
    function relLum(rgb) {
      var ch = rgb.map(function (v) {
        var c = v / 255;
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
    }
    var la = relLum(a);
    var lb = relLum(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  }

  function contrastRatioFromRgb(a, b) {
    function relLum(rgb) {
      var ch = rgb.map(function (v) {
        var c = v / 255;
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
    }
    var la = relLum(a);
    var lb = relLum(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  }

  function scanTag(html, start) {
    if (html.charAt(start) !== "<") return null;
    var second = html.charAt(start + 1);
    if (second === "/" || second === "!" || second === "?") return null;
    if (!/[A-Za-z_]/.test(second)) return null;
    var nameEnd = start + 2;
    while (nameEnd < html.length && /[A-Za-z0-9_:-]/.test(html.charAt(nameEnd))) nameEnd++;
    var tag = html.slice(start + 1, nameEnd).toLowerCase();
    var quote = "";
    var brace = 0;
    var cursor = nameEnd;
    while (cursor < html.length) {
      var ch = html.charAt(cursor);
      if (quote) {
        if (ch === quote) quote = "";
        cursor++;
        continue;
      }
      if (ch === "'" || ch === '"') { quote = ch; cursor++; continue; }
      if (ch === "{") brace++;
      else if (ch === "}" && brace) brace--;
      else if (ch === ">" && brace === 0) {
        return { tag: tag, attrs: html.slice(nameEnd, cursor), start: start, end: cursor };
      }
      cursor++;
    }
    return null;
  }

  function iterOpenTags(html) {
    var out = [];
    var cursor = 0;
    while (cursor < html.length) {
      var start = html.indexOf("<", cursor);
      if (start === -1) break;
      var parsed = scanTag(html, start);
      if (!parsed) { cursor = start + 1; continue; }
      out.push(parsed);
      cursor = parsed.end + 1;
    }
    return out;
  }

  function attrValue(attrs, names) {
    for (var i = 0; i < names.length; i++) {
      var re = new RegExp("(?:^|[\\s/>])" + names[i] + "\\s*=\\s*(['\"])([\\s\\S]*?)\\1", "i");
      var match = re.exec(attrs);
      if (match) return match[2];
    }
    return null;
  }

  function elementInner(html, openEnd, tag) {
    var depth = 1;
    var cursor = openEnd + 1;
    var closer = "</" + tag;
    while (cursor < html.length && depth) {
      var next = html.indexOf("<", cursor);
      if (next === -1) break;
      if (html.slice(next, next + closer.length).toLowerCase() === closer) {
        var after = html.charAt(next + closer.length);
        if (!after || !/[A-Za-z0-9]/.test(after)) {
          depth--;
          if (depth === 0) return html.slice(openEnd + 1, next);
          cursor = next + closer.length;
          continue;
        }
      }
      var parsed = scanTag(html, next);
      if (parsed && parsed.tag === tag) {
        depth++;
        cursor = parsed.end + 1;
        continue;
      }
      cursor = next + 1;
    }
    return html.slice(openEnd + 1);
  }

  function extractCssSegments(text, isCssOnly) {
    if (isCssOnly) return [{ seg: text, base: 0 }];
    var segs = [];
    var re = /<style\b[^>]*>([\s\S]*?)<\/style>/gi;
    var m;
    while ((m = re.exec(text)) !== null) {
      segs.push({ seg: m[1], base: m.index + m[0].indexOf(m[1]) });
    }
    return segs;
  }

  function maskKeepNewlines(value) {
    return String(value).replace(/[^\n]/g, " ");
  }

  function stripNonCopyBlocks(html) {
    return String(html).replace(/<(script|style|pre|code)\b[^>]*>[\s\S]*?<\/\1>/gi, function (block) {
      return maskKeepNewlines(block);
    });
  }

  function visibleCopy(html) {
    return stripNonCopyBlocks(html).replace(/<(?:"[^"]*"|'[^']*'|[^>"'])*>/g, function (tag) {
      return maskKeepNewlines(tag);
    });
  }

  function stripComments(css) {
    return String(css).replace(/\/\*[\s\S]*?\*\//g, function (block) {
      return maskKeepNewlines(block);
    });
  }

  function scoreDimensions(findings) {
    var dims = {
      hierarchy: 5,
      spacing: 5,
      uniqueness: 5,
      restraint: 5,
      accessibility: 5,
      product_fit: 5,
    };
    for (var i = 0; i < findings.length; i++) {
      var f = findings[i];
      var d = Object.prototype.hasOwnProperty.call(dims, f.dimension) ? f.dimension : "restraint";
      var penalty = f.severity === "error" ? 2 : 1;
      dims[d] = Math.max(1, dims[d] - penalty);
    }
    return dims;
  }

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function auditCode(rawText, fileLabel, options) {
    var text = String(rawText || "");
    var label = fileLabel || "snippet.html";
    var opts = options || {};
    var allowFonts = {};
    (opts.allowFonts || []).forEach(function (name) {
      if (String(name).trim()) allowFonts[String(name).trim().toLowerCase()] = true;
    });
    var isCssOnly = /\.css$/i.test(label);
    var newlineAt = [];
    for (var ni = 0; ni < text.length; ni++) {
      if (text.charCodeAt(ni) === 10) newlineAt.push(ni);
    }
    function lineAt(offset) {
      if (offset <= 0) return 1;
      var lo = 0;
      var hi = newlineAt.length;
      while (lo < hi) {
        var mid = (lo + hi) >> 1;
        if (newlineAt[mid] < offset) lo = mid + 1;
        else hi = mid;
      }
      return lo + 1;
    }
    var lines = text.split("\n");
    var findings = [];
    var cssSegments = extractCssSegments(text, isCssOnly);

    function add(line, rule, dimension, severity, message, fix) {
      if (ignoredRulesOnLine(lines, line).has(rule)) return;
      findings.push({
        file: label,
        line: line,
        rule: rule,
        dimension: dimension,
        severity: severity,
        message: message,
        fix: fix,
      });
    }

    // 1. type.avoid-tells
    var fontContexts = [];
    var m;
    var gfonts = /fonts\.googleapis\.com\/css[^\s"'>]+/gi;
    while ((m = gfonts.exec(text)) !== null) {
      fontContexts.push([lineAt( m.index), m[0].replace(/\+/g, " ")]);
    }
    var ffRe = /font-family\s*:\s*([^;}\n]+)/gi;
    while ((m = ffRe.exec(text)) !== null) {
      fontContexts.push([lineAt( m.index), m[1]]);
    }
    var twFont = /\bfont-(inter|geist|space-grotesk|dm-sans|plus-jakarta|playfair)\b/gi;
    while ((m = twFont.exec(text)) !== null) {
      fontContexts.push([lineAt( m.index), m[1].replace(/-/g, " ")]);
    }

    var seenTells = new Set();
    for (var i = 0; i < fontContexts.length; i++) {
      var ln = fontContexts[i][0];
      var snip = fontContexts[i][1];
      for (var j = 0; j < COSTUME_FONTS.length; j++) {
        var face = COSTUME_FONTS[j];
        if (allowFonts[face.toLowerCase()]) continue;
        var fRe = new RegExp("(^|[^A-Za-z0-9-])" + escapeRegex(face) + "(?![A-Za-z0-9-])", "i");
        if (fRe.test(snip)) {
          var key = face.toLowerCase() + ":" + ln;
          if (!seenTells.has(key)) {
            seenTells.add(key);
            add(
              ln,
              "type.avoid-tells",
              "uniqueness",
              "error",
              "Costume typeface '" + face + "' detected.",
              "Use a system stack or a quieter open face (IBM Plex, Public Sans, Newsreader, Source Serif 4) after fixing the layout."
            );
          }
        }
      }
    }

    // 2. type.two-families
    var declared = {};
    for (var s = 0; s < cssSegments.length; s++) {
      var segObj = cssSegments[s];
      var ffSeg = /font-family\s*:\s*([^;}\n]+)/gi;
      while ((m = ffSeg.exec(segObj.seg)) !== null) {
        var firstRaw = m[1].split(",")[0].trim().replace(/^["']|["']$/g, "");
        var famKey = firstRaw.toLowerCase();
        if (!firstRaw || /^var\(/.test(firstRaw) || GENERIC_FONTS.has(famKey)) continue;
        if (!Object.prototype.hasOwnProperty.call(declared, famKey)) {
          declared[famKey] = { name: firstRaw, line: lineAt(segObj.base + m.index) };
        }
      }
    }
    var famKeys = Object.keys(declared);
    if (famKeys.length > 2) {
      var famNames = famKeys.map(function (key) { return declared[key].name; });
      var famLine = famKeys.reduce(function (min, key) {
        return Math.min(min, declared[key].line);
      }, declared[famKeys[0]].line);
      add(
        famLine,
        "type.two-families",
        "restraint",
        "error",
        "Found " + famKeys.length + " primary font families (" + famNames.join(", ") + "). Maximum is 2.",
        "Collapse extra roles into weights or sizes of the two primary families."
      );
    }

    // 3. color.aurora
    for (s = 0; s < cssSegments.length; s++) {
      segObj = cssSegments[s];
      var bgClip = /background-clip\s*:\s*text/gi;
      while ((m = bgClip.exec(segObj.seg)) !== null) {
        add(
          lineAt( segObj.base + m.index),
          "color.aurora",
          "restraint",
          "error",
          "Gradient-clipped text headline detected (background-clip: text).",
          "Set the headline in solid ink on a flat surface."
        );
      }
    }
    var twClip = /\bbg-clip-text\b[^\n]*\bbg-gradient-/g;
    while ((m = twClip.exec(text)) !== null) {
      add(
        lineAt( m.index),
        "color.aurora",
        "restraint",
        "error",
        "Tailwind gradient-clipped text detected (bg-clip-text + bg-gradient-*).",
        "Remove the gradient text and set solid ink."
      );
    }

    // 4. color.indigo-default
    var indM = /(?:bg-indigo-[4567]00|text-indigo-[56]00|from-indigo-[456]00|bg-violet-[56]00|#4f46e5|#6366f1|#7c3aed)/i.exec(text);
    if (indM) {
      add(
        lineAt( indM.index),
        "color.indigo-default",
        "restraint",
        "warn",
        "Default SaaS indigo/violet accent detected (" + indM[0] + ").",
        "Choose temperature and structure from the screen's direction before picking an accent."
      );
    }

    // 5. material.glass-on-flat
    var blurRe = /(?:backdrop-filter\s*:\s*blur|backdrop-blur-)/gi;
    while ((m = blurRe.exec(text)) !== null) {
      add(
        lineAt( m.index),
        "material.glass-on-flat",
        "restraint",
        "warn",
        "Backdrop blur panel detected; ensure it sits over live/photographic content, not a flat surface.",
        "Use a solid surface or raised paper tone instead of decorative blur."
      );
    }

    // 6. motion.hover, material.gray-card-shadow, color.contrast, motion.reduced, motion.timing, type.no-hairline-body, type.caps-tracking
    var hasMotion = false;
    var hasReducedMotion = text.indexOf("@media (prefers-reduced-motion") !== -1 || text.indexOf("motion-reduce:") !== -1;
    var rootVars = {};
    for (s = 0; s < cssSegments.length; s++) {
      var rootClean = stripComments(cssSegments[s].seg);
      var rootRule = /([^{}]+)\{([^}]+)\}/g;
      var rootMatch;
      while ((rootMatch = rootRule.exec(rootClean)) !== null) {
        if (!/(?:^|[\s,]):root\b/.test(rootMatch[1])) continue;
        var propRe = /(--[A-Za-z0-9_-]+)\s*:\s*([^;]+)/g;
        var propMatch;
        while ((propMatch = propRe.exec(rootMatch[2])) !== null) rootVars[propMatch[1]] = propMatch[2].trim();
      }
    }
    function firstColorToken(body, propRe) {
      var found = new RegExp("(?:^|[;{])\\s*(?:" + propRe + ")\\s*:\\s*([^;}]+)", "i").exec(body);
      if (!found) return null;
      var token = /#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)|var\(\s*--[A-Za-z0-9_-]+/i.exec(found[1]);
      return token ? token[0] : null;
    }
    for (s = 0; s < cssSegments.length; s++) {
      segObj = cssSegments[s];
      var cleanSeg = stripComments(segObj.seg);
      if (cleanSeg.indexOf("@keyframes") !== -1 || cleanSeg.indexOf("transition:") !== -1 || cleanSeg.indexOf("scroll-behavior:") !== -1) {
        hasMotion = true;
      }
      var trAllRe = /transition\s*:\s*all\b/gi;
      while ((m = trAllRe.exec(cleanSeg)) !== null) {
        add(
          lineAt(segObj.base + m.index),
          "motion.timing",
          "restraint",
          "warn",
          "transition: all animates layout properties unnecessarily.",
          "Specify exact transitions (color, border-color, opacity) keeping durations 120–180ms."
        );
      }
      var hoverRe = /([^{}]+:hover[^{]*)\{([^}]+)\}/gi;
      while ((m = hoverRe.exec(cleanSeg)) !== null) {
        if (/transform\s*:\s*(?:translate|scale)/i.test(m[2]) && /box-shadow/i.test(m[2])) {
          add(
            lineAt( segObj.base + m.index),
            "motion.hover",
            "restraint",
            "error",
            "Hover rule combines transform lift/scale with box-shadow.",
            "Hover should change ink, underline, or hairline only—do not lift cards."
          );
        }
      }
      var ruleRe = /([^{}]+)\{([^}]+)\}/g;
      while ((m = ruleRe.exec(cleanSeg)) !== null) {
        var sel = m[1].trim();
        var body = m[2];
        if (/box-shadow\s*:\s*(?!none|inset)[^;]+/i.test(body) && /border-radius\s*:\s*(?:1[6-9]|[2-9]\d)px/i.test(body)) {
          add(
            lineAt( segObj.base + m.index),
            "material.gray-card-shadow",
            "restraint",
            "error",
            "In-flow card selector (" + sel + ") uses large border-radius with box-shadow.",
            "Use flat paper, margins, and 1px hairlines; reserve shadow for overlays only."
          );
        }
        var fwM = /font-weight\s*:\s*(100|200)\b/i.exec(body);
        if (fwM) {
          var fsM = /font-size\s*:\s*(\d+(?:\.\d+)?)px/i.exec(body);
          var isReadingSel = /(?:^|[\s,])(body|p|li|dd|article|main|nav|label|button|a)\b/i.test(sel);
          if (isReadingSel || (fsM && parseFloat(fsM[1]) <= 18)) {
            add(
              lineAt(segObj.base + m.index),
              "type.no-hairline-body",
              "accessibility",
              "error",
              "Hairline font-weight " + fwM[1] + " applied on '" + sel + "' (fails practical legibility below 18px).",
              "Use weight 400 (or 500 for short UI labels) for readable text and navigation."
            );
          }
        }
        if (/text-transform\s*:\s*uppercase/i.test(body)) {
          var lsM = /letter-spacing\s*:\s*([^;}]+)/i.exec(body);
          var hasPosLs = false;
          if (lsM) {
            var lsRaw = lsM[1].trim();
            var lsNum = /^([+-]?(?:\d+\.?\d*|\.\d+))\s*(?:px|em|rem)?\b/i.exec(lsRaw);
            if ((lsNum && parseFloat(lsNum[1]) > 0) || lsRaw.indexOf("var(") === 0) {
              hasPosLs = true;
            }
          }
          if (!hasPosLs) {
            add(
              lineAt(segObj.base + m.index),
              "type.caps-tracking",
              "restraint",
              "warn",
              "Uppercase transform in '" + sel + "' lacks positive letter-spacing.",
              "Add letter-spacing: 0.05em to 0.08em on a short kicker, or set in sentence case."
            );
          }
        }
        var fgToken = firstColorToken(body, "(?<![a-z-])color");
        var bgToken = firstColorToken(body, "background(?:-color)?");
        if (fgToken && bgToken) {
          var fgRgb = parseColor(fgToken, rootVars, 0);
          var bgRgb = parseColor(bgToken, rootVars, 0);
          if (fgRgb && bgRgb) {
            var ratio = contrastRatioFromRgb(fgRgb, bgRgb);
            if (ratio < 4.5) {
              var fgAt = body.indexOf(fgToken);
              var bgAt = body.indexOf(bgToken);
              var propAt = Math.min(fgAt < 0 ? body.length : fgAt, bgAt < 0 ? body.length : bgAt);
              var bodyStart = m.index + m[1].length + 1;
              add(
                lineAt(segObj.base + bodyStart + propAt),
                "color.contrast",
                "accessibility",
                "error",
                "Contrast " + ratio.toFixed(2) + ":1 between " + fgToken + " and " + bgToken + " in '" + sel + "' is under 4.5:1.",
                "Darken muted ink or raise foreground/background contrast to at least 4.5:1."
              );
            }
          }
        }
      }
    }

    var twTrAll = /\btransition-all\b/g;
    while ((m = twTrAll.exec(text)) !== null) {
      add(
        lineAt(m.index),
        "motion.timing",
        "restraint",
        "warn",
        "Tailwind transition-all utility detected.",
        "Replace with transition-colors or specific property transitions (120–180ms)."
      );
    }

    var twLift = /hover:(?:-?translate-y-|scale-)/g;
    while ((m = twLift.exec(text)) !== null) {
      add(
        lineAt( m.index),
        "motion.hover",
        "restraint",
        "error",
        "Tailwind hover lift/scale utility '" + m[0] + "' detected.",
        "Replace card lift with a border or ink color change."
      );
    }

    if (hasMotion && !hasReducedMotion) {
      add(
        1,
        "motion.reduced",
        "accessibility",
        "warn",
        "Transitions or animations found without a prefers-reduced-motion fallback.",
        "Add @media (prefers-reduced-motion: reduce) to remove transforms and long transitions."
      );
    }

    // 7. a11y.focus-removed
    var outlineNone = /(?:outline\s*:\s*(?:none|0)\b|focus:outline-none)/i.exec(text);
    if (outlineNone && text.indexOf(":focus-visible") === -1 && text.indexOf("focus-visible:") === -1) {
      add(
        lineAt( outlineNone.index),
        "a11y.focus-removed",
        "accessibility",
        "error",
        "Focus outline removed without a :focus-visible replacement.",
        "Add a 2px offset :focus-visible outline in ink or accent."
      );
    }

    // 8. a11y.size
    for (s = 0; s < cssSegments.length; s++) {
      segObj = cssSegments[s];
      var smallBody = /(?:^|[}\n]\s*)(body|p|li|dd|article|main)\s*\{[^}]*font-size\s*:\s*(\d+(?:\.\d+)?)px/gim;
      while ((m = smallBody.exec(segObj.seg)) !== null) {
        var px = parseFloat(m[2]);
        if (px < 14) {
          add(
            lineAt( segObj.base + m.index),
            "a11y.size",
            "accessibility",
            "error",
            "Reading selector '" + m[1] + "' sets font-size to " + px + "px (below 14px minimum).",
            "Raise body reading text to at least 14px (16–18px for prose)."
          );
        }
      }
    }

    // 9. HTML/JSX structural, copy & accessibility checks
    if (!isCssOnly) {
      var labelFors = {};
      var openTags = iterOpenTags(text);
      openTags.forEach(function (tag) {
        if (tag.tag !== "label") return;
        var target = attrValue(tag.attrs, ["for", "htmlFor"]);
        if (target) labelFors[target] = true;
      });
      openTags.forEach(function (tag) {
        if (tag.tag !== "input" && tag.tag !== "textarea") return;
        var controlType = (attrValue(tag.attrs, ["type"]) || "").toLowerCase();
        if (controlType === "hidden" || controlType === "submit" || controlType === "button" || controlType === "reset") return;
        if (attrValue(tag.attrs, ["placeholder"]) == null) return;
        var hasAria = attrValue(tag.attrs, ["aria-label", "aria-labelledby"]) != null;
        var controlId = attrValue(tag.attrs, ["id"]);
        var hasFor = Boolean(controlId && labelFors[controlId]);
        var prefix = text.slice(Math.max(0, tag.start - 250), tag.start).toLowerCase();
        var insideLabel = prefix.lastIndexOf("<label") > prefix.lastIndexOf("</label");
        if (!hasAria && !hasFor && !insideLabel) {
          add(
            lineAt(tag.start),
            "a11y.placeholder-label",
            "accessibility",
            "error",
            "Form control relies on placeholder without a visible <label> or aria-label.",
            "Add a visible <label for=...> above or beside the field."
          );
        }
      });

      openTags.forEach(function (tag) {
        if (tag.tag !== "div") return;
        var className = attrValue(tag.attrs, ["class", "className"]) || "";
        if (!/(?:^|[\s_])(?:cta|actions|hero-actions|buttons)(?:$|[\s_])/i.test(className)) return;
        var inner = elementInner(text, tag.end, "div");
        var filled = 0;
        iterOpenTags(inner).forEach(function (innerTag) {
          if (innerTag.tag !== "button" && innerTag.tag !== "a") return;
          var cls = attrValue(innerTag.attrs, ["class", "className"]) || "";
          if ((cls.indexOf("btn") !== -1 || cls.indexOf("button") !== -1 || cls.indexOf("bg-") !== -1) &&
              !/\b(?:ghost|secondary|outline|quiet|text|link)\b/i.test(cls)) {
            filled++;
          }
        });
        if (filled > 1) {
          add(
            lineAt(tag.start),
            "chrome.two-primaries",
            "hierarchy",
            "error",
            "Action group has " + filled + " primary-styled buttons side by side.",
            "Keep one filled primary action; demote secondary actions to underlined text or quiet buttons."
          );
        }
      });

      var visibleText = visibleCopy(text);
      for (var c = 0; c < ABSTRACT_CLICHES.length; c++) {
        var cm = ABSTRACT_CLICHES[c].exec(visibleText);
        if (cm) {
          add(
            lineAt(cm.index),
            "content.abstract-verbs",
            "uniqueness",
            "error",
            "Generic marketing phrasing '" + cm[0].trim() + "' could fit any product.",
            "Replace with concrete nouns, materials, prices, or actions specific to this product."
          );
        }
      }

      var fakeM = FAKE_PROOF_RE.exec(visibleText);
      if (fakeM) {
        add(
          lineAt(fakeM.index),
          "content.fake-proof",
          "uniqueness",
          "error",
          "Unsourced social proof pattern '" + fakeM[0] + "' detected.",
          "Remove invented counts or logo clouds; use one verifiable fact or nothing."
        );
      }

      var sparkM = SPARKLE_RE.exec(stripNonCopyBlocks(text));
      if (sparkM) {
        add(
          lineAt(sparkM.index),
          "chrome.sparkle",
          "uniqueness",
          "error",
          "Sparkle motif '" + sparkM[0] + "' used as UI decoration.",
          "Remove sparkle/wand icons; depict the product's real object or state."
        );
      }

      var copyHtml = stripNonCopyBlocks(text);
      var divClickRe = /<(div|span)\b([^>]*\bon(?:click|Click)\s*=[^>]*)>/g;
      while ((m = divClickRe.exec(copyHtml)) !== null) {
        if (!/\brole=["']?(?:button|link|menuitem|tab)/i.test(m[2])) {
          var divPos = text.indexOf(m[0]);
          add(
            lineAt(divPos !== -1 ? divPos : 0),
            "a11y.semantics",
            "accessibility",
            "error",
            "Clickable <" + m[1] + "> lacks native button/link semantics.",
            "Replace with <button type=\"button\"> or <a href=\"...\"> for keyboard and screen-reader support."
          );
        }
      }

      var vpM = /<meta\b[^>]*name=["']viewport["'][^>]*content=["']([^"']+)["']/i.exec(text);
      if (vpM && /(?:user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0+)?\b)/i.test(vpM[1])) {
        add(
          lineAt(vpM.index),
          "a11y.semantics",
          "accessibility",
          "error",
          "Viewport meta disables pinch zoom (user-scalable=no or maximum-scale=1).",
          "Allow zooming with content=\"width=device-width, initial-scale=1.0\"."
        );
      }

      var tblM = /<table\b/i.exec(copyHtml);
      var usesExtCss = /<link\b[^>]+rel=["']stylesheet["']/i.test(text) || /import\s+["'][^"']+\.css/.test(text);
      if (tblM && !usesExtCss && text.indexOf("tabular-nums") === -1) {
        var tblPos = text.indexOf(tblM[0]);
        add(
          lineAt(tblPos !== -1 ? tblPos : 0),
          "type.numbers",
          "hierarchy",
          "warn",
          "Data table present without font-variant-numeric: tabular-nums or Tailwind tabular-nums.",
          "Set font-variant-numeric: tabular-nums on numeric/table columns so figures stay aligned."
        );
      }

      var twUpperRe = /class(?:Name)?=["']([^"']*\buppercase\b[^"']*)["']/g;
      while ((m = twUpperRe.exec(copyHtml)) !== null) {
        if (!/\btracking-(?:wide|wider|widest)\b/.test(m[1])) {
          var upPos = text.indexOf(m[0]);
          add(
            lineAt(upPos !== -1 ? upPos : 0),
            "type.caps-tracking",
            "restraint",
            "warn",
            "Tailwind 'uppercase' utility used without positive tracking-* spacing.",
            "Pair uppercase with tracking-wider on one short kicker or remove uppercase."
          );
        }
      }
    }

    var scores = scoreDimensions(findings);
    return {
      file: label,
      findings: findings,
      scores: scores,
      passed: findings.length === 0,
    };
  }

  function formatReport(result) {
    var s = result.scores;
    var lines = [
      "Premium Taste Audit (" + result.file + ", " + result.findings.length + " finding(s))",
      "",
      "Static Scores (automated check):",
      "  - Hierarchy:     " + s.hierarchy + "/5",
      "  - Spacing:       " + s.spacing + "/5",
      "  - Uniqueness:    " + s.uniqueness + "/5",
      "  - Restraint:     " + s.restraint + "/5",
      "  - Accessibility: " + s.accessibility + "/5",
      "  - Product fit:   " + s.product_fit + "/5",
      "",
    ];
    if (!result.findings.length) {
      lines.push("PASS: No automated rule violations found.");
      return lines.join("\n");
    }
    lines.push("Findings:");
    result.findings.forEach(function (f, idx) {
      lines.push("  " + (idx + 1) + ". [" + f.severity.toUpperCase() + "] " + f.file + ":" + f.line + " — " + f.rule);
      lines.push("     Now: " + f.message);
      lines.push("     Fix: " + f.fix);
    });
    return lines.join("\n");
  }

  global.PremiumTasteAudit = {
    auditCode: auditCode,
    scoreDimensions: scoreDimensions,
    contrastRatio: contrastRatio,
    hexToRgb: hexToRgb,
    parseColor: parseColor,
    formatReport: formatReport,
  };
})(typeof window !== "undefined" ? window : globalThis);
