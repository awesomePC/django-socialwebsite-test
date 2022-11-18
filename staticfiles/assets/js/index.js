

document.getElementById("hamTrigger").addEventListener("click", showSidebar);
function showSidebar() {

    var sideBar = document.getElementById("sideBar");

    if (sideBar.classList.contains("hidden")) {
      sideBar.classList.remove("hidden");
    }
}

document.getElementById("hamTrigger2").addEventListener("click", showSidebar2);
function showSidebar2() {

    var sideBar = document.getElementById("sideBar");

    if (sideBar.classList.contains("hidden")) {
      sideBar.classList.remove("hidden");
    }
}


document.getElementById("closeSidebar1").addEventListener("click", closeSidebar1);
function closeSidebar1() {


      sideBar.classList.add("hidden");

}

document.getElementById("closeSidebar2").addEventListener("click", closeSidebar2);
function closeSidebar2() {


      sideBar.classList.add("hidden");

}


document.getElementById("loginButton").addEventListener("click", toggleNav);
function toggleNav() {

    var loggedOut = document.getElementById("navout");
    if (loggedOut.classList.contains("flex")) {
      loggedOut.classList.add("hidden");
      document.getElementById("navin").style.display = "flex";
      showLogin.classList.add("hidden");
      document.getElementById("inOut").classList.add("hidden");
    }
}

document.getElementById("signupButton").addEventListener("click", zignupButton);
function zignupButton() {
  var loggedOut = document.getElementById("navout");

      loggedOut.classList.add("hidden");
      document.getElementById("navin").style.display = "flex";
      showSignup.classList.add("hidden");

}





document.getElementById("video1").addEventListener("click", playPause);
var myVideo = document.getElementById("video1"); 

function playPause() { 
  if (myVideo.paused) 
    myVideo.play(); 
  else 
    myVideo.pause(); 
} 

document.getElementById("video2").addEventListener("click", playPause2);
var myVideo2 = document.getElementById("video2"); 

function playPause2() { 
  if (myVideo2.paused) 
    myVideo2.play(); 
  else 
    myVideo2.pause(); 
} 

document.getElementById("login").addEventListener("click", showLogin);
var showLogin = document.getElementById("loginID"); 

function showLogin() { 
  if (showLogin.classList.contains("hidden")) {
      showLogin.classList.remove("hidden");
      sideBar.classList.add("hidden");

      
    }
} 

document.getElementById("login2").addEventListener("click", showLogin2);
var showLogin = document.getElementById("loginID"); 

function showLogin2() { 
  if (showLogin.classList.contains("hidden")) {
      showLogin.classList.remove("hidden");
      sideBar.classList.add("hidden");

    }
} 

document.getElementById("uploadButton").addEventListener("click", showUploader);
var uploadModal = document.getElementById("uploadVideos"); 

function showUploader() { 
  if (uploadModal.classList.contains("hidden")) {
      uploadModal.classList.remove("hidden");
    }
} 


document.getElementById("uploadButton2").addEventListener("click", showUploader2);
var uploadModal = document.getElementById("uploadVideos"); 

function showUploader2() { 
  if (uploadModal.classList.contains("hidden")) {
      uploadModal.classList.remove("hidden");
    }
} 



document.querySelector(".close-modal").addEventListener("click", closeLogin);
document.getElementById("close-modal2").addEventListener("click", closeSignup);
document.getElementById("closeUploader").addEventListener("click", closeUploader);
document.getElementById("closeReset").addEventListener("click", closeResetModal);
document.getElementById("closeReset2").addEventListener("click", closeResetModal2);

var closeLogin = document.getElementById("loginID"); 
var closeSignup = document.getElementById("CreateID"); 
var closeUploader = document.getElementById("uploadVideos"); 
var resetPass = document.getElementById("resetPass"); 
var resetPass2 = document.getElementById("resetPass2"); 


function closeLogin() { 
  if (closeLogin.classList.contains("fixed")) {
      closeLogin.classList.add("hidden");
      
    }
} 
function closeSignup() { 
  if (closeSignup.classList.contains("fixed")) {
      closeSignup.classList.add("hidden");

    }
} 

function closeUploader() { 
  if (closeUploader.classList.contains("fixed")) {
      closeUploader.classList.add("hidden");

    }

}

function closeResetModal() { 
  if (resetPass.classList.contains("fixed")) {
      resetPass.classList.add("hidden");

    }

}

function closeResetModal2() { 
  if (resetPass2.classList.contains("fixed")) {
      resetPass2.classList.add("hidden");

    }

}





document.getElementById("forgotPassword").addEventListener("click", showReset);

var closeLogin = document.getElementById("loginID"); 
var resetModal = document.getElementById("resetPass"); 


function showReset() { 
  if (closeLogin.classList.contains("fixed")) {
      closeLogin.classList.add("hidden");
      resetModal.classList.remove("hidden");
    }
} 

document.getElementById("resetButtonLast").addEventListener("click", showReset2);

var closeLogin = document.getElementById("loginID"); 
var closeResetModal = document.getElementById("resetPass"); 
var resetModal2 = document.getElementById("resetPass2"); 


function showReset2() { 
  if (closeLogin.classList.contains("fixed")) {
      closeLogin.classList.add("hidden");
      closeResetModal.classList.add("hidden");
      resetModal2.classList.remove("hidden");
    }
} 





document.querySelector("#signup").addEventListener("click", showSignup);
var showSignup = document.getElementById("CreateID"); 

function showSignup() { 
  if (showSignup.classList.contains("hidden")) {
      showSignup.classList.remove("hidden");
      sideBar.classList.add("hidden");
    }
} 

document.querySelector("#signup2").addEventListener("click", showSignup2);
var showSignup = document.getElementById("CreateID"); 

function showSignup2() { 
  if (showSignup.classList.contains("hidden")) {
      showSignup.classList.remove("hidden");
      sideBar.classList.add("hidden");

    }
} 



document.getElementById("openComments").addEventListener("click", showComments);

var userComments = document.getElementById("userComments"); 
var hideParrent = document.getElementById("hideParrent");
var openBtn = document.getElementById("openComments");
var commentsParrent = document.getElementById("commentsParrent");

function showComments() { 

  if (userComments.style.top === "710px") {
    userComments.style.top = "0px";
    openBtn.style.top = "500px";
    openBtn.style.zIndex = "0";
    commentsParrent.style.left = "0";
    commentsParrent.classList.remove("delay-700");
  } else {
    userComments.style.top = "710px";

  }


} 

document.getElementById("closeComments").addEventListener("click", closeComments)

function closeComments() { 

  if (userComments.style.top === "0px") {
    userComments.style.top = "710px";
    openBtn.style.top = "610px";
    openBtn.style.zIndex = "50";
    commentsParrent.style.left = "-400px";
    commentsParrent.classList.add("delay-700");
  }

} 


document.getElementById("nextVideo").addEventListener("click", nextVideo)

var scrollVideos = document.getElementById("scrollVideos");

function nextVideo() { 

  if (scrollVideos.style.marginLeft === "-300px") {
    scrollVideos.style.marginLeft = "0px";
  }

} 


document.getElementById("prevVideo").addEventListener("click", prevVideo)

var prevVideo = document.getElementById("prevVideo");

function prevVideo() { 

  if (scrollVideos.style.marginLeft === "0px") {
    scrollVideos.style.marginLeft = "-300px";

  }

} 

document.getElementById("logout").addEventListener("click", logoutt);
function logoutt() {
    var loggedOut = document.getElementById("navout");
    if (loggedOut.classList.contains("flex")) {
      loggedOut.classList.remove("hidden");
      document.getElementById("navin").style.display = "none";
      document.getElementById("inOut").classList.remove("hidden")
    }
}

document.getElementById("logout2").addEventListener("click", logout2);
function logout2() {

  var loggedOut = document.getElementById("navout");
    if (loggedOut.classList.contains("flex")) {
      loggedOut.classList.remove("hidden");
      document.getElementById("navin").style.display = "none";
      document.getElementById("inOut").classList.remove("hidden");
      document.getElementById("inOut").classList.remove("hidden");
  sideBar.classList.add("hidden");
    }



}

