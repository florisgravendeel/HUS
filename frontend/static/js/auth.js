  window.addEventListener('error', function(e) {
    console.log("We got an error m8" + e);
  }, true);

  let access_token = 1
  // Are we logged in? If not, go to the login page.
  if (access_token == null && window.location.pathname !== "/login"){
      redirect_to_login()
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
                  "Authorization": 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzYzODYzMTEsImlhdCI6MTYzNjM4NDUxMSwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJqb2huZG9lMiJ9.GXDHNohcewFKGRxfaREY_tlsd4pe5Ol_1KbdfLGutCg'
              }
          }).then(function (response) {
              console.log(response.status);
              if (response.status === 401){ // Is the access token expired?
                  redirect_to_login()
              }
              response.text().then(result => {
                  const status = document.getElementById("privateStatus");
                  status.innerText = result
              }).catch(error => console.log('error', error))
            })
      }
  }

  function logout() {
      access_token = 0
      // to support logging out from all windows
      //window.localStorage.setItem('logout', Date.now()) // Do something with logging out across all tabs.
      redirect_to_login()
  }
  function redirect_to_login() {
      window.location.href="login";
  }