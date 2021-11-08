  window.addEventListener('error', function(e) {
    console.log("We got an error m8" + e);
  }, true);

  let access_token = 1
  // Are we logged in? If not, go to the login page.
  if (access_token == null && window.location.pathname !== "/login"){
      window.location.href="login";
  }
  const loginSubmit = document.getElementById("loginSubmit");

  if (loginSubmit != null) {
      loginSubmit.onclick = (ev) => {
          ev.preventDefault();
          const loginForm = document.getElementById("loginForm")
          const data = new FormData(loginForm)
          let xhr = new XMLHttpRequest();
          xhr.open("POST", "http://127.0.0.1:8000/token", true);

          xhr.onload = (ev) => {
              const status = document.getElementById("loginStatus")
              const responseData = JSON.parse(xhr.responseText)
              if (xhr.status === 200) {
                  status.innerText = "Successfully logged in, token: " + responseData.access_token;
                  access_token = `${responseData.token_type} ${responseData.access_token}`;
              } else {
                  status.innerText = "Error logging in: " + responseData.detail
              }
          }
          xhr.send(data)
      }
  }

  // request dashboard info
  const privateRequest = document.getElementById("privateRequest");
  if (privateRequest != null) { // Does the dashboard exist?
      privateRequest.onclick = (ev) => {
          fetch("http://127.0.0.1:8000/users/me/", {
              method: "GET",
              headers: {
                  "Content-Type": 'application/json',
                  "Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lMiIsImV4cCI6MTYzNjA0Mjc3M30.T6EWncfS-3YiLghesUyQudA4Lqq4ZmhnpXSra1hwB4o'
              }
          }).then(function (response) {
              console.log(response.status);
            }).then(
                result => {}
          )
              // .then(response => response.text())
              // .then(result => {
              //
              //     const status = document.getElementById("privateStatus");
              //     status.innerText = result
              //
              // })
              // .catch(error => console.log('error', error))
      }
  }

  function logout() {
      window.location.href="login";
  }