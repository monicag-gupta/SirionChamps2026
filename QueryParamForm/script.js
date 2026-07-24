const form = document.getElementById("employeeForm");
const tableBody = document.querySelector("#employeeTable tbody");

// Function to add a row to the table
function addEmployee(empId, empName) {
    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${empId}</td>
        <td>${empName}</td>
    `;

    tableBody.appendChild(row);
}

// Submit button functionality
form.addEventListener("submit", function (event) {
    event.preventDefault();

    const empId = document.getElementById("empId").value;
    const empName = document.getElementById("empName").value;

    addEmployee(empId, empName);

    form.reset();
});

// Read query parameters when the page loads
const params = new URLSearchParams(window.location.search);

const employeeId = params.get("employeeId");
const employeeName = params.get("employeeName");

// If both query parameters exist, add them to the table
if (employeeId && employeeName) {
    addEmployee(employeeId, employeeName);
}