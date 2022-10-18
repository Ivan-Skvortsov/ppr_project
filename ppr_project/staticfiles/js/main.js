// select/deselect all checkboxes
function toggle(source) {
  var checkboxes = document.querySelectorAll('input[name="selected_schedule"]');
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i] != source) checkboxes[i].checked = source.checked;
  }
}

// get coockie for csrf token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

let emptyModalHTML = `
  <div class="modal-dialog">
    <div class="modal-content" id="modalWindowContent">
      <div class="modal-header">
        <h5 class="modal-title">Загрузка...</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="spinner-border text-secondary" role="status">
          <span class="visually-hidden">Загрузка...</span>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
      </div>
    </div>
  </div>
  `;

// show modal form
function showModalForm(url) {
  const modalWindowEl = document.querySelector("#modalWindow");
  const modalWindow = new bootstrap.Modal(modalWindowEl);
  modalWindowEl.innerHTML = emptyModalHTML;
  modalWindow.show();
  fetch(url)
    .then((response) => response.text())
    .then((html) => (modalWindowEl.innerHTML = html))
    .catch((error) => console.error("Error", error));
}

// submit form and download file
function submitModalForm(evnt, form) {
  const submitButton = document.querySelector("#submitAndDownload");
  submitButton.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Загрузка`;
  submitButton.disabled = true;
  evnt.preventDefault();
  const formData = new FormData(form);
  const url = form.getAttribute("action");
  const options = {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: formData,
  };
  fetch(url, options)
    .then((response) => {
      const contentType = response.headers.get("Content-Type");
      return contentType.includes("text/html")
        ? response.text()
        : response.blob();
    })
    .then((data) => {
      const modalWindowEl = document.querySelector("#modalWindow");
      const modalWindow = bootstrap.Modal.getInstance(modalWindowEl);
      if (typeof data === "string") {
        modalWindowEl.innerHTML = data;
      } else {
        const downloadFile = window.URL.createObjectURL(data);
        window.location.assign(downloadFile);
        modalWindow.hide();
      }
    })
    .catch((error) => console.error("Error", error));
}

// mark journal checked
function markJournalCheckbox(source) {
  const url = `/api/v1/schedules/${source.value}/`;
  let payload = {};
  payload[source.name] = source.checked;

  // replace checkbox with spinner
  const spinner = document.createElement("div");
  spinner.className = "spinner-border spinner-border-sm text-secondary";
  source.parentNode.replaceChild(spinner, source);

  fetch(url, {
    method: "PATCH",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      //replace spinner with checkbox
      spinner.parentNode.replaceChild(source, spinner);
      //row color when completed
      const sheduleRow = document.getElementById("sheduleRow" + source.value);
      if (
        data.result_journal_filled === true &&
        data.access_journal_filled === true &&
        data.date_completed !== null
      ) {
        sheduleRow.className =
          "row border-bottom my-auto py-1 bg-success bg-opacity-25";
      } else {
        sheduleRow.className = "row border-bottom my-auto py-1";
      }
    })
    .catch((error) => console.error("Error", error));
}
