document.addEventListener("DOMContentLoaded", function () {
    var uploadButton = document.getElementById("upload-button");
    var fileInput = document.getElementById("file-input");
    var imagePreview = document.getElementById("image-preview");
    var resultDiv = document.getElementById("result");

    uploadButton.addEventListener("click", function () {
        fileInput.click();
    });

    fileInput.addEventListener("change", function () {
        var file = fileInput.files[0];
        var reader = new FileReader();

        reader.onload = function (e) {
            imagePreview.src = e.target.result;
        };

        reader.readAsDataURL(file);
    });

    var classifyButton = document.getElementById("classify-button");
    classifyButton.addEventListener("click", function () {
        var formData = new FormData();
        formData.append("image", fileInput.files[0]);

        fetch("/classify", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                resultDiv.innerText = "Prediction: " + data.prediction;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    });
});
