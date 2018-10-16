
$(document).ready(() => {
    
    function displaySeconds(timer) {
        // takes in seconds and returns a string
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);
        // if minutes < 10, give 09:00 etc. else give 11:00 etc.
        minutes = minutes < 10 ? "0" + minutes : minutes;
        // same for seconds (normal time format)
        seconds = seconds < 10 ? "0" + seconds : seconds;
        return minutes + " : " + seconds;
        }
    var refr = 0; // we define the refresh out of scope to we can stop when user skips the timer
    function showAlert() {
        alert("Time's Up!");
       }
    function startTimer(duration) {
      duration = duration*60
      var timer = duration, minutes, seconds;
      var refresh = setInterval(function () { // refresh every second
          refr = refresh;
          var output = displaySeconds(timer);
          document.getElementById("timer").innerHTML = output //minutes + "m " + seconds + "s ";
          $("title").html(output + " - Pomni");
          
          if (--timer < 0) {
            clearInterval(refresh);  // exit refresh loop
            var music = $("#over_music")[0];
            music.addEventListener('ended', showAlert);
            music.currentTime=0;
            music.play();
            
          };
      }, 1000);
}
    function changeTimer(response, pn) {
        // given `stage` we need to update the db with the changes, receive any info we need to update the page with new timer        
        $('#stage_num').text(response['stage']);
        $('#summary_header').text(response['header']);
        $('#submit_button').text(response['button']);
        $('#summary_header').text(response['header']);
        $('#timer').text(displaySeconds(60*parseInt(response['time'])));
        var progress_percentage = Math.round(100*(parseFloat(response['stage']))/(3*parseFloat(pn)));
        $('#progress_bar').css('width', progress_percentage.toString()+"%");
        $('#progress_bar').text(progress_percentage)
        if (progress_percentage==100) {
            $('#progress_bar').addClass("bg-success")
            $('#progress_bar').removeClass("bg-secondary")
        }
        else {
            $('#progress_bar').addClass("bg-secondary")
            $('#progress_bar').removeClass("bg-success")
        }
        if (parseInt(response['stage'])>0){
            startTimer(parseInt(response['time']));
        }
        
        //if (response['show_timer']) {
        //    $("#timer").css("visibility","hidden")
        //}
        //else {
        //    $("#timer").addClass("d-none")
        //}
        //if (response['show_form']) {
        //    $("#summary").removeClass("d-none")
        //}
        //else {
        //    $("#summary").addClass("d-none")
        //}
        
    };
        

    function updateDB(stage, params, title) {
        // on click of submit button, take form and send it to the db
        // we definitely need the end timestamp and the stage 
        // `stage` must be incremented serverside, so that if the user exits, we know which stage they are actually on.
        // params : [worktime, summarytime, resttime, numpoms, numblocks]
        $('#submit_button').bind('click', function(e) {
        e.preventDefault();
        var summary_text = document.getElementById("summary").value;
        $.post('/_new_pomodoro', {
            summary: summary_text,
            timestamp: new Date(),
            stage: parseInt($('#stage_num').text()),
            wt: params[0], st: params[1], sbt: params[2], lbt: params[3], pn: params[4], bn: params[5],
            title: title
            }).done(function(response) {changeTimer(response, params[4])}
            ).fail(function() {
                $('#summary_header').text("Error: Could not contact server.");
                });
            });
        };
    $.getJSON("/_get_response_json/"+stage.toString()+"/"+params[4].toString(), function(data) {
        changeTimer(data, params[4]) // crazy hack to make the initial app state correct
    });
    var refr = updateDB(stage, params, title);
    // if user clicks the submit button at any time, stop the timer
    $('#submit_button').bind('click', function(e) {clearInterval(refr)})

})