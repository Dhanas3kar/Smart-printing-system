function previewFiles() {
    let files = document.getElementById('files').files;
    let preview = document.getElementById('file-preview');
    preview.innerHTML = "";
    for (let i = 0; i < files.length; i++) {
        let reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML += `<img src="${e.target.result}" width="100">`;
        };
        reader.readAsDataURL(files[i]);
    }
}

function calculatePrice() {
    let copies = document.getElementById('copies').value;
    let color = document.getElementById('color').value;
    fetch('/calculate_price', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({copies: copies, color: color})
    }).then(response => response.json()).then(data => {
        document.getElementById('price-display').innerText = "Total Price: ₹" + data.total_price;
    });
}

function makePayment() {
    let price = document.getElementById('price-display').innerText.split('₹')[1];
    fetch('/make_payment', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({amount: price})
    }).then(response => response.json()).then(data => {
        alert('Payment successful! Printing started.');
        fetch('/print', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({file_paths: ['/path/to/file1', '/path/to/file2']})
        });
    });
}
