$(window).on('load', function () {

    $('.selectpicker').selectpicker({
        // 'selectedText': 'cat'
        // style: 'btn btn-primary btn-lg'
    });

    // $('.selectpicker').selectpicker('hide');
});

// Main code run when the document is ready
$(document).ready(function() {
    get_initial_state();
});

$('.selectpicker').on('change', function() {
    // alert( $('.selectpicker').selectpicker('val') ); // or $(this).val()
    $("#download_button").attr("href", "{{ url_for('download') }}" + '/' + $('.selectpicker').selectpicker('val') + '/' + $("#download_button").attr("title"));
});

function get_initial_state() {
    $('#input_box').val();
    $('#button_check').popover({}).hide();
    $('#button_check').show().html('Check');
    $('#button_convert').hide().html('Download');

    $('#success_div').hide();  
    $("#audio_div").hide(); 
    $("video").hide();
    $('#progress_div').hide(); 


    $('#convert_button').hide();     
    $('#download_button').hide();
    $('#format_select_div').hide();
    $(".panel").hide();
}

function get_download_button(uid){
    var output_format = 'mp3';
    var target_url = $("#download_button").attr("href") + '/' + output_format + '/' + uid;
    $("#download_button").attr("href", target_url);
    $("#download_button").attr("title", uid);
    $("#download_button").show();
    $('#format_select_div').show();

    $("#convert_button").hide();
    
    $("#success_div").show("fade-in");
    $('#progress_div').hide(); 
}


function get_convert_button(uid){
    $("#convert_button").attr("href", $("#convert_button").attr("href") + uid);
    $("#convert_button").show();
    $('#format_select_div').hide();
    $(".panel").show();

    $("#download_button").hide();

    $("#success_div").show("fade-in");
    $('#progress_div').hide(); 
}


function get_video_player(url){
    $('#audio_div').show();
    $('#video_player source').attr('src', url);
}

function get_progress(progress_url) {
    $('#success_div').hide(); 
    $('#progress_div').show(); 

    var my_timer = setInterval(function() {
        $.get( progress_url, function( progress_data ) {
            var progress_percent = parseInt(progress_data.dl_progress)
            javascript: console.log("[DONE] progress: " + progress_percent + "%");
            $(".progress-bar").animate({ width: progress_percent+'%'}, 1);

            if (parseInt(progress_percent) >= 100){
                javascript: console.log("Clearing interval...");
                clearInterval(my_timer);
                get_download_button(progress_data.uid);
            }
        })
        .fail( function (data) {
            $('#button_check').show().html('Check');
            javascript: console.log("Failed to update download progress: " + data)
            message_html = "<div class='alert alert-danger'><h2>Failed to update download progress bar.</h2></div>";
            $('#message_div').html(message_html);
        });
    }, 5000);  
}

$("#convert_button").click(function(ev) {
    ev.preventDefault();
    var dl_url = $("#convert_button").attr("href")

    $.get( dl_url, function( dl_data ) {
        get_progress(dl_data);
    }).fail( function (data) {
        $('#button_check').show().html('Check');
        javascript: console.log("Failed to convert video: " + data)
        message_html = "<div class='alert alert-danger'><h2>Failed to convert video.</h2></div>";
        $('#message_div').html(message_html);
    });
    return false;
});

$("#button_check").click(function(ev) { // catch the form's submit event
    ev.preventDefault();
    // $('#message_div').html("");  
    $('#button_check').html('<i class="icon-spinner icon-spin icon-large icon-1x"></i>');

    var target = "{{ url_for('check') }}"
    $.ajax({ // create an AJAX call...
        data: $('#download_form').serialize(), // get the form data
        type: $('#download_form').attr("method"),
        url: target
    }, "json")
    .done(function(data) {
        $('#button_check').show().html('Check');
        javascript: console.log("[DONE] Sucess getting video info: " + data.url);
        javascript: console.log("[DONE] Video ext: " + data.ext);
        javascript: console.log("[DONE] Video uid: " + data.uid);
        javascript: console.log("[DONE] Video uid: " + "<a href='{{ url_for('convert', uid='') }}'" + data.uid);

        get_convert_button(data.uid);
        get_video_player(data.url);
        $(".panel-title").text(data.stitle);
        $(".panel-body").html("<img height='100%' width='100%' src='"+data.thumbnail+"'></img>");
        // $("#success_div").html("")
        // $("#success_div").append(dl_link);
        // $("#download_button").attr("href", $("#download_button").attr("href") + data.uid);
        // $("#success_div").show("fade-in");
        // $('#button_check').show().html('Check');
        // $('#button_convert').html("Download"); 
    })
    .fail( function (data) {
        $('#button_check').show().html('Check');
        javascript: console.log("Failed to get video info: " + data)
        $('#button_convert').html("Download"); 
        message_html = "<div class='alert alert-danger'><h2>Failed to fetch video info.</h2></div>";
        $('#message_div').html(message_html);
    });  
    return false;
});

$("#input_box").bind('change paste keyup', function() {
    get_initial_state();
});