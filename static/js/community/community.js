function voteCommunity(communityId) {

    fetch(voteCommunityUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "communityId": communityId })
    })
    .then(response => {
        // ✅ 401 Unauthorized 응답이면 JSON이 아니라 로그인 페이지로 이동
        if (response.status === 401) {
            return response.json().then(data => {
                alert(data.message);
                window.location.href = data.redirect;  // ✅ 로그인 페이지로 이동
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("✅ " + data.message);
            location.reload();
            // ✅ 투표 수 UI 업데이트
            let voteButton = document.querySelector(`button[onclick="voteCommunity('${communityId}')"]`);
            if (voteButton) {
                voteButton.innerHTML = `🗳️ +${data.vote_count}`;
            }
        } else {
            alert("✖️ " + data.message);
        }
    })
    .catch(error => console.error("❌ 투표 오류:", error));
}

function getCSRFToken() {
    let csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfTokenElement) {
        return csrfTokenElement.value;
    } else {
        console.error("❌ CSRF 토큰을 찾을 수 없습니다.");
        return "";
    }
}
