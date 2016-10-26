
//Konfigureringsfil som innehåller HTML-komponenter för återanvändning.
function objects(item){
    var modules ={
        'recorder_div':
            '<div id="recorder_div">\
                <h3 id="state_heading">Tap to capture booking</h3>\
                <div id="recorder">\
                    <div>\
                        <p id="timer">9</p>\
                    </div>\
                </div>\
                <p class="list_bookings">List bookings</p>\
            </div>',

        'confirm_booking':
            '<h3 id="state_heading">We will book a room for you</h3>\
            <div id="confirm_booking">\
                <div class="float_container">\
                    <div class="res_container" id="date">\
                        <p class="blue"></p>\
                    </div>\
                    <div class="res_container blue" id="time">\
                        <p class="blue"></p>\
                        <div class="btn_container"></div>\
                    </div>\
                    <div class="res_container" id="location">\
                        <p></p>\
                        <div class="btn_container"></div>\
                    </div>\
                </div>\
                <button type="button" id="confirm_button" class="red">Okay, do it!</button>\
                <p id="cancel">Cancel</p>\
            </div>',

        'loading':
        '<h3 id="state_heading">Wait for it...</h3>\
        <div id="loading"></div>',

        'booking_done':
            "<h3 id='state_heading'></h3>\
            <div id='booking_done'>\
                <h4></h4>\
                <p>You'll recive an email with the details the same day.</p>\
                <button id='new_booking' class='red'>New booking</button>\
                <button class='red list_bookings'>List bookings</button>\
            </div>",

        'booking_list':
            "<div id='booking_list'>\
                <h3>Upcoming bookings</h3>\
                <ul></ul>\
                <button id='new_booking' class='red'>New booking</button>\
            </div>",

        'text_container':
            '<div id="text_container">\
                <h3 id="state_heading">Sorry!</h3>\
                <p>You need to use a modern version of Chrome to use Roomify.</p>\
                <p>You can find it <a href="https://www.google.com/chrome/browser/desktop/index.html">here.</a></p>\
            </div>'
    }
    return modules[item]
}


//Lista med alla tidsluckor som resten av front-end koden parat med.
var timeslots =
    ['08:15-10:00',
    '10:15-13:00',
    '13:15-15:00',
    '15:15-17:00',
    '17:15-20:00']

function timeslot(slot){
    return timeslots[slot]
}

function timeslot_match(start){
    for (j = 0; j < timeslots.length; j++){
        if (timeslots[j].indexOf(start) > -1){
            time = timeslots[j]
        }
    }
    return time
}
