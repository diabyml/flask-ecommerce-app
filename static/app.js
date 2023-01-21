const adminBtnDeletes = document.querySelectorAll(".admin-btn-delete");

let productToDeleteId = null;
// Admin delete a product from admin dashboard
adminBtnDeletes.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    // show modal
    modalContainer = document.querySelector(".modal-container");
    modalContainer.classList.remove("hidden");
    productToDeleteId = btn.getAttribute("data-id");
  });
});

// MODAL ACTIONS
// cancel delete product
const closeDeleteModal = () => {
  // console.log("closing modal");
  const container = document.querySelector(".modal-container");
  container.classList.add("hidden");
};
// cancel modal
document
  .querySelector(".admin-cancel-delete-product")
  .addEventListener("click", () => {
    // console.log("cancel modal");
    closeDeleteModal();
  });

// close modal
document.querySelector(".admin-close-modal").addEventListener("click", () => {
  // console.log("close modal");
  closeDeleteModal();
});

// confirm product deletion
document
  .querySelector(".admin-btn-delete-product")
  .addEventListener("click", () => {
    if (productToDeleteId) {
      // make an api call to flask backend for deleting product
      console.log("deleting...");
      fetch(`${window.origin}/admin/dashboard/delete`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ product_id: productToDeleteId }),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then(function (response) {
          // console.log(response);
          if (response.status !== 200) {
            // console.log(
            //   `Looks like there was a problem. Status code: ${response.status}`
            // );
            productToDeleteId = null;
            closeDeleteModal();
            return;
          }
          response.json().then(function (data) {
            // console.log(data);
            productToDeleteId = null;
            location.reload();
            closeDeleteModal();
          });
        })
        .catch(function (error) {
          console.log("Fetch error: " + error);
          productToDeleteId = null;
          closeDeleteModal();
        });
    }

    // reset productToDeleteId to null after deletion
  });
