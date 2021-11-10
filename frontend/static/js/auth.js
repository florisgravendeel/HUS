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
                  // There was no other way, I'm inevitable
                  let year = response.token_expiry.year;
                  let month = response.token_expiry.month-1; // Between 0-11, instead of 1-12
                  let day = response.token_expiry.day; // Between 1-31
                  let hours = response.token_expiry.hours; // Between 0-23
                  let minutes = response.token_expiry.minutes;
                  let seconds = response.token_expiry.seconds;
                  console.log("Year: ", year);
                  console.log("Month: ", month);
                  console.log("Day: ", day);
                  console.log("Hours: ", hours);
                  console.log("Minutes: ", minutes);
                  console.log("Seconds: ", seconds)

                  token_expiry = Date.UTC(year, month, day, hours, minutes, seconds); // This is valid!

                  //token_expiry = new Date(year, month, day, hours, minutes, seconds);
                  //let utc_date = Date.UTC(2021,10,9,15,28,52);
                  console.log("Token_exp: ", token_expiry);
                  let now = Date.now();
                  console.log("Now: ", now);
                  let token_expired = token_expiry < now;
                  console.log("Token expired: ", token_expired);
                  status.innerText = "Successfully logged in, token: " + access_token + " token_expiry: " + token_expiry;

                  // let utc_date = Date.UTC(2021,11,9,14,28,52);

                  //console.log("token_exp: ", token_expiry.getHours(), ":", token_expiry.getMinutes())
                  // console.log("UTC Valid Token Date: " + utc_date);
                  //
                  // // console.log("Current Time: " + now.getHours());
                  // console.log("Current Time: " + now.getTime());
                  // var utc_now = new Date().toUTCString(); //THIS works
                  // console.log("UTC_Now: " + utc_now);

                  // console.log("Token_Expiry Hours: (UTC) " + token_expiry.getUTCHours());
                  // console.log("Token_Expiry Hours: ", token_expiry.getHours())
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
      access_token = 0
      // to support logging out from all windows
      //window.localStorage.setItem('logout', Date.now()) // Do something with logging out across all tabs.
      redirect_to_login()
  }
  function redirect_to_login() {
      window.location.href="login";
  }