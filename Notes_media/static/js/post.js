const like_buttons = document.querySelectorAll(".like-unlike")
const delete_buttons = document.querySelectorAll("#delete_post")

like_buttons.forEach((like) =>{
    like.addEventListener("click", () => {
        console.log(post)
        const post = like.parentElement.parentElement.parentElement
        console.log(post)
        const like_count = post.querySelector("#like-count")
        fetch(`/post/${post.id}`, {
            method : "POST",
            headers : {
                "Source" : "like_unlike",
                "Content-Type" : "application/json",
                "X-CSRFToken" : post.dataset.csrf
            },
            body : JSON.stringify({
                perform : like.id
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success == true){
                if (like.id == "like"){
                    like.id = "unlike"
                    like.classList.remove("fa-regular")
                    like.classList.add("fa-solid")
                    like_count.innerText = parseInt(like_count.innerText) + 1
                }
                else{
                    like.id = "like"
                    like.classList.remove("fa-solid")
                    like.classList.add("fa-regular")
                    like_count.innerText = parseInt(like_count.innerText) - 1
                }
            }
        })
    })
})

delete_buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const post = button.parentElement
        fetch(`/post/${post.id}`, {
                method : "DELETE",
                headers : {
                    "Source" : "delete_post",
                    "Content-Type" : "application/json",
                    "X-CSRFToken" : post.dataset.csrf
                },
                body : JSON.stringify({
                    perform : "delete"
                })
            })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success == true){
                post.style.display = "none";
            }
        })
    })
})
