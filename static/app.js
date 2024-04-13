const drop_zone = document.getElementById("drop-zone");
const browse_file_button = document.getElementById("browse_file_btn");
const upload_file = document.getElementById("file_input");
const error_block = document.getElementById("error");
const error_text = document.querySelector(".error_text");
const close_error_button = document.getElementById("close_error");
const drag_and_drop_area = document.querySelector(".drag-n-drop-area");
const prediction_block = document.querySelector(".prediction_block");
const image = document.getElementById("prediction_image");
const prediction_button = document.getElementById("predict_button");
const prediction_button_container =
  document.getElementById("prediction_buttons");

const prediction_result_container =
  document.getElementById("prediction_results");
const result_text = document.getElementById("result_text");

drop_zone.addEventListener("dragover", (e) => {
  e.preventDefault();

  drop_zone.classList.add("drag-over");
});
drop_zone.addEventListener("dragleave", (e) => {
  e.preventDefault();

  drop_zone.classList.remove("drag-over");
});
drop_zone.addEventListener("drop", (e) => {
  e.preventDefault();
  drop_zone.classList.remove("drag-over");
  let file = e.dataTransfer.files;
  handleFileDrop(file);
});

browse_file_button.addEventListener("click", (e) => {
  e.preventDefault();
  upload_file.click();
});

upload_file.addEventListener("change", (e) => {
  handleFileDrop(e.target.files);
});

close_error_button.addEventListener("click", (e) => {
  e.preventDefault();
  error_text.innerHTML = "";
  error_block.classList.add("hidden");
});

function handleFileDrop(file) {
  file_error = checkFile(file[0]);
  if (file_error.length > 0) {
    error_block.classList.remove("hidden");
    error_text.innerHTML = file_error;
  } else {
    handle_upload_file("/upload", file[0]);
  }
}

function checkFile(file) {
  if (
    file.type !== "image/jpg" &&
    file.type !== "image/png" &&
    file.type !== "image/jpeg"
  ) {
    return "File uploaded is not a valid image type";
  }
  if (file.size > 20000) {
    return "Image file must be less than 20kb size";
  }
  return "";
}

async function handle_upload_file(url, file) {
  const formData = new FormData();
  formData.append("img_file", file);
  const requestOptions = {
    method: "POST",
    body: formData,
  };

  try {
    const result = await fetch("/upload", requestOptions);
    const data = await result.json();
    if (data.status === "success") {
      drag_and_drop_area.classList.add("hidden");
      prediction_block.classList.remove("hidden");
      image.src = data.message;
    }
    if (data.status === "error") {
      error_block.classList.remove("hidden");
      error_text.innerHTML = data.message;
    }
  } catch (e) {
    error_block.classList.remove("hidden");
    error_text.innerHTML = e.message;
  }
}

prediction_button.addEventListener("click", (e) => {
  handle_prediction();
});

async function handle_prediction() {
  try {
    const request = await fetch("/predict", { method: "POST" });
    const data = await request.json();
    if (data.status === "success") {
      prediction_button_container.classList.add("hidden");
      prediction_result_container.classList.remove("hidden");
      const spanElement = document.createElement("span");
      spanElement.classList.add("inter-font-medium");
      if (data.message === "Parasitized") {
        spanElement.classList.add("text-danger");
      } else {
        spanElement.classList.add("text-success");
      }
      spanElement.innerHTML = data.message;
      result_text.appendChild(spanElement);
    }
    if (data.status === "error") {
      error_block.classList.remove("hidden");
      error_text.innerHTML = data.message;
    }
  } catch (e) {
    error_block.classList.remove("hidden");
    error_text.innerHTML = e.message;
  }
}
