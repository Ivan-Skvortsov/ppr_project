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

const popoverSelectSchedules = (facilityId) => {
  let checkboxes = document.querySelectorAll(
    `input[data-popover="select-${facilityId}"]`
  );
  checkboxes.forEach((checkbox) => (checkbox.checked = !checkbox.checked));
};

const popoverMarkJournalsFilled = async (facilityId, journalType) => {
  let checkboxes = document.querySelectorAll(
    `input[data-popover="${journalType}-${facilityId}"]`
  );
  for (const checkbox of checkboxes) {
    checkbox.checked = !checkbox.checked;
    await markJournalCheckbox(checkbox);
  }
};
