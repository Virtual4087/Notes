function countOccurrences(sentence, char) {
    // Use a regular expression to match the character globally in the sentence
    const regex = new RegExp(char, 'g');
    const matches = sentence.match(regex);

    // If matches are found, return the count, otherwise return 0
    return matches ? matches.length : 0;
}

document.addEventListener("DOMContentLoaded", () => {
    if (window.location.href.includes("/search?sort=saved") || window.location.href .includes("/search?sort=following")){
        document.querySelector(".filter-bar").classList.add("hidden")
    } 
    document.querySelectorAll("#description_view").forEach((desc) => {
        var count = countOccurrences(desc.innerText, "\n")
        if (count > 7){
            var lines = desc.innerText.split("\n");
            desc.innerHTML = lines.slice(0, 7).join("\n") + "<span class='text-gray-500 text-lg ml-2 hover:underline'>read more...</span>";
        }
    })
})
