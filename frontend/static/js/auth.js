  window.addEventListener('error', function(e) {
    console.log("We got an error m8" + e);
  }, true);

  let access_token
  let token_expiry
  let silent_refresh_enabled = true
  // Are we logged in? If not, go to the login page.
  if (access_token == null && window.location.pathname !== "/login"){
      redirect_to_login()
  }
  const loginSubmit = document.getElementById("loginSubmit");

  if (loginSubmit != null) {
      loginSubmit.onclick = (ev) => {
          let response = undefined;
          ev.preventDefault();
          const loginForm = document.getElementById("loginForm")
          const data = new FormData(loginForm)
          let xhr = new XMLHttpRequest();
          xhr.open("POST", "http://127.0.0.1:8000/login", true);

          xhr.onload = (ev) => {
              const status = document.getElementById("loginStatus")
              const response = JSON.parse(xhr.responseText)
              if (xhr.status === 200) {
                  access_token = `${response.token_type} ${response.access_token}`;
                  let date_gmt = new Date(parseFloat(`${response.token_expiry}`)); // UTC values but in GMT format

                  token_expiry = Date.UTC(date_gmt.getFullYear(), date_gmt.getMonth(),
                      date_gmt.getDate(), date_gmt.getHours(),
                      date_gmt.getMinutes(), date_gmt.getSeconds()); //UTC date in UTC format
                  let time_left_ms = token_expiry - Date.now();
                  let time_left_s = time_left_ms/1000;
                  console.log("Time left (ms): " , time_left_ms);
                  console.log("Token expired: ", is_token_expired());
                  status.innerText = "Successfully logged in, token: " + access_token + " token_expiry: " + token_expiry;
                  setTimeout(() => {
                    silent_refresh();
                  }, 2000);
              } else {
                  status.innerText = "Error logging in: " + response.detail
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
                  "Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lMiIsImV4cCI6MTYzNjM3NjkwM30.ActOwBFz0_bkT5oZXF6TNXEP7MVofvYMXywv_5-j3c8'
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
      access_token = null;
      // to support logging out from all windows
      window.localStorage.setItem('logout', Date.now()); // Do something with logging out across all tabs.
      silent_refresh_enabled = false; // What about the timer? // Timer_enabled loses it value, when redirected to other login page
      // Do something with cookies? Done

      redirect_to_login() // Does this set silent_refresh_enabled back to true?
  }
  function redirect_to_login() {
      window.location.href="login";
  }
  // 4000 = 4 sec
  // 1200000 = 1200 sec
  // 1199751

  /* If there is no access token, then the token is automatically expired */
  function is_token_expired(){
      return token_expiry == null ? true : (token_expiry < Date.now())
  }

  function silent_refresh() {
      if (silent_refresh_enabled){
      console.log("silent refreshing");
      }
  }