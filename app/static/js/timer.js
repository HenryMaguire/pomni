
$(document).ready(() => {
  function startTimer(duration) {
      duration = duration*60
      var timer = duration, minutes, seconds;
      var refresh = setInterval(function () { // refresh every second
          minutes = parseInt(timer / 60, 10)
          seconds = parseInt(timer % 60, 10);
          // if minutes < 10, give 09:00 etc. else give 11:00 etc.
          minutes = minutes < 10 ? "0" + minutes : minutes;
          // same for seconds (normal time format)
          seconds = seconds < 10 ? "0" + seconds : seconds;

          var output = minutes + " : " + seconds;
          document.getElementById("timer").innerHTML = output //minutes + "m " + seconds + "s ";
          $("title").html(output + " - Pomni");

          if (--timer < 0) {
              var music = $("#over_music")[0];
              music.currentTime=0;
              music.play();
              clearInterval(refresh);  // exit refresh loop
              alert("Time's Up!");
          }
      }, 1000);
}

          startTimer(Minutes);
})
