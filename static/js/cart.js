let updateBtns = document.getElementsByClassName('update-cart') //Name of class of button

//Adding EventListener to the button
for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product //Taken using data-product : id
        let action = this.dataset.action   //Taken using data-action
        console.log('productId: ', productId, 'Action:', action)
        console.log('User : ', user)
        if (user === 'AnonymousUser') {
            console.log('Not logged in')
        } else {
            updateUserOrder(productId, action)
        }
    })
}

//We set the url variable to update_item and create and use fetch api to send a 'POST' request. In 'POST' we stringify and send our productId and action as Json object.
function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data....')
    let url = '/update_item/'
    //Lookup fetch API
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data : ', data)
        })
}