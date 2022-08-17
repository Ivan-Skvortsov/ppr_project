// ----> select/deselect all checkboxes
function toggle(source) {
  var checkboxes = document.querySelectorAll('input[name="selected_schedule"]')
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i] != source) checkboxes[i].checked = source.checked
  }
}

// ----> get coockie for csrf token
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// ----> modal forms
function showModalForm() {
  fetch("http://127.0.0.1:8000/xlsx_report/", {
    method: "GET",
    credentials: "same-origin"
  })
    .then((response) => response.text())
    .then((html) => console.log(html))
}
