function clickButton(element_id) {
    document.getElementById(element_id).click();
}

function solve() {
    let file_upload = document.getElementById("select_input").files[0]

    console.log(file_upload)

    let form = new FormData();
    let xhr = new XMLHttpRequest();


    // posting the values to flask
    form.append('uploaded_file', file_upload, 'net_file.txt')
    xhr.open('post', '/api/solve', true);
    xhr.send(form);

    // responses to the ajax post
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {

            // change back to global if it doesn't work
            let result = JSON.parse(xhr.responseText)
            console.log(result)
        }
    }
}
