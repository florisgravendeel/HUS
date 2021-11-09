  window.addEventListener('error', function(e) {
    console.log("We got an error m8" + e);
  }, true);

  let access_token
  let token_expiry
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
          xhr.open("POST", "http://127.0.0.1:8000/login", true);

          xhr.onload = (ev) => {
              const status = document.getElementById("loginStatus")
              const responseData = JSON.parse(xhr.responseText)
              if (xhr.status === 200) {
                  access_token = `${responseData.token_type} ${responseData.access_token}`;
                  let time_gmt = new Date(parseFloat(`${responseData.token_expiry}`)); // Numbers are correct, but is in GMT

                  token_expiry = Date.UTC(time_gmt.getFullYear(), time_gmt.getMonth(), time_gmt.getDay(), time_gmt.getHours(), time_gmt.getMinutes(), time_gmt.getSeconds());

                  status.innerText = "Successfully logged in, token: " + access_token + " token_expiry: " + token_expiry;
                  // console.log("token_exp: ", token_expiry.getHours(), ":", token_expiry.getMinutes())


                  // let utc_date = Date.UTC(2021,11,9,14,28,52);
                  // console.log("UTC Valid Token Date: " + utc_date);
                  //
                  let now = new Date();
                  // // console.log("Current Time: " + now.getHours());
                  // console.log("Current Time: " + now.getTime());
                  // var utc_now = new Date().toUTCString(); //THIS works
                  // console.log("UTC_Now: " + utc_now);
                  console.log("Token expired: ", (now < token_expiry))

                  // console.log("Token_Expiry Hours: (UTC) " + token_expiry.getUTCHours());
                  // console.log("Token_Expiry Hours: ", token_expiry.getHours())
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
      access_token = 0
      // to support logging out from all windows
      //window.localStorage.setItem('logout', Date.now()) // Do something with logging out across all tabs.
      redirect_to_login()
  }
  function redirect_to_login() {
      window.location.href="login";
  }