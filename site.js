/* Green Lotus Spices — shared site behaviour */

/* --------------------------------------------------------------------------
   FORM ENDPOINT
   --------------------------------------------------------------------------
   The old forms used action="mailto:..." which does not reliably work: most
   browsers either ignore it or dump a garbled message into a desktop mail
   client, and it fails outright on most phones. Enquiries were being lost.

   To fix it, create a free form endpoint and paste the URL below:
     - Formspree  https://formspree.io      -> "https://formspree.io/f/xxxxxxxx"
     - Web3Forms  https://web3forms.com     -> "https://api.web3forms.com/submit"
     - Vercel     an /api/enquiry function on this same project

   While this is left empty the forms fall back to opening the visitor's mail
   client, exactly as before, so nothing breaks in the meantime.
   -------------------------------------------------------------------------- */
window.GL_FORM_ENDPOINT = "";

window.GL_FALLBACK_EMAIL = "sales@greenlotusvn.com";

(function () {
  "use strict";

  /* Logo (stored as a data URI in img/logo-data.js) */
  function paintLogos() {
    if (!window.GL_LOGO) return;
    document.querySelectorAll(".js-logo").forEach(function (i) {
      i.src = window.GL_LOGO;
    });
  }

  /* Mobile navigation */
  function wireNav() {
    var toggle = document.querySelector(".mobile-toggle");
    var nav = document.querySelector(".main-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", nav.classList.contains("open"));
    });
  }

  /* Enquiry forms */
  function wireForms() {
    document.querySelectorAll("form.enquiry, form.newsletter-form").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        var endpoint = window.GL_FORM_ENDPOINT;

        if (!endpoint) {
          /* No endpoint configured yet — fall back to a mail client. */
          event.preventDefault();
          var data = new FormData(form);
          var lines = [];
          data.forEach(function (value, key) {
            if (value) lines.push(key + ": " + value);
          });
          var subject = form.getAttribute("data-subject") || "Website enquiry";
          window.location.href =
            "mailto:" + window.GL_FALLBACK_EMAIL +
            "?subject=" + encodeURIComponent(subject) +
            "&body=" + encodeURIComponent(lines.join("\n"));
          return;
        }

        event.preventDefault();
        var status = form.querySelector(".form-status");
        var button = form.querySelector("button[type=submit]");
        if (button) {
          button.disabled = true;
          button.dataset.label = button.textContent;
          button.textContent = "Sending…";
        }

        fetch(endpoint, {
          method: "POST",
          body: new FormData(form),
          headers: { Accept: "application/json" }
        })
          .then(function (response) {
            if (!response.ok) throw new Error("Request failed");
            form.reset();
            if (status) {
              status.className = "form-status ok";
              status.textContent =
                "Thank you — your enquiry has reached our sales team. We reply to quote requests within one business day.";
            }
          })
          .catch(function () {
            if (status) {
              status.className = "form-status err";
              status.textContent =
                "Something went wrong sending the form. Please email " +
                window.GL_FALLBACK_EMAIL + " and we will come straight back to you.";
            }
          })
          .finally(function () {
            if (button) {
              button.disabled = false;
              button.textContent = button.dataset.label || "Submit";
            }
          });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      paintLogos();
      wireNav();
      wireForms();
    });
  } else {
    paintLogos();
    wireNav();
    wireForms();
  }
})();
