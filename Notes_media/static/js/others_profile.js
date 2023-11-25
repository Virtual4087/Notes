document.querySelector(".follow_unfollow").onclick = (event) => {
    const button = event.target
    const followers_count = document.querySelector("#followers_count")
    fetch("", {
        method : "POST",
        headers : {
            "Source" : "follow_unfollow",
            "Content-Type" : "application/json",
            "X-CSRFToken" : button.dataset.csrf
        },
        body : JSON.stringify({
            perform : button.id
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success == true){
            console.log(button)
            if (button.id == "follow"){
                button.id = "unfollow"
                button.innerText = "Unfollow"
                button.classList.value = "btn rounded-full p-1 px-4 font-semibold cursor-pointer ml-2 text-black bg-white border-2 border-black hover:text-red-800 hover:border-red-800 follow_unfollow"
                followers_count.innerText = parseInt(followers_count.innerText) + 1
            }else{
                button.id = "follow"
                button.innerText = "Follow"
                button.classList.value = "btn rounded-full p-1 px-4 font-semibold cursor-pointer ml-2 text-white bg-green-500 border-2 border-green-500 hover:bg-green-900 hover:border-green-900 hover:text-green-300 follow_unfollow"
                followers_count.innerText = parseInt(followers_count.innerText) - 1
            }
        }
    })
} 