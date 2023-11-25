document.addEventListener("DOMContentLoaded", () => {
    //  Profile pic change
    const save_button = document.querySelector("#save_pp")
    const cancel_button = document.querySelector("#cancel_pp")
    const change_pp = document.querySelector("#change_pp")
    const pp = document.querySelector("#profile_picture")
    var previous_pp = pp.src
    const formData = new FormData();

    change_pp.addEventListener("change", () => {
        save_button.hidden = false
        cancel_button.hidden = false

        const filesList = change_pp.files
        formData.set("file", filesList[0]);

        const reader = new FileReader();
        reader.onload = function (e) {
            pp.src = e.target.result;
        };
        reader.readAsDataURL(filesList[0])
    })

    cancel_button.addEventListener("click", () => {
        pp.src = previous_pp
        cancel_button.hidden = true
        save_button.hidden = true
        change_pp.value = ""
    })

    save_button.addEventListener("click", () => {
        fetch("", {
            method : "POST",
            headers : {
                "Source" : "change_pp",
                "X-CSRFToken" : change_pp.dataset.csrf
            },
            body : formData
        })
        .then(response=>response.json())
        .then(data=>{
            console.log(data)
            if (data["success"] == true){
                cancel_button.hidden = true
                save_button.hidden = true
                change_pp.value = ""
                previous_pp = pp.src

            }else{
                alert("Some error occured!")
            }    
        })
    })  

    // Change about and personal info
    const about = document.querySelector("#about")
    const edit_about = document.querySelector("#edit_about")
    const save_about = document.querySelector("#save_about")
    const cancel_about = document.querySelector("#cancel_about")

    const char_count = document.querySelector("#char-count")

    var about_text = about.innerText

    edit_about.onclick = () => {
        save_about.hidden = false
        cancel_about.hidden = false
        char_count.hidden = false
        char_count.innerText = `${about.innerText.length}/200`

        // Make about section editable
        about.contentEditable = true

        about.focus();       
    }

    about.addEventListener("input", () => {

        if (about.innerText.length > 200) {
            about.innerText = about.innerText.slice(0, 200);
        }
        char_count.innerText = `${about.innerText.length}/200`
        
    })

    save_about.onclick = () => {
        fetch("", {
            method : "PUT",
            headers : {
                "Source" : "edit_about",
                "Content-Type" : "application/json",
                "X-CSRFToken" : change_pp.dataset.csrf
            },
            body : about.innerText
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success == true){
                about.contentEditable = false
                save_about.hidden = true
                cancel_about.hidden = true
                char_count.hidden = true
                about_text = about.innerText
            }
            else{
                alert("An error occured!")
            }
        })
    }

    cancel_about.onclick = () => {
        about.innerText = about_text
        about.contentEditable = false
        save_about.hidden = true
        cancel_about.hidden = true
        char_count.hidden = true
    }


    const uname = document.querySelector('#fullName')
    const ueducation = document.querySelector('#userEducation')
    const ueducationview = document.querySelector("#userEducationview")
    const birth = document.querySelector('#userBirthday')
    const location = document.querySelector('#userLocation')

    const edit_info = document.querySelector("#edit_info")
    const save_info = document.querySelector("#save_info")
    const cancel_info = document.querySelector("#cancel_info")
    
    var uname_value = uname.value
    var ueducation_value = ueducation.value
    var birth_value = birth.value
    var location_value = location.value

    edit_info.onclick = () => {
        save_info.hidden = false
        cancel_info.hidden = false

        uname.disabled = false;
        ueducation.hidden = false;
        ueducationview.hidden = true;
        birth.disabled = false;
        location.disabled = false;
    }

    cancel_info.onclick = () => {
        save_info.hidden = true
        cancel_info.hidden = true

        uname.disabled = true;
        uname.value = uname_value;
        ueducation.hidden = true;
        ueducation.value = ueducation_value
        ueducationview.hidden = false;
        ueducationview.innerText = ueducation_value
        birth.disabled = true;
        birth.value = birth_value
        location.disabled = true;
        location.value = location_value
    }

    save_info.onclick = () => {
        fetch("", {
            method : "PUT",
            headers : {
                "Source" : "edit_info",
                "Content-Type" : "application/json",
                "X-CSRFToken" : change_pp.dataset.csrf
            },
            body : JSON.stringify({
                "fullname" : uname.value,
                "level" : ueducation.value,
                "birthday" : birth.value,
                "location" : location.value 
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success == true){
                save_info.hidden = true
                cancel_info.hidden = true
        
                uname.disabled = true;
                uname_value = uname.value
                ueducation.hidden = true;
                ueducation_value = ueducation.value
                ueducationview.hidden = false;
                ueducationview.innerText = ueducation.value
                birth.disabled = true;
                birth_value = birth.value
                location.disabled = true;
                location_value = location.value  
            }else{
                alert("Something went wrong!")
            }
        })
    }
})