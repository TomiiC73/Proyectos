// Segundo factor: confirmar con la passkey del usuario ya identificado por
// contraseña (ver app.py /api/login y /webauthn).
//
// Un solo boton dispara navigator.credentials.get() con allow_credentials
// ya acotado a las credenciales de ESTE usuario (ver webauthn_auth.py): el
// propio navegador resuelve solo, sin que la app tenga que preguntar nada,
// que autenticador sirve - si el usuario registro una YubiKey, le va a
// pedir la YubiKey; si registro Windows Hello, le va a pedir Windows Hello.
// WebAuthn no permite forzar ese metodo desde JS en el paso de login
// (a diferencia del registro, get() no acepta authenticatorAttachment), asi
// que no hace falta -ni se puede- tener un boton distinto por metodo aca.
(function () {
  const statusLine = document.getElementById("webauthn-status");
  const buttons = [
    document.getElementById("webauthn-confirm-btn"),
  ];

  async function confirmIdentity() {
    buttons.forEach((b) => (b.disabled = true));
    statusLine.textContent = "Verificando identidad...";
    statusLine.className = "status-line";

    const result = await window.loginWithPasskey();
    if (result.ok) {
      statusLine.textContent = "¡Listo! Entrando...";
      statusLine.className = "status-line success";
      window.location.href = result.next;
    } else {
      statusLine.textContent = "No se pudo confirmar: " + result.error;
      statusLine.className = "status-line error";
      buttons.forEach((b) => (b.disabled = false));
    }
  }

  buttons.forEach((b) => b.addEventListener("click", confirmIdentity));
})();
