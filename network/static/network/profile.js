document.addEventListener('DOMContentLoaded', () => {

    makeAllLikesDiv();
});

async function makeAllLikesDiv(){
    logged_user_info = await getLoggedInUserInfo();
    document.querySelectorAll('.like').forEach(async likeDiv => {
        post_id = likeDiv.dataset.post_id;
        response = await fetch(`/get_post?post_id=${post_id}`,{
            method: 'GET',
        })
        post_info = await response.json();
        makeLikeButton(post_info.likes, likeDiv, post_info.id, logged_user_info);
    })
}