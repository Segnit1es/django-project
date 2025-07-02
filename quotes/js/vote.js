export function sendVote(pk, csrftoken, action) {
  fetch(`/vote/${pk}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({ action: action })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('likes-count').textContent = data.likes;
    document.getElementById('dislikes-count').textContent = data.dislikes;
  })
  .catch(() => alert('Ошибка голосования'));
}