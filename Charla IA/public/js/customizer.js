(function () {
  "use strict";

  // --- Valores por defecto (coinciden con el CSS actual) ---
  const DEFAULTS = {
    "c-bg-primary":    "#0b0d1a",
    "c-bg-secondary":  "#10132a",
    "c-bg-elevated":   "#161a38",
    "c-glass-alpha":   "75",
    "c-text-primary":  "#eef2ff",
    "c-text-secondary":"#a5b4fc",
    "c-text-muted":    "#6b7cb3",
    "c-accent-1":      "#71bbf1",
    "c-accent-2":      "#9c6ce5",
    "c-border":        "#71bbf1",
    "c-danger":        "#c084fc",
  };

  const DEFAULT_FONT = "Montserrat";

  // --- Fuentes disponibles con sus pesos ---
  const FONTS = {
    "Montserrat":    "Montserrat:wght@400;500;600;700;800;900",
    "Inter":         "Inter:wght@400;500;600;700;800;900",
    "Roboto":        "Roboto:wght@400;500;700;900",
    "Poppins":       "Poppins:wght@400;500;600;700;800;900",
    "Raleway":       "Raleway:wght@400;500;600;700;800;900",
    "DM Sans":       "DM+Sans:wght@400;500;600;700;800",
    "Nunito":        "Nunito:wght@400;500;600;700;800;900",
    "Sora":          "Sora:wght@400;500;600;700;800",
    "Space Grotesk": "Space+Grotesk:wght@400;500;600;700",
    "Outfit":        "Outfit:wght@400;500;600;700;800;900",
  };

  // --- Estado actual ---
  const currentValues = { ...DEFAULTS };
  let currentFont = DEFAULT_FONT;

  // --- DOM ---
  const root   = document.documentElement;
  const panel  = document.getElementById("customizer-panel");
  const toggle = document.getElementById("customizer-toggle");
  const close  = document.getElementById("customizer-close");
  const fontSelect   = document.getElementById("font-select");
  const fontPreview  = document.getElementById("font-preview");
  const fontLink     = document.getElementById("font-link");
  const resetBtn     = document.getElementById("cust-reset");
  const copyCssBtn   = document.getElementById("cust-copy-css");

  // --- Abrir / cerrar panel ---
  toggle.addEventListener("click", () => panel.classList.toggle("open"));
  close.addEventListener("click",  () => panel.classList.remove("open"));

  // Cerrar al hacer click fuera
  document.addEventListener("click", (e) => {
    if (panel.classList.contains("open") &&
        !panel.contains(e.target) &&
        e.target !== toggle) {
      panel.classList.remove("open");
    }
  });

  // --- Aplicar variable CSS al root ---
  function applyVar(cssVar, value) {
    root.style.setProperty(cssVar, value);
  }

  // --- Recalcular variables derivadas del gradiente y el glass ---
  function applyAccentGradient() {
    const c1 = currentValues["c-accent-1"];
    const c2 = currentValues["c-accent-2"];
    applyVar("--accent-primary",   c1);
    applyVar("--accent-secondary", c2);
    applyVar("--accent-gradient",  `linear-gradient(135deg, ${c1}, ${c2})`);
    applyVar("--accent-gradient-hover", `linear-gradient(135deg, ${lighten(c1, 15)}, ${lighten(c2, 15)})`);
    applyVar("--accent-gradient-mid",   `linear-gradient(135deg, ${c1}, ${c2})`);
    applyVar("--blue-1",   c1);
    applyVar("--blue-2",   c1);
    applyVar("--blue-3",   c1);
    applyVar("--purple-1", c2);
    applyVar("--purple-2", c2);
    applyVar("--purple-3", c2);
    applyVar("--purple-4", c2);
    applyVar("--success",  c1);
    applyVar("--warning",  c2);
    applyVar("--border-glow", hexToRgba(c1, 0.3));

    // Actualizar color del icono del header
    const headerIcon = document.querySelector(".header-icon");
    if (headerIcon) {
      headerIcon.style.filter = `drop-shadow(0 0 10px ${hexToRgba(c1, 0.5)})`;
    }
  }

  function applyGlass() {
    const alpha = parseInt(currentValues["c-glass-alpha"], 10) / 100;
    const bg = currentValues["c-bg-secondary"];
    const r = parseInt(bg.slice(1, 3), 16);
    const g = parseInt(bg.slice(3, 5), 16);
    const b = parseInt(bg.slice(5, 7), 16);
    applyVar("--bg-glass", `rgba(${r}, ${g}, ${b}, ${alpha.toFixed(2)})`);
  }

  function applyBorder() {
    const c = currentValues["c-border"];
    applyVar("--border-color", hexToRgba(c, 0.15));
    applyVar("--border-glow",  hexToRgba(c, 0.3));
  }

  // --- Conectar inputs de color ---
  Object.keys(DEFAULTS).forEach((id) => {
    const input = document.getElementById(id);
    if (!input) return;

    input.value = DEFAULTS[id];

    input.addEventListener("input", () => {
      currentValues[id] = input.value;

      switch (id) {
        case "c-bg-primary":
          applyVar("--bg-primary", input.value);
          break;
        case "c-bg-secondary":
          applyVar("--bg-secondary", input.value);
          applyGlass();
          break;
        case "c-bg-elevated":
          applyVar("--bg-elevated", input.value);
          break;
        case "c-glass-alpha":
          applyGlass();
          break;
        case "c-text-primary":
          applyVar("--text-primary", input.value);
          break;
        case "c-text-secondary":
          applyVar("--text-secondary", input.value);
          break;
        case "c-text-muted":
          applyVar("--text-muted", input.value);
          break;
        case "c-accent-1":
        case "c-accent-2":
          applyAccentGradient();
          break;
        case "c-border":
          applyBorder();
          break;
        case "c-danger":
          applyVar("--danger", input.value);
          break;
      }
    });
  });

  // --- Selector de tipografia ---
  fontSelect.addEventListener("change", () => {
    currentFont = fontSelect.value;
    loadFont(currentFont);
  });

  function loadFont(fontName) {
    const query = FONTS[fontName];
    if (!query) return;

    fontLink.href = `https://fonts.googleapis.com/css2?family=${query}&display=swap`;

    // Aplicar la variable CSS
    applyVar("--font-family", `'${fontName}', sans-serif`);

    // Preview
    fontPreview.style.fontFamily = `'${fontName}', sans-serif`;
    fontSelect.style.fontFamily  = `'${fontName}', sans-serif`;
  }

  // --- Resetear a valores por defecto ---
  resetBtn.addEventListener("click", () => {
    // Resetear colores
    Object.keys(DEFAULTS).forEach((id) => {
      const input = document.getElementById(id);
      if (input) {
        input.value = DEFAULTS[id];
        currentValues[id] = DEFAULTS[id];
      }
    });

    // Limpiar overrides inline del root
    root.removeAttribute("style");

    // Resetear fuente
    currentFont = DEFAULT_FONT;
    fontSelect.value = DEFAULT_FONT;
    fontPreview.style.fontFamily  = "";
    fontSelect.style.fontFamily   = "";
    fontLink.href = `https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap`;
  });

  // --- Copiar CSS variables ---
  copyCssBtn.addEventListener("click", () => {
    const c1    = currentValues["c-accent-1"];
    const c2    = currentValues["c-accent-2"];
    const alpha = (parseInt(currentValues["c-glass-alpha"], 10) / 100).toFixed(2);
    const bgSec = currentValues["c-bg-secondary"];
    const r = parseInt(bgSec.slice(1,3), 16);
    const g = parseInt(bgSec.slice(3,5), 16);
    const b = parseInt(bgSec.slice(5,7), 16);

    const css = `:root {
  --bg-primary:   ${currentValues["c-bg-primary"]};
  --bg-secondary: ${currentValues["c-bg-secondary"]};
  --bg-elevated:  ${currentValues["c-bg-elevated"]};
  --bg-glass:     rgba(${r}, ${g}, ${b}, ${alpha});
  --text-primary:   ${currentValues["c-text-primary"]};
  --text-secondary: ${currentValues["c-text-secondary"]};
  --text-muted:     ${currentValues["c-text-muted"]};
  --accent-primary:  ${c1};
  --accent-secondary:${c2};
  --accent-gradient: linear-gradient(135deg, ${c1}, ${c2});
  --border-color: ${hexToRgba(currentValues["c-border"], 0.15)};
  --border-glow:  ${hexToRgba(currentValues["c-border"], 0.3)};
  --danger: ${currentValues["c-danger"]};
  --font-family: '${currentFont}', sans-serif;
}`;

    navigator.clipboard.writeText(css).then(() => {
      showCopiedToast();
    }).catch(() => {
      // Fallback para navegadores sin clipboard API
      const ta = document.createElement("textarea");
      ta.value = css;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      showCopiedToast();
    });
  });

  function showCopiedToast() {
    let toast = document.querySelector(".cust-copied-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "cust-copied-toast";
      toast.textContent = "CSS copiado al portapapeles";
      document.body.appendChild(toast);
    }
    toast.classList.add("visible");
    setTimeout(() => toast.classList.remove("visible"), 2500);
  }

  // --- Helpers de color ---
  function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  function lighten(hex, amount) {
    const r = Math.min(255, parseInt(hex.slice(1,3), 16) + amount);
    const g = Math.min(255, parseInt(hex.slice(3,5), 16) + amount);
    const b = Math.min(255, parseInt(hex.slice(5,7), 16) + amount);
    return `#${r.toString(16).padStart(2,"0")}${g.toString(16).padStart(2,"0")}${b.toString(16).padStart(2,"0")}`;
  }

})();
