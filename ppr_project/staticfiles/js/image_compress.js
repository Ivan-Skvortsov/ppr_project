document.querySelector("#photo_approval").addEventListener("change", (e) => {
  const fileInputEl = e.target;
  const file = fileInputEl.files[0];
  if (!file) {
    return;
  }

  const spinner = document.createElement("div");
  spinner.className =
    "spinner-border spinner-border text-secondary text-center";
  fileInputEl.parentNode.innerHTML = spinner.outerHTML;
  new Compressor(file, {
    quality: 0.5,
    width: 1920,
    height: 1024,
    resize: "contain",
    success(result) {
      const formData = new FormData();
      formData.append("photo", result, result.name);
      postCompressedImage(formData);
    },
    error(err) {
      console.log(err.message);
    },
  });
});

function postCompressedImage(formData) {
  const url = document.querySelector("#photoUploadUrl").value;
  const options = {
    method: "PATCH",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: formData,
  };

  fetch(url, options)
    .then((response) => document.location.reload(true))
    .catch((error) => console.error(error));
}
