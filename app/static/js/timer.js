
function updateRecentActivity(current_aim, last_summary){
    $("#current_aim").text(current_aim);
    $("#last_summary").text(last_summary);
}
function resetSession() {
    var stage = -1
    $.post('/_reset_session/'+title).done(function(response) {location.reload()});
    }


function countRemainingCharacters() {
    summary_form = $("#summary")
    var summary_length = summary_form.val().length;
    var max_length = parseInt(summary_form.attr('max_length'));
    var diff = max_length-summary_length
    $("#char_count").text(diff + " characters remaining");
    if (diff <0) {
        console.log(diff)
        $("#char_count").addClass("text-danger")
        $("#char_count").removeClass("text-muted")
        $('#submit_button').prop('disabled', true)
    }
    else {
        $("#char_count").removeClass("text-danger")
        $("#char_count").addClass("text-muted")
        $('#submit_button').prop('disabled', false)
    }
        
    // if summary_length > max_length add danger class to thing
    // also turn off the submit button
    // change name of attribute to maxLength
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
        pb.html(progress_percentage+"&percnt;")
        updateRecentActivity(response["current_aim"], response["last_summary"])
        if (progress_percentage==100) {
            pb.addClass("bg-success")
            pb.removeClass("bg-warning")
        }
        else {
            pb.addClass("bg-warning")
            pb.removeClass("bg-success")
        }
        if (parseInt(response['stage'])>=0){
            // BEGIN TIMER (if the user is ready)!
            startTimer(parseInt(response['time']));
        }
        if (! response['show_timer']) {
            stopTimers()}

        if (response['show_form']) {
            $("#char_count").removeClass("text-danger")
            $("#char_count").css("visibility","visible")
            summary_form.css("visibility","visible")
            summary_form.val("")
            // hide character count too
            
        }
            
        else {
            var max_length = parseInt(summary_form.attr('max_length'));
            $("#char_count").css("visibility","hidden")
            $("#char_count").text(max_length + " characters remaining");
            
            summary_form.css("visibility","hidden")}
            
            summary_form.focus(); // html autofocus doesn't work with hidden
            
    };
        

    function updateDB(json_data, params, title) {
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
        // start listening to users clicking submit button
        submit_button.bind('click', function(e) {
            e.preventDefault();
            console.log(json_data['show_form'])
            if (json_data['show_form']){
                var summary_text = summary_form.val();
                // Naughty hack below: get stage secretly via HTML page
                // allows info to be passed from python to JS without db call. Unsafe
                var current_stage = parseInt($('#stage_num').text());
                var pom_num = params[4];
                var timestamp = Date.now();
                // only make a new pomodoro if form is shown
                $.post('/_new_pomodoro', {
                    summary: summary_text,
                    timestamp: timestamp, 
                    stage: current_stage, 
                    wt: params[0], st: params[1], sbt: params[2], 
                    lbt: params[3], pn: pom_num, bn: params[5], title: title
                    }).done(function(response) {
                        json_data = response
                        changeTimer(response, pom_num)}
                    ).fail(function() {
                        $('#summary_header').text("Error: Could not contact server.");
                        });
                }
            else {
                $.getJSON("/_next_stage/"+title.toString(), function(response) {
                    var pom_num = params[4];
                    json_data = response
                    changeTimer(response, pom_num)
                });

            };
        });
    };
    // upon page load, find out which stage of session user is at from db
    $.getJSON("/_get_response_json/"+title.toString()+"/"+stage.toString()+"/"+params[4].toString(), function(data) {
        changeTimer(data, params[4]) // crazy hack to make the initial app state correct
        updateDB(data, params, title);
    });
    
    // if user clicks the submit button at any time, stop the timer
    $('#submit_button').bind('click', function(e) {stopTimers()})
    if (stage==-1) {
        stopTimers()
    }
    
    
});