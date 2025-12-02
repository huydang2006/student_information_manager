document.addEventListener("DOMContentLoaded", function () {

    // =======================
    //        EDIT MODAL
    // =======================
    const modalEdit = document.getElementById("modalEditInstructors");

    if (modalEdit) {
        modalEdit.addEventListener("show.bs.modal", function (event) {
            const button = event.relatedTarget;

            const id = button.getAttribute("data-id");
            const name = button.getAttribute("data-name");
            const email = button.getAttribute("data-email");
            const specialization = button.getAttribute("data-specialization");
            const officeLocation = button.getAttribute("data-office-location");

            modalEdit.querySelector("#update-id").value = id;
            modalEdit.querySelector("#update-name").value = name;
            modalEdit.querySelector("#update-email").value = email;
            modalEdit.querySelector("#update-specialization").value = specialization;
            modalEdit.querySelector("#update-office-location").value = officeLocation;

            // Gắn sự kiện save
            const saveBtn = modalEdit.querySelector("#btnSaveInstructor");
            saveBtn.onclick = () => {
                fetch(`/student_management/instructors/update/${id}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        full_name: modalEdit.querySelector("#update-name").value,
                        email: modalEdit.querySelector("#update-email").value,
                        specialization: modalEdit.querySelector("#update-specialization").value,
                        office_location: modalEdit.querySelector("#update-office-location").value,
                    })
                })
                    .then(res => res.json())
                    .then(data => {
                        alert(data.message);
                        window.location.reload();
                    });
            };
        });
    }

    // =======================
    //       DELETE MODAL
    // =======================
    const modalDelete = document.getElementById("modalDeleteInstructor");

    if (modalDelete) {
        modalDelete.addEventListener("show.bs.modal", function (event) {
            const button = event.relatedTarget;

            const id = button.getAttribute("data-id");

            const confirmBtn = modalDelete.querySelector("#btnConfirmDeleteInstructor");

            confirmBtn.onclick = () => {
                fetch(`/student_management/delete_instructor/${id}`, { method: "POST" })
                    .then(res => res.json())
                    .then(data => {
                        alert(data.message);
                        window.location.reload();
                    });
            };
        });
    }

});
