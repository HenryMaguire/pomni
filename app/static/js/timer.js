
$(document).ready(() => {
    var running_timers = [] // keep track of all running timers
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

    var refr = 0; // define the refresh out of startTimer scope to user can stop it

    function showAlert() {
        alert("Time's Up!");
       }

    function startTimer(duration) {
      duration = duration*60
      var timer = duration-1;
      var refresh = setInterval(function () { // refresh every second
          refr = refresh;
          var output = displaySeconds(timer);
          $("#timer").text(output) //minutes + "m " + seconds + "s ";
          $("title").html(output + " - Pomni");
          if (--timer < 0) {
            clearInterval(refresh);  // exit refresh loop
            var music = $("#over_music")[0];
            music.addEventListener('ended', showAlert);
            music.currentTime=0;
            music.play();
            
          };
      }, 1000);
      running_timers.push(refresh)
    }
    function stopTimers(){
        // multiple timers are running, submit button needs to stop all of them
        for (var i=0; i < running_timers.length; i++) {
            clearInterval(running_timers[i])
        }
        running_timers = []; // Now there are no running timers
    }
    function changeTimer(response, pn) {
        // given `stage` we need to update the db with the changes, receive any info we need to update the page with new timer     
        var pb = $('#progress_bar')
        var time;
        $('#stage_num').text(response['stage']);
        $('#summary_header').text(response['header']);
        $('#submit_button').text(response['button']);
        $('#timer').text(displaySeconds(60*parseInt(response['time'])));
        var progress_percentage = Math.round(100*(parseFloat(response['stage']))/(3*parseFloat(pn)));
        pb.css('width', progress_percentage.toString()+"%");
        pb.text(progress_percentage)
        if (progress_percentage==100) {
            pb.addClass("bg-success")
            pb.removeClass("bg-secondary")
        }
        else {
            pb.addClass("bg-secondary")
            pb.removeClass("bg-success")
        }
        if (parseInt(response['stage'])>=0){
            // BEGIN TIMER (if the user is ready)!
            startTimer(parseInt(response['time']));
        }
        
        //if (response['show_timer']) {
        //    $("#timer").css("visibility","hidden")
        //}
        //else {
        //    $("#timer").addClass("d-none")
        // or // .removeClass("d-none")
        //}
        if (response['show_form']) {
            $("#summary").css("visibility","visible")}
        else {
            $("#summary").css("visibility","hidden")}

        $("#summary").focus(); // html autofocus doesn't work with hidden
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
    // upon page load, find out which stage of session user is at from db
    $.getJSON("/_get_response_json/"+stage.toString()+"/"+params[4].toString(), function(data) {
        changeTimer(data, params[4]) // crazy hack to make the initial app state correct
    });
    updateDB(stage, params, title);
    // if user clicks the submit button at any time, stop the timer
    $('#submit_button').bind('click', function(e) {stopTimers()})

})