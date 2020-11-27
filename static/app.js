var nos;
var curr = 0;
var data = {};
const NOT_MARKED=0;
const MARKED=1;
const BOOKMARKED=2;
const MARKED_BOOKMARKED=3;
const SUBMITTED = 4;
const SUBMITTED_BOOKMARKED = 5;

window.onbeforeunload = function() {
    return "Dude, are you sure you want to leave?!";
}


$(document).ready( function() {
    var url = window.location.href;
    var list = url.split('/');
    if (url.includes('/give-test/')) {
        $.ajax({
            type:"POST",
            url:"/randomize",
            dataType:"json",
            data : {id: list[list.length-1]},
            success: function(temp) {
                nos = temp;
                
                display_ques(1);
                make_array();
            }
        });
    }
    var time = parseInt($('#time').text()), display = $('#time');
    startTimer(time, display);
    
    flag_time = true;
})

var unmark_all = function() {
    $('#options td').each(function(i) 
    {
        $(this).css("background-color",'rgba(0, 0, 0, 0)');
    });
}
var inittable = function(){

}
$(document).keyup(function(e){
   if(e.which==122){
       e.preventDefault();
       window.location.reload(); 
       return false;
   }
});

var display_ques = function(move) {
    if(fullscreen==1){
    unmark_all();
    $.ajax({
        type: "POST",
        dataType: 'json',
        data : {flag: 'get', no: nos[curr]},
        success: function(temp) {
            $('#que').text(temp['question']);
            $('#a').text('𝐀.  '+temp['a']);
            $('#b').text('𝐁.  '+temp['b']);
            $('#c').text('𝐂.  '+temp['c']);
            $('#d').text('𝐃.  '+temp['d']);
            $('#queid').text('Question No. '+ (move));
            $('#mark').text('Marks: '+temp['marks']);
            if(data[curr+1].marked != null)
               $('#' + data[curr+1].marked).css("background-color",'rgba(0, 255, 0, 0.6)');
        },
        error: function(error){
            console.log("Here is the error res: " + JSON.stringify(error));
        }
    });}
    else{
        alert('Please enter fullscreen mode by pressing F11 to view questions');
        
    }
}
var flag_time = true;
function startTimer(duration, display) {
  var timer = duration,minutes, seconds;
  setInterval(function() {
    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    display.textContent = minutes + ":" + seconds;

    setCookie("minutes", minutes.toString(), 1);
    setCookie("seconds", seconds.toString(), 1);

    if (--timer < 0) {
      timer = 0;
      finish_test();
      clearInterval(interval);
      flag_time = false;
    }
  }, 1000);
}


window.onload = function() {
   var minutes_data = getCookie("minutes");
   var seconds_data = getCookie("seconds");
   var timer_amount = (60*10); //default
    if (!minutes_data || !seconds_data){
      //no cookie found use default
    }
    else{
      console.log(minutes_data+" minutes_data at start");
      console.log(seconds_data+" seconds_data at start");
      console.log(parseInt(minutes_data*60)+parseInt(seconds_data));
            timer_amount = parseInt(minutes_data*60)+parseInt(seconds_data)
    }

  var fiveMinutes = timer_amount,
      display = document.querySelector('#time');
  startTimer(fiveMinutes, display); //`enter code here`
};

 function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
 } 
 
 function getCookie(cname) {
 var name = cname + "=";
 var ca = document.cookie.split(';');
 for(var i=0; i<ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
 }
 return "";
} 


function finish_test() {
    $('#msg').addClass('alert-info');
    $('#msg').append("Test submitted successfully");
    $.ajax({
        type: "POST",
        dataType: "json",
        data: {flag: 'completed'},
        success: function(data) {
            window.location.replace('/home');
        }
    });
    
}
function sendTime() {
    var intervalTime = setInterval(function() {
        if(flag_time == false){
            clearInterval(intervalTime);
        }
        var time = $('#time').text();
        var [hh,mm,ss] = time.split(':');
        hh = parseInt(hh);
        mm = parseInt(mm);
        ss = parseInt(ss);
        var seconds = hh*3600 + mm*60 + ss;
        $.ajax({
            type: 'POST',
            dataType: "json",
            data: {flag:'time', time: seconds},
        });
        if(flag_time == false){
            clearInterval(intervalTime);
        }
    }, 5000);
}
$(document).on('click', '#next', function(e){
    if(curr<nos.length-1){
    e.preventDefault();
    curr += 1;
    display_ques(curr+1);}
    
});

$(document).on('click', '#prev', function(e){
    if(curr>0){
    e.preventDefault();
    curr -= 1;
    display_ques(curr+1);
    }
});

$('#submit').on('click', function(e){
    e.preventDefault();
    var marked;
    if(flag_time == false){
        window.location.replace('/home');
        return;
    }
    $('#options td').each(function(i) 
    {
        if($(this).css("background-color") != 'rgba(0, 0, 0, 0)'){
            marked =  $(this).attr('id');
            data[curr+1].marked= marked;
            data[curr+1].status = SUBMITTED;
        }
    });
    $.ajax({
        type: "POST",
        dataType: 'json',
        data : {flag: 'mark', qid: nos[curr], ans: marked},
        success: function(data) {
            console.log('Answer posted')
        },
        error: function(error){
            console.log("Here is the error res: " + JSON.stringify(error));
        }
    });
    if(curr<nos.length-1){
    $('#next').trigger('click');}
});

function onn() {
    $('.question').remove();
    document.getElementById("overlay").style.display = "block";
    $('#question-list').append('<div id="close">X</div>');
    $('#close').on('click', function(e){
        off();
    });
}

function off() {
    document.getElementById("overlay").style.display = "none";
    $('#close').remove();
} 

$('#questions').on('click', function(e){
    onn();
    for(var i=1;i<=nos.length;i++) {
        var color = '';
        var status = data[i].status;
        if(status == NOT_MARKED)
            color = '#1976D2';
        else if(status == SUBMITTED)
            color = '#42ed62';
        else if(status == BOOKMARKED || status == SUBMITTED_BOOKMARKED)
            color = '#e6ed7b';
        else{
            color = '#f44336';
        }
        j = i<10 ? "0" + i: i
        $('#question-list').append('<div class="question" style="background-color:' + color + '; color:white;">' + j + '</div>');
    }
    $('.question').click(function() {
        var id = parseInt($(this).text());
        curr = id-1;
        display_ques(curr+1);
        off();
    });

});


$('#bookmark').on('click', function(e){
    var status = data[curr+1].status;
    if( status == MARKED)
        data[curr+1].status = MARKED_BOOKMARKED;
    else if(status == SUBMITTED)
        data[curr+1].status = SUBMITTED_BOOKMARKED;
    else
        data[curr+1].status = BOOKMARKED;
});



$('#options').on('click', 'td', function(){
    if ($(this).css("background-color") != 'rgba(0, 255, 0, 0.6)') {
        var clicked = $(this).attr('id');
        var que = $('#queid').attr('id');
        unmark_all();
        $(this).css("background-color",'rgba(0, 255, 0, 0.6)');
        data[curr+1].status = MARKED;
        data[curr+1].marked = $(this).attr('id');
    }
    else {
        $(this).css("background-color",'rgba(0, 0, 0, 0)');
        data[curr+1].status = NOT_MARKED;
        data[curr+1].marked = null;
    }
});
$('#clr').on('click', function(e){
    
        unmark_all();
        data[curr+1].status = NOT_MARKED;
        data[curr+1].marked = null;
    

});
var submit_overlay_display = true;
$('#finish').on("click", function(e) {
    $('#submit-overlay').empty();
    var count = marked();
    var remaining = nos.length - count;
    if(cheat>5||tab_change>=3){
        finish_test();
    }
    if(submit_overlay_display) {
        document.getElementById("submit-overlay").style.display = "block";
        $('#submit-overlay').append('<div style="background-color:white; display: inline-block;/*! margin: auto; *//*! margin: 0 auto; */position: absolute;left: 40%;top: 33%;padding: 10PX; width:30%;" align="center"><table class="table"> <tr><td>Total Questions</td><td>Attempted</td><td>Remaining</td></tr><tr><td>'+ nos.length +'</td><td>'+ count +'</td><td>'+ remaining +'</td></tr></table> <a class="btn btn-primary" onclick="finish_test();">Submit Test</a></div>');
        submit_overlay_display=false;
    } else {
        document.getElementById("submit-overlay").style.display = "none";
        submit_overlay_display = true;
    }
});

var marked = function() {
    var count = 0;
    for(var i=1;i<=nos.length;i++){
        if(data[i].status == SUBMITTED || data[i].status == SUBMITTED_BOOKMARKED){
            count++;
        } 
    }
    return count;
}

var make_array = function() {
    for(var i=0; i<nos.length; i++){
        data[i+1] = {marked : null, status: NOT_MARKED}; 
    }
    var txt = document.createElement('textarea');
    txt.innerHTML = answers;
    answers = txt.value;
    answers = JSON.parse(answers);
    for(var key in answers) {
        data[parseInt(key)+1].marked = answers[key]
        data[parseInt(key)+1].status = SUBMITTED;
    }
}
session.pop('_flashes', None);