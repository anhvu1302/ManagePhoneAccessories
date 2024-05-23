let searchForm = document.querySelector(".search-form");
let searchBox = document.getElementById("search-box");
let searchLabel = document.querySelector("label[for='search-box']");

document.querySelector("#search-btn").onclick = () => {
  searchForm.classList.toggle("active");

  if (searchForm.classList.contains("active")) {
    searchBox.focus();
  }
};

$("#user-btn").click(function () {
  var userBox = $("#user-box");
  var displayValue = userBox.css("display");

  if (displayValue === "none") {
    userBox.css("display", "unset");
  } else {
    userBox.css("display", "none");
  }
});
function cancelOrder(orderId, isPaid, isCancelled) {
  if (isPaid === "True") {
    Swal.fire({
      icon: "info",
      title: "Đơn hàng đã thanh toán không thể hủy.",
      showConfirmButton: false,
      timer: 3000,
    });
    return;
  }
  if (isCancelled === "True") {
    Swal.fire({
      icon: "info",
      title: "Đơn hàng này đã được hủy.",
      showConfirmButton: false,
      timer: 3000,
    });
    return;
  }
  Swal.fire({
    title: "Bạn có chắc chắn muốn hủy đơn hàng này không?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Có!",
    cancelButtonText: "Không",
  }).then((result) => {
    if (result.isConfirmed) {
      const csrftoken = getCookie("csrftoken");

      fetch(`/admin/order/cancel_order/${orderId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify({}),
      })
        .then((response) => {
          if (response.ok) {
            Swal.fire(
              "Đã hủy!",
              "Đơn hàng của bạn đã được hủy.",
              "success"
            ).then(() => {
              location.reload();
            });
          } else {
            Swal.fire("Lỗi!", "Không thể hủy đơn hàng.", "error");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          Swal.fire("Lỗi!", "Đã xảy ra lỗi khi hủy đơn hàng.", "error");
        });
    }
  });
}
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}