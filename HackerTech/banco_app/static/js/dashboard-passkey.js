// Dashboard: registrar una passkey para reforzar la seguridad del login.
//
// Los 4 botones (huella / PIN / rostro / llave de seguridad) llaman al
// mismo window.registerPasskey(method) (definido en webauthn-common.js),
// pasando cual se toco. El backend usa eso para pedirle al navegador un
// authenticatorAttachment especifico (ver webauthn_auth.py y
// app.py:_METHOD_TO_ATTACHMENT): "llave" fuerza cross-platform (el
// navegador solo ofrece llaves externas tipo YubiKey), los otros tres
// fuerzan platform (solo el autenticador integrado - Windows Hello, Touch
// ID). Dentro de los 3 de plataforma, el SO decide que pedir exactamente
// segun lo que el dispositivo tenga configurado: si el usuario toca
// "Huella" pero su equipo solo tiene reconocimiento facial, Windows Hello
// va a pedir la cara igual - es esperado, la app no puede forzar que
// biometria especifica usa el SO (si puede forzar plataforma vs. externa,
// pero no mas fino que eso).
//
// Los 3 metodos de plataforma (huella/PIN/rostro) comparten un chequeo
// previo de disponibilidad (isUserVerifyingPlatformAuthenticatorAvailable):
// la app no puede saber DE ANTEMANO cual de los tres esta configurado,
// solo si hay o no un autenticador de plataforma en general. "Llave de
// seguridad" es independiente de ese chequeo - una YubiKey externa no
// depende de que el dispositivo tenga biometria/PIN configurados, asi que
// siempre se ofrece si el navegador soporta WebAuthn.
//
// El fallback entre metodos es reactivo: si un intento falla/cancela,
// recien ahi se saca esa opcion de la lista y se ofrecen las que quedan.
// Adaptado desde ../../utn_frc_redesign/static/js/portal.js.
(function () {
  const container = document.getElementById("passkey-methods");
  if (!container) return; // ya tiene passkey, o no aplica en esta pagina

  const intro = document.getElementById("passkey-intro");
  const unsupported = document.getElementById("passkey-unsupported");
  const statusLine = document.getElementById("register-status");

  const PLATFORM_METHODS = new Set(["huella", "pin", "rostro"]);

  const METHOD_LABELS = {
    huella: "huella dactilar",
    pin: "PIN",
    rostro: "reconocimiento facial",
    llave: "llave de seguridad",
  };
  const CONFIRM_TEXT = {
    huella: "Confirmá con tu huella dactilar en tu dispositivo...",
    pin: "Ingresá tu PIN...",
    rostro: "Mirá a la cámara para el reconocimiento facial...",
    llave: "Insertá (o acercá) tu llave de seguridad y tocala para confirmar...",
  };

  function showUnsupported() {
    intro.classList.add("hidden");
    container.classList.add("hidden");
    unsupported.classList.remove("hidden");
  }

  function showNoMethodsLeft() {
    statusLine.textContent =
      "No fue posible registrar un método de seguridad en este dispositivo. Podés intentarlo desde otro dispositivo compatible.";
    statusLine.className = "status-line text-xs error";
  }

  // Chequeo especifico de autenticadores de PLATAFORMA (no aplica a la
  // llave de seguridad externa, que no depende de esto).
  async function isPlatformAuthenticatorAvailable() {
    if (!window.PublicKeyCredential || !PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable) {
      return false;
    }
    try {
      return await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
    } catch {
      return false;
    }
  }

  // Saca un metodo de la lista (fallo el chequeo previo o el create() en si)
  // y ofrece los que quedan - o el mensaje final si ya no queda ninguno.
  function dropMethodAndOfferRemaining(failedBtn, failureMessage) {
    failedBtn.remove();
    const remaining = Array.from(container.querySelectorAll(".passkey-method-btn"));
    remaining.forEach((b) => (b.disabled = false));

    if (remaining.length === 0) {
      showNoMethodsLeft();
      return;
    }

    const remainingLabels = remaining.map((b) => METHOD_LABELS[b.dataset.method]);
    statusLine.textContent = `${failureMessage} ¿Querés probar con ${remainingLabels.join(" o ")}?`;
    statusLine.className = "status-line text-xs error";
  }

  // 1. Chequeo al cargar la pagina: sin soporte de WebAuthn no hay nada
  // que ofrecer. Con soporte pero sin autenticador de plataforma, se sacan
  // solo huella/PIN/rostro - "Llave de seguridad" queda disponible igual.
  if (!window.PublicKeyCredential) {
    showUnsupported();
  } else {
    isPlatformAuthenticatorAvailable().then((available) => {
      if (available) return;
      const platformButtons = Array.from(container.querySelectorAll(".passkey-method-btn")).filter((b) =>
        PLATFORM_METHODS.has(b.dataset.method)
      );
      platformButtons.forEach((b) => b.remove());
    });
  }

  container.addEventListener("click", async (event) => {
    const btn = event.target.closest(".passkey-method-btn");
    if (!btn || btn.disabled) return;

    const allButtons = Array.from(container.querySelectorAll(".passkey-method-btn"));
    allButtons.forEach((b) => (b.disabled = true));

    const method = btn.dataset.method;

    // Re-chequeo antes de llamar a create(), solo para metodos de
    // plataforma: si no hay ningun autenticador de plataforma, ni siquiera
    // intentamos la ceremonia WebAuthn - se trata igual que un intento
    // fallido de ESTE metodo (nunca un error generico) y se ofrecen los
    // que quedan. La llave de seguridad no pasa por este chequeo.
    if (PLATFORM_METHODS.has(method)) {
      statusLine.textContent = "Verificando disponibilidad...";
      statusLine.className = "status-line text-xs";
      const available = await isPlatformAuthenticatorAvailable();
      if (!available) {
        dropMethodAndOfferRemaining(btn, "No se detectó un método de autenticación biométrica en este dispositivo.");
        return;
      }
    }

    statusLine.textContent = CONFIRM_TEXT[method] || "Confirmá en tu dispositivo...";
    statusLine.className = "status-line text-xs";

    const result = await window.registerPasskey(method);
    if (result.ok) {
      // Exito: el SO pudo haber resuelto con un metodo distinto al elegido
      // - eso es esperado (ver comentario arriba) y sigue contando como
      // registro valido, no como fallo.
      statusLine.textContent = "¡Passkey registrada! Recargando...";
      statusLine.className = "status-line text-xs success";
      setTimeout(() => window.location.reload(), 700);
      return;
    }

    // Fallback reactivo: recien con el intento fallido sabemos que ESE
    // metodo no funciono aca - se saca de la lista (no un error generico)
    // y se ofrecen los que quedan.
    dropMethodAndOfferRemaining(btn, `No pudimos usar ${METHOD_LABELS[method]} en este dispositivo.`);
  });
})();
