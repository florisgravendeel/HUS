  let accessToken; // A JWT token to access our API
  let tokenExpiry; // Expiry date of our access token.

  // Are we logged in? If so, refresh the tokens or go to the login page.
  silentRefresh()

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
                  accessToken = `${response.token_type} ${response.access_token}`;
                  let dateGMT = new Date(parseFloat(`${response.token_expiry}`)); // UTC values but in GMT format

                  tokenExpiry = Date.UTC(dateGMT.getFullYear(), dateGMT.getMonth(),
                      dateGMT.getDate(), dateGMT.getHours(),
                      dateGMT.getMinutes(), dateGMT.getSeconds()); //UTC date in UTC format
                  let timeLeftMS = tokenExpiry - Date.now();
                  setTimeout(() => { // If the access token is expired, then do a silent refresh
                      silentRefresh();
                  }, timeLeftMS);
                  if (isAtLoginPage()) {
                      redirectToDashboard();
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
      accessToken = null;
      fetch("http://127.0.0.1:8000/logout", {
          method: "POST",
          credentials: "include"
      }).then(function () {
          redirectToLogin();
      }).catch(()=>{
          redirectToLogin();
      })
  }

  /** Redirects to login if the user is not at the login page. */
  function redirectToLogin() {
      if (!isAtLoginPage()) {
          window.location.href = "login";
      }
  }

  /** Redirects to the dashboard if the user is not at the dashboard. */
  function redirectToDashboard() {
      if (!(window.location.pathname === "/home")) {
          window.location.href = "home"
      }
  }

  /** @returns {boolean} True if the user is at the login page, otherwise False. */
  function isAtLoginPage(){
      return window.location.pathname === "/login";
  }

  /**
   * Function that verifies if the access token is expired or not.
   * If there is no access token, then the token is automatically expired.
   * @returns {boolean} True if the token is expired.
   */
  function isTokenExpired(){
      return tokenExpiry == null ? true : (tokenExpiry < Date.now())
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
                    "Authorization": accessToken
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
  function silentRefresh() {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "http://127.0.0.1:8000/refresh_token", true);
      xhr.withCredentials = true;
      xhr.onload = (ev) => {
          const response = JSON.parse(xhr.responseText);
          if (xhr.status === 200) {
              accessToken = `${response.token_type} ${response.access_token}`;
              let date_gmt = new Date(parseFloat(`${response.token_expiry}`)); // UTC values but in GMT format

              tokenExpiry = Date.UTC(date_gmt.getFullYear(), date_gmt.getMonth(),
                  date_gmt.getDate(), date_gmt.getHours(),
                  date_gmt.getMinutes(), date_gmt.getSeconds()); //UTC date in UTC format
              let time_left_ms = tokenExpiry - Date.now();
              setTimeout(() => {
                  silentRefresh();
              }, time_left_ms);
              if (isAtLoginPage()) {
                  redirectToDashboard();
              } else {
                  loadDashboard()
              }
          } else if (xhr.status === 401) {
              logout(); // Reset session, and login
          }
      };
      xhr.send()
  }