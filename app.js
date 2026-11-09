// THE GOLDEN — Thiệp Mời Year End Party 2026
const $ = s => document.querySelector(s);

// Nút mở thiệp mời cuộn mượt mà
const openInviteBtn = $('#openInvite');
if (openInviteBtn) {
  openInviteBtn.onclick = () => {
    const target = $('#invitation');
    if (target) {
      target.scrollIntoView({
        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
      });
    }
  };
}

// Xử lý Popup thông báo cảm ơn
const thankYouModal = $('#thankYouModal');
const closeModalBtn = $('#closeModalBtn');
const confirmModalBtn = $('#confirmModalBtn');
const modalSummary = $('#modalSummary');

function showModal(data) {
  if (!thankYouModal) return;

  const isAttending = data.attend === 'yes';
  const modalTitle = $('#modalTitle');
  const highlightText = $('.highlight-text');
  const emailNotice = $('#emailNotice');
  const noticeEmail = $('#noticeEmail');
  const emailPreviewCard = $('#emailPreviewCard');
  const emailGuestName = $('#emailGuestName');

  if (isAttending) {
    if (modalTitle) modalTitle.textContent = 'Cảm ơn bạn đã tham gia';
    if (highlightText) highlightText.textContent = 'Cảm ơn bạn đã tham gia, mong bạn sẽ sớm có mặt trong buổi tiệc!';
    if (emailNotice && data.email) {
      emailNotice.classList.remove('hidden');
      if (noticeEmail) noticeEmail.textContent = data.email;
    }
    if (emailPreviewCard) {
      emailPreviewCard.classList.remove('hidden');
      if (emailGuestName) emailGuestName.textContent = data.name;
    }
  } else {
    if (modalTitle) modalTitle.textContent = 'Đã ghi nhận phản hồi';
    if (highlightText) highlightText.textContent = 'Cảm ơn bạn đã phản hồi. Ban tổ chức rất tiếc vì bạn chưa thể tham gia, chúc bạn luôn nhiều niềm vui và hẹn gặp bạn ở dịp tiếp theo!';
    if (emailNotice) emailNotice.classList.add('hidden');
    if (emailPreviewCard) emailPreviewCard.classList.add('hidden');
  }

  if (modalSummary && data) {
    modalSummary.innerHTML = `
      <div><strong>Khách mời:</strong> ${escapeHtml(data.name)}</div>
      <div><strong>Số điện thoại:</strong> ${escapeHtml(data.phone)}</div>
      ${data.email ? `<div><strong>Email:</strong> ${escapeHtml(data.email)}</div>` : ''}
      ${data.department ? `<div><strong>Phòng ban:</strong> ${escapeHtml(data.department)}</div>` : ''}
      <div><strong>Trạng thái:</strong> ${isAttending ? 'Xác nhận sẽ tham dự' : 'Rất tiếc chưa thể tham dự'}</div>
      ${data.note ? `<div><strong>Lời nhắn:</strong> ${escapeHtml(data.note)}</div>` : ''}
    `;
  }

  thankYouModal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function hideModal() {
  if (!thankYouModal) return;
  thankYouModal.classList.add('hidden');
  document.body.style.overflow = '';
}

if (closeModalBtn) closeModalBtn.onclick = hideModal;
if (confirmModalBtn) confirmModalBtn.onclick = hideModal;

if (thankYouModal) {
  thankYouModal.onclick = e => {
    if (e.target === thankYouModal) hideModal();
  };
}

window.addEventListener('keydown', e => {
  if (e.key === 'Escape' && thankYouModal && !thankYouModal.classList.contains('hidden')) {
    hideModal();
  }
});

// Xử lý nộp Form xác nhận tham dự
const rsvpForm = $('#rsvpForm');
if (rsvpForm) {
  rsvpForm.onsubmit = async e => {
    e.preventDefault();

    const name = $('#guestName').value.trim();
    const phone = $('#guestPhone').value.trim();
    const email = $('#guestEmail') ? $('#guestEmail').value.trim() : '';
    const department = $('#guestDept').value.trim();
    const attend = $('input[name="attend"]:checked')?.value || 'yes';
    const note = $('#guestNote').value.trim();

    if (!name) {
      $('#guestName').focus();
      return;
    }

    if (!phone) {
      $('#guestPhone').focus();
      return;
    }

    if (attend === 'yes' && !email) {
      $('#guestEmail')?.focus();
      return;
    }

    const formData = {
      name,
      phone,
      email,
      department,
      attend,
      note,
      timestamp: Date.now()
    };

    try {
      localStorage.setItem('golden-rsvp-submission', JSON.stringify(formData));
    } catch {}

    // Gửi yêu cầu tới server để xử lý gửi email và lưu trữ
    const submitBtn = $('#submitBtn');
    let originalText = '';
    if (submitBtn) {
      originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Đang xử lý...';
    }

    try {
      await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
    } catch (err) {
      console.log('API call:', err);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    }

    // Hiển thị thông báo popup theo yêu cầu
    showModal(formData);
  };

  // Khôi phục thông tin đã điền trước đó nếu có
  try {
    const saved = JSON.parse(localStorage.getItem('golden-rsvp-submission') || 'null');
    if (saved) {
      if (saved.name) $('#guestName').value = saved.name;
      if (saved.phone) $('#guestPhone').value = saved.phone;
      if (saved.email && $('#guestEmail')) $('#guestEmail').value = saved.email;
      if (saved.department) $('#guestDept').value = saved.department;
      if (saved.note) $('#guestNote').value = saved.note;
      const radio = $(`input[name="attend"][value="${saved.attend}"]`);
      if (radio) radio.checked = true;
    }
  } catch {}
}

// Cập nhật trạng thái nút bấm linh hoạt theo lựa chọn tham dự
const submitBtn = $('#submitBtn');
const attendRadios = document.querySelectorAll('input[name="attend"]');

function updateSubmitBtn() {
  const attend = $('input[name="attend"]:checked')?.value || 'yes';
  if (!submitBtn) return;

  if (attend === 'no') {
    submitBtn.innerHTML = 'Gửi phản hồi <span>&nearr;</span>';
    submitBtn.classList.add('btn-decline');
  } else {
    submitBtn.innerHTML = 'Gửi xác nhận tham dự <span>&nearr;</span>';
    submitBtn.classList.remove('btn-decline');
  }
}

attendRadios.forEach(radio => {
  radio.addEventListener('change', updateSubmitBtn);
});

// Khởi chạy cập nhật trạng thái nút bấm ban đầu
updateSubmitBtn();

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[m]));
}

