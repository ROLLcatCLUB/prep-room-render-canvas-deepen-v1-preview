
      document.addEventListener("click", function (event) {
        if (event.target.closest("[data-r6p-modal-close]") || event.target.classList.contains("r6p-modal-backdrop")) {
          const modal = document.querySelector(".r6p-modal-backdrop");
          if (modal) {
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");
          }
        }
      });
    