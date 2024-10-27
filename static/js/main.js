// static/js/main.js
function handleLike(postId) {
    fetch('/forum/like_post/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken 
        },
        body: JSON.stringify({ post_id: postId })
    })
    .then(response => response.json())
    .then(data => {
        const likeButton = document.getElementById(`like-btn-${postId}`);
        if (data.success) {
            // Toggle the 'liked' class based on the 'liked' status from the server
            if (data.liked) {
                likeButton.classList.add('liked');
            } else {
                likeButton.classList.remove('liked');
            }
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
    if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
        commentsSection.style.display = 'block';
    } else {
        commentsSection.style.display = 'none';
    }
}

function postComment(event, postId) {
    event.preventDefault();
    const commentInput = event.target.querySelector('textarea');
    const commentText = commentInput.value;

    fetch('/forum/comment_post/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
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

    fetch('/forum/report_post/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
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

document.addEventListener('DOMContentLoaded', function() {
    const restaurantInput = document.getElementById('restaurant-input');
    const restaurantList = document.getElementById('restaurant-list');
    const restaurantIdInput = document.getElementById('restaurant-id');

    restaurantInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length > 0) {
            fetch('/forum/search_restaurants/?q=' + encodeURIComponent(query))
            .then(response => response.json())
                .then(data => {
                    // Clear previous results
                    restaurantList.innerHTML = '';
                    data.restaurants.forEach(function(restaurant) {
                        const item = document.createElement('div');
                        item.classList.add('autocomplete-item');
                        item.textContent = restaurant.nama;
                        item.dataset.id = restaurant.id;
                        restaurantList.appendChild(item);
                    });
                })
                .catch(error => {
                    console.error('Error fetching restaurants:', error);
                });
        } else {
            restaurantList.innerHTML = '';
        }
    });

    // Click event for selecting a restaurant
    restaurantList.addEventListener('click', function(e) {
        if (e.target && e.target.matches('.autocomplete-item')) {
            restaurantInput.value = e.target.textContent;
            restaurantIdInput.value = e.target.dataset.id;
            // Clear the list
            restaurantList.innerHTML = '';
        }
    });

    // Close the autocomplete list if clicked outside
    document.addEventListener('click', function(e) {
        if (e.target !== restaurantInput && e.target.parentNode !== restaurantList) {
            restaurantList.innerHTML = '';
        }
    });
});