function handleLike(postId) {
    fetch(`/like_post/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ post_id: postId })
    })
    .then(response => response.json())
    .then(data => {
        const likeButton = document.querySelector(`#like-btn-${postId}`);
        if (data.success) {
            likeButton.classList.toggle('liked', data.liked);
        } else {
            alert(`Failed to like the post: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function toggleComments(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    commentsSection.style.display = commentsSection.style.display === 'none' ? 'block' : 'none';
}

function postComment(event, postId) {
    event.preventDefault();
    const commentInput = event.target.querySelector('textarea');
    const commentText = commentInput.value;

    fetch(`/post_comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ post_id: postId, comment: commentText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const commentsSection = document.querySelector(`#comments-${postId} .existing-comments`);
            const newComment = document.createElement('p');
            newComment.innerHTML = `<strong>${data.username}:</strong> ${data.comment}`;
            commentsSection.appendChild(newComment);
            commentInput.value = '';
        } else {
            alert(`Failed to post comment: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function handleShare(url) {
    navigator.clipboard.writeText(url)
    .then(() => {
        alert("Link copied to clipboard!");
    })
    .catch((err) => {
        console.error("Failed to copy: ", err);
        alert("Failed to copy the link.");
    });
}

function showReportModal(postId) {
    document.getElementById(`report-modal-${postId}`).style.display = 'flex';
}

function closeReportModal(postId) {
    document.getElementById(`report-modal-${postId}`).style.display = 'none';
}

function submitReport(postId) {
    const reason = document.getElementById(`report-reason-${postId}`).value;

    if (!reason) {
        alert("Silakan pilih alasan laporan.");
        return;
    }

    fetch('/report_post/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ post_id: postId, reason: reason })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Postingan telah dilaporkan.');
            closeReportModal(postId);
        } else {
            alert('Gagal melaporkan postingan: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Terjadi kesalahan saat mengirim laporan.');
    });
}
