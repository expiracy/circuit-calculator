function addResistor() {
    let form = new FormData();
    let xhr = new XMLHttpRequest();

    try {
        // posting the values to flask
        form.append('resistor', JSON.stringify('resistor'))
        xhr.open('post', '/api/add_resistor', true);
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
