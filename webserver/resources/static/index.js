
function validateResistor() {
    let form = new FormData();
    let xhr = new XMLHttpRequest();

    try {
        // posting the values to flask
        form.append('test', JSON.stringify('test'))
        xhr.open('post', '/draw', true);
        xhr.send(form);


        // responses to the ajax post
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {

                // change back to global if it doesn't work
                let response = JSON.parse(xhr.responseText)
                print(response)
            }
        }
    }

    catch {
        let error = 'Error.'
        console.log(error)
    }
}
