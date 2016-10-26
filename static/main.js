var audio_context;
var recorder;

//Main for startup
$(document).ready(function() {
    init()
    send_data()
    startStopRecording();
    list_bookings();
});



//Creats recorder object and handels non-recorder support.
function init(){
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
      window.URL = window.URL || window.webkitURL;

      audio_context = new AudioContext;
      if (navigator.getUserMedia){
          $('#text_container').hide()
          $('main').html(objects('recorder_div'))
      }
      else{
          fallback()
      }
    } catch (e) {
      fallback()
    }

    if (navigator.getUserMedia){
        navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
            fallback()
        });
      }
}

function fallback(){
    $('main').html(objects('text_container'))
}



//Creats recorder
function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  recorder = new Recorder(input);
}


//Start stops recording
function startStopRecording(){
    var recording = false;
    $('main').on('click','#recorder',function(){
        if(recording == false){
            recording = true
            recorder && recorder.record();
            $('#recorder_div').find('h3').text('Recording, tap to stop.')
            var count=9;
            $('#timer').show()
            $('#timer').text(count)
            var counter=setInterval(timer, 1000);
            function timer(){
                count=count-1;
                if (count <= 0){
                    clearInterval(counter);
                    if(recording == true){
                        recording = false
                        recorder && recorder.stop();
                        $('#timer').hide()
                        audioStream();
                    }
                    return;
                }
                $('#timer').text(count)
            }
        }
        else{
            recording = false
            recorder && recorder.stop();
            $('#timer').hide()
            audioStream();
        }
    });
}


//Converts audio and send it to server. And handles return.
function audioStream() {
    $('main').html(objects('loading'))
    recorder && recorder.exportWAV(function(blob) {
        var reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function() {
            base64data = reader.result;
            var encodedData = window.btoa(base64data);
            recorder.clear();
            $.ajax({
                url: '/new_speech_request',
                method: 'POST',
                data:{'sound':encodedData},
                dataType: "json",
                success: function(response) {
                    $('main').html(objects('confirm_booking'))
                    $('.btn_container').empty()
                    // Location, date och time skrivs ut + tillhörande knapper
                    if(response[0]['errors'].indexOf('location') > -1){
                        $('#location').find('p').text('where?')
                        $('#location').find('.btn_container').append("<button class='location' data-location='Niagara'>Niagara</button>")
                        $('#location').find('.btn_container').append("<button class='location' data-location='Orkanen'>Orkanen</button>")
                        $('#confirm_button').addClass('disabled')
                        $('#confirm_button').prop('disabled', true);
                    }
                    else{
                        $('#location').find('p').text('in ' + response[1]['location'])
                        $('#location').find('p').addClass('blue')
                        $('#location').find('p').attr('data-location',response[1]['location'])
                    }

                    $('#date').find('p').text(response[1]['date'])
                    var prime = timeslot(response[1]['primary_slot'])
                    $('#time').find('p').text(prime)
                    $('#time').find('p').attr('data-time', response[1]['primary_slot'])

                    if(response[1]['sec_slot'] != null){
                        var secondary = timeslot(response[1]['sec_slot'])
                        btns = [
                            "<button class='time blue' data-time="+ response[1]['primary_slot'] + " >"+ prime +"</button>",
                            "<button class='time' data-time="+ response[1]['sec_slot'] + " >"+ secondary +"</button>"
                        ]
                        if (response[1]['sec_slot'] < response[1]['primary_slot']){
                            btns.reverse()
                        }
                        $.each(btns, function(index,value ) {
                          $('#time').find('.btn_container').append(value);
                        });
                    }
                    $('.location').click(function(){
                        var value = $(this).text();
                        $('#location').find('p').text('in ' + value);
                        $('#location').find('p').addClass('blue')
                        $('#confirm_button').removeClass('disabled')
                        $('#confirm_button').prop('disabled', false);
                        var attri = $(this).attr('data-location')
                        $('#location').find('p').attr('data-location', attri);
                    });
                    $('.time').click(function(){
                        var value = $(this).text();
                        var attri = $(this).attr('data-time')
                        $('#time').find('p').text(value);
                        $('#time').find('p').attr('data-time', attri);

                    });

                    $('.btn_container > button').click(function(){
                        $(this).addClass('blue');
                        if($(this).siblings().hasClass('blue')){
                            $(this).siblings().removeClass('blue')
                        }
                    });


                    confirm_booking()
                    new_booking()
                }
            });
        }
  });
}

//Handles text-input insted of audio
function send_data(){
    $("#new_text_request").submit(function(e){
        e.preventDefault();
        input = $('#text_request').val()
        console.log(input);
        $.ajax({
            url: '/new_text_request',
            method: 'POST',
            data:$(this).serialize(),
            success: function(response) {
            }
        });

    });
}

function confirm_booking(){
    $('#confirm_button').click(function(){
        var value = $(this).text();
        var location = $('#location').find('p').attr('data-location');
        var time = $('#time').find('p').attr('data-time');
        var date = $('#date').find('p').text();
        $('main').html(objects('loading'))
        $.ajax({
            url: '/grouprooms',
            method: 'POST',
            data:{
                'location':location,
                'time':time,
                'date':date
            },
            dataType: "text",
            success: function(response) {
                $('main').html(objects('booking_done'))
                if (response == 'OK'){
                    $('#state_heading').text("Great, we're done!")
                }
                else{
                    $('#state_heading').text("Sorry, no room available")
                }
                new_booking();
            }
        });
    });
}



//List all bookings
function list_bookings(){
    $('main').on('click','.list_bookings' ,function(){
        $('main').html(objects('loading'))

        //Här ska dagens boknignar in
        $.ajax({
            url: '/bookedrooms',
            method: 'GET',
            dataType: "json",
            success: function(todayResp) {
                $.ajax({
                    url: '/grouprooms',
                    method: 'GET',
                    dataType: "json",
                    success: function(response) {
                        $('main').html(objects('booking_list'))
                        list = $('#booking_list').find('ul');
                        for (i = 0; i < todayResp.length; i++) {
                            book_id = todayResp[i]['book_id']
                            room = todayResp[i]['room']
                            tims = timeslot_match(todayResp[i]['start'])
                            list.append("<li data-book-id="+ book_id +"><p>Today | "+ tims + " | " + room + "<span class='delete_icon delte_kroon'></span></p></li>")
                        }

                        for (i = 0; i < response.length; i++) {
                            list.append("<li data-id="+response[i][0]+"><p>"+response[i][1] +" | "+ timeslot(response[i][2])+ " | " +response[i][3]+"<span class='delete_icon delte_db'></span></p></li>")
                        }
                        removeBooking();
                        new_booking();
                    }
                });
            }
        });
    });
}


//Removes a booking
function removeBooking(){
    $('.delete_icon').click(function(){
        $(this).addClass('removing_loader')
        to_delte = $(this).parents('li')
        if ($(this).hasClass('delte_kroon')){
            var del_attr = to_delte.attr('data-book-id');
            url = '/bookedrooms/'+del_attr
        }
        else{
            var del_attr = to_delte.attr('data-id');
            url = '/grouprooms/'+ del_attr
        }

        $.ajax({
            url: url,
            method: 'DELETE',
            dataType: "text",
            success: function(response) {
                to_delte.remove()
            }
        });
    });
}

function new_booking(){
    $('#new_booking, #cancel').click(function(){
        $('main').html(objects('recorder_div'))
        $('#recorder_div').find('h3').text('Tap to capture booking.')
    });
}
