/* =============================================================================
   LABORATORIO ATS - LOGICA DEL FRONTEND
   ============================================================================= */

(function () {
  "use strict";

  // --- Estado ---
  const state = {
    files: [],
    isLoading: false,
  };

  // --- Referencias DOM ---
  const dom = {
    closeBanner: document.getElementById("close-banner"),
    infoBanner: document.getElementById("info-banner"),
    jobPosition: document.getElementById("job-position"),
    requirements: document.getElementById("requirements"),
    dropZone: document.getElementById("drop-zone"),
    fileInput: document.getElementById("file-input"),
    fileList: document.getElementById("file-list"),
    cvCounter: document.getElementById("cv-counter"),
    analyzeBtn: document.getElementById("analyze-btn"),
    loadingSection: document.getElementById("loading-section"),
    loadingSteps: document.querySelectorAll(".loading-step"),
    panelResults: document.getElementById("panel-results"),
    resultsBody: document.getElementById("results-body"),
    panelBest: document.getElementById("panel-best"),
    bestBody: document.getElementById("best-body"),
    panelRaw: document.getElementById("panel-raw"),
    rawResponse: document.getElementById("raw-response"),
    resetBtn: document.getElementById("reset-btn"),
  };

  // --- Banner ---
  dom.closeBanner.addEventListener("click", () => {
    dom.infoBanner.style.display = "none";
  });

  // --- Drop Zone ---
  dom.dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dom.dropZone.classList.add("drag-over");
  });

  dom.dropZone.addEventListener("dragleave", () => {
    dom.dropZone.classList.remove("drag-over");
  });

  dom.dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dom.dropZone.classList.remove("drag-over");
    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      (f) => f.type === "application/pdf"
    );
    addFiles(droppedFiles);
  });

  dom.fileInput.addEventListener("change", () => {
    const selectedFiles = Array.from(dom.fileInput.files);
    addFiles(selectedFiles);
    dom.fileInput.value = "";
  });

  function addFiles(newFiles) {
    newFiles.forEach((file) => {
      const alreadyAdded = state.files.some((f) => f.name === file.name && f.size === file.size);
      if (!alreadyAdded) {
        state.files.push(file);
      }
    });
    renderFileList();
    updateAnalyzeBtn();
  }

  function removeFile(index) {
    state.files.splice(index, 1);
    renderFileList();
    updateAnalyzeBtn();
  }

  function renderFileList() {
    dom.fileList.innerHTML = "";
    dom.cvCounter.textContent = `${state.files.length} CV${state.files.length !== 1 ? "s" : ""} cargado${state.files.length !== 1 ? "s" : ""}`;

    state.files.forEach((file, index) => {
      const item = document.createElement("div");
      item.className = "file-item";
      item.innerHTML = `
        <div class="file-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
        </div>
        <div class="file-info">
          <div class="file-name">${escapeHtml(file.name)}</div>
          <div class="file-size">${formatFileSize(file.size)}</div>
        </div>
        <button class="file-remove" data-index="${index}" aria-label="Eliminar archivo">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      `;
      dom.fileList.appendChild(item);
    });

    dom.fileList.querySelectorAll(".file-remove").forEach((btn) => {
      btn.addEventListener("click", () => {
        removeFile(parseInt(btn.dataset.index, 10));
      });
    });
  }

  function updateAnalyzeBtn() {
    dom.analyzeBtn.disabled = state.files.length === 0 || state.isLoading;
  }

  // --- Analyze ---
  dom.analyzeBtn.addEventListener("click", runAnalysis);

  async function runAnalysis() {
    const jobPosition = dom.jobPosition.value.trim();

    if (!jobPosition) {
      showError("El puesto a cubrir es obligatorio.");
      dom.jobPosition.focus();
      return;
    }

    if (state.files.length === 0) {
      showError("Debes cargar al menos un CV en PDF.");
      return;
    }

    setLoadingState(true);
    hideResults();

    try {
      // Simular progreso de pasos
      animateLoadingSteps();

      const formData = new FormData();
      formData.append("jobPosition", jobPosition);
      formData.append("requirements", dom.requirements.value.trim());

      state.files.forEach((file) => {
        formData.append("cvFiles", file);
      });

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error?.message || "Error al analizar los CVs.");
      }

      renderResults(data);
    } catch (error) {
      showError(error.message || "Error inesperado. Verificar la API key y el servidor.");
    } finally {
      setLoadingState(false);
    }
  }

  function animateLoadingSteps() {
    const steps = Array.from(dom.loadingSteps);
    let current = 0;

    steps.forEach((s) => s.classList.remove("active", "done"));
    steps[0].classList.add("active");

    const interval = setInterval(() => {
      if (current < steps.length - 1) {
        steps[current].classList.remove("active");
        steps[current].classList.add("done");
        current++;
        steps[current].classList.add("active");
      } else {
        clearInterval(interval);
      }
    }, 1800);
  }

  function setLoadingState(loading) {
    state.isLoading = loading;
    dom.loadingSection.style.display = loading ? "block" : "none";
    dom.analyzeBtn.disabled = loading;
    dom.analyzeBtn.querySelector("span").textContent = loading
      ? "Analizando..."
      : "Analizar CVs con IA";
    updateAnalyzeBtn();
  }

  function hideResults() {
    dom.panelResults.style.display = "none";
    dom.panelBest.style.display = "none";
    dom.panelRaw.style.display = "none";
    dom.resultsBody.innerHTML = "";
    dom.bestBody.innerHTML = "";
    dom.rawResponse.textContent = "";
  }

  // --- Render Results ---
  function renderResults(data) {
    // Respuesta sin parsear (fallback)
    if (data.parseError) {
      dom.panelRaw.style.display = "block";
      dom.rawResponse.textContent = data.rawResponse || "Sin respuesta.";
      dom.panelRaw.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    if (!data.ranking || data.ranking.length === 0) {
      showError("La IA no retorno un ranking. Intentar nuevamente.");
      return;
    }

    const cvSources = data.cvSources || [];

    // Ordenar por score descendente
    const sorted = [...data.ranking].sort((a, b) => b.score - a.score);

    dom.panelResults.style.display = "block";
    dom.resultsBody.innerHTML = "";

    sorted.forEach((candidate, displayIndex) => {
      const rank = displayIndex + 1;
      const source = cvSources.find((s) => s.cvNumber === candidate.cvNumber);
      const fileName = source ? source.fileName : `CV ${candidate.cvNumber}`;

      const card = document.createElement("div");
      card.className = `result-card ${rank === 1 ? "result-card-1" : ""}`;

      const rankBadgeClass =
        rank === 1 ? "badge-rank-1"
        : rank === 2 ? "badge-rank-2"
        : rank === 3 ? "badge-rank-3"
        : "badge-rank-default";

      const skillTags = (candidate.keySkillsFound || [])
        .slice(0, 6)
        .map((s) => `<span class="result-tag">${escapeHtml(s)}</span>`)
        .join("");

      const strengthItems = (candidate.strengths || [])
        .map((s) => `<li>${escapeHtml(s)}</li>`)
        .join("");

      const weaknessItems = (candidate.weaknesses || [])
        .map((w) => `<li>${escapeHtml(w)}</li>`)
        .join("");

      card.innerHTML = `
        <div class="badge-rank ${rankBadgeClass}">${rank}</div>
        <div class="result-content">
          <div class="result-header">
            <div class="result-name-block">
              <div class="result-name">${escapeHtml(candidate.candidateName || "Candidato sin nombre")}</div>
              <div class="result-file">${escapeHtml(fileName)}</div>
            </div>
            <div class="result-score-block">
              <div class="result-score">${candidate.score}</div>
              <div class="result-score-label">puntos</div>
            </div>
          </div>
          <div class="score-bar-bg">
            <div class="score-bar-fill" data-score="${candidate.score}"></div>
          </div>
          <p class="result-justification">${escapeHtml(candidate.justification || "")}</p>
          ${skillTags ? `<div class="result-tags">${skillTags}</div>` : ""}
          ${(strengthItems || weaknessItems) ? `
            <div class="result-details">
              ${strengthItems ? `
                <div class="result-detail-section">
                  <h4>Fortalezas</h4>
                  <ul class="result-detail-list strengths-list">${strengthItems}</ul>
                </div>` : ""}
              ${weaknessItems ? `
                <div class="result-detail-section">
                  <h4>Debilidades</h4>
                  <ul class="result-detail-list weaknesses-list">${weaknessItems}</ul>
                </div>` : ""}
            </div>` : ""}
        </div>
      `;

      dom.resultsBody.appendChild(card);
    });

    // Animar score bars despues de que el DOM este listo
    requestAnimationFrame(() => {
      document.querySelectorAll(".score-bar-fill").forEach((bar) => {
        const score = parseFloat(bar.dataset.score) || 0;
        requestAnimationFrame(() => {
          bar.style.width = `${score}%`;
        });
      });
    });

    // Mejor candidato
    if (data.bestCandidate) {
      const best = data.bestCandidate;
      const bestSource = cvSources.find((s) => s.cvNumber === best.cvNumber);
      const bestFileName = bestSource ? bestSource.fileName : `CV ${best.cvNumber}`;

      dom.panelBest.style.display = "block";
      dom.bestBody.innerHTML = `
        <div class="best-card">
          <div class="best-card-header">
            <span class="best-card-crown">&#127942;</span>
            <div class="best-card-info">
              <h3>${escapeHtml(bestFileName)}</h3>
              <p>CV ${best.cvNumber} &mdash; Mejor candidato para el puesto</p>
            </div>
          </div>
          <p class="best-card-summary">${escapeHtml(best.summary || "")}</p>
        </div>
      `;
    }

    dom.panelResults.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // --- Reset ---
  dom.resetBtn.addEventListener("click", () => {
    state.files = [];
    renderFileList();
    updateAnalyzeBtn();
    hideResults();
    dom.jobPosition.value = "";
    dom.requirements.value = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // --- Error Toast ---
  function showError(message) {
    let toast = document.querySelector(".error-toast");

    if (!toast) {
      toast = document.createElement("div");
      toast.className = "error-toast";
      toast.innerHTML = `
        <span class="error-toast-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </span>
        <span class="error-toast-message"></span>
      `;
      document.body.appendChild(toast);
    }

    toast.querySelector(".error-toast-message").textContent = message;
    toast.classList.add("visible");

    setTimeout(() => {
      toast.classList.remove("visible");
    }, 4000);
  }

  // --- Helpers ---
  function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(String(text)));
    return div.innerHTML;
  }

  // Inicializar
  renderFileList();
  updateAnalyzeBtn();
})();
