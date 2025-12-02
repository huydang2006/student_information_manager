document.addEventListener('DOMContentLoaded', function () {
  // Khởi tạo modal (an toàn nếu phần tử không tồn tại)
  const modalMoreEl = document.getElementById('modalMore');
  const modalMore = modalMoreEl ? new bootstrap.Modal(modalMoreEl) : null;

  const modalUpdateEl = document.getElementById('modalUpdate');
  const modalUpdate = modalUpdateEl ? new bootstrap.Modal(modalUpdateEl, {backdrop: 'static', keyboard: false}) : null;

  // Lấy footer modal1 để thêm nút Save
  const modalMoreFooter = modalMoreEl ? modalMoreEl.querySelector('.modal-footer') : null;

  // Bấm More trong table / or show.bs.modal
  function populateModalFromSource(source) {
    const id = source.getAttribute('data-id');
    const name = source.getAttribute('data-name');
    const email = source.getAttribute('data-email');
    const birth = source.getAttribute('data-birth');
    const phone = source.getAttribute('data-phone');
    const address = source.getAttribute('data-address');
    const program = source.getAttribute('data-program');
    const enrollmentYear = source.getAttribute('data-enrollment-year');
    const programName = source.getAttribute('data-program-name');

    const setText = (idEl, value) => {
      const el = document.getElementById(idEl);
      if (el) el.textContent = value || '';
    };

    setText('modal-id', id);
    setText('modal-name', name);
    setText('modal-email', email);
    setText('modal-birth', birth);
    setText('modal-phone', phone);
    setText('modal-address', address);
    setText('data-program', program);
    setText('data-enrollment-year', enrollmentYear);
    setText('data-program-name', programName);
  }

  if (modalMoreEl) {
    modalMoreEl.addEventListener('show.bs.modal', function (event) {
      // event.relatedTarget is the element that triggered the modal
      const button = event.relatedTarget;
      if (button) populateModalFromSource(button);
    });
  }

  document.querySelectorAll('.btn-more').forEach(button => {
    button.addEventListener('click', function () {
      populateModalFromSource(this);
      if (modalMore) modalMore.show();
    });
  });

  // Bấm Update → modal2
  const btnUpdate = document.getElementById('btnUpdate');
  if (btnUpdate) {
    btnUpdate.addEventListener('click', function () {
      const getTxt = id => document.getElementById(id) ? document.getElementById(id).textContent : '';

      const inputs = [
        ['update-id', 'modal-id'],
        ['update-name', 'modal-name'],
        ['update-email', 'modal-email'],
        ['update-birth', 'modal-birth'],
        ['update-phone', 'modal-phone'],
        ['update-address', 'modal-address'],
        ['update-program', 'data-program'],
        ['update-enrollment-year', 'data-enrollment-year'],
        ['update-program-name', 'data-program-name'],
      ];

      inputs.forEach(([inputId, srcId]) => {
        const inputEl = document.getElementById(inputId);
        if (inputEl) inputEl.value = getTxt(srcId);
      });

      if (modalMore) modalMore.hide();
      if (modalUpdate) modalUpdate.show();
    });
  }

  // Bấm Back → quay lại modal1
  const btnBack = document.getElementById('btnBack');
  if (btnBack) {
    btnBack.addEventListener('click', function () {
      if (modalUpdate) modalUpdate.hide();
      if (modalMore) modalMore.show(); // dữ liệu modal1 giữ nguyên
    });
  }

  // Bấm Save Changes → cập nhật modal1
  const btnSave = document.getElementById('btnSave');
  if (btnSave) {
    btnSave.addEventListener('click', function () {
      const vals = {
        name: document.getElementById('update-name') ? document.getElementById('update-name').value : '',
        email: document.getElementById('update-email') ? document.getElementById('update-email').value : '',
        birth: document.getElementById('update-birth') ? document.getElementById('update-birth').value : '',
        phone: document.getElementById('update-phone') ? document.getElementById('update-phone').value : '',
        address: document.getElementById('update-address') ? document.getElementById('update-address').value : '',
        enrollmentYear: document.getElementById('update-enrollment-year') ? document.getElementById('update-enrollment-year').value : '',
      };

      // Build payload and persist to server
      const id = (document.getElementById('update-id') && document.getElementById('update-id').value) ? document.getElementById('update-id').value : (document.getElementById('modal-id') ? document.getElementById('modal-id').textContent : null);

      const payload = {
        full_name: vals.name,
        date_of_birth: vals.birth,
        email: vals.email,
        phone_number: vals.phone,
        address: vals.address,
        program_id: vals.program,
        enrollment_year: vals.enrollmentYear
      };

      if (!id) return alert('Missing student id');

      fetch(`/student_management/update/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(res => res.json())
        .then(data => {
          if (data && data.success) {
            // Update UI and close
            if (document.getElementById('modal-name')) document.getElementById('modal-name').textContent = vals.name;
            if (document.getElementById('modal-email')) document.getElementById('modal-email').textContent = vals.email;
            if (document.getElementById('modal-birth')) document.getElementById('modal-birth').textContent = vals.birth;
            if (document.getElementById('modal-phone')) document.getElementById('modal-phone').textContent = vals.phone;
            if (document.getElementById('modal-address')) document.getElementById('modal-address').textContent = vals.address;
            if (document.getElementById('data-enrollment-year')) document.getElementById('data-enrollment-year').textContent = vals.enrollmentYear;

            if (modalUpdate) modalUpdate.hide();
            if (modalMore) modalMore.show();

            // Optionally refresh the page so table shows updated values
            alert(data.message);
            window.location.reload();
          } else {
            alert(data && data.message ? data.message : 'Failed to update student');
          }
        })
        .catch(err => {
          console.error('Update failed', err);
          alert('Failed to update student');
        });
    });
  }

  // Modal confirm
  const modalDeleteEl = document.getElementById('modalDeleteConfirm');
  const modalDelete = modalDeleteEl ? new bootstrap.Modal(modalDeleteEl) : null;

  // Khi bấm Delete trong modal More
  const btnDelete = document.getElementById('btnDelete');
  if (btnDelete) {
    btnDelete.addEventListener('click', function () {
      if (modalMore) modalMore.hide();
      if (modalDelete) modalDelete.show();
    });
  }

  // Khi bấm Delete Confirm
  const btnDeleteConfirm = document.getElementById('btnDeleteConfirm');
  if (btnDeleteConfirm) {
    btnDeleteConfirm.addEventListener('click', function () {
      const id = document.getElementById('modal-id') ? document.getElementById('modal-id').textContent : null;

      if (!id) return alert('Missing student id');

      fetch(`/student_management/delete/${id}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
          if (data && data.success) {
            // Xoá thành công → reload trang
            alert(data.message);
            window.location.reload();
          } else {
            alert(data && data.message ? data.message : 'Failed to delete student');
          }
        })
        .catch(err => {
          console.error('Delete failed', err);
          alert('Failed to delete student');
        });
    });
  }
});
