//cookie with csrf-token standard snippet
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
                  }
              }
          }
      return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

//
// parse all elements fav-js and swith grey and red 
// status by add and removing it by user clicks
const fav = document.querySelectorAll(".favjs")
fav.forEach(element => {
    element.addEventListener('click', () => {
      const favOut = element.classList.contains('fav-out');
      const favIn = element.classList.contains('fav-in');
      if(favOut){
        element.classList.remove('fav-out');
        element.classList.add('fav-in');
      }
      if(favIn){
        element.classList.remove('fav-in');
        element.classList.add('fav-out');
      }
      
      fav_function(element.dataset.id, element.dataset.bundlename)
      
    });
  });

  function fav_function(id, element){
    fetch("/", {
      method: 'POST',
      credentials: 'same-origin',
      headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrftoken,
    },
      body: JSON.stringify({'favid':id, 'bundlename': element}) //JavaScript object of data to POST
    })
    .then(response => {
          return response.json() //Convert response to JSON
    })
    .then(data => {
      console.log(data)
    //Perform actions with the response data from the view
    })
  }