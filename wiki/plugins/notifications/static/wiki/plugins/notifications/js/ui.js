notify_latest_id = 0;
notify_update_timeout = 30000;
notify_update_timeout_adjust = 1.2; // factor to adjust between each timeout.

function notify_update() {
  jsonWrapper(URL_NOTIFY_GET_NEW, function (data) {
    if (data.success) {
      $('.notification-cnt').html(data.objects.length);
      if (data.objects.length> 0) {
        $('.notification-cnt').addClass('badge-important');
        $('.notifications-empty').hide();
      } else {
        $('.notification-cnt').removeClass('badge-important');
      }
      for (var i=0; i < data.objects.length; i++) {
        n = data.objects[i];
        notify_latest_id = n.pk>notify_latest_id ? n.pk:notify_latest_id;
        $('.notification-li-container').prepend($('<li><a href="'+URL_NOTIFY_GOTO+n.pk+'/"><div>'+n.message+'</div><div class="since">'+n.since+'</div></a></li>'))
      }
    }
  });
}

function notify_mark_read() {
  $('.notification-li-container').empty();
  url = URL_NOTIFY_MARK_READ+notify_latest_id+'/';
  jsonWrapper(url, function (data) {
    if (data.success) {
      notify_update();
    }
  });
}

function update_timeout() {
  setTimeout("notify_update()", notify_update_timeout);
  setTimeout("update_timeout()", notify_update_timeout);
  notify_update_timeout *= notify_update_timeout_adjust;
}

$(document).ready(function () {
  // Don't check immediately... some users just click through pages very quickly.
  setTimeout("notify_update()", 2000);
  update_timeout();
})

