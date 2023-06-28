document.getElementById("cancel-button").addEventListener("click", deleteConfirmationClose)

function deleteConfirmationClose() {
  const dialog = document.getElementById("delete-confirmation")
  const deleteConfirmation = dialog.close();
}