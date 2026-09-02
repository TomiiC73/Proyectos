// Registro de cuenta nueva (nombre, apellido, email, contraseña). El
// usuario queda logueado directo (todavia sin passkey), igual que el
// camino de "primer ingreso" del login.
(function () {
  const form = document.getElementById("signup-form");
  const errorBox = document.getElementById("signup-error");
  const submitBtn = document.getElementById("signup-submit");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorBox.classList.remove("visible");
    submitBtn.disabled = true;
    submitBtn.textContent = "Creando cuenta...";

    const first_name = document.getElementById("first_name").value.trim();
    const last_name = document.getElementById("last_name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ first_name, last_name, email, password }),
      });
      const data = await response.json();

      if (!data.ok) {
        errorBox.textContent = data.error || "No se pudo crear la cuenta.";
        errorBox.classList.add("visible");
        return;
      }

      window.location.href = data.next;
    } catch (err) {
      errorBox.textContent = "Error de conexión con el servidor.";
      errorBox.classList.add("visible");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Crear cuenta";
    }
  });
})();
