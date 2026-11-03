
const API = "/students";

// GET - Load all students
async function loadStudents() {

    const response = await fetch(API);
    const students = await response.json();

    const table = document.getElementById("studentTable");

    table.innerHTML = "";

    students.forEach(student => {

        table.innerHTML += `
            <tr>
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.email}</td>
                <td>${student.marks}</td>
                <td>
                    <button onclick="editStudent(${student.id})">
                        Edit
                    </button>

                    <button onclick="deleteStudent(${student.id})">
                        Delete
                    </button>
                </td>
            </tr>
        `;
    });
}


// POST / PUT - Add or update student
async function saveStudent() {

    const id = document.getElementById("student_id").value;

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        marks: Number(document.getElementById("marks").value)
    };

    const method = id ? "PUT" : "POST";

    const url = id ? `${API}/${id}` : API;

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        alert(JSON.stringify(result.detail || result));
        return;
    }

    alert(result.message);

    clearForm();
    loadStudents();
}


// GET - Load one student for editing
async function editStudent(id) {

    const response = await fetch(`${API}/${id}`);

    const student = await response.json();

    document.getElementById("student_id").value = student.id;
    document.getElementById("name").value = student.name;
    document.getElementById("email").value = student.email;
    document.getElementById("marks").value = student.marks;
}


// DELETE - Remove student
async function deleteStudent(id) {

    if (!confirm("Are you sure you want to delete?")) {
        return;
    }

    const response = await fetch(`${API}/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    if (!response.ok) {
        alert(result.detail);
        return;
    }

    alert(result.message);
    loadStudents();
}


// Clear form
function clearForm() {

    document.getElementById("student_id").value = "";
    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("marks").value = "";
}


// Load records when page opens
loadStudents();
