
$(document).ready(() => {function startTimer(duration) {
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
    
    function stageHTML(stage, pom_num, block_num){
        // create HTML given by relationship between stage, pom_num and block_num. i.e if (stage-1)%3==0 and (stage < 3*pom_num) send "work" parameters = {header: "Work!", timerOn: True, formOn: False, buttonText: "Skip", "buttonColour: "yellow"}
    };
    function changeTimer(response) {
        // given `stage` we need to update the db with the changes, receive any info we need to update the page with new timer
        //var html_list = stageHTML(stage, num_poms);
        //$("#summary_header").text(html_list[0]);
        //$("#timer").classList.add(html_list[1]);
        console.log(response)
    };
        

    function updateDB(stage) {
        // on click of submit button, take form and send it to the db
        // we definitely need the end timestamp and the stage 
        // `stage` must be incremented serverside, so that if the user exits, we know which stage they are actually on.
        $('#submit').bind('click', function(e) {
        e.preventDefault();
        var summary_text = document.getElementById("summary").value;
        $.post('/_new_pomodoro', {
            summary: summary_text,
            timestamp: new Date(),
            stage: stage
        }).done(function(response) {changeTimer(response)}
            ).fail(function() {
                $('#summary_header').text("Error: Could not contact server.");
                });
            });
        }


    updateDB(stage)
})