  let access_token; // A JWT token to access our API
  let token_expiry; // Expiry date of our access token.

  // Are we logged in? If so, refresh the tokens or go to the login page.
  silent_refresh()

  const logoutButton = document.getElementById("logoutButton");
  if (logoutButton != null){
      logoutButton.addEventListener('click',function () {
      logout();
  });
  }

  const loginButton = document.getElementById("loginButton");
  if (loginButton != null) {
      loginButton.onclick = (ev) => {
          let response = undefined;
          ev.preventDefault();
          const loginForm = document.getElementById("loginForm");
          const data = new FormData(loginForm);
          let xhr = new XMLHttpRequest();
          xhr.open("POST", "http://127.0.0.1:8000/login", true);
          xhr.withCredentials = true;
          xhr.onload = (ev) => {
              const status = document.getElementById("loginStatus");
              const response = JSON.parse(xhr.responseText);
              if (xhr.status === 200) {
                  access_token = `${response.token_type} ${response.access_token}`;
                  let date_gmt = new Date(parseFloat(`${response.token_expiry}`)); // UTC values but in GMT format

                  token_expiry = Date.UTC(date_gmt.getFullYear(), date_gmt.getMonth(),
                      date_gmt.getDate(), date_gmt.getHours(),
                      date_gmt.getMinutes(), date_gmt.getSeconds()); //UTC date in UTC format
                  let time_left_ms = token_expiry - Date.now();
                  setTimeout(() => { // If the access token is expired, then do a silent refresh
                      silent_refresh();
                  }, time_left_ms);
                  if (is_at_login_page()) {
                      redirect_to_dashboard();
                  }
              } else if (xhr.status === 401) {
                  alert("Wrong username or password");
              }
          };
          xhr.send(data);
      }
  }

  /**
   * Sends a request to the server to reset the refresh token (httponly cookie).
   */
  function logout() {
      access_token = null;
      fetch("http://127.0.0.1:8000/logout", {
          method: "POST",
          credentials: "include"
      }).then(function () {
          redirect_to_login();
      }).catch(()=>{
          redirect_to_login();
      })
  }

  /** Redirects to login if the user is not at the login page. */
  function redirect_to_login() {
      if (!is_at_login_page()) {
          window.location.href = "login";
      }
  }

  /** Redirects to the dashboard if the user is not at the dashboard. */
  function redirect_to_dashboard() {
      if (!(window.location.pathname === "/home")) {
          window.location.href = "home"
      }
  }

  /** @returns {boolean} True if the user is at the login page, otherwise False. */
  function is_at_login_page(){
      return window.location.pathname === "/login";
  }

  /**
   * Function that verifies if the access token is expired or not.
   * If there is no access token, then the token is automatically expired.
   * @returns {boolean} True if the token is expired.
   */
  function is_token_expired(){
      return token_expiry == null ? true : (token_expiry < Date.now())
  }

  /**
   * This function is directly called if:
   * (1) the access token is stored in memory;
   * (2) the user is at dashboard page;
   * To prevent the access token from being null when fetching.
   */
  function loadDashboard() {
      fetch("http://127.0.0.1:8000/users/me/", {
                method: "POST",
                headers: {
                    "Content-Type": 'application/json',
                    "Authorization": access_token
                }
            }).then(function (response) {
                response.text().then(result => {
                    const status = document.getElementById("dashboardText");
                    status.innerText = result
                }).catch(error => console.log('error', error))
            })
  }

  /**
   * Makes an API call to fetch a new access token.
   * If there is no refresh token set, the user will automatically logout (to reset the session).
   */
  function silent_refresh() {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "http://127.0.0.1:8000/refresh_token", true);
      xhr.withCredentials = true;
      xhr.onload = (ev) => {
          const response = JSON.parse(xhr.responseText);
          if (xhr.status === 200) {
              access_token = `${response.token_type} ${response.access_token}`;
              let date_gmt = new Date(parseFloat(`${response.token_expiry}`)); // UTC values but in GMT format

              token_expiry = Date.UTC(date_gmt.getFullYear(), date_gmt.getMonth(),
                  date_gmt.getDate(), date_gmt.getHours(),
                  date_gmt.getMinutes(), date_gmt.getSeconds()); //UTC date in UTC format
              let time_left_ms = token_expiry - Date.now();
              setTimeout(() => {
                  silent_refresh();
              }, time_left_ms);
              if (is_at_login_page()) {
                  redirect_to_dashboard();
              } else {
                  loadDashboard()
              }
          } else if (xhr.status === 401) {
              logout(); // Reset session, and login
          }
      };
      xhr.send()
  }