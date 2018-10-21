
function updateRecentActivity(current_aim, last_summary){
    $("#current_aim").text(current_aim);
    $("#last_summary").text(last_summary);
}
function resetSession() {
    var stage = -1
    $.post('/_reset_session/'+title).done(function(response) {location.reload()});
    }
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
        var summary_form = $("#summary")
        
        $('#stage_num').text(response['stage']);
        $('#summary_header').text(response['header']);
        $('#submit_button').text(response['button']);
        $('#timer').text(displaySeconds(60*parseInt(response['time'])));
        var progress_percentage = Math.round(100*(parseFloat(response['stage']))/(3*parseFloat(pn)));
        pb.css('width', progress_percentage.toString()+"%");
        pb.text(progress_percentage)
        updateRecentActivity(response["current_aim"], response["last_summary"])
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
        if (! response['show_timer']) {
            stopTimers()}
        if (response['show_form']) {
            summary_form.css("visibility","visible")
            summary_form.val("")
        }
            
        else {
            summary_form.css("visibility","hidden")}
            summary_form.focus(); // html autofocus doesn't work with hidden
    };
        

    function updateDB(params, title) {
        // on click of submit button, take form and send it to the db
        // we definitely need the end timestamp and the stage 
        // `stage` must be incremented serverside, so that if the user exits, we know which stage they are actually on. Also stops people having post access to db via JS script
        // params : [worktime, summarytime, resttime, numpoms, numblocks]
        var submit_button =  $("#submit_button");
        var summary_form = $("#summary")

        // When enter key is pressed, press submit button. 
        $(document).keyup(function(event) {
            if (event.keyCode === 13) {
                // make it harder for user to skip timers with no return key
                if (submit_button.text() != "Skip"){
                    submit_button.click();
                }
            }
        });
        submit_button.bind('click', function(e) {
            e.preventDefault();
            var summary_text = summary_form.val();
            // Naughty hack below: get stage secretly via HTML page
            // allows info to be passed from python to JS without db call. Unsafe
            var current_stage = parseInt($('#stage_num').text());
            var pom_num = params[4];
            var timestamp = Date.now(); 
            $.post('/_new_pomodoro', {
                summary: summary_text,
                timestamp: timestamp, 
                stage: current_stage, 
                wt: params[0], st: params[1], sbt: params[2], 
                lbt: params[3], pn: pom_num, bn: params[5], title: title
                }).done(function(response) {changeTimer(response, pom_num)}
                ).fail(function() {
                    $('#summary_header').text("Error: Could not contact server.");
                    });
            });
        };
    // upon page load, find out which stage of session user is at from db
    $.getJSON("/_get_response_json/"+title.toString()+"/"+stage.toString()+"/"+params[4].toString(), function(data) {
        changeTimer(data, params[4]) // crazy hack to make the initial app state correct
    });
    updateDB(params, title);
    // if user clicks the submit button at any time, stop the timer
    $('#submit_button').bind('click', function(e) {stopTimers()})
    if (stage==-1) {
        stopTimers()
    }
    
    
})