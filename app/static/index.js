// alert("hello");

// const date = new Date();
// const day = date.getDay();
// const dayNames = ["SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY"];

// function formatDate(date){
//     const year = date.getFullYear();
//     const month = (date.getMonth() + 1).toString().padStart(2,'0');
//     const day = date.getDate().toString().padStart(2,'0');
//     return `${year}-${month}-${day}`;
// }

// function showHeaderDate(){
//     for(var i = 0; i < 7; i++){
//         const today = new Date();
//         if(date.toLocaleDateString() === today.toLocaleDateString()) {
//             $("th div.fw-bold:eq(0)").text("TODAY");
//             $("th div.fw-light:eq(0)").text("");
//             $("th input:eq(0)").attr("value", formatDate(date));
//             date.setDate(date.getDate()+1);
//             continue;
//         }   
//         $("th div.fw-bold").eq(i).text(dayNames[(day+i)%7]);
//         $("th div.fw-light").eq(i).text(date.toLocaleDateString());
//         $("th input").eq(i).attr("value",formatDate(date));
//         date.setDate(date.getDate()+1);
//     }
// }
// showHeaderDate();





var userRole;
var bookingsData;
let currentDate = new Date();



var clickedPopover;
var modal;
$(".popover").on("click", function(){
    if (!$(".change-color").hasClass("bg-primary")){
        clickedPopover = $(this);
        modal = clickedPopover.siblings(".popoverModal");
        clickedPopover.find(".change-color").addClass("bg-primary shadow");
        modal.addClass("active-block");
        
        var offSet = 10;
        var scrollPosition = $(window).scrollTop(); 
        var screenWidth = $(window).width();
        var screenHeight = $(window).height();
        var thisLeft = $(this).offset().left;
        var thisTop = $(this).offset().top;
        var thisWidth = $(this).width();
        var thisHeight = $(this).height();
        var idWidth = modal.width();
        var idHeight = modal.height();
        if(thisLeft <= screenWidth / 2 ){
            modal.css({left: thisLeft + thisWidth + offSet});
        } else {
            modal.css({ left: thisLeft - idWidth - offSet });
        }
        if((thisTop + thisHeight - scrollPosition) < (screenHeight - idHeight - 28) ){
            modal.css({top: thisTop+thisHeight - scrollPosition})
        } else {
            modal.css({top: screenHeight - idHeight - 28})
        }
         
    } 
});


$(".click-modal-disappear").on("click", function(event) {
    var targetPopoverModal = $(event.target).closest(".popoverModal");
    if (((!clickedPopover.find(".change-color").is(event.target)) && (!targetPopoverModal.is(clickedPopover.siblings(".popoverModal"))))
    ) {
        clickedPopover.find(".change-color").removeClass("bg-primary shadow");
        modal.removeClass("active-block");
    }
});

// $(".above-div").each(function(){
//     $(this).on("click", function(event){
//     $(".popoverModal").each(function(){
//         $(this).removeClass("active-block");
//     });
// });
// });

$(".close").click(function(){
    clickedPopover.find(".change-color").removeClass("bg-primary shadow");
    $(this).closest(".popoverModal").removeClass("active-block");
});


var pool = ["Olympic pool","hydrotherapy pool","training pool","family pool"]
$(".popover").on("click", function(){
    var poolID = Math.floor(Math.random()*4);
    $(".poolID").attr("value", poolID+1);
    $(".poolType").attr("value", pool[poolID]);

});




const numDaysToShow = 7;
let startIndex = 0;
// var tableId = $(".instructor-timetable").attr("id");
$(".instructor-timetable").css("visibility","visible");
updateDataDisplay(startIndex);

$(".left-scroll").on("click",function(){
    $(".right-scroll").removeClass("disabled");
    // date.setDate(date.getDate()-14);
    // showHeaderDate();
    startIndex = 0;
    updateDataDisplay(startIndex);
    $(".left-scroll").addClass("disabled");

});

$(".right-scroll").click(function(){
    $(".left-scroll").removeClass("disabled");
    // showHeaderDate();
    startIndex += 7;
    updateDataDisplay(startIndex);
    $(".right-scroll").addClass("disabled");
});


function updateDataDisplay(startIndex){
    const $dataTable = $(".instructor-timetable").find(".data-table");
    const $prevButton = $(".instructor-timetable").find("left-scroll");
    const $nextButton = $(".instructor-timetable").find(".right-scroll");
    const $dateCells = $(".instructor-timetable").find(".date-cell");
    const $dataRows = $(".instructor-timetable").find(".data-row");
    $dateCells.hide();
    $dateCells.slice(startIndex, startIndex + numDaysToShow).show();
    $dataRows.each(function(){
        const $dataCells = $(this).find(".data-cell");
        $dataCells.hide();
        $dataCells.slice(startIndex, startIndex + numDaysToShow).show();
    });
}

// function updateAboveDiv() {
//     // Find all the rows with class "data-row"
//     var divsToSelect = $(".bg-body-secondary.data-cell");
//     $(divsToSelect).each(function(){
//         // console.log($(this).get(0));
//         var startTime = $(this).find('div').attr("id");
//         startTime = new Date(startTime);
//         var booking = getBookingForTime(startTime);
//         if (booking){
//             $(this).find('div').addClass('sessionStart');
//             // console.log($(this).get(0));
//             var endTime = new Date(startTime.getTime() + (booking.lessonDuration - 15) * 60000)
//             // Create the above <div> element
//             var aboveDiv = $('<div>').addClass('above-div'); // Create the above <div> element
//             // Insert the aboveDiv element before the matchingDivs
//             var matchingDivs = $(".bg-body-secondary.data-cell").find('div').filter(function() {
//                 var divId = $(this).attr('id');
//                 var time = new Date(divId);
//                 return time >= startTime && time <= endTime;
//             });
//             // console.log($(matchingDivs).get(0));
//             // matchingDivs.attr('id', "session_" + booking.bookingID);
//             // matchingDivs.addClass('matchingDivs');
        
//             // Calculate the width and height of the matchingDivs
//             var matchingDivsWidth = matchingDivs.closest('td').outerWidth();
//             var matchingDivsHeight = 0;
//             matchingDivs.each(function() {
//                 matchingDivsHeight += $(this).closest('td').outerHeight();
//             });
        
//             // Set the size of aboveDiv to match the matchingDivs
//             aboveDiv.css({
//                 position: 'absolute',
//                 width: matchingDivsWidth + 'px',
//                 height: matchingDivsHeight + 'px',
//                 zIndex: 1, // Adjust the z-index value as needed
//                 // Other CSS styles if necessary
//             });

//             aboveDiv.insertBefore(matchingDivs.first());

    
//             var sessionEndTime = new Date(startTime.getTime() + (booking.lessonDuration) * 60000)
//             // console.log(sessionEndTime);
//             // if (booking.bookingID >= 200000000 ) {
//             //     var additionalText = `lesson with ${booking.firstName}`;
//             // } else {
//             //     var additionalText = booking.sessionName;
//             // }
//             aboveDiv.addClass("bg-success-subtle").text(`${booking.sessionName}`);
//             // .html(formatTime(startTime)+"-"+formatTime(sessionEndTime)+ "<br>" + additionalText); 
//         }
//     });
// };

// $(".timetable-static").on("click", '.above-div', function(){
//     updateAboveDiv();
// });

// $(window).resize(function() {
//     updateAboveDiv();
// });
            
    
// make timetable show the specific booking information
function updateAboveDiv(){
$(".bg-body-secondary.data-cell").each(function(){
    var startTime = $(this).find('div').attr("id");
    startTime = new Date(startTime);
    // console.log(time);
    var booking = getBookingForTime(startTime);
    var matchingDivsWidth=0;
    var matchingDivsHeight = 0;
    if (booking){
        // console.log("booking:",booking);
        // $(this).find('div').addClass('sessionStart')
        var endTime = new Date(startTime.getTime() + (booking.lessonDuration - 15) * 60000)
        // console.log(startTime);
        // console.log(endTime);

        // Create the above <div> element
        var aboveDiv = $('<div>').addClass('above-div'); // Create the above <div> element
        // Insert the aboveDiv element before the matchingDivs

        // update the size of AboveDive

        var matchingDivs = $(".bg-body-secondary.data-cell").find('div').filter(function() {
            var divId = $(this).attr('id');
            var time = new Date(divId);
            return time >= startTime && time <= endTime;
        });
    
        // Calculate the width and height of the matchingDivs
        matchingDivsWidth = matchingDivs.closest('td').outerWidth();
        matchingDivsHeight = 0;
        matchingDivs.each(function() {
            matchingDivsHeight += $(this).closest('td').outerHeight();
        });
    
        // Set the size of aboveDiv to match the matchingDivs
        aboveDiv.css({
            position: 'absolute',
            width: matchingDivsWidth + 'px',
            height: matchingDivsHeight + 'px',
            zIndex: 1, // Adjust the z-index value as needed
            // Other CSS styles if necessary
        });

        aboveDiv.insertBefore(matchingDivs.first());
        $(aboveDiv).attr('id', booking.bookingID);


        // Add content into the AboveDiv
        // var sessionEndTime = new Date(startTime.getTime() + (booking.lessonDuration) * 60000)
        // console.log(sessionEndTime);
        // if (booking.bookingID >= 200000000 ) {
        //     var additionalText = `lesson with ${booking.firstName}`;
        // } else {
        //     var additionalText = booking.sessionName;
        // }
        if (userRole != 1){
            aboveDiv.text(`${booking.sessionName}`);
        }
        // .html(formatTime(startTime)+"-"+formatTime(sessionEndTime)+ "<br>" + additionalText);
        
        // updateAboveDivSize();

        // $(window).resize(function() {
        //     updateAboveDivSize();
        // });

    }
});
};

updateAboveDiv();
$(window).resize(function() {
    updateAboveDiv();
});
$('.timetable-static').on('click', $('.above-div'), function () {
    updateAboveDiv();
    $(window).resize(function() {
        updateAboveDiv();
    });
});



// display time
function updateDivDimensions() {
    // Find all the rows with class "data-row"
    var divs = $('[id^="timeSlot_"]');

    // Initialize variables to keep track of width and height
    var divWidth = 0;
    var divHeight = 0;
    // Iterate through the rows
    divs.each(function(index) {
        // Check if the row index is a multiple of 4 (0-based index)
        if (index % 4 === 0) {

            var div = $(this).find('div').length ? $(this).find('div') : $("<div>");
            div.addClass(".div-time")

            // Add text based on timeSlots data
            var time = $(this).attr("id").split("_")[1];

            // Set the text content of the div
            time = convertTo12HourFormat(time);
            div.text(time);
            // div.addClass("bg-success-subtle")

            // Insert the div as the first child of the first <th> in the row
            $(this).prepend(div);

            // Update div width to match the width of the first <th>
            divWidth = $(this).closest('th').outerWidth();

            // Update div height by adding the height of each row
            divHeight = 0;
            for (var i = index; i < index + 4; i++) {
                divHeight += divs.eq(i).closest('th').outerHeight();
            }
            // console.log("height: ",divHeight);
            // console.log(divWidth);

            // Set the width and height of the div
            div.css({
                position: 'absolute',
                width: divWidth + "px",
                height: divHeight + "px",
                // backgroundcolor: "yellow",
                zIndex: 1, 
            });
        }
    });
}



// $('.timetable-static').on('mouseenter', $('.div-time'), function () {
//     updateDivDimensions();
//     $(window).resize(function() {
//         updateDivDimensions();
//     });
// });
$('.timetable-static').on('click', $('.div-time'), function () {
    updateDivDimensions();
    $(window).resize(function() {
        updateDivDimensions();
    });
});
updateDivDimensions();
$(window).resize(function() {
    updateDivDimensions();
});



// Attach a resize event handler to update div dimensions on window resize


function formatTime(date) {
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const amOrPm = hours >= 12 ? 'pm' : 'am';
  
    const formattedHours = (hours % 12) || 12; // Convert to 12-hour format
    const formattedMinutes = minutes.toString().padStart(2, '0'); // Ensure two-digit minutes
  
    return `${formattedHours}:${formattedMinutes}${amOrPm}`;
}


// function isTimeInRange(time) {
//     const startTime = "08:00 AM";
//     const endTime = "05:45 PM";
//     const startTimeValue = new Date("1970-01-01 " + startTime);
//     const endTimeValue = new Date("1970-01-01 " + endTime);
//     const timeValue = new Date("1970-01-01 " + time);
//     return timeValue >= startTimeValue && timeValue <= endTimeValue;
// }
// // Filter and display only rows within the desired time range
// $(".instructor-timetable").find(".data-row").each(function() {
//     const time = $(this).find(".change-time-format").text().trim();
//     if (isTimeInRange(time)) {
//         $(this).show();
//     } else {
//         $(this).hide();
//     }
// });

$('.change-time-format').each(function() {
    var originalTime = $(this).text();
    var convertedTime = convertTo12HourFormat(originalTime);
    $(this).text(convertedTime);
    // var hourMinute = $(this).text().trim().split(" ")[0]
    // if (!hourMinute.endsWith(":00")){
    //     $(this).text("");
    // }
});


function convertTo12HourFormat(time24) {
    var timeParts = time24.split(':');
    var hours = parseInt(timeParts[0]);
    var minutes = timeParts[1];
    var period = 'AM';
    if (hours >= 12) {
        period = 'PM';
        if (hours > 12) {
            hours -= 12;
        }
    }
    return hours + ':' + minutes + ' ' + period;
}



// $(".instructor-link").click(function(evt) {
//     evt.preventDefault();
//     tableId = $(this).attr("href");
//     $(".instructor-link").removeClass("active");
//     $(this).addClass("active");
//     $(".instructor-timetable").hide();
//     $(tableId).show();
//     updateDataDisplay(tableId, startIndex);
// });


$('[name="lessonDuration"]').on('change', function() {
    const selectedOption = $(this).find(':selected');
    const fee = selectedOption.attr('fee')
    $('[name="lessonFee"]').attr('value',fee)
});


// calendar function


$('#prevMonth').on('click', function(){
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

$('#nextMonth').on('click', function(){
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

function renderCalendar(){
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    $('#monthYear').text(`${new Intl.DateTimeFormat('en-US', { month: 'long' }).format(currentDate)} ${year}`);

    $('#calendarBody').empty();

    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month+1, 0);
    const daysInMonth = lastDayOfMonth.getDate();

    let newRow = $('<tr>');

    for (let i = 0; i < firstDayOfMonth.getDay(); i++) {
      newRow.append('<td>');
    }

    for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(year, month, i);
        const day = date.getDate();
        const cell = $('<td>');
        const dateDiv = $('<div>').text(day).addClass('calendar-date');
        // dateDiv.on("click", function(){
        //     $(this).toggleClass('clicked-date');
        // })
        const bookingsForDate = getBookingsForDate(date);
        // console.log(bookingsForDate);
        if (bookingsForDate.length > 0){
            dateDiv.addClass('active-calendar-date');
            const bookingsList = $('<div>').addClass('bookings-list d-flex flex-wrap');
            bookingsForDate.forEach(function(booking){
                const bookingItem = $('<div>').addClass('booking-item');
                bookingsList.append(bookingItem);

                const imageSrc = `/static/uploadAvatar/${booking.instructorID}.jpg`;
                const image = $('<img>').attr('src', imageSrc).addClass('calendar-avatar');
                image.on('error', function () {
                    $(this).attr('src', '/static/img/avatar.png');
                });
                bookingItem.append(image).addClass('d-flex overflow-hidden');

                if (booking.sessionName === 'Private lesson'){
                    var bookingName = $('<span>').addClass('text-start d-inline-block text-nowrap text-truncate').text("PL-" + booking.firstName);
                    image.addClass('calendar-avatar-private-lesson')
                } else {
                    var bookingName = $('<span>').addClass('text-start d-inline-block text-nowrap text-truncate').text(booking.sessionName);
                    image.addClass('calendar-avatar-group-class')
                }
                if (bookingsForDate.length <= 2){
                    image.addClass('d-inline-block');
                    bookingItem.append(bookingName);
                }
                bookingItem.attr('id', booking.bookingID)
                dateDiv.attr('id', date)
            });
            dateDiv.append(bookingsList);
            
        }
        // const url = "/member/timetable";
        const url = "#"
        // const anchor = $('<a>').attr('href', url).addClass('hyperLinkStyle');
        // cell.append(anchor);
        // anchor.append(dateDiv); 
        cell.append(dateDiv);
        newRow.append(cell);
  
        if (date.getDay() === 6 || i === daysInMonth) {
          $('#calendarBody').append(newRow);
          newRow = $('<tr>');
        }
    }
}

renderCalendar();

function getBookingsForDate(date){
    var filteredBookings = [];
    if(bookingsData){
        filteredBookings = bookingsData.filter(function(booking){
            // console.log("for each booking, check if it's sessionTime is on the same date as:", date)
            var timeString = booking.sessionTime.substring(0, booking.sessionTime.length - 12);
            const sessionTime = new Date(timeString);
            // console.log("sessionTime:", sessionTime);
            // console.log("date:", date);
            // return date == sessionTime;
            // console.log("---------------------------");
            return date.getFullYear() === sessionTime.getFullYear() && date.getMonth() === sessionTime.getMonth() && date.getDate() === sessionTime.getDate();
        });
    }
    
    filteredBookings.sort(function(a, b) {
        const sessionTimeA = new Date(a.sessionTime);
        const sessionTimeB = new Date(b.sessionTime);
        return sessionTimeA - sessionTimeB;
    });
    // console.log(filteredBookings);
    return filteredBookings;
}

function getBookingForTime(time){
    var bookings = getBookingsForDate(time);
    var booking = null;
    // console.log("booking list:", bookings);
    for(var i = 0; i < bookings.length; i++){
        // console.log("bookings.length:", bookings.length);
        // console.log("i: ", i);
        // console.log(booking);
        // console.log("for each booking, check if it's starting time is equal to time: ", time);
        var timeString = bookings[i].sessionTime.substring(0, bookings[i].sessionTime.length - 3);
        const sessionTime = new Date(timeString);
        // console.log("booking's sessionTime:",sessionTime);
        // console.log("unavailable timeslot start time:", time);
        if (sessionTime.getHours() === time.getHours() && sessionTime.getMinutes() === time.getMinutes()){
            booking = bookings[i];
            // console.log(booking);
        }
    }
    // console.log("return booking:",booking);
    return booking;
}

// when click the calender date, a modal will pop out
var clickedDateDiv;
var calendarModal = $('<div>').addClass('calendarModal shadow');

$('table').on('mouseenter', '.active-calendar-date', function () {
    $(this).addClass("hand-cursor");
});

$('table').on('mouseleave', '.active-calendar-date', function () {
    $(this).removeClass("hand-cursor");
});

$('table').on('click', '.active-calendar-date', function (event) {
    event.stopPropagation();
    $(calendarModal).empty();
    clickedDateDiv = $(this).closest('.active-calendar-date');
    var date = new Date($(this).attr("id"));
    const bookingsForDate = getBookingsForDate(date);
    $(clickedDateDiv).after(calendarModal);
    // if (bookingsForDate.length > 0){
    // calendarModal.addClass("active-block"); 
    var listOfBookings = $('<div>').addClass('d-flex flex-column gap-4 p-4 align-items-center justify-content-center');
    $(calendarModal).append(listOfBookings);
    bookingsForDate.forEach(function (booking){
        var eachBooking = $('<div>').addClass('col-12 list-group border border-success-subtle p-3');
        $(listOfBookings).append(eachBooking);

        // var lessonTitle = $('<p>').addClass('lessonTitle fs-6 fw-semibold');
        // if (booking.sessionName === 'Private lesson'){
        //     lessonTitle.text("Private lesson with " + booking.firstName);
        // } else {
        //     lessonTitle.text(booking.sessionName);
        // }
        // lessonTitle.text(booking.sessionName);
        // eachBooking.append(lessonTitle);

        // var lessonTime = $('<p>').addClass('lessonTime blockquote-footer mb-0');
        // var time = booking.sessionTime.slice(0,-3);
        var sessionTime = new Date(booking.sessionTime);
        // console.log(sessionTime);

        var finishTime = new Date(sessionTime.getTime() + parseInt(booking.lessonDuration) * 60000);
        // console.log(finishTime);
        var day = sessionTime.getDate();
        var month = sessionTime.toLocaleString('en-US', { month: 'short' });
        var year = sessionTime.getFullYear();
        var hour = sessionTime.getHours();
        var minute = sessionTime.getMinutes();
        var finishHour = finishTime.getHours();
        var finishMinute = finishTime.getMinutes();

        // Determine AM/PM
        var ampm = hour >= 12 ? 'PM' : 'AM';
        var finishAmpm = finishHour >= 12 ? 'PM' : 'AM';

        // Convert hour to 12-hour format
        hour = hour % 12;
        hour = hour ? hour : 12; // Handle midnight (0) as 12 AM
        finishHour = finishHour % 12;
        finishHour = finishHour ? finishHour : 12;

        // Construct the custom format
        // var formattedSessionTime = `${day} ${month} ${year} ${hour}:${(minute < 10 ? '0' : '')}${minute} ${ampm} - ${finishHour}:${(finishMinute < 10 ? '0' : '')}${finishMinute} ${finishAmpm}`;
        // lessonTime.text(formattedSessionTime);
        // eachBooking.append(lessonTime);
        var userType;
        // console.log(userRole);
        if (userRole === 2){
            userType = "Member";
        } else if (userRole === 3){
            userType = "Instructor";
        }
       
        var htmlContent = `
            <div class="lessonTitle fs-5 fw-semibold">${booking.sessionName}</div>
            <p class="lessonTime blockquote-footer my-0">${day} ${month} ${year} ${hour}:${(minute < 10 ? '0' : '')}${minute} ${ampm} - ${finishHour}:${(finishMinute < 10 ? '0' : '')}${finishMinute} ${finishAmpm}</p>
            <hr>
            <div class="d-flex mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hourglass-split inline-block me-2 mt-1" viewBox="0 0 16 16">
                    <path d="M2.5 15a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11zm2-13v1c0 .537.12 1.045.337 1.5h6.326c.216-.455.337-.963.337-1.5V2h-7zm3 6.35c0 .701-.478 1.236-1.011 1.492A3.5 3.5 0 0 0 4.5 13s.866-1.299 3-1.48V8.35zm1 0v3.17c2.134.181 3 1.48 3 1.48a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 9.052 8.5 8.351z"/>
                </svg>
                <p class="inline-block mb-0 p-0">Lesson duration: ${booking.lessonDuration} minutes</p>
            </div>
            <div class="d-flex mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-badge inline-block me-2 mt-1" viewBox="0 0 16 16">
                    <path d="M6.5 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1h-3zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                    <path d="M4.5 0A2.5 2.5 0 0 0 2 2.5V14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2.5A2.5 2.5 0 0 0 11.5 0h-7zM3 2.5A1.5 1.5 0 0 1 4.5 1h7A1.5 1.5 0 0 1 13 2.5v10.795a4.2 4.2 0 0 0-.776-.492C11.392 12.387 10.063 12 8 12s-3.392.387-4.224.803a4.2 4.2 0 0 0-.776.492V2.5z"/>
                </svg> 
                <p class="inline-block mb-0 p-0"><span>${userType}<span>: <a href="#">${booking.firstName} ${booking.lastName}<a></p>
            </div class="d-flex">
            <div class="d-flex mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt inline-block me-2 mt-1" viewBox="0 0 16 16">
                    <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                    <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                </svg>
                <p class="inline-block mb-0 p-0">Location: ${booking.poolType}</p>
            </div>`
        $(eachBooking).html(htmlContent);
    });


    $(calendarModal).show();
    var offSet = 10;
    var scrollPosition = $(window).scrollTop(); 
    var screenWidth = $(window).width();
    var screenHeight = $(window).height();
    var thisLeft = $(this).offset().left;
    var thisTop = $(this).offset().top;
    var thisWidth = $(this).width();
    var thisHeight = $(this).height();
    var idWidth = calendarModal.width();
    var idHeight = calendarModal.height();
    
    if(thisLeft <= screenWidth / 2 ){
        calendarModal.css({left: thisLeft + thisWidth + 2 * offSet});
    } else {
        calendarModal.css({ left: thisLeft - idWidth - offSet });
    }
    if((thisTop + thisHeight - scrollPosition) < (screenHeight - idHeight - 28) ){
        calendarModal.css({top: thisTop+thisHeight - scrollPosition})
    } else {
        calendarModal.css({top: screenHeight - idHeight - 28})
    }
    // }
});  


$(".click-calendar-modal-disappear").on("click", function(event) {
    targetCalendarModal = $(event.target).closest(".calendarModal");
    // console.log(targetCalendarModal.get(0));
    if ((!clickedDateDiv.is(event.target)) && (!targetCalendarModal.is(clickedDateDiv.next()))){
        // calendarModal.removeClass("active-block");
        calendarModal.hide();
    }
});


$('.instructor-link-for-adminDashboard').each(function() {
    $(this).on('click', function(){
        var id = $(this).attr('href');
    $('.instructor-link-for-adminDashboard').each(function(){
        $(this).removeClass('active');
    });
    $(this).addClass('active');

    // Hide all tables with the same class as the links
    $('.instructor-table-for-adminDashboard').each(function(){             
        $(this).hide();
    });
    
    // Show the corresponding table
    $(id).show(); // Change this to the desired display method (e.g., .show(), .css('display', 'block'))
    });
});

$('.instructor-link-for-adminDashboard:first').click();


$("select[name='lessonDuration']").each(function() {
    // Store a reference to the current select element
    var selectElement = $(this);

    // Listen for changes in the current select element
    selectElement.change(function() {
        // console.log(selectElement.get(0));
        // Get the selected option's value
        var selectedDuration = selectElement.val();
        // console.log(selectedDuration);

        // Find the corresponding lessonFee input within the same form
        var lessonFeeInput = selectElement.closest("form").find("input.lessonFee");
        // console.log(lessonFeeInput.get(0))

        // Update the lessonFee input field based on the selected duration
        if (selectedDuration === "30") {
            lessonFeeInput.val("44");
            // console.log(30);
        } else if (selectedDuration === "60") {
            lessonFeeInput.val("80");
            // console.log(60);
        } else {
            // Handle other cases if needed
            lessonFeeInput.val(""); // Clear the value
        }
    });
});



var clickedAboveDiv;
var timetableModal = $('<div>').addClass('timetableModal shadow');

$('table').on('click', '.above-div', function (event) {
    event.stopPropagation();
    $(timetableModal).empty();
    clickedAboveDiv = $(event.target).closest('.above-div');
    // console.log($(clickedAboveDiv).get(0));
    $(clickedAboveDiv).after(timetableModal);
    bookingID = clickedAboveDiv.attr('id');
    bookingID = parseInt(bookingID);
    // console.log(bookingID);
    bookingsData.forEach(function(booking){
        if (booking.bookingID === bookingID){
            // console.log(booking);
        var sessionTime = new Date(booking.sessionTime);
        // console.log(sessionTime);

        var finishTime = new Date(sessionTime.getTime() + parseInt(booking.lessonDuration) * 60000);
        // console.log(finishTime);
        var day = sessionTime.getDate();
        var month = sessionTime.toLocaleString('en-US', { month: 'short' });
        var year = sessionTime.getFullYear();
        var hour = sessionTime.getHours();
        var minute = sessionTime.getMinutes();
        var finishHour = finishTime.getHours();
        var finishMinute = finishTime.getMinutes();

        // Determine AM/PM
        var ampm = hour >= 12 ? 'PM' : 'AM';
        var finishAmpm = finishHour >= 12 ? 'PM' : 'AM';

        // Convert hour to 12-hour format
        hour = hour % 12;
        hour = hour ? hour : 12; // Handle midnight (0) as 12 AM
        finishHour = finishHour % 12;
        finishHour = finishHour ? finishHour : 12;

        console.log(userRole);
        var userType;
        // console.log(userRole);
        if (userRole === 2){
            userType = "Member";
        } else if (userRole === 3){
            userType = "Instructor";
        }

        var htmlContent = `
            <div class="lessonTitle fs-5 fw-semibold">${booking.sessionName}</div>
            <p class="lessonTime my-0"><small>${day} ${month} ${year} ${hour}:${(minute < 10 ? '0' : '')}${minute} ${ampm} - ${finishHour}:${(finishMinute < 10 ? '0' : '')}${finishMinute} ${finishAmpm}<small></p>
            <hr>
            <div class="d-flex mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hourglass-split inline-block me-2 mt-1" viewBox="0 0 16 16">
                    <path d="M2.5 15a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11zm2-13v1c0 .537.12 1.045.337 1.5h6.326c.216-.455.337-.963.337-1.5V2h-7zm3 6.35c0 .701-.478 1.236-1.011 1.492A3.5 3.5 0 0 0 4.5 13s.866-1.299 3-1.48V8.35zm1 0v3.17c2.134.181 3 1.48 3 1.48a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 9.052 8.5 8.351z"/>
                </svg>
                <p class="inline-block mb-0 p-0">Lesson duration: ${booking.lessonDuration} minutes</p>
            </div>
            <div class="d-flex mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-badge inline-block me-2 mt-1" viewBox="0 0 16 16">
                    <path d="M6.5 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1h-3zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                    <path d="M4.5 0A2.5 2.5 0 0 0 2 2.5V14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2.5A2.5 2.5 0 0 0 11.5 0h-7zM3 2.5A1.5 1.5 0 0 1 4.5 1h7A1.5 1.5 0 0 1 13 2.5v10.795a4.2 4.2 0 0 0-.776-.492C11.392 12.387 10.063 12 8 12s-3.392.387-4.224.803a4.2 4.2 0 0 0-.776.492V2.5z"/>
                </svg> 
                <p class="inline-block mb-0 p-0"><span>${userType}<span>: <a href="#">${booking.firstName} ${booking.lastName}<a></p>
            </div class="d-flex">
            <div class="d-flex mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt inline-block me-2 mt-1" viewBox="0 0 16 16">
                    <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                    <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                </svg>
                <p class="inline-block mb-0 p-0">Location: ${booking.poolType}</p>
            </div>`
        $(timetableModal).html(htmlContent);
    }

    });
    $(timetableModal).show();
    var offSet = 10;
    var scrollPosition = $(window).scrollTop(); 
    var screenWidth = $(window).width();
    var screenHeight = $(window).height();
    var thisLeft = $(clickedAboveDiv).offset().left;
    var thisTop = $(clickedAboveDiv).offset().top;
    var thisWidth = $(clickedAboveDiv).width();
    var thisHeight = $(clickedAboveDiv).height();
    var idWidth = timetableModal.width();
    var idHeight = timetableModal.height();
    
    if(thisLeft <= screenWidth / 2 ){
        timetableModal.css({left: thisLeft + thisWidth + 2 * offSet});
    } else {
        timetableModal.css({ left: thisLeft - idWidth - offSet });
    }
    if((thisTop + thisHeight - scrollPosition) < (screenHeight - idHeight - 28) ){
        timetableModal.css({top: thisTop+thisHeight - scrollPosition})
    } else {
        timetableModal.css({top: screenHeight - idHeight - 50})
    }

});  


$(".click-timetable-modal-disappear").on("click", function(event) {
    targetTimetableModal = $(event.target).closest(".timetableModal");
    // console.log(targetCalendarModal.get(0));
    if ((!clickedAboveDiv.is(event.target)) && (!targetTimetableModal.is(clickedAboveDiv.next()))){
        // timetableModal.removeClass("active-block");
        timetableModal.hide();
    }
});


$('.group-class-booking-button').each(function(){
    var parts = $(this).attr('id').split("_");
    if(parts.length > 1){
        targetTime = new Date(parts[1]);
        // console.log(targetTime);
    }
    if(targetTime <= currentDate){
        $(this).prop("disabled", true).text("Finished").removeClass("btn-outline-info").addClass("btn btn-outline-secondary btn-sm rounded-pill mt-1");
        $(this).attr("style", "font-size:0.75rem; padding: 0.25rem 0.5rem;" )
    }
});

$('.mail-alert-red-dot').click(function(){
    $(this).hide();
});

    





