document.addEventListener("DOMContentLoaded", function () {
  const day1Select = document.getElementById("day1");
  const day2Select = document.getElementById("day2");
  const monthSelect = document.getElementById("month");
  const yearSelect = document.getElementById("year");
  const hiddenInput = document.getElementById("payment_date");

  if (!day1Select || !day2Select || !monthSelect || !yearSelect || !hiddenInput) {
    console.warn("Date picker elements not found.");
    return;
  }

  // Populate day columns
  for (let d = 1; d <= 31; d++) {
    const padded = String(d).padStart(2, '0');
    day1Select.innerHTML += `<option value="${padded}">${padded}</option>`;
    day2Select.innerHTML += `<option value="${padded}">${padded}</option>`;
  }

  // Populate months
  for (let m = 1; m <= 12; m++) {
    const padded = String(m).padStart(2, '0');
    monthSelect.innerHTML += `<option value="${padded}">${padded}</option>`;
  }

  // Populate years
  const currentYear = new Date().getFullYear();
  for (let y = currentYear - 50; y <= currentYear + 10; y++) {
    yearSelect.innerHTML += `<option value="${y}">${y}</option>`;
  }

  // Button actions
  window.clearDate = function () {
    day1Select.selectedIndex = 0;
    day2Select.selectedIndex = 0;
    monthSelect.selectedIndex = 0;
    yearSelect.selectedIndex = 0;
    hiddenInput.value = "";
  };

  window.cancelDate = function () {
    alert("تم الإلغاء");
  };

  window.setDate = function () {
    const day = day2Select.value;
    const month = monthSelect.value;
    const year = yearSelect.value;

    if (!day || !month || !year) {
      alert("يرجى اختيار اليوم والشهر والسنة");
      return;
    }

    const formattedDate = `${year}-${month}-${day}`; // Django expects YYYY-MM-DD
    hiddenInput.value = formattedDate;
    alert(`التاريخ المختار: ${formattedDate}`);
  };
    const modal = document.getElementById("addPaymentModal");
  modal.addEventListener("shown.bs.modal", function () {
    // Auto-select today's date
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();

    day2Select.value = day;
    monthSelect.value = month;
    yearSelect.value = year;
    hiddenInput.value = `${year}-${month}-${day}`;
});
});