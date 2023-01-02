const popoverTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="popover"]')
);
popoverTriggerList.map((popoverTriggerEl) => {
  const options = {
    html: true,
    sanitize: false,
    placement: "auto",
    title: "Для этого объекта:",
    trigger: "hover focus",
    content: document.querySelector(`#${popoverTriggerEl.id}-body`),
  };
  return new bootstrap.Popover(popoverTriggerEl, options);
});
