
document.addEventListener("DOMContentLoaded", () => {
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
})

const like_buttons = document.querySelectorAll(".like_unlike")
const delete_buttons = document.querySelectorAll("#delete_post")

like_buttons.forEach((like_button) =>{
    like_button.addEventListener("click", () => {
        console.log(like_button)
        const post = like_button.parentElement.parentElement.parentElement
        const like = like_button.querySelector('svg')
        const like_count = like_button.querySelector("#like_count")
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
                    like.classList.replace("icon-tabler-bulb", "icon-tabler-bulb-filled")
                    like.innerHTML = `<path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 11a1 1 0 0 1 .117 1.993l-.117 .007h-1a1 1 0 0 1 -.117 -1.993l.117 -.007h1z" stroke-width="0" fill="#e8c62c" /><path d="M12 2a1 1 0 0 1 .993 .883l.007 .117v1a1 1 0 0 1 -1.993 .117l-.007 -.117v-1a1 1 0 0 1 1 -1z" stroke-width="0" fill="#e8c62c" /><path d="M21 11a1 1 0 0 1 .117 1.993l-.117 .007h-1a1 1 0 0 1 -.117 -1.993l.117 -.007h1z" stroke-width="0" fill="#e8c62c" /><path d="M4.893 4.893a1 1 0 0 1 1.32 -.083l.094 .083l.7 .7a1 1 0 0 1 -1.32 1.497l-.094 -.083l-.7 -.7a1 1 0 0 1 0 -1.414z" stroke-width="0" fill="#e8c62c" /><path d="M17.693 4.893a1 1 0 0 1 1.497 1.32l-.083 .094l-.7 .7a1 1 0 0 1 -1.497 -1.32l.083 -.094l.7 -.7z" stroke-width="0" fill="#e8c62c" /><path d="M14 18a1 1 0 0 1 1 1a3 3 0 0 1 -6 0a1 1 0 0 1 .883 -.993l.117 -.007h4z" stroke-width="0" fill="#e8c62c" /><path d="M12 6a6 6 0 0 1 3.6 10.8a1 1 0 0 1 -.471 .192l-.129 .008h-6a1 1 0 0 1 -.6 -.2a6 6 0 0 1 3.6 -10.8z" stroke-width="0" fill="#e8c62c" />`
                    like_count.innerText = parseInt(like_count.innerText) + 1
                }
                else{
                    like.id = "like"
                    like.classList.replace("icon-tabler-bulb-filled", "icon-tabler-bulb")
                    like.innerHTML = `<path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 12h1m8 -9v1m8 8h1m-15.4 -6.4l.7 .7m12.1 -.7l-.7 .7" /><path d="M9 16a5 5 0 1 1 6 0a3.5 3.5 0 0 0 -1 3a2 2 0 0 1 -4 0a3.5 3.5 0 0 0 -1 -3" /><path d="M9.7 17l4.6 0" />`
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
                alert("Post deleted successfully!")
            }
        })
    })
})

function save_post(event){
    const save = event.currentTarget
    const post = save.parentElement.parentElement.parentElement
    const save_button = save.querySelector("svg")
    
    fetch(`/post/${post.id}`, {
        method : "POST",
        headers : {
            "Source" : "save_post",
            "Content-Type" : "application/json",
            "X-CSRFToken" : post.dataset.csrf
        },
        body : JSON.stringify({
            perform : save_button.id
        }) 
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success == true){
            if (save_button.id == "save"){
                save.querySelector('div').innerText = 'Saved'
                save_button.id = "unsave"
                save_button.setAttribute('fill', 'currentColor')
            }
            else{
                save.querySelector('div').innerText = 'Save'
                save_button.id = "save"
                save_button.setAttribute('fill', 'none')
            }
        }
        else{
            alert("error while saving")
        }
    })
}