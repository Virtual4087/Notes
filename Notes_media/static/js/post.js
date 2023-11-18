document.querySelectorAll(".date_posted").forEach(element => {
    const current = new Date();
    const post_date = new Date(element.innerText);
    let diff = (current - post_date)/1000;
    if (diff >= 60){ 
        diff /= 60;
        if(diff >= 60){
            diff /= 60;
            if(diff >= 24){
                diff /= 24;
                if(diff >= 7){
                    diff /= 7;
                    if(diff >= 4){
                        diff /= 4;
                        if (diff >= 12){
                            element.innerText = '{{opinion.date|date:"M, j"}}';
                        }
                        else{
                            element.innerText = `${Math.floor(diff)}mon ago`;
                        }
                    }
                    else{
                        element.innerText = `${Math.floor(diff)}w ago`;
                    }
                }
                else{
                    element.innerText = `${Math.floor(diff)}d ago`;  
                }
            }
            else{
                element.innerText = `${Math.floor(diff)}h ago`;
            }
        }
        else{
            element.innerText = `${Math.floor(diff)}m ago`;
        }
    }
    else{
        element.innerText = `${Math.floor(diff)}s ago`;
    }
})

const like_buttons = document.querySelectorAll(".like-unlike")
const delete_buttons = document.querySelectorAll("#delete_post")

like_buttons.forEach((like) =>{
    like.addEventListener("click", () => {
        const post = like.parentElement.parentElement.parentElement
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
        const post = button.parentElement.parentElement
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
                window.location.href = "/"
            }
        })
    })
})
