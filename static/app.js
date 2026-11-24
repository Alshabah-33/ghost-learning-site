
async function submitLogin(formId, endpoint, statusId) {
  const form = document.getElementById(formId);
  const status = document.getElementById(statusId);
  if (!form || !status) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const button = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);
    const payload = {
      username: String(formData.get("username") || "").trim(),
      password: String(formData.get("password") || "")
    };

    status.textContent = "جارٍ الاتصال...";
    if (button) button.disabled = true;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const result = await response.json().catch(() => ({}));
      status.textContent = result.message || (
        response.ok ? "تم الاتصال بنجاح." : "تعذر الاتصال، راجع البيانات وحاول مرة أخرى."
      );
    } catch (error) {
      status.textContent = "تعذر الوصول إلى الخادم. حاول مرة أخرى.";
    } finally {
      if (button) button.disabled = false;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  submitLogin("qureo-form", "/api/login", "qureo-status");
  submitLogin("spx-form", "/api/spx-login", "spx-status");
});
