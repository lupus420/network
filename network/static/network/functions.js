
async function getPages(nr_pages) {
    try{
        deletePostOnPage();
        const current_page_posts = document.createElement('div');
        current_page_posts.className = 'post_container container show_post';
        document.querySelector('#all-posts').append(current_page_posts);
        response = await fetch(`/get_posts?page=${nr_pages}`);
        posts = await response.json();
        console.log(posts);
        const logged_user_info = await getLoggedInUserInfo();
        posts.forEach(post => {
            const newPost = makeDivPost(post, logged_user_info);
            current_page_posts.append(newPost);
        });
        document.querySelector('.show_post').style.animationPlayState = 'running';
    }
    catch(error){
        console.error('Error:', error);
    }
}


function makeDivPost(post, logged_user_info){
    const template = document.querySelector('#post-template');
    const newPost = template.content.cloneNode(true);
    newPost.querySelector('.post').id = `post_${post.id}`;
    newPost.querySelector('.post_body').innerHTML = post.body;
    newPost.querySelector('.post_author').textContent = `${post.author.username}`;
    newPost.querySelector('.post_author').href = `profile/${post.author.username}`;
    newPost.querySelector('.post_date').innerHTML = `${post.date_posted}`;
    makeLikeButton(post.likes, newPost.querySelector('.like'), post.id, logged_user_info);
    newPost.querySelector('.like_count').innerHTML = post.likes_nr;
    return newPost;
}


async function makeLikeButton(post_likes_by_id, like_div, post_id, logged_user_info) {
    const like_button = like_div.querySelector('.like_button');
    const user_id = logged_user_info['id'];
    if (user_id && post_likes_by_id.includes(user_id)) {
        like_button.classList.add('bi','bi-heart-fill');
    }
    else {
        like_button.classList.add('bi','bi-heart');
    }

    like_counter = like_div.querySelector('.like_count');
    // Make functionality just if user is logged in
    if (user_id) {
        makeLikeButtonFunctionality(like_button, like_counter);
        //backend like unlike
        like_button.addEventListener('click', () => {
            like_unlikePost(user_id, post_id);
        });
    }
}


function makeLikeButtonFunctionality(like_button, like_counter) {
    like_button.addEventListener('click', () => {
        if (like_button.classList.contains('bi-heart-fill')) {
            like_button.classList.remove('bi-heart-fill');
            like_button.classList.add('bi-heart');
            like_counter.innerHTML = parseInt(like_counter.innerHTML) - 1;
        }
        else {
            like_button.classList.remove('bi-heart');
            like_button.classList.add('bi-heart-fill');
            like_button.style.animationPlayState = 'running';
            like_counter.innerHTML = parseInt(like_counter.innerHTML) + 1;
        }
    });
}


function makePagesNavigationBar() {
    nav_bar = document.querySelector('.pagination');
    fetch(`/pages_count`)
    .then(response => response.json())
    .then(nr_pages => {
        // create page navigation
        for (let i = 1; i <= nr_pages["pages_counter"] ; i++) {
            const list_item = document.createElement('li');
            list_item.className = 'page-item';
            nav_bar.append(list_item);
            const pageNumber = document.createElement('a');
            pageNumber.className = 'page-link';
            pageNumber.innerHTML = i;
            pageNumber.href =`#page${i}`;
            pageNumber.addEventListener('click', () => {
                getPages(i);
            });
            list_item.append(pageNumber);
        }
    });
}


function deletePostOnPage() {
    document.querySelectorAll('.post_container').forEach(posts_container => {
    if (posts_container) {
        posts_container.classList.remove('show_post');
        posts_container.classList.add('hide_post');
        posts_container.style.animationPlayState = 'running';
        posts_container.addEventListener('animationend', () => {
            posts_container.remove();
        })
    }
    });
}


async function like_unlikePost(user_id, post_id) {
    // if user.is_authenticated the csrf token is in the page
    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrf_token == null) {
        console.error("CSRF token not found - user not logged in.");
        return
    }
    response = await fetch(`/like_post`, {
        method: 'POST',
        body: JSON.stringify({
            "post_id": post_id,
            "user_id": user_id
        }),
        headers: {
            "X-CSRFToken": csrf_token.value
        }
    })
    result = await response.json();
    console.log(result);
}


async function getLoggedInUserInfo(){
    /* Get info of the logged in user */
    try{
        const response = await fetch(`/get_logged_user`)
        const user = await response.json();
        console.log("logged in user", user);
        if(user){
            return user;
        }
        return null;
    }
    catch(error){
        console.error('Error:', error);
        return null;
    }
}

function makeNewPostFunctionality(){
    document.querySelector('#new-post-button').addEventListener('click',() => {
        const text_field = document.querySelector('#new-post-text');
        text = text_field.value;
        if (text){
            csrf_token = document.querySelector('[name=csrfmiddlewaretoken]');
            try{
                fetch('/make_post', {
                    method: "POST",
                    body: JSON.stringify({
                        "post_content": text
                    }),
                    headers: {
                        "X-CSRFToken": csrf_token.value
                    }
                })
                .then(response => response.json())
                .then(post_info => {
                    console.log(post_info);
                    addNewPost(post_info);
                })
            }
            catch(error){
                console.error("Error:", error);
            }
        }
        text_field.value = '';
    });
}


function addNewPost(post_info){
    const newPostTemplate = makeDivPost(post_info, post_info.author);
    const tempDiv = document.createElement('div');
    tempDiv.append(newPostTemplate);
    const newPost = tempDiv.firstElementChild;
    newPost.classList.add('new_post');
    postContainer = document.querySelector('.post_container');
    postContainer.prepend(newPost);
}